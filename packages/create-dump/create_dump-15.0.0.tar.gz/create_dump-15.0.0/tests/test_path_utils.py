# tests/test_path_utils.py

"""
Tests for Phase 1: src/create_dump/path_utils.py
"""

from __future__ import annotations
import pytest
import anyio
import os
from pathlib import Path


# [TEST_SKELETON_START]
# Add these imports at the top of tests/test_path_utils.py
from create_dump.path_utils import confirm
from unittest.mock import MagicMock, AsyncMock, patch
# [TEST_SKELETON_END]

# ⚡ REFACTOR: Import the new async-native functions
from create_dump.path_utils import (
    safe_is_within,
    find_matching_files
)

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test safe_is_within() ---

@pytest.mark.parametrize(
    "path_str, expected",
    [
        # Standard valid cases
        ("src/main.py", True),
        ("file.txt", True),
        (".", True),
        ("src/sub/deep/file.py", True),
        
        # Standard invalid cases
        ("..", False),
        ("../", False),
        ("../file.txt", False),
        ("../src/file.txt", False),
        ("src/../../file.txt", False),
        
        # Absolute paths
        ("/etc/passwd", False),
        ("/tmp/file", False),
        ("/var/log/syslog", False),
    ],
)
# ⚡ RENAMED: Appended 
async def test_safe_is_within_basic(test_project, path_str: str, expected: bool):
    """
    Tests safe_is_within() for basic path traversal and absolute paths.
    """
    # ⚡ REFACTOR: Use anyio.Path objects
    anyio_root = test_project.async_root
    anyio_path_to_check = anyio_root / path_str
    
    # ⚡ REFACTOR: Call the async function and await it
    # The function handles its own resolution.
    assert await safe_is_within(anyio_path_to_check, anyio_root) is expected

# ⚡ RENAMED: Appended 
async def test_safe_is_within_symlinks(test_project):
    """
    Tests that safe_is_within() correctly handles symlinks.
    This is the most critical security test for this function.
    """
    # ⚡ REFACTOR: Use anyio.Path objects
    anyio_root = test_project.async_root
    root = test_project.root # Keep sync root for os.symlink
    
    # 1. Create a "safe" symlink pointing *inside* the project
    await test_project.create({
        "src/main.py": "print('hello')",
    })
    safe_symlink_path = root / "safe_link.py"
    await anyio.to_thread.run_sync(os.symlink, "src/main.py", safe_symlink_path)
    anyio_safe_symlink = anyio_root / "safe_link.py"

    # 2. Create a "dangerous" symlink pointing *outside* the project
    secret_file = Path(f"/tmp/secret_file_{os.getpid()}")
    await anyio.Path(secret_file).write_text("iamasecret")
    
    dangerous_symlink_path = root / "danger_link"
    await anyio.to_thread.run_sync(os.symlink, secret_file, dangerous_symlink_path)
    anyio_dangerous_symlink = anyio_root / "danger_link"

    # 3. Create a symlink that traverses up and back in
    target_file = root.parent / "src" / "main.py"
    await anyio.Path(target_file.parent).mkdir(parents=True, exist_ok=True)
    await anyio.Path(target_file).write_text("external")
    
    complex_symlink_path = root / "complex_link"
    await anyio.to_thread.run_sync(os.symlink, "../src/main.py", complex_symlink_path)
    anyio_complex_symlink = anyio_root / "complex_link"

    # Test assertions
    # ⚡ REFACTOR: Call the async function directly with anyio.Path objects
    assert await safe_is_within(anyio_safe_symlink, anyio_root) is True
    
    assert await safe_is_within(anyio_dangerous_symlink, anyio_root) is False
    
    assert await safe_is_within(anyio_complex_symlink, anyio_root) is False

    # Cleanup the external files
    await anyio.Path(secret_file).unlink()
    await anyio.Path(target_file).unlink()
    await anyio.Path(target_file.parent).rmdir()


# ⚡ RENAMED: Appended 
async def test_safe_is_within_root_as_path(test_project):
    """
    Tests that checking the root directory itself returns True.
    """
    anyio_root = test_project.async_root
    # ⚡ REFACTOR: Call the async function
    assert await safe_is_within(anyio_root, anyio_root) is True


# --- Test find_matching_files() ---

# ⚡ RENAMED: Appended 
async def test_find_matching_files(test_project):
    """
    Tests the async file finder.
    """
    await test_project.create({
        "src/main.py": "",
        "src/data/dump_2025.md": "",
        "src/data/dump_2024.md.sha256": "",
        "README.md": "",
        "logs/app.log": "",
    })
    
    # Test finding all .md files
    # ⚡ FIX: Consume the async generator using an async list comprehension
    md_files = [p async for p in find_matching_files(test_project.root, r"\.md$")]
    assert len(md_files) == 2
    paths_as_str = {p.name for p in md_files}
    assert paths_as_str == {"dump_2025.md", "README.md"}
    
    # Test finding canonical dump files
    # ⚡ FIX: Consume the async generator using an async list comprehension
    dump_files_gen = find_matching_files(
        test_project.root, 
        r"dump_.*\.md(\.sha256)?$"
    )
    dump_files = [p async for p in dump_files_gen]
    assert len(dump_files) == 2
    paths_as_str = {p.name for p in dump_files}
    assert paths_as_str == {"dump_2025.md", "dump_2024.md.sha256"}
    

# [TEST_SKELETON_START]
# --- Test safe_is_within() Error Paths ---

async def test_safe_is_within_attribute_error_fallback(mocker):
    """
    Action Plan 1: Test safe_is_within() fallback logic.
    Mocks is_relative_to to raise AttributeError, forcing the str() check.
    """
    # 1. Setup mock pathlib.Path objects that will be returned by .resolve()
    mock_resolved_path = MagicMock(spec=Path)
    mock_resolved_root = MagicMock(spec=Path)

    # 2. Mock is_relative_to to raise AttributeError
    mocker.patch.object(
        mock_resolved_path, 
        "is_relative_to", 
        side_effect=AttributeError("Simulating Python < 3.9")
    )

    # 3. Configure the string representations for the fallback check
    # Case 1: Path IS within root
    mock_resolved_path.__str__.return_value = "/app/src/main.py"
    mock_resolved_root.__str__.return_value = "/app"

    # 4. Setup mock anyio.Path objects
    mock_path = AsyncMock(spec=anyio.Path)
    mock_path.resolve = AsyncMock(return_value=mock_resolved_path)
    mock_root = AsyncMock(spec=anyio.Path)
    mock_root.resolve = AsyncMock(return_value=mock_resolved_root)

    # 5. Act & Assert (Case 1: Success)
    assert await safe_is_within(mock_path, mock_root) is True

    # Case 2: Path is NOT within root (e.g., sibling folder)
    mock_resolved_path.__str__.return_value = "/other/main.py"
    mock_resolved_root.__str__.return_value = "/app"
    
    # 6. Act & Assert (Case 2: Failure)
    assert await safe_is_within(mock_path, mock_root) is False

# --- Test confirm() ---

def test_confirm_keyboard_interrupt(mocker):
    """
    Action Plan 2: Test confirm() handles KeyboardInterrupt.
    """
    # 1. Mock built-in 'input' to raise KeyboardInterrupt
    mocker.patch("builtins.input", side_effect=KeyboardInterrupt)
    
    # 2. Mock 'print' to suppress output during test
    mocker.patch("builtins.print")
    
    # 3. Act & Assert
    assert confirm("Delete everything?") is False

def test_confirm_yes_answers(mocker):
    """
    Tests that 'y' and 'yes' are accepted.
    """
    mocker.patch("builtins.input", side_effect=["y", "yes", "Y", "YES "])
    assert confirm("Prompt 1") is True
    assert confirm("Prompt 2") is True
    assert confirm("Prompt 3") is True
    assert confirm("Prompt 4") is True

def test_confirm_no_answers(mocker):
    """
    Tests that 'n', 'no', and empty input are rejected.
    """
    mocker.patch("builtins.input", side_effect=["n", "no", "N", " anything else", ""])
    assert confirm("Prompt 1") is False
    assert confirm("Prompt 2") is False
    assert confirm("Prompt 3") is False
    assert confirm("Prompt 4") is False
    assert confirm("Prompt 5") is False
# [TEST_SKELETON_END]