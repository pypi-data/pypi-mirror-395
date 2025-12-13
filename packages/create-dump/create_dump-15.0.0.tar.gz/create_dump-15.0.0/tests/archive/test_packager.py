# tests/archive/test_packager.py

"""
Tests for Phase 3: src/create_dump/archive/packager.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from typing import List, Tuple, Optional
import zipfile
import tarfile
import stat # ⚡ FIX: Import stat module

import anyio

# Import the class to test
from create_dump.archive.packager import ArchivePackager
from create_dump.helpers import _unique_path
from create_dump.logging import setup_logging

# -----------------
# Import all required mocks
# -----------------
from datetime import datetime
from unittest.mock import MagicMock, patch, AsyncMock, call
from create_dump.archive.core import ArchiveError

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
async def archives_dir(test_project) -> Path:
    """Creates an 'archives' dir and returns its path."""
    archives_path = test_project.root / "archives"
    await anyio.Path(archives_path).mkdir(exist_ok=True)
    return archives_path

@pytest.fixture
async def quarantine_dir(test_project, archives_dir) -> Path:
    """Creates a 'quarantine' dir and returns its path."""
    q_path = Path(archives_dir) / "quarantine"
    await anyio.Path(q_path).mkdir(exist_ok=True)
    return q_path

@pytest.fixture
async def project_with_files(test_project, archives_dir, quarantine_dir):
    """Creates a project with dump files for packager tests."""
    await test_project.create({
        # --- Single/Default Group ---
        "default_all_create_dump_20250101_000100.md": "old",
        "default_all_create_dump_20250101_000100.sha256": "hash_old",
        "default_all_create_dump_20250101_000200.md": "new",
        "default_all_create_dump_20250101_000200.sha256": "hash_new",

        # --- Grouped Files ---
        "src_all_create_dump_20250101_000100.md": "src_old",
        "src_all_create_dump_20250101_000100.sha256": "src_hash_old",
        "src_all_create_dump_20250101_000200.md": "src_new",
        "src_all_create_dump_20250101_000200.sha256": "src_hash_new",
        "tests_all_create_dump_20250101_000100.md": "tests_old",
        "tests_all_create_dump_20250101_000100.sha256": "tests_hash_old",
    })

    await anyio.Path(archives_dir).mkdir(exist_ok=True)
    await anyio.Path(quarantine_dir).mkdir(exist_ok=True)

    # Return all valid pairs
    return [
        (test_project.path("default_all_create_dump_20250101_000100.md"),
         test_project.path("default_all_create_dump_20250101_000100.sha256")),
        (test_project.path("default_all_create_dump_20250101_000200.md"),
         test_project.path("default_all_create_dump_20250101_000200.sha256")),
        (test_project.path("src_all_create_dump_20250101_000100.md"),
         test_project.path("src_all_create_dump_20250101_000100.sha256")),
        (test_project.path("src_all_create_dump_20250101_000200.md"),
         test_project.path("src_all_create_dump_20250101_000200.sha256")),
        (test_project.path("tests_all_create_dump_20250101_000100.md"),
         test_project.path("tests_all_create_dump_20250101_000100.sha256")),
    ]


@pytest.fixture
async def base_packager_args(test_project, archives_dir, quarantine_dir):
    """Provides the base dict of args for instantiating a packager."""
    setup_logging(quiet=True)
    return {
        "root": test_project.root,
        "archives_dir": archives_dir,
        "quarantine_dir": quarantine_dir,
        "timestamp": "20251107_120000",
        "keep_latest": True,
        "verbose": False,
        "dry_run": False,
        "yes": True,
        "clean_root": False,
        "no_remove": False,
        "archive_format": "zip",
    }


class TestArchivePackager:
    """Groups tests for the ArchivePackager."""

    @pytest.mark.parametrize("archive_format, extension, reader, test_func", [
        ("zip", ".zip", zipfile.ZipFile, lambda z: z.testzip()),
        ("tar.gz", ".tar.gz", tarfile.open, lambda t: t.getnames()),
        ("tar.bz2", ".tar.bz2", tarfile.open, lambda t: t.getnames()),
    ])
    async def test_create_archive_sync(
        self, base_packager_args, test_project, archive_format, extension, reader, test_func
    ):
        """
        Test Case 1: _create_archive_sync for zip, tar.gz, and tar.bz2.
        Also implicitly tests _safe_arcname.
        """
        await test_project.create({
            "src/file1.txt": "file1",
            "src/sub/file2.txt": "file2",
        })
        files = [
            test_project.path("src/file1.txt"),
            test_project.path("src/sub/file2.txt"),
        ]

        args = base_packager_args | {"archive_format": archive_format}
        packager = ArchivePackager(**args)

        archive_name = f"test_archive{extension}"
        archive_path, archived_files = packager._create_archive_sync(files, archive_name)

        assert archive_path.name == archive_name
        assert len(archived_files) == 2
        assert await anyio.Path(archive_path).exists()

        # Validate contents
        with reader(archive_path, 'r') as ar:
            test_func(ar) # Validate integrity
            names = ar.getnames() if hasattr(ar, "getnames") else ar.namelist()
            assert "src/file1.txt" in names
            assert "src/sub/file2.txt" in names

    async def test_group_pairs_by_prefix(self, base_packager_args, project_with_files):
        """Test Case 2: group_pairs_by_prefix correctly groups files."""
        packager = ArchivePackager(**base_packager_args)
        groups = packager.group_pairs_by_prefix(project_with_files)

        assert "default" in groups
        assert "src" in groups
        assert "tests" in groups
        assert len(groups["default"]) == 2
        assert len(groups["src"]) == 2
        assert len(groups["tests"]) == 1

    async def test_handle_single_archive_keep_latest(
        self, base_packager_args, project_with_files, test_project
    ):
        """Test Case 3: handle_single_archive with keep_latest=True."""
        args = base_packager_args | {"keep_latest": True}
        packager = ArchivePackager(**args)
        
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        
        archive_paths, to_delete = await packager.handle_single_archive(pairs)
        
        assert "default" in archive_paths
        archive_path = archive_paths["default"]
        assert archive_path.name.startswith(f"{test_project.root.name}_dumps_archive_")
        
        assert len(to_delete) == 2
        assert "default_all_create_dump_20250101_000100.md" in to_delete[0].name
        
        assert "default_all_create_dump_20250101_000200.md" not in {p.name for p in to_delete}

    async def test_handle_single_archive_no_keep_latest(
        self, base_packager_args, project_with_files
    ):
        """Test Case 4: handle_single_archive with keep_latest=False."""
        args = base_packager_args | {"keep_latest": False}
        packager = ArchivePackager(**args)
        
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        archive_paths, to_delete = await packager.handle_single_archive(pairs)

        assert "default" in archive_paths

        assert len(to_delete) == 4
        assert "default_all_create_dump_20250101_000100.md" in to_delete[0].name
        assert "default_all_create_dump_20250101_000200.md" in to_delete[2].name

    async def test_handle_grouped_archives(
        self, base_packager_args, project_with_files, quarantine_dir
    ):
        """Test Case 5: handle_grouped_archives processes groups correctly."""
        args = base_packager_args | {"keep_latest": True}
        packager = ArchivePackager(**args)
        
        groups = packager.group_pairs_by_prefix(project_with_files)
        archive_paths, to_delete = await packager.handle_grouped_archives(groups)

        assert "src" in archive_paths
        assert "tests" not in archive_paths
        assert "default" not in archive_paths 
        
        assert archive_paths["src"].name.startswith("src_all_create_dump_")
        
        assert "src_all_create_dump_20250101_000100.md" in {p.name for p in to_delete}
        assert "src_all_create_dump_20250101_000200.md" not in {p.name for p in to_delete}
        
        assert "tests_all_create_dump_20250101_000100.md" not in {p.name for p in to_delete}
        
        q_path = anyio.Path(quarantine_dir)
        assert await (q_path / "default_all_create_dump_20250101_000100.md").exists()
        assert await (q_path / "default_all_create_dump_20250101_000200.md").exists()

    async def test_handle_archives_dry_run(
        self, base_packager_args, project_with_files, archives_dir, caplog
    ):
        """Test Case 6: No archives created or files moved on dry_run."""
        args = base_packager_args | {"dry_run": True}
        packager = ArchivePackager(**args)
        
        # Test single
        all_pairs = project_with_files
        pairs = [p for p in all_pairs if "default" in p[0].name]
        archive_paths, to_delete = await packager.handle_single_archive(pairs)
        
        assert len(archive_paths) == 1
        assert archive_paths["default"] is None # No path returned
        assert len(to_delete) == 0 # No files marked for deletion
        
        # Test grouped
        groups = packager.group_pairs_by_prefix(all_pairs)
        archive_paths, to_delete = await packager.handle_grouped_archives(groups)
        
        assert len(archive_paths) == 1 # src only
        assert archive_paths["src"] is None
        assert "tests" not in archive_paths
        assert len(to_delete) == 0
        
        # Assert nothing was actually created
        file_count = 0
        async for p in anyio.Path(archives_dir).rglob("*"):
            if p.name != "quarantine":
                file_count += 1
        assert file_count == 0 # Should be empty


    async def test_create_archive_sync_zip_write_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (zip).
        Tests that _create_archive_sync rolls back zip on write failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock: Make zipfile.ZipFile fail on write
        mocker.patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Simulated write error"))
        
        # 3. Mock: Spy on Path.unlink
        archive_path = base_packager_args["archives_dir"] / "fail_archive.zip"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)
        
        # -----------------
        # 🐞 FIX: Patch the *class method* `pathlib.Path.unlink`, not the instance.
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")

        # 4. Act & Assert
        with pytest.raises(zipfile.BadZipFile):
            packager._create_archive_sync(files, "fail_archive.zip")
        
        # 5. Assert rollback
        # -----------------
        # 🐞 FIX: The mock is called with (self=archive_path, missing_ok=True)
        # The assertion should NOT include the self argument.
        # -----------------
        mock_unlink.assert_called_once_with(missing_ok=True)


    async def test_create_archive_sync_tar_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (tar).
        Tests that _create_archive_sync rolls back tar on write failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "tar.gz"}
        packager = ArchivePackager(**args)

        # 2. Mock
        archive_path = base_packager_args["archives_dir"] / "fail_archive.tar.gz"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)
        
        # -----------------
        # 🐞 FIX: Patch `pathlib.Path.unlink`
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")
        
        mocker.patch("tarfile.open", side_effect=tarfile.TarError("Simulated tar error"))
        
        # 3. Act & Assert
        with pytest.raises(tarfile.TarError):
            packager._create_archive_sync(files, "fail_archive.tar.gz")
            
        # -----------------
        # 🐞 FIX: Assert with keyword args only
        # -----------------
        mock_unlink.assert_called_once_with(missing_ok=True)

    async def test_create_archive_sync_zip_validation_failure(
        self, base_packager_args, test_project, mocker
    ):
        """
        Action Plan 1: Test archive failure (zip validation).
        Tests that _create_archive_sync rolls back zip on testzip() failure.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1"})
        files = [test_project.path("src/file1.txt")]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock
        archive_path = base_packager_args["archives_dir"] / "validate_fail.zip"
        mocker.patch("create_dump.helpers._unique_path", return_value=archive_path)

        # -----------------
        # 🐞 FIX: Patch `pathlib.Path.unlink` and `pathlib.Path.stat`
        # -----------------
        mock_unlink = mocker.patch.object(Path, "unlink")
        
        # ⚡ FIX: Create a mock stat_result with a valid st_mode
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1234
        mock_stat_result.st_mode = stat.S_IFREG  # This makes path.is_file() True
        
        mocker.patch.object(Path, "stat", return_value=mock_stat_result)
        
        # -----------------
        # 🐞 FIX: Correctly mock the two separate calls to ZipFile
        # -----------------
        mock_write_zip = MagicMock() # Mock for the 'w' mode call
        mock_validate_zip = MagicMock() # Mock for the 'r' mode call
        mock_validate_zip.testzip.return_value = "badfile.txt" # This triggers the error
        
        mock_zip_open = mocker.patch("zipfile.ZipFile")
        # ⚡ FIX: Use side_effect to provide a *different* mock for each call.
        # Add a mock for __exit__ to be robust.
        mock_zip_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=mock_write_zip), __exit__=MagicMock(return_value=None)), # Call 1 (write)
            MagicMock(__enter__=MagicMock(return_value=mock_validate_zip), __exit__=MagicMock(return_value=None)) # Call 2 (read)
        ]
        
        # 3. Act & Assert
        # -----------------
        # 🐞 FIX: The test now correctly raises ArchiveError
        # -----------------
        with pytest.raises(ArchiveError, match="Corrupt file in ZIP: badfile.txt"):
            packager._create_archive_sync(files, "validate_fail.zip")
            
        mock_unlink.assert_called_once_with(missing_ok=True)

    async def test_handle_grouped_archives_quarantine_logic(
        self, base_packager_args, fs, quarantine_dir
    ):
        """
        Tests that the quarantine logic moves files correctly, even when overwriting.
        """
        # 1. Setup
        root = Path("/fake_project")
        fs.create_file(root / "unmatched.md", contents="md content")
        fs.create_file(root / "unmatched.sha256", contents="sha content")

        fs.create_dir(quarantine_dir)
        fs.create_file(quarantine_dir / "unmatched.md", contents="pre-existing")

        args = base_packager_args | {"dry_run": False, "root": root}
        packager = ArchivePackager(**args)
        
        pair = (root / "unmatched.md", root / "unmatched.sha256")
        groups = {"default": [pair]}

        # 2. Act
        await packager.handle_grouped_archives(groups)
        
        # 3. Assert
        assert not fs.exists(root / "unmatched.md")
        assert not fs.exists(root / "unmatched.sha256")
        assert fs.exists(quarantine_dir / "unmatched.md")
        with open(quarantine_dir / "unmatched.md", "r") as f:
            assert f.read() == "md content"
        assert fs.exists(quarantine_dir / "unmatched.sha256")


    async def test_handle_grouped_archives_mtime_fallback(
        self, base_packager_args, fs, mocker, caplog
    ):
        """
        Covers the mtime fallback for sorting in grouped archives using a robust mock.
        """
        from datetime import datetime
        import time

        # 1. Setup
        root = Path("/fake_project")
        old_path = root / "group1_file_old.md"
        new_path = root / "group1_file_new.md"
        fs.create_file(old_path, contents="old")
        time.sleep(0.02)
        fs.create_file(new_path, contents="new")
        fs.create_dir(base_packager_args["archives_dir"])

        mocker.patch("create_dump.archive.packager.extract_timestamp", return_value=datetime.min)
        
        pairs = [(new_path, None), (old_path, None)]
        groups = {"group1": pairs}

        # 2. Setup Packager
        args = base_packager_args | {"keep_latest": True, "verbose": True, "root": root}
        packager = ArchivePackager(**args)

        # 3. Act
        with caplog.at_level("DEBUG"):
            _, to_delete = await packager.handle_grouped_archives(groups)

        # 4. Assert
        assert len(to_delete) == 1
        assert to_delete[0].name == "group1_file_old.md"
        assert "Fallback to mtime for sorting in group1" in caplog.text

    async def test_create_archive_sync_no_files(self, base_packager_args):
        """
        Test Coverage for line 64: _create_archive_sync handles empty list.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_path, archived_files = packager._create_archive_sync([], "empty.zip")
        
        assert archive_path is None
        assert archived_files == []

    async def test_create_archive_sync_none_in_list(self, base_packager_args):
        """
        Test Coverage for line 69: _create_archive_sync handles list of Nones.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_path, archived_files = packager._create_archive_sync([None, None], "empty.zip")
        
        assert archive_path is None
        assert archived_files == []

    @pytest.mark.anyio(backend='asyncio')
    async def test_create_archive_sync_stores_compressed_files(
        self, base_packager_args, test_project, mocker
    ):

        """
        Test Coverage for line 89: _create_archive_sync uses ZIP_STORED for .gz files.
        """
        # 1. Setup
        await test_project.create({"src/file1.txt": "file1", "src/file2.gz": "gz_content"})
        files = [
            test_project.path("src/file1.txt"),
            test_project.path("src/file2.gz"),
        ]
        
        args = base_packager_args | {"archive_format": "zip"}
        packager = ArchivePackager(**args)

        # 2. Mock
        # -----------------
        # 🐞 FIX: Correctly mock the .write method and the testzip method
        # -----------------
        
        # ⚡ FIX: Mock for the 'w' (write) call. We will assert on this mock.
        mock_write_zip = MagicMock()
        
        # ⚡ FIX: Mock for the 'r' (read/validate) call
        mock_validate_zip = MagicMock()
        mock_validate_zip.testzip.return_value = None # This makes validation pass
        
        mock_zip_open = mocker.patch("zipfile.ZipFile")
        # ⚡ FIX: Use side_effect to provide a *different* mock for each call.
        mock_zip_open.side_effect = [
            MagicMock(__enter__=MagicMock(return_value=mock_write_zip), __exit__=MagicMock(return_value=None)), # Call 1 (write)
            MagicMock(__enter__=MagicMock(return_value=mock_validate_zip), __exit__=MagicMock(return_value=None)) # Call 2 (read)
        ]
        
        # ⚡ FIX: Create a mock stat_result with a valid st_mode
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1234
        mock_stat_result.st_mode = stat.S_IFREG  # This makes path.is_file() True
        
        mocker.patch.object(Path, "stat", return_value=mock_stat_result)
        
        # 3. Act
        packager._create_archive_sync(files, "test.zip")

        # 4. Assert
        # -----------------
        # 🐞 FIX: Assert the call count on the correct mock
        # -----------------
        # ⚡ FIX: Assert against the correct mock (mock_write_zip)
        assert mock_write_zip.write.call_count == 2
        calls = mock_write_zip.write.call_args_list
        
        # ⚡ FIX: The files are sorted alphabetically by path before archival.
        assert calls[0][1]["arcname"] == "src/file1.txt"
        assert calls[0][1]["compress_type"] == zipfile.ZIP_DEFLATED
        
        assert calls[1][1]["arcname"] == "src/file2.gz"
        assert calls[1][1]["compress_type"] == zipfile.ZIP_STORED

    async def test_handle_single_archive_no_pairs(self, base_packager_args):
        """
        Test Coverage for line 148: handle_single_archive returns empty if no pairs.
        """
        packager = ArchivePackager(**base_packager_args)
        archive_paths, to_delete = await packager.handle_single_archive([])
        
        assert archive_paths == {}
        assert to_delete == []

    async def test_handle_grouped_archives_no_historical(
        self, base_packager_args, project_with_files, caplog
    ):
        """
        Test Coverage for line 272: handle_grouped_archives skips group with no historical pairs.
        """
        packager = ArchivePackager(**base_packager_args)
        
        tests_pairs = [p for p in project_with_files if "tests" in p[0].name]
        assert len(tests_pairs) == 1 # Pre-condition
        groups = {"tests": tests_pairs}

        with caplog.at_level("INFO"):
            # -----------------
            # 🐞 FIX: Add the missing variable assignment
            # -----------------
            archive_paths, to_delete = await packager.handle_grouped_archives(groups)
        
        assert archive_paths == {}
        assert to_delete == []
        
        # -----------------
        # 🐞 FIX: Use a simpler assertion that works with structlog
        # -----------------
        assert "No historical pairs for group" in caplog.text
        assert "tests" in caplog.text