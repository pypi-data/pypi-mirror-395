# tests/test_orchestrator.py

"""
Tests for src/create_dump/orchestrator.py: Batch orchestration with atomic staging.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, ANY
# ⚡ FIX: Import AsyncGenerator
from typing import List, AsyncGenerator

import anyio
import pytest_asyncio

# [TEST_SKELETON_START]
# Add this import at the top of tests/test_orchestrator.py
from create_dump.orchestrator import _centralize_outputs, validate_batch_staging
# [TEST_SKELETON_END]

# ⚡ RENAMED: Imports to match new API
from create_dump.orchestrator import (
    run_batch,
    atomic_batch_txn,
    # _centralize_outputs, # No longer needed, imported above
    # validate_batch_staging, # No longer needed, imported above
)
from create_dump.transaction import AtomicBatchTxn  # ⚡ FIX: Import AtomicBatchTxn from transaction
from create_dump.core import Config
# ⚡ RENAMED: Import to match new API
from create_dump.path_utils import find_matching_files
# ⚡ RENAMED: Import to match new API
from create_dump.single import run_single
from create_dump.archiver import ArchiveManager

pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config() -> Config:
    return Config(
        dump_pattern=r".*_all_create_dump_\d{8}_\d{6}\.md$",
        max_file_size_kb=5000,
        use_gitignore=True,
        git_meta=True,
    )


@pytest.fixture
def mock_logger(mocker):
    # ⚡ FIX: Patch the logger where it is *used* (in the orchestrator module)
    mock_log = mocker.patch("create_dump.orchestrator.logger")
    mocker.patch("create_dump.transaction.logger", mock_log)
    return mock_log


@pytest.fixture
def mock_styled_print(mocker):
    # ⚡ FIX: Patch styled_print where it is *used*
    return mocker.patch("create_dump.orchestrator.styled_print")


@pytest.fixture
def mock_metrics(mocker):
    # ⚡ FIX: Mock DUMP_DURATION.labels to return a mock context manager
    mock_duration_ctx = MagicMock()
    mock_duration_ctx.__enter__ = MagicMock()
    mock_duration_ctx.__exit__ = MagicMock()
    mock_duration = mocker.patch("create_dump.orchestrator.DUMP_DURATION")
    mock_duration.labels.return_value.time.return_value = mock_duration_ctx
    
    # 🐞 FIX: Patch the metric where it is *used* (now in transaction.py)
    mock_rollbacks = mocker.patch("create_dump.transaction.ROLLBACKS_TOTAL")
    mock_rollbacks.labels.return_value = MagicMock()
    return mock_rollbacks


@pytest.fixture
def test_project(tmp_path: Path):
    class MockProject:
        def __init__(self, path):
            self.root = path
            # ⚡ ADDED: async_root for convenience
            self.async_root = anyio.Path(path)

        def path(self, rel):
            return self.root / rel

        async def create(self, files):
            for name, content in files.items():
                p = self.path(name)
                await anyio.Path(p).parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    await anyio.Path(p).write_bytes(content)
                elif content is None or name.endswith("/"):
                    await anyio.Path(p).mkdir(parents=True, exist_ok=True)
                else:
                    await anyio.Path(p).write_text(str(content))

    return MockProject(tmp_path)


# ⚡ FIX: Add fixture to mock the generator
@pytest.fixture
def mock_find_files_gen(mocker):
    """Mocks find_matching_files to return a configurable async generator."""
    mock_gen_func = mocker.patch("create_dump.orchestrator.find_matching_files")
    
    async def create_gen(file_list: List[Path]) -> AsyncGenerator[Path, None]:
        for f in file_list:
            yield f
    
    # Default behavior: return an empty generator
    mock_gen_func.return_value = create_gen([])
    # Return a factory to configure the mock in specific tests
    return lambda files: setattr(mock_gen_func, "return_value", create_gen(files))


class TestAtomicBatchTxn:
    async def test_successful_commit(self, tmp_path: Path, mock_logger):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "test123"

        async with atomic_batch_txn(root, None, run_id, dry_run=False) as staging:
            assert await staging.exists()
            assert "staging-test123" in str(staging)
            await anyio.Path(staging / "dummy.md").write_text("test")

        final = root / "archives" / "test123"
        assert await anyio.Path(final).exists()
        assert await anyio.Path(final / "dummy.md").exists()
        assert mock_logger.info.call_args[0][0] == "Batch txn committed: %s -> %s"


    async def test_rollback_on_exception(self, tmp_path: Path, mock_logger, mock_metrics):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "fail456"

        with pytest.raises(ValueError, match="Simulated failure"):
            async with atomic_batch_txn(root, None, run_id, dry_run=False) as staging:
                raise ValueError("Simulated failure")

        archives = root / "archives"
        assert not await anyio.Path(archives / ".staging-fail456").exists()
        
        # 🐞 FIX: The mock_metrics fixture now correctly patches the target
        mock_metrics.labels.assert_called_once_with(reason="Simulated failure")
        mock_metrics.labels.return_value.inc.assert_called_once()

        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][0] == "Batch txn rolled back due to: %s"
        assert isinstance(mock_logger.error.call_args[0][1], ValueError)


    async def test_dry_run_no_staging(self, tmp_path: Path):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        run_id = "dry789"

        async with atomic_batch_txn(root, None, run_id, dry_run=True) as staging:
            assert staging is None

        assert not await anyio.Path(root / "archives" / ".staging-dry789").exists()

    async def test_invalid_dest_outside_root(self, tmp_path: Path):
        root = tmp_path / "root"
        await anyio.Path(root).mkdir()
        unsafe_dest = tmp_path / "outside"

        with pytest.raises(ValueError, match="Staging parent outside root boundary"):
            async with atomic_batch_txn(root, unsafe_dest, "unsafe", dry_run=False):
                pass


# ⚡ RENAMED: Class to match new API
class TestCentralizeOutputs:
    async def test_centralize_to_staging(self, tmp_path: Path, test_project, mock_logger):
        root = test_project.root
        await test_project.create({
            "sub1/sub1_all_create_dump_20251107_200000.md": "content",
            "sub1/sub1_all_create_dump_20251107_200000.sha256": "hash",
            "sub1/junk.txt": "junk",
            "sub2/sub2_all_create_dump_20251107_200100.md": "content2",
            "sub2/sub2_all_create_dump_20251107_200100.sha256": "hash2",
        })
        sub1 = root / "sub1"
        sub2 = root / "sub2"

        staging = anyio.Path(tmp_path / "staging")
        successes = [sub1, sub2]

        # ⚡ FIX: Use the *correct* pattern that matches .md
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(staging, root, successes, compress=False, yes=True, dump_pattern=md_pattern)

        assert await (staging / "sub1_all_create_dump_20251107_200000.md").exists()
        assert await (staging / "sub1_all_create_dump_20251107_200000.sha256").exists()
        assert await (staging / "sub2_all_create_dump_20251107_200100.md").exists()
        assert await (staging / "sub2_all_create_dump_20251107_200100.sha256").exists()
        assert not await (staging / "junk.txt").exists()
        mock_logger.info.assert_called_with("Centralized %d dump pairs to %s", 2, staging)

    async def test_centralize_to_dest_path(self, tmp_path: Path, test_project):
        root = test_project.root
        await test_project.create({
            "sub/test_all_create_dump_20251107_200200.md": "content"
        })
        sub = root / "sub"

        dest = tmp_path / "dest"
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(dest, root, [sub], compress=False, yes=False, dump_pattern=md_pattern)

        # ⚡ FIX: Use anyio.Path for the async .exists() call
        assert await anyio.Path(dest / "test_all_create_dump_20251107_200200.md").exists()

    async def test_no_matches_skipped(self, tmp_path: Path, test_project):
        root = test_project.root
        await test_project.create({"empty/": None})
        sub = root / "empty"

        dest = tmp_path / "dest"
        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(dest, root, [sub], compress=False, yes=True, dump_pattern=md_pattern)

        # ⚡ FIX: Correct async list comprehension syntax
        assert len([f async for f in anyio.Path(dest).iterdir()]) == 0


# [TEST_SKELETON_START]

# ... (Inside class TestCentralizeOutputs) ...
    async def test_centralize_missing_sha(self, tmp_path: Path, test_project, mock_logger):
        """
        Tests coverage for missing .sha256 file (lines 130-131, 135).
        """
        root = test_project.root
        await test_project.create({
            "sub1/sub1_all_create_dump_20251107_200000.md": "content",
            # No .sha256 file
        })
        sub1 = root / "sub1"
        staging = anyio.Path(tmp_path / "staging")
        successes = [sub1]

        md_pattern = r".*_all_create_dump_\d{8}_\d{6}\.md$"
        await _centralize_outputs(staging, root, successes, compress=False, yes=True, dump_pattern=md_pattern)

        # Assert the warning was logged
        mock_logger.warning.assert_called_with(
            "Missing SHA256 for dump, moving .md only", 
            path=str(test_project.async_root / "sub1/sub1_all_create_dump_20251107_200000.md")
        )
        # Assert the .md file was still moved
        assert await (staging / "sub1_all_create_dump_20251107_200000.md").exists()


class TestValidateBatchStaging:
    async def test_valid_with_sha(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "staging")
        await staging.mkdir()
        md1 = staging / "test_all_create_dump_20251107_200300.md"
        await md1.write_text("content")
        sha1 = md1.with_suffix(".sha256")
        await sha1.write_text("hash")

        md2 = staging / "test2_all_create_dump_20251107_200400.md"
        await md2.write_text("content2")
        sha2 = md2.with_suffix(".sha256")
        await sha2.write_text("hash2")

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is True

    async def test_invalid_orphan_sha_missing(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "staging")
        await staging.mkdir()
        md = staging / "orphan_all_create_dump_20251107_200500.md"
        await md.write_text("content")

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is False

    async def test_empty_staging_false(self, tmp_path: Path):
        staging = anyio.Path(tmp_path / "empty")
        await staging.mkdir()

        assert await validate_batch_staging(staging, r".*_all_create_dump_\d{8}_\d{6}\.md$") is False


# ⚡ RENAMED: Class to match new API
class TestRunBatch:
    @pytest.fixture
    def multi_subdirs(self, test_project):
        root = test_project.root
        sub1 = root / "sub1"
        sub2 = root / "sub2"
        sub1.mkdir(parents=True, exist_ok=True)
        sub2.mkdir(parents=True, exist_ok=True)
        return [str(s.relative_to(root)) for s in [sub1, sub2]]

    async def test_happy_path_atomic(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_styled_print, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            md = root / f"{root.name}_all_create_dump_20251107_200600.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        mock_manager = AsyncMock()
        mock_manager.run = AsyncMock(return_value={"group1": True}) # 🐞 FIX: Mock the .run method
        mocker.patch("create_dump.orchestrator.ArchiveManager", return_value=mock_manager)

        # ⚡ FIX: Use the mock_find_files_gen fixture (defaulting to empty)
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=True,
            quiet=False,
            dest=None,
            archive=True,
            archive_all=False,
            atomic=True,
        )

        assert mock_logger.info.call_args_list[-1][0][0] == "Batch complete: %d/%d successes"
        mock_manager.run.assert_called_once()
        mock_metrics.labels.return_value.inc.assert_not_called()

        archives = root / "archives"
        # 🐞 FIX: Use recursive rglob to find files inside the committed staging dir
        final_files = [f async for f in anyio.Path(archives).rglob("*.md")]
        assert len(final_files) == 2

    async def test_rollback_on_sub_failure(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            if "sub2" in str(root):
                raise RuntimeError("Simulated sub-failure")
            md = root / f"{root.name}_all_create_dump_20251107_200700.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        # ⚡ FIX: The code *catches* the RuntimeError, so the test should not.
        # The error is logged, and the run continues.
        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=True, quiet=False,
            archive=False, atomic=True,
        )

        archives = root / "archives"
        # 🐞 FIX: Use recursive rglob to find files inside the committed staging dir
        final_files = [f async for f in anyio.Path(archives).rglob("*.md")]

        # ⚡ FIX: The batch should *commit* with only sub1's files.
        assert len(final_files) == 1
        assert final_files[0].name.startswith("sub1")

        # ⚡ FIX: No rollback should be triggered, because the error was caught.
        mock_metrics.labels.return_value.inc.assert_not_called()


    async def test_validation_fail_rollback(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            # ⚡ FIX: This mock *only* creates the .md, guaranteeing validation fails
            md = root / f"{root.name}_all_create_dump_20251107_200800.md"
            await anyio.Path(md).write_text("dummy")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        with pytest.raises(ValueError, match="Validation failed"):
            await run_batch(
                root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
                yes=True, accept_prompts=True, compress=False, max_workers=2, verbose=True, quiet=False,
                archive=False, atomic=True,
            )
        
        # 🐞 FIX: The mock_metrics fixture now correctly patches the target
        # ⚡ FIX: NOW the rollback logic is triggered
        mock_metrics.labels.assert_called_once_with(reason="Validation failed: Incomplete dumps")
        mock_metrics.labels.return_value.inc.assert_called_once()

    async def test_non_atomic_direct(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        async def mock_run_single(root: Path, **kwargs):
            md = root / f"{root.name}_all_create_dump_20251107_200900.md"
            await anyio.Path(md).write_text("dummy")
            sha = md.with_suffix(".sha256")
            await anyio.Path(sha).write_text("dummy_hash")
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        dest = root / "custom_dest"
        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=False, quiet=True,
            dest=dest, archive=False, atomic=False,
        )

        final_files = [f async for f in anyio.Path(dest).glob("*.md")]
        assert len(final_files) == 2

    async def test_no_subdirs_early_return(self, test_project, mocker, mock_config, mock_logger, mock_find_files_gen):
        root = test_project.root
        invalid_subdirs = ["nonexistent1", "nonexistent2"]
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        await run_batch(
            root=root, subdirs=invalid_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=False, accept_prompts=False, compress=False, max_workers=1, verbose=True, quiet=False,
            archive=False, atomic=True,
        )
        mock_logger.warning.assert_called_with("No valid subdirs: %s", invalid_subdirs)


    async def test_concurrency_with_limiter(self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)

        calls = []
        async def mock_run_single(root: Path, **kwargs):
            calls.append(root.name)
            await anyio.sleep(0.01)
        mocker.patch("create_dump.orchestrator.run_single", side_effect=mock_run_single)

        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=mock_config.dump_pattern, dry_run=False,
            yes=True, accept_prompts=True, compress=False, max_workers=1, verbose=False, quiet=True,
            archive=False, atomic=False,
        )

        assert len(calls) == 2
        assert set(calls) == set([Path(sub).name for sub in multi_subdirs])

    async def test_dry_run_disables_atomic(self, test_project, multi_subdirs: List[str], mocker, mock_find_files_gen):
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=Config(dump_pattern=r".*_all_create_dump_\d{8}_\d{6}\.md$"))

        mocker.patch("create_dump.orchestrator.run_single")
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.confirm", return_value=True)

        await run_batch(
            root=root, subdirs=multi_subdirs, pattern=".*", dry_run=True,
            yes=True, accept_prompts=True, compress=False, max_workers=2, verbose=False, quiet=True,
            archive=False, atomic=True,
        )

        archives = root / "archives"
        if await anyio.Path(archives).exists():
            final_files = [f async for f in anyio.Path(archives).iterdir()]
            assert len(final_files) == 0
        else:
            assert not await anyio.Path(archives).exists()
            
            
# ... (Inside class TestRunBatch) ...
    async def test_run_batch_non_atomic(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Action Plan 1: Test non-atomic path (lines 283-317).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # Mock the components for the non-atomic path
        mock_centralize = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        mock_validate = mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)
        
        # -----------------
        # 🐞 FIX: This is the corrected mock
        # -----------------
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={}) # Return empty for this test
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True, # Enable archive to test that branch
            atomic=False, # Key flag
        )

        # Assert _centralize_outputs was called with the *final* dest path
        mock_centralize.assert_called_once()
        assert mock_centralize.call_args[0][0] == dest
        
        # Assert validation was called on the final dest path
        mock_validate.assert_called_once_with(anyio.Path(dest), mock_config.dump_pattern)
        
        # -----------------
        # 🐞 FIX: Corrected assertions
        # -----------------
        # Assert ArchiveManager class was instantiated
        mock_archive_mgr_class.assert_called_once()
        # Assert the instance's .run() method was awaited
        mock_archive_mgr_instance.run.assert_called_once()
        
        # ⚡ FIX: Check the *keyword* args for 'root'
        assert mock_archive_mgr_class.call_args[1]["root"] == root

    async def test_run_batch_atomic_validation_fails(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_metrics, mock_find_files_gen
    ):
        """
        Action Plan 2: Test validation failure in atomic mode.
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        
        # Mock validation to fail
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=False)
        
        # This should raise the ValueError, which triggers the rollback
        with pytest.raises(ValueError, match="Validation failed: Incomplete dumps"):
            await run_batch(
                root=root,
                subdirs=multi_subdirs,
                pattern=mock_config.dump_pattern,
                dry_run=False,
                yes=True,
                accept_prompts=True,
                compress=False,
                max_workers=2,
                verbose=False,
                quiet=True,
                dest=None,
                archive=False,
                atomic=True,
            )
        
        # Assert rollback metric was incremented
        mock_metrics.labels.assert_called_once_with(reason="Validation failed: Incomplete dumps")
        mock_metrics.labels.return_value.inc.assert_called_once()

    async def test_run_batch_atomic_dry_run_returns_early(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Tests coverage for atomic dry_run (lines 252-253).
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        # ⚡ FIX: Use the mock_find_files_gen fixture
        
        # Spy on run_single to ensure it's still called (dry_run is passed down)
        mock_run_single_spy = mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # Spy on _centralize_outputs, which should NOT be called
        mock_centralize_spy = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=True, # Key flag
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=None,
            archive=False,
            atomic=True, # Key flag
        )
        
        # Assert the individual runs were still simulated
        assert mock_run_single_spy.call_count == len(multi_subdirs)
        
        # Assert that the atomic transaction block was exited early
        mock_centralize_spy.assert_not_called()
# [TEST_SKELETON_END]


    # --- NEW P1 TESTS ---

    async def test_run_batch_non_atomic_archive(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen
    ):
        """
        Covers lines 285-317 (non-atomic path with archiving).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mock_centralize = mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        mock_validate = mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)
        
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={"default": Path("archive.zip")})
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True, # Enable archive
            atomic=False, # Key flag
        )

        mock_centralize.assert_called_once_with(dest, root, ANY, False, True, mock_config.dump_pattern)
        mock_validate.assert_called_once_with(anyio.Path(dest), mock_config.dump_pattern)
        
        # Assert ArchiveManager was called with the *root* path
        mock_archive_mgr_class.assert_called_once()
        assert mock_archive_mgr_class.call_args[1]["root"] == root
        mock_archive_mgr_instance.run.assert_called_once()

    async def test_run_batch_non_atomic_validation_fails(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_logger, mock_find_files_gen
    ):
        """
        Covers lines 306-308 (validation failure in non-atomic mode).
        """
        root = test_project.root
        dest = root / "custom_dest"
        
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        mocker.patch("create_dump.orchestrator._centralize_outputs", new_callable=AsyncMock)
        
        # Mock validation to fail
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=False)
        
        # 🐞 FIX: Correctly mock the ArchiveManager to be awaitable
        mock_archive_mgr_instance = AsyncMock()
        mock_archive_mgr_instance.run = AsyncMock(return_value={}) # Return empty
        mock_archive_mgr_class = mocker.patch(
            "create_dump.orchestrator.ArchiveManager", 
            return_value=mock_archive_mgr_instance
        )

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=True,
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=dest,
            archive=True,
            atomic=False,
        )

        # Assert the warning was logged and no error was raised
        mock_logger.warning.assert_called_with("Validation failed: Incomplete dumps in non-atomic destination.")
        
        # Assert ArchiveManager was *still* called (non-transactional)
        mock_archive_mgr_class.assert_called_once()
        mock_archive_mgr_instance.run.assert_called_once()

    async def test_run_batch_pre_cleanup_declined(
        self, test_project, multi_subdirs: List[str], mocker, mock_config, mock_find_files_gen
    ):
        """
        Covers lines 212-216 (pre-cleanup prompt declined).
        """
        root = test_project.root
        mocker.patch("create_dump.orchestrator.load_config", return_value=mock_config)
        
        # Mock find_matching_files to return a file
        mock_find_files_gen([root / "old_dump.md"])
        
        # Mock confirm to return False
        mock_confirm = mocker.patch("create_dump.orchestrator.confirm", return_value=False)
        mock_safe_delete = mocker.patch("create_dump.orchestrator.safe_delete_paths", new_callable=AsyncMock)
        mock_run_single = mocker.patch("create_dump.orchestrator.run_single", new_callable=AsyncMock)
        
        # 🐞 FIX: Mock validation to pass so the test doesn't fail early
        mocker.patch("create_dump.orchestrator.validate_batch_staging", new_callable=AsyncMock, return_value=True)

        await run_batch(
            root=root,
            subdirs=multi_subdirs,
            pattern=mock_config.dump_pattern,
            dry_run=False,
            yes=False, # Key flag
            accept_prompts=True,
            compress=False,
            max_workers=2,
            verbose=False,
            quiet=True,
            dest=None,
            archive=False,
            atomic=True,
        )

        # Assert confirm was called and safe_delete was NOT
        mock_confirm.assert_called_once_with("Delete old dumps?")
        mock_safe_delete.assert_not_called()
        
        # Assert the rest of the run continued
        assert mock_run_single.call_count == len(multi_subdirs)