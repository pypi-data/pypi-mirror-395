# tests/test_system.py

"""
Tests for Phase 2: src/create_dump/system.py
"""

from __future__ import annotations
import pytest
import subprocess
import asyncio
# ✨ NEW: Import signal and sys for handler testing
import signal
import sys
from unittest.mock import MagicMock, AsyncMock

from create_dump.system import (
    get_git_meta,
    get_git_ls_files,
    get_git_diff_files,
    # ✨ NEW: Import the global handler instance
    handler as global_handler
)
from create_dump.core import GitMeta

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test get_git_meta() (Sync) ---

def test_get_git_meta_success(test_project, mocker):
    """
    Tests that get_git_meta() correctly parses git output.
    """
    root = test_project.root

    # Mock subprocess.check_output
    def mock_check_output(*args, **kwargs):
        cmd = args[0]
        if "rev-parse" in cmd and "--abbrev-ref" in cmd:
            return b"main\n"  # Mock branch
        if "rev-parse" in cmd and "--short" in cmd:
            return b"a1b2c3d\n"  # Mock commit
        return b""

    mocker.patch("subprocess.check_output", side_effect=mock_check_output)

    git_meta = get_git_meta(root)

    assert isinstance(git_meta, GitMeta)
    assert git_meta.branch == "main"
    assert git_meta.commit == "a1b2c3d"

def test_get_git_meta_failure(test_project, mocker):
    """
    Tests that get_git_meta() returns None on a subprocess error.
    """
    root = test_project.root

    # Mock subprocess.check_output to raise an error
    mocker.patch(
        "subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, "git")
    )

    git_meta = get_git_meta(root)
    assert git_meta is None

# ✨ NEW: Add tests for CleanupHandler
class TestCleanupHandler:
    """Tests for the CleanupHandler signal and cleanup logic."""

    @pytest.fixture(autouse=True)
    def mock_sys_exit(self, mocker):
        """Mock sys.exit to prevent the test runner from exiting."""
        return mocker.patch("sys.exit")

    def test_cleanup_handler_sigint(self, mocker, mock_sys_exit):
        """Tests that SIGINT calls _cleanup and exits with 130."""
        mock_cleanup = mocker.patch("create_dump.system.CleanupHandler._cleanup")
        
        # Call the handler directly to simulate the signal
        global_handler._handler(signal.SIGINT, None)
        
        mock_cleanup.assert_called_once()
        mock_sys_exit.assert_called_once_with(130)

    def test_cleanup_handler_sigterm(self, mocker, mock_sys_exit):
        """Tests that SIGTERM calls _cleanup and exits with 143."""
        mock_cleanup = mocker.patch("create_dump.system.CleanupHandler._cleanup")

        # Call the handler directly to simulate the signal
        global_handler._handler(signal.SIGTERM, None)
        
        mock_cleanup.assert_called_once()
        mock_sys_exit.assert_called_once_with(143)

    def test_cleanup_handler_cleanup_with_temp_dir(self, mocker):
        """Tests the _cleanup logic when _temp_dir is set."""
        mock_temp_dir = MagicMock()
        mocker.patch("create_dump.system._temp_dir", mock_temp_dir)
        
        mock_stack = MagicMock()
        mocker.patch("create_dump.system._cleanup_stack", mock_stack)
        
        global_handler._cleanup()
        
        mock_temp_dir.cleanup.assert_called_once()
        mock_stack.close.assert_called_once()

    def test_cleanup_handler_cleanup_no_temp_dir(self, mocker):
        """Tests the _cleanup logic when _temp_dir is None."""
        # Ensure _temp_dir is None (default test state, but good to be explicit)
        mocker.patch("create_dump.system._temp_dir", None)
        
        mock_stack = MagicMock()
        mocker.patch("create_dump.system._cleanup_stack", mock_stack)
        
        global_handler._cleanup()
        
        mock_stack.close.assert_called_once()


# --- Test Async Git Functions ---

async def mock_subprocess(stdout: bytes, stderr: bytes, returncode: int) -> AsyncMock:
    """Helper to create a mock asyncio.subprocess.Process."""
    # Create a mock for the process object
    process_mock = AsyncMock()
    
    # Set the return value for the communicate() awaitable
    process_mock.communicate = AsyncMock(return_value=(stdout, stderr))
    
    # Set the returncode attribute
    process_mock.returncode = returncode
    
    return process_mock

async def test_get_git_ls_files_success(test_project, mocker):
    """
    Tests get_git_ls_files() on successful command execution.
    """
    root = test_project.root
    
    # Mock the return value of create_subprocess_exec
    process_mock = await mock_subprocess(
        stdout=b"src/main.py\nsrc/helpers.py\nREADME.md\n",
        stderr=b"",
        returncode=0
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_ls_files(root)

    assert files == ["src/main.py", "src/helpers.py", "README.md"]

async def test_get_git_ls_files_failure(test_project, mocker):
    """
    Tests get_git_ls_files() when the git command fails.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"",
        stderr=b"fatal: not a git repository",
        returncode=128
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_ls_files(root)

    assert files == []

# ✨ NEW: Test for the generic exception block
async def test_get_git_ls_files_exception(test_project, mocker):
    """
    Tests that get_git_ls_files() catches generic exceptions.
    """
    root = test_project.root
    mock_logger = mocker.patch("create_dump.system.logger")
    mocker.patch(
        "create_dump.system._run_async_cmd",
        side_effect=Exception("Test exception")
    )
    
    files = await get_git_ls_files(root)
    
    assert files == []
    mock_logger.error.assert_called_once_with(
        "Failed to run git ls-files", error="Test exception"
    )

async def test_get_git_diff_files_success(test_project, mocker):
    """
    Tests get_git_diff_files() on successful command execution.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"src/main.py\nREADME.md\n",
        stderr=b"",
        returncode=0
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_diff_files(root, "main")

    assert files == ["src/main.py", "README.md"]

async def test_get_git_diff_files_failure(test_project, mocker):
    """
    Tests get_git_diff_files() when the git command fails.
    """
    root = test_project.root
    
    process_mock = await mock_subprocess(
        stdout=b"",
        stderr=b"fatal: bad revision 'main'",
        returncode=1
    )
    mocker.patch("asyncio.create_subprocess_exec", return_value=process_mock)

    files = await get_git_diff_files(root, "main")

    assert files == []

# ✨ NEW: Test for the generic exception block
async def test_get_git_diff_files_exception(test_project, mocker):
    """
    Tests that get_git_diff_files() catches generic exceptions.
    """
    root = test_project.root
    mock_logger = mocker.patch("create_dump.system.logger")
    mocker.patch(
        "create_dump.system._run_async_cmd",
        side_effect=Exception("Test exception")
    )
    
    files = await get_git_diff_files(root, "main")
    
    assert files == []
    mock_logger.error.assert_called_once_with(
        "Failed to run git diff", ref="main", error="Test exception"
    )