# tests/test_cleanup.py

"""
Tests for Phase 3: src/create_dump/cleanup.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging
import shutil  # For mock targets
# ⚡ REFACTOR: Import AsyncGenerator for mocking
from typing import AsyncGenerator

import anyio

# Import the functions to test
from create_dump.cleanup import (
    safe_delete_paths,
    safe_cleanup
)
from create_dump.logging import setup_logging
# ⚡ REFACTOR: Import the new async util
from create_dump.path_utils import safe_is_within


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestSafeDeletePathsAsync:
    """Groups tests for the core safe_delete_paths worker."""

    async def test_deletes_files_and_dirs(self, test_project):
        """
        Test Case 1: (Happy Path)
        Ensures files and directories are actually deleted (passing a List).
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
            "keep_me.txt": "content"
        })

        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (1, 1)
        assert not await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert not await (anyio.Path(root) / "dir_to_delete").exists()
        assert await (anyio.Path(root) / "keep_me.txt").exists()

    async def test_deletes_from_generator(self, test_project):
        """
        Test Case 1b: (Happy Path - Generator)
        Ensures files and directories are deleted when passed as an AsyncGenerator.
        """
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
        })

        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]
        
        async def path_gen() -> AsyncGenerator[Path, None]:
            for p in paths_to_delete:
                yield p

        deleted_files, deleted_dirs = await safe_delete_paths(
            path_gen(), root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (1, 1)
        assert not await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert not await (anyio.Path(root) / "dir_to_delete").exists()

    async def test_dry_run_logs_and_skips_deletion(self, test_project, capsys):
        """
        Test Case 2: (Dry Run)
        Ensures no files are deleted and logs are produced.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete.txt": "content",
            "dir_to_delete/file.txt": "content",
        })
        paths_to_delete = [
            root / "file_to_delete.txt",
            root / "dir_to_delete"
        ]

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=True, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        assert await (anyio.Path(root) / "file_to_delete.txt").exists()
        assert await (anyio.Path(root) / "dir_to_delete").exists()

        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        assert err.count("[dry-run] would delete file") == 1
        assert err.count("[dry-run] would remove directory") == 1

    async def test_skips_paths_outside_root(self, test_project, capsys):
        """
        Test Case 3: (Path Safety)
        Ensures files outside the root are ignored.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        # Create a file *outside* the test project root
        external_file = root.parent / "external_file.txt"
        await anyio.Path(external_file).write_text("external")

        try:
            deleted_files, deleted_dirs = await safe_delete_paths(
                [external_file], root, dry_run=False, assume_yes=True
            )

            assert (deleted_files, deleted_dirs) == (0, 0)
            assert await anyio.Path(external_file).exists()
            # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
            out, err = capsys.readouterr()
            assert "Skipping path outside root" in err

        finally:
            # Clean up the external file
            await anyio.Path(external_file).unlink(missing_ok=True)

    async def test_prompts_for_dir_deletion(self, test_project, mocker):
        """
        Test Case 4: (User Prompting)
        Ensures `confirm` is called and respected.
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({"dir_to_delete": None})
        dir_path = root / "dir_to_delete"

        # Mock the confirm function (which is run in a thread)
        mock_confirm = mocker.patch(
            "create_dump.cleanup.confirm", return_value=False
        )

        # 1. Test "No" response
        deleted_files, deleted_dirs = await safe_delete_paths(
            [dir_path], root, dry_run=False, assume_yes=False
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        mock_confirm.assert_called_once()
        assert await anyio.Path(dir_path).exists()

        # 2. Test "Yes" response
        mock_confirm.return_value = True
        mock_confirm.reset_mock()

        deleted_files, deleted_dirs = await safe_delete_paths(
            [dir_path], root, dry_run=False, assume_yes=False
        )

        assert (deleted_files, deleted_dirs) == (0, 1)
        mock_confirm.assert_called_once()
        assert not await anyio.Path(dir_path).exists()

    # ⚡ NEW: Test case to validate the exception hardening
    async def test_delete_async_logs_ioerror_and_fails_on_other_errors(self, test_project, mocker, capsys):
        """
        Test Case 5: (Error Hardening)
        Ensures the refactored exception block catches (OSError, IOError)
        but correctly *re-raises* other exceptions (like TypeError).
        """
        setup_logging(verbose=True)
        root = test_project.root
        await test_project.create({"file_to_delete.txt": "content"})
        paths_to_delete = [root / "file_to_delete.txt"]

        # --- Part 1: Test OSError is caught ---
        # 🐞 FIX: Mock the correct object (anyio.Path.unlink) with OSError
        mocker.patch.object(
            anyio.Path, "unlink",
            side_effect=OSError("Simulated Disk Full")
        )

        deleted_files, deleted_dirs = await safe_delete_paths(
            paths_to_delete, root, dry_run=False, assume_yes=True
        )

        assert (deleted_files, deleted_dirs) == (0, 0)
        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        assert "Failed to delete file" in err
        assert "Simulated Disk Full" in err

        # --- Part 2: Test TypeError is NOT caught ---
        mocker.patch.object(
            anyio.Path, "unlink",
            side_effect=TypeError("Simulated Non-IO Error")
        )

        with pytest.raises(TypeError, match="Simulated Non-IO Error"):
            await safe_delete_paths(
                paths_to_delete, root, dry_run=False, assume_yes=True
            )

# ⚡ REFACTOR: Add fixture to mock the generator
@pytest.fixture
def mock_find_matching_files(mocker):
    """Mocks the find_matching_files generator."""
    mock_gen_func = mocker.patch("create_dump.cleanup.find_matching_files")
    
    async def create_gen(file_list: List[Path]) -> AsyncGenerator[Path, None]:
        for f in file_list:
            yield f
    
    # Default behavior: return an empty generator
    mock_gen_func.return_value = create_gen([])
    return mock_gen_func, create_gen

class TestSafeCleanupAsync:
    """Groups tests for the safe_cleanup wrapper."""

    async def test_safe_cleanup_finds_and_deletes(self, test_project, mock_find_matching_files):
        """
        Test Case 6: (Integration)
        Tests the full wrapper finds files by pattern and deletes them.
        """
        # 🐞 FIX: Setup logging for this test to see error logs
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete_1.log": "delete me",
            "subdir/file_to_delete_2.log": "delete me too",
            "file_to_keep.txt": "keep me"
        })

        pattern = r".*\.log$"
        
        # ⚡ REFACTOR: Configure mock to return the files
        mock_gen_func, gen_factory = mock_find_matching_files
        files_to_find = [
            root / "file_to_delete_1.log",
            root / "subdir/file_to_delete_2.log"
        ]
        mock_gen_func.return_value = gen_factory(files_to_find)

        await safe_cleanup(
            root, pattern, dry_run=False, assume_yes=True, verbose=True
        )

        assert not await (anyio.Path(root) / "file_to_delete_1.log").exists()
        assert not await (anyio.Path(root) / "subdir/file_to_delete_2.log").exists()
        assert await (anyio.Path(root) / "file_to_keep.txt").exists()


    async def test_safe_cleanup_dry_run(self, test_project, capsys, mock_find_matching_files):
        """
        Test Case 7: (Integration - Dry Run)
        Tests that the wrapper respects dry_run.
        """
        # 🐞 FIX: Setup logging *inside* test to bind to caplog
        setup_logging(verbose=True)

        root = test_project.root
        await test_project.create({
            "file_to_delete_1.log": "delete me",
        })
        
        # ⚡ REFACTOR: Configure mock to return the file
        mock_gen_func, gen_factory = mock_find_matching_files
        mock_gen_func.return_value = gen_factory([root / "file_to_delete_1.log"])

        pattern = r".*\.log$"

        await safe_cleanup(
            root, pattern, dry_run=True, assume_yes=True, verbose=True
        )

        assert await (anyio.Path(root) / "file_to_delete_1.log").exists()

        # 🐞 FIX: Check the rendered 'err' for ConsoleRenderer via capsys
        out, err = capsys.readouterr()
        # ⚡ REFACTOR: Test the new generator-aware log message
        assert "Found paths to clean (starting with: file_to_delete_1.log)" in err
        assert "Dry-run: Skipping deletions." in err

    async def test_safe_cleanup_no_matches(self, test_project, capsys, mock_find_matching_files):
        """
        Test Case 8: (Integration - No Matches)
        Tests the "no matches" branch.
        """
        setup_logging(verbose=True)
        root = test_project.root
        
        # ⚡ REFACTOR: Mock is already configured to return an empty generator
        
        pattern = r".*\.log$"
        await safe_cleanup(
            root, pattern, dry_run=False, assume_yes=True, verbose=True
        )
        
        out, err = capsys.readouterr()
        assert "No matching files found for cleanup." in err