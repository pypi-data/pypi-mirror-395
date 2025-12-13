# tests/rollback/test_engine.py

"""
Tests for src/create_dump/rollback/engine.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator, Tuple

import anyio

# Import classes to test
from create_dump.rollback.engine import RollbackEngine
from create_dump.rollback.parser import MarkdownParser
# ✨ NEW: Import safe_is_within to check its call
from create_dump.path_utils import safe_is_within


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_parser(mocker) -> MagicMock:
    """Mocks the MarkdownParser."""
    mock = MagicMock(spec=MarkdownParser)

    async def mock_generator() -> AsyncGenerator[Tuple[str, str], None]:
        yield ("src/main.py", "print('hello')")
        yield ("src/nested/util.py", "def helper(): pass")
        yield ("README.md", "# Title")
        # 🔒 Add a malicious path to test safety
        yield ("../etc/passwd", "root:x:0:0")

    mock.parse_dump_file = mock_generator
    return mock


class TestRollbackEngine:
    """Tests for the RollbackEngine."""

    async def test_rehydrate_creates_files_and_dirs(self, test_project, mock_parser):
        """
        Test Case 1: (Happy Path)
        Ensures the engine correctly creates nested directories and files
        with the correct content and skips unsafe paths.
        """
        output_dir = test_project.path("my_rollback")
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=False)

        created_files = await engine.rehydrate(mock_parser)

        # Should be 3 files; the malicious path is skipped
        assert len(created_files) == 3

        # Check file 1
        file1_path = anyio.Path(output_dir / "src/main.py")
        assert await file1_path.exists()
        assert await file1_path.read_text() == "print('hello')"

        # Check file 2 (nested)
        file2_path = anyio.Path(output_dir / "src/nested/util.py")
        assert await file2_path.exists()
        assert await file2_path.read_text() == "def helper(): pass"

        # Check file 3 (root)
        file3_path = anyio.Path(output_dir / "README.md")
        assert await file3_path.exists()
        assert await file3_path.read_text() == "# Title"

        # Check that the malicious file was NOT created
        assert not await anyio.Path(output_dir / "../etc/passwd").exists()
        assert not await anyio.Path(test_project.root / "etc/passwd").exists()

    async def test_rehydrate_dry_run(self, test_project, mock_parser, mocker):
        """
        Test Case 2: (Dry Run)
        Ensures no files or directories are created when dry_run=True,
        but logging still occurs.
        """
        output_dir = test_project.path("dry_run_rollback")
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=True)

        mock_logger_info = mocker.patch("create_dump.rollback.engine.logger.info")
        mock_logger_warn = mocker.patch("create_dump.rollback.engine.logger.warning")

        created_files = await engine.rehydrate(mock_parser)

        # It still *reports* what it would do (minus the skipped file)
        assert len(created_files) == 3

        # Assert no directory or files were actually created
        assert not await anyio.Path(output_dir).exists()
        assert not await anyio.Path(output_dir / "src/main.py").exists()

        # ⚡ FIX: Assert logging using the f-string format
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'src/main.py')}"
        )
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'src/nested/util.py')}"
        )
        mock_logger_info.assert_any_call(
            f"[dry-run] Would rehydrate file to: {anyio.Path(output_dir / 'README.md')}"
        )

        # ♻️ REFACTOR: Assert the new, more descriptive warning message
        mock_logger_warn.assert_called_once_with(
            "Skipping unsafe path: Resolves outside root",
            path="../etc/passwd",
            # Check that the resolved path is logged correctly
            resolved_to=str(anyio.Path(output_dir / "../etc/passwd"))
        )

        # Assert the final summary log
        mock_logger_info.assert_any_call(
            "Rehydration complete",
            files_created=3
        )

    async def test_rehydrate_handles_write_error(self, test_project, mock_parser, mocker):
        """
        Test Case 3: (Error Handling)
        Ensures that if the engine fails to write a file,
        the error is logged and the loop continues.
        """
        output_dir = test_project.path("error_rollback")
        # 🐞 NOTE: We instantiate engine *after* setting up the patch

        mock_logger_error = mocker.patch("create_dump.rollback.engine.logger.error")

        # 🐞 FIX: Mock the individual paths that will be returned by __truediv__
        mock_good_path = AsyncMock(spec=anyio.Path)
        mock_good_path.parent.mkdir = AsyncMock()
        mock_good_path.write_text = AsyncMock()
        # ✨ NEW: Implement the __fspath__ protocol
        mock_good_path.__fspath__ = MagicMock(return_value=str(output_dir / "src/main.py"))

        mock_bad_path = AsyncMock(spec=anyio.Path)
        mock_bad_path.parent.mkdir = AsyncMock()
        mock_bad_path.write_text = AsyncMock(side_effect=OSError("Disk full"))
        # ✨ NEW: Implement the __fspath__ protocol (even though it fails)
        mock_bad_path.__fspath__ = MagicMock(return_value=str(output_dir / "src/nested/util.py"))

        mock_readme_path = AsyncMock(spec=anyio.Path)
        mock_readme_path.parent.mkdir = AsyncMock()
        mock_readme_path.write_text = AsyncMock()
        # ✨ NEW: Implement the __fspath__ protocol
        mock_readme_path.__fspath__ = MagicMock(return_value=str(output_dir / "README.md"))

        mock_unsafe_path = AsyncMock(spec=anyio.Path) # For the ../etc/passwd path
        # ✨ NEW: Implement the __fspath__ protocol
        mock_unsafe_path.__fspath__ = MagicMock(return_value=str(output_dir / "../etc/passwd"))

        # We also need to mock safe_is_within as it's called on every path
        mock_safe_is_within = mocker.patch(
            "create_dump.rollback.engine.safe_is_within",
            new_callable=AsyncMock
        )
        # 🐞 FIX: Configure side_effect based on the mock object *identity*
        def safe_side_effect(path, root):
            if path is mock_unsafe_path:
                return False
            return True
        mock_safe_is_within.side_effect = safe_side_effect

        # 🐞 FIX: Use a side_effect on the *mock root's* __truediv__ method
        def truediv_side_effect(rel_path):
            if "main.py" in str(rel_path):
                return mock_good_path
            if "util.py" in str(rel_path):
                return mock_bad_path
            if "README.md" in str(rel_path):
                return mock_readme_path
            if "passwd" in str(rel_path):
                return mock_unsafe_path
            # Fallback for parent dirs, etc.
            return AsyncMock(parent=AsyncMock(mkdir=AsyncMock()), write_text=AsyncMock())

        # 🐞 FIX: Create the mock for engine.anyio_root *itself*
        mock_anyio_root = AsyncMock(spec=anyio.Path)
        # 🐞 FIX: Configure the mock's method, not patch it
        mock_anyio_root.__truediv__ = MagicMock(side_effect=truediv_side_effect)

        # 🐞 FIX: Patch the anyio.Path constructor *in the engine module*
        # to return our pre-configured mock root.
        mocker.patch(
            "create_dump.rollback.engine.anyio.Path",
            return_value=mock_anyio_root
        )

        # 🐞 FIX: NOW instantiate the engine.
        # Its self.anyio_root will be our mock_anyio_root.
        engine = RollbackEngine(root_output_dir=output_dir, dry_run=False)

        # We must also assert that the *correct* object was patched
        assert engine.anyio_root is mock_anyio_root

        # 🐞 FIX: The failing patch.object call is removed.

        # ⚡ FIX: We must use the *original* parser mock, which yields all 4 files
        created_files = await engine.rehydrate(mock_parser)

        # ⚡ FIX: Should have created "src/main.py" and "README.md"
        # Should have skipped "src/nested/util.py" (error) and "../etc/passwd" (unsafe)
        assert len(created_files) == 2
        # ✨ NEW: The assertions will now pass
        assert created_files[0].name == "main.py"
        assert created_files[1].name == "README.md"

        # Assert the "Disk full" error was logged
        mock_logger_error.assert_called_once_with(
            "Failed to rehydrate file",
            path="src/nested/util.py",
            error="Disk full"
        )