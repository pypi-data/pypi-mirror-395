# tests/test_helpers.py

"""
Tests for Phase 1: src/create_dump/helpers.py
"""

from __future__ import annotations
import pytest
import anyio

# ⚡ FIXED: This import is correct because `pythonpath = "src"` in pyproject.toml
from create_dump.helpers import (
    slugify,
    get_language,
    is_text_file
)

from create_dump.helpers import _unique_path, parse_patterns
from unittest.mock import MagicMock, AsyncMock
from pathlib import Path
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


# --- Test slugify() ---

@pytest.mark.parametrize(
    "input_path, expected_slug",
    [
        ("src/main.py", "src-main-py"),
        ("src/archive/core.py", "src-archive-core-py"),
        ("./a/b/c.md", "a-b-c-md"),
        ("README.md", "readme-md"),
        ("a_b-c.d", "a-b-c-d"),
        ("a__b--c..d", "a-b-c-d"),
        ("a/b/", "a-b"),
        (".", ""),
        ("a/b/c", "a-b-c"),
        ("file with spaces", "file-with-spaces"),
    ],
)
def test_slugify(input_path: str, expected_slug: str):
    """
    Tests that slugify() correctly converts paths to safe anchor slugs.
    """
    assert slugify(input_path) == expected_slug


# --- Test get_language() ---

@pytest.mark.parametrize(
    "filename, expected_lang",
    [
        # Standard extensions
        ("main.py", "python"),
        ("script.sh", "bash"),
        ("config.yaml", "yaml"),
        ("config.yml", "yaml"),
        ("data.json", "json"),
        ("README.md", "markdown"),
        ("index.html", "html"),
        ("style.css", "css"),
        ("app.js", "javascript"),
        ("server.ts", "typescript"),
        ("component.jsx", "jsx"),
        ("component.tsx", "tsx"),
        ("README", "text"),
        ("file.unknown", "text"),
        ("data.txt", "text"),
        ("setup.cfg", "ini"),
        ("config.ini", "ini"),
        ("config.toml", "toml"),
        
        # Special basenames
        ("Dockerfile", "dockerfile"),
        ("dockerfile", "dockerfile"),
        (".dockerignore", "ini"),
        
        # Paths
        ("src/components/button.tsx", "tsx"),
        ("src/api/Dockerfile", "dockerfile"),
        ("file.zig", "zig"),
        # -----------------
        # 🐞 ADD THESE LINES
        # -----------------
        ("file.carbon", "carbon"),
        ("file.mojo", "mojo"),
        ("file.verse", "verse"),
        # -----------------
        # Special basenames
        ("Dockerfile", "dockerfile"),
    ],
)
def test_get_language(filename: str, expected_lang: str):
    """
    Tests that get_language() correctly identifies the language from a filename.
    """
    assert get_language(filename) == expected_lang

# --- Test is_text_file() ---

async def test_is_text_file_for_text(test_project):
    """
    Tests that a valid UTF-8 text file is correctly identified.
    """
    # Setup: Create a text file
    await test_project.create({
        "hello.txt": "This is a standard text file.\nWith multiple lines."
    })
    
    # Get the async path object
    text_file_path = anyio.Path(test_project.path("hello.txt"))
    
    # Test
    assert await is_text_file(text_file_path) is True

async def test_is_text_file_for_binary(test_project):
    """
    Tests that a binary file (containing null bytes) is correctly identified.
    """
    # Setup: Create a binary file (must write bytes, not text)
    binary_content = b"This is binary \x00 code"
    bin_path = test_project.root / "app.bin"
    
    # Use anyio to run the sync byte write in a thread
    await anyio.to_thread.run_sync(bin_path.write_bytes, binary_content)
    
    # Get the async path object
    binary_file_path = anyio.Path(bin_path)

    # Test
    assert await is_text_file(binary_file_path) is False

async def test_is_text_file_for_empty(test_project):
    """
    Tests that an empty file is considered text (not binary).
    """
    # Setup: Create an empty file
    await test_project.create({
        "empty.txt": ""
    })
    
    # Get the async path object
    empty_file_path = anyio.Path(test_project.path("empty.txt"))
    
    # Test
    assert await is_text_file(empty_file_path) is True

async def test_is_text_file_for_unicode(test_project):
    """
    Tests that a file with Unicode (but not null bytes) is text.
    """
    # Setup: Create a text file with unicode
    await test_project.create({
        "unicode.txt": "Hello, world! 🌍"
    })
    
    # Get the async path object
    unicode_file_path = anyio.Path(test_project.path("unicode.txt"))
    
    # Test
    assert await is_text_file(unicode_file_path) is True
    

# [TEST_SKELETON_START]
# --- Test is_text_file() Error Paths ---

async def test_is_text_file_os_error(mocker):
    """
    Action Plan 2: Test is_text_file Errors (OSError).
    Tests that an OSError during file open returns False.
    """
    # 1. Setup
    mock_path = AsyncMock(spec=anyio.Path)
    # 2. Mock: Make .open() raise an error
    mock_path.open = AsyncMock(side_effect=OSError("Permission denied"))
    
    # 3. Act
    result = await is_text_file(mock_path)
    
    # 4. Assert
    assert result is False

async def test_is_text_file_unicode_error(mocker):
    """
    Action Plan 2: Test is_text_file Errors (UnicodeDecodeError).
    Tests that a UnicodeDecodeError during read returns False.
    """
    # 1. Setup
    mock_path = AsyncMock(spec=anyio.Path)
    mock_file = AsyncMock()
    # 2. Mock: Make .read() raise the error
    mock_file.read = AsyncMock(side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte"))
    mock_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_file))
    mock_path.open = AsyncMock(return_value=mock_context)
    
    # 3. Act
    result = await is_text_file(mock_path)
    
    # 4. Assert
    assert result is False

# --- Test parse_patterns() Error Path ---

def test_parse_patterns_error(mocker):
    """
    Tests that a GitWildMatchPatternError is caught and re-raised as a ValueError.
    """
    # 1. Mock
    mocker.patch(
        "create_dump.helpers.PathSpec.from_lines",
        side_effect=GitWildMatchPatternError("Bad pattern")
    )
    
    # 2. Act & Assert
    with pytest.raises(ValueError, match="Invalid patterns"):
        parse_patterns(["[invalid"])

# --- Test _unique_path() Collision Logic ---

def test_unique_path_collision(mocker, tmp_path: Path):
    """
    Action Plan 1: Test _unique_path Collisions.
    Tests the collision-handling loop logic.
    """
    # 1. Setup
    base_path = tmp_path / "file.txt"
    
    # 2. Mock UUID to return predictable values
    mock_uuid_1 = MagicMock()
    mock_uuid_1.hex = "11111111" # First collision
    mock_uuid_2 = MagicMock()
    mock_uuid_2.hex = "22222222" # Second, successful
    mocker.patch("create_dump.helpers.uuid.uuid4", side_effect=[mock_uuid_1, mock_uuid_2])

    # 3. Mock path existence checks
    # First check (os.path.exists) on base path is True
    mocker.patch("create_dump.helpers.os.path.exists", return_value=True)
    
    # -----------------
    # 🐞 FIX: Correct patch target from "create_dump.helpers.pathlib.Path.exists"
    # to "create_dump.helpers.Path.exists"
    # -----------------
    mock_path_exists = mocker.patch(
        "create_dump.helpers.Path.exists", 
        side_effect=[True, False]
    )
    
    # 4. Define expected paths
    colliding_path = tmp_path / "file_11111111.txt"
    # Loop 1: counter = 0. stem = "file_11111111"
    # Loop 2: counter = 1. stem = "file_1_22222222"
    final_path = tmp_path / "file_1_22222222.txt"

    # 5. Act
    result = _unique_path(base_path)

    # 6. Assert
    assert result == final_path
    
    # Check that Path.exists was called twice
    assert mock_path_exists.call_count == 2
    # Check the paths it was called with
    assert mock_path_exists.call_args_list[0].args[0].name == "file_11111111.txt"
    assert mock_path_exists.call_args_list[1].args[0].name == "file_1_22222222.txt"

def test_unique_path_no_collision(mocker, tmp_path: Path):
    """
    Tests the happy path where the original file does not exist.
    """
    base_path = tmp_path / "file.txt"
    
    # Mock os.path.exists to return False
    mocker.patch("create_dump.helpers.os.path.exists", return_value=False)
    
    # -----------------
    # 🐞 FIX: Correct patch target
    # -----------------
    mock_path_exists = mocker.patch("create_dump.helpers.Path.exists")

    result = _unique_path(base_path)

    # Assert it returns the original path immediately
    assert result == base_path
    # Assert the loop was never entered
    mock_path_exists.assert_not_called()
# [TEST_SKELETON_END]