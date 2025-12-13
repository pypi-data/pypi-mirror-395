# tests/test_orchestrator_coverage.py

import pytest
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import anyio
import re
from typer import Exit

from create_dump.orchestrator import (
    run_batch,
    validate_batch_staging,
    _centralize_outputs,
)
from create_dump.transaction import AtomicBatchTxn, ROLLBACKS_TOTAL

@pytest.fixture
def mock_fs(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    sub1 = root / "sub1"
    sub1.mkdir()
    sub2 = root / "sub2"
    sub2.mkdir()
    return root, sub1, sub2

@pytest.mark.anyio
class TestOrchestratorCoverage:

    async def test_atomic_batch_txn_rollback(self, mock_fs):
        root, _, _ = mock_fs
        run_id = "test_run"

        # Test rollback on exception
        with pytest.raises(ValueError, match="Test Error"):
            async with AtomicBatchTxn(root, None, run_id, dry_run=False) as staging:
                assert await staging.exists()
                # Simulate work
                await (staging / "test.txt").touch()
                raise ValueError("Test Error")

        # Verify staging dir is gone
        staging_dir = root / "archives" / f".staging-{run_id}"
        assert not staging_dir.exists()

    async def test_atomic_batch_txn_cleanup_error(self, mock_fs):
        root, _, _ = mock_fs
        run_id = "test_run"

        # Mock rmtree to fail
        with patch("shutil.rmtree", side_effect=OSError("Permission denied")):
            with pytest.raises(ValueError, match="Test Error"):
                async with AtomicBatchTxn(root, None, run_id, dry_run=False) as staging:
                     raise ValueError("Test Error")

    async def test_atomic_batch_txn_dry_run(self, mock_fs):
        root, _, _ = mock_fs
        run_id = "test_run"

        async with AtomicBatchTxn(root, None, run_id, dry_run=True) as staging:
            assert staging is None

        staging_dir = root / "archives" / f".staging-{run_id}"
        assert not staging_dir.exists()

    async def test_atomic_batch_txn_outside_root(self, mock_fs, tmp_path):
        root, _, _ = mock_fs
        run_id = "test_run"
        outside_dest = tmp_path / "outside"
        outside_dest.mkdir()

        # Mock safe_is_within to fail
        with patch("create_dump.orchestrator.safe_is_within", new=AsyncMock(return_value=False)):
            with pytest.raises(ValueError, match="Staging parent outside root boundary"):
                async with AtomicBatchTxn(root, outside_dest, run_id, dry_run=False):
                    pass

    async def test_validate_batch_staging_missing_sha(self, mock_fs):
        root, _, _ = mock_fs
        staging = anyio.Path(root / "staging")
        await staging.mkdir()

        # Create MD without SHA
        md_file = staging / "dump_123.md"
        await md_file.touch()

        pattern = r".*\.md$"

        is_valid = await validate_batch_staging(staging, pattern)
        assert not is_valid

    async def test_validate_batch_staging_empty(self, mock_fs):
        root, _, _ = mock_fs
        staging = anyio.Path(root / "staging")
        await staging.mkdir()

        pattern = r".*\.md$"

        is_valid = await validate_batch_staging(staging, pattern)
        assert not is_valid

    async def test_centralize_outputs_missing_sha(self, mock_fs):
        root, sub1, _ = mock_fs
        dest = root / "dest"

        md_file = sub1 / "dump_123.md"
        md_file.touch()
        # SHA missing

        pattern = r"dump_.*\.md$"

        # Mock safe_is_within to always return True
        with patch("create_dump.orchestrator.safe_is_within", new=AsyncMock(return_value=True)):
            await _centralize_outputs(anyio.Path(dest), root, [sub1], False, True, pattern)

        assert (dest / "dump_123.md").exists()
        assert not (dest / "dump_123.sha256").exists()

    async def test_centralize_outputs_unsafe_path(self, mock_fs):
        root, sub1, _ = mock_fs
        dest = root / "dest"

        md_file = sub1 / "dump_123.md"
        md_file.touch()

        pattern = r"dump_.*\.md$"

        # Mock safe_is_within to return False
        with patch("create_dump.orchestrator.safe_is_within", new=AsyncMock(return_value=False)):
            await _centralize_outputs(anyio.Path(dest), root, [sub1], False, True, pattern)

        assert not (dest / "dump_123.md").exists()

    async def test_run_batch_no_subdirs(self, mock_fs):
        root, _, _ = mock_fs

        await run_batch(
            root=root, subdirs=["nonexistent"], pattern=".*",
            dry_run=False, yes=True, accept_prompts=True, compress=False,
            max_workers=1, verbose=True, quiet=False
        )
        # Should return early without error

    async def test_run_batch_failure_handling(self, mock_fs):
        root, sub1, _ = mock_fs

        # Mock run_single to raise exception
        with patch("create_dump.orchestrator.run_single", side_effect=Exception("Batch Error")):
            await run_batch(
                root=root, subdirs=["sub1"], pattern=".*",
                dry_run=False, yes=True, accept_prompts=True, compress=False,
                max_workers=1, verbose=True, quiet=False
            )
        # Should handle exception and log failure, not crash

    async def test_run_batch_validation_failure(self, mock_fs):
        root, sub1, _ = mock_fs

        with patch("create_dump.orchestrator.run_single", new=AsyncMock()):
             with patch("create_dump.orchestrator.validate_batch_staging", new=AsyncMock(return_value=False)):
                 with patch("create_dump.orchestrator.safe_delete_paths", new=AsyncMock(return_value=(0,0))):
                     # We need find_matching_files to return async iterator
                     async def mock_find_files(*args):
                         yield root / "old.md"
                     with patch("create_dump.orchestrator.find_matching_files", side_effect=mock_find_files):

                        with pytest.raises(ValueError, match="Validation failed"):
                             await run_batch(
                                root=root, subdirs=["sub1"], pattern=".*",
                                dry_run=False, yes=True, accept_prompts=True, compress=False,
                                max_workers=1, verbose=True, quiet=False, atomic=True
                            )

    async def test_run_batch_non_atomic(self, mock_fs):
        root, sub1, _ = mock_fs

        with patch("create_dump.orchestrator.run_single", new=AsyncMock()):
             with patch("create_dump.orchestrator.validate_batch_staging", new=AsyncMock(return_value=True)):
                 with patch("create_dump.orchestrator.safe_delete_paths", new=AsyncMock(return_value=(0,0))):
                     async def mock_find_files(*args):
                         if False: yield
                     with patch("create_dump.orchestrator.find_matching_files", side_effect=mock_find_files):
                         with patch("create_dump.orchestrator._centralize_outputs", new=AsyncMock()):
                             with patch("create_dump.orchestrator.ArchiveManager") as MockAM:
                                 mock_am_inst = MockAM.return_value
                                 mock_am_inst.run = AsyncMock(return_value={"group": Path("archive.zip")})

                                 await run_batch(
                                    root=root, subdirs=["sub1"], pattern=".*",
                                    dry_run=False, yes=True, accept_prompts=True, compress=False,
                                    max_workers=1, verbose=True, quiet=False, atomic=False, archive=True
                                )

                                 assert mock_am_inst.run.called

    async def test_run_batch_cleanup_confirmation(self, mock_fs):
        root, sub1, _ = mock_fs

        async def mock_find_files(*args):
            yield root / "old.md"

        with patch("create_dump.orchestrator.find_matching_files", side_effect=mock_find_files):
            with patch("create_dump.orchestrator.confirm", return_value=False):
                 with patch("create_dump.orchestrator.run_single", new=AsyncMock()):
                     with patch("create_dump.orchestrator.validate_batch_staging", new=AsyncMock(return_value=True)):
                         with patch("create_dump.orchestrator._centralize_outputs", new=AsyncMock()):
                             # We need to mock safe_delete_paths to ensure it wasn't called
                             with patch("create_dump.orchestrator.safe_delete_paths") as mock_delete:

                                 await run_batch(
                                    root=root, subdirs=["sub1"], pattern=".*",
                                    dry_run=False, yes=False, accept_prompts=True, compress=False,
                                    max_workers=1, verbose=True, quiet=False
                                )

                                 mock_delete.assert_not_called()

    async def test_run_batch_non_atomic_validation_fail(self, mock_fs):
        root, sub1, _ = mock_fs

        with patch("create_dump.orchestrator.run_single", new=AsyncMock()):
             with patch("create_dump.orchestrator.validate_batch_staging", new=AsyncMock(return_value=False)):
                 with patch("create_dump.orchestrator.safe_delete_paths", new=AsyncMock(return_value=(0,0))):
                     async def mock_find_files(*args):
                         if False: yield
                     with patch("create_dump.orchestrator.find_matching_files", side_effect=mock_find_files):
                         with patch("create_dump.orchestrator._centralize_outputs", new=AsyncMock()):
                             # Should log warning but not raise
                             await run_batch(
                                root=root, subdirs=["sub1"], pattern=".*",
                                dry_run=False, yes=True, accept_prompts=True, compress=False,
                                max_workers=1, verbose=True, quiet=False, atomic=False
                            )
