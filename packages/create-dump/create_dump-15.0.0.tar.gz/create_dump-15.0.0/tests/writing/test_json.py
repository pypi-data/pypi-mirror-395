# tests/writing/test_json.py

"""
Tests for Phase 3: src/create_dump/writing/json.py
"""

from __future__ import annotations
from datetime import datetime, timezone
import pytest
import json
from pathlib import Path
from typing import Callable, Awaitable
# ⚡ FIX: Import MagicMock and AsyncMock
from unittest.mock import MagicMock, AsyncMock

import anyio

# Import the class to test
from create_dump.writing.json import JsonWriter
from create_dump.core import DumpFile, GitMeta

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_git_meta() -> GitMeta:
    """Provides a standard GitMeta object."""
    return GitMeta(branch="main", commit="abc1234")


@pytest.fixture
async def temp_dumpfile_factory(tmp_path_factory):
    """
    Provides an async factory to create a DumpFile object
    backed by a real temporary file with content.
    (This fixture can be shared with test_markdown.py)
    """
    temp_dir = tmp_path_factory.mktemp("json_writer_temps")
    
    async def _create(
        file_path: str,
        content: str | None = None,
        language: str | None = "python",
        error: str | None = None
    ) -> DumpFile:
        
        if error:
            return DumpFile(path=file_path, language=language, error=error)
        
        # Create the temp file
        temp_file = anyio.Path(temp_dir) / f"{file_path.replace('/', '_')}.tmp"
        await temp_file.write_text(content or "")
        
        return DumpFile(
            path=file_path,
            language=language,
            temp_path=Path(temp_file) # The writer expects a sync Path
        )
    
    return _create


async def test_json_writer(
    test_project, temp_dumpfile_factory, mock_git_meta
):
    """
    Tests that the JsonWriter correctly writes a JSON file,
    including metadata, successful files, and error files.
    """
    # 1. Setup
    outfile = test_project.path("dump.json")
    
    files_to_process = [
        await temp_dumpfile_factory(
            file_path="src/main.py",
            content="print('hello')",
            language="python"
        ),
        await temp_dumpfile_factory(
            file_path="src/failed.py",
            language="python",
            error="File read error"
        ),
    ]

    writer = JsonWriter(outfile)
    
    # 2. Act
    await writer.write(files_to_process, mock_git_meta, "8.0.0", total_files=2, total_loc=2)

    # 3. Assert
    
    # Check atomic write
    output_path = anyio.Path(outfile)
    assert await output_path.exists()
    assert not await anyio.Path(outfile.with_suffix(".tmp")).exists()
    
    # Parse the JSON content
    content_str = await output_path.read_text()
    data = json.loads(content_str)
    
    # Check top-level metadata
    assert data["version"] == "8.0.0"
    assert data["git_meta"]["branch"] == "main"
    assert data["git_meta"]["commit"] == "abc1234"
    assert "generated" in data
    assert len(data["files"]) == 2
    assert data["total_files"] == 2
    assert data["total_lines_of_code"] == 2
    
    # Check successful file entry
    file1 = data["files"][0]
    assert file1["path"] == "src/main.py"
    assert file1["language"] == "python"
    assert file1["content"] == "print('hello')"
    assert file1["error"] is None
    
    # Check error file entry
    file2 = data["files"][1]
    assert file2["path"] == "src/failed.py"
    assert file2["language"] == "python"
    assert file2["content"] is None
    assert file2["error"] == "File read error"


# ✨ NEW: Test for lines 61-63
async def test_json_writer_read_temp_file_error(
    test_project, temp_dumpfile_factory, mock_git_meta, mocker
):
    """
    Tests that if reading a temp file fails, the error is
    logged and included in the final JSON.
    """
    # 1. Setup
    outfile = test_project.path("dump_error.json")
    
    # This file will fail
    failing_dumpfile = await temp_dumpfile_factory(
        file_path="src/fails.py",
        content="i will fail",
        language="python"
    )
    
    writer = JsonWriter(outfile)
    
    # 2. Mock: Make _read_temp_file fail
    mocker.patch.object(
        JsonWriter, 
        "_read_temp_file", 
        side_effect=OSError("Simulated read error")
    )
    mock_logger_error = mocker.patch("create_dump.writing.json.logger.error")
    
    # 3. Act
    await writer.write([failing_dumpfile], mock_git_meta, "8.0.0", total_files=1, total_loc=1)

    # 4. Assert
    output_path = anyio.Path(outfile)
    assert await output_path.exists()
    data = json.loads(await output_path.read_text())
    
    assert len(data["files"]) == 1
    
    # Check failed file
    assert data["files"][0]["path"] == "src/fails.py"
    assert data["files"][0]["content"] is None
    assert "Simulated read error" in data["files"][0]["error"]
    
    # Check logger
    mock_logger_error.assert_called_once_with(
        "Failed to read content for JSON dump",
        path="src/fails.py", 
        error="Simulated read error"
    )


# ✨ NEW: Test for lines 91-94
async def test_json_writer_atomic_write_failure(
    test_project, temp_dumpfile_factory, mock_git_meta, mocker
):
    """
    Tests that if the final atomic rename fails, the .tmp file is
    cleaned up.
    """
    # 1. Setup
    outfile = test_project.path("dump_fail.json")
    
    files_to_process = [
        await temp_dumpfile_factory(
            file_path="src/main.py",
            content="print('hello')"
        ),
    ]
    
    writer = JsonWriter(outfile)
    
    # ⚡ FIX: Mock _read_temp_file to prevent it from calling anyio.Path
    # and interfering with the mock below. This ensures json.dumps() succeeds.
    mocker.patch.object(
        JsonWriter, 
        "_read_temp_file", 
        new_callable=AsyncMock, 
        return_value="print('hello')"
    )
    
    # ⚡ FIX: Store the original anyio.Path class *before* patching
    original_anyio_path = anyio.Path

    # 2. Mock: Mock anyio.Path to control the temp *output* file
    mock_temp_out = AsyncMock(spec=anyio.Path)
    
    # ⚡ FIX: Mock .open() as an AsyncMock, not a MagicMock
    mock_temp_out.open = AsyncMock(
        return_value=AsyncMock(
            __aenter__=AsyncMock(), 
            __aexit__=AsyncMock(return_value=None)
        )
    )
    # Make rename fail
    mock_temp_out.rename = AsyncMock(side_effect=OSError("Rename failed!"))
    # Make exists return True for cleanup
    mock_temp_out.exists = AsyncMock(return_value=True)
    mock_temp_out.unlink = AsyncMock()

    # ⚡ FIX: Make the anyio.Path mock *only* apply to the temp output file
    def path_side_effect(path_arg):
        if str(path_arg) == str(outfile.with_suffix(".tmp")):
            return mock_temp_out
        # ⚡ FIX: Fallback to the *original* implementation
        return original_anyio_path(path_arg)

    mocker.patch("create_dump.writing.json.anyio.Path", side_effect=path_side_effect)

    # 3. Act & Assert
    with pytest.raises(OSError, match="Rename failed!"):
        await writer.write(files_to_process, mock_git_meta, "8.0.0", total_files=1, total_loc=1)
        
    # 4. Assert cleanup
    mock_temp_out.rename.assert_called_once_with(outfile)
    mock_temp_out.exists.assert_called_once()
    mock_temp_out.unlink.assert_called_once()
    
    # ⚡ FIX: This assertion will now use the original anyio.Path and pass
    assert not await anyio.Path(outfile).exists()


async def test_json_writer_includes_todos(
    test_project, temp_dumpfile_factory
):
    """
    Tests that the JsonWriter correctly includes the 'todos' field.
    """
    # 1. Setup
    outfile = test_project.path("dump_todos.json")

    files_to_process = [
        await temp_dumpfile_factory(
            file_path="src/main.py",
            content="pass",
        ),
    ]
    files_to_process[0].todos = ["src/main.py (Line 1): TODO: Implement this"]

    writer = JsonWriter(outfile)

    # 2. Act
    await writer.write(files_to_process, None, "9.0.0", total_files=1, total_loc=1)

    # 3. Assert
    data = json.loads(await anyio.Path(outfile).read_text())

    assert "todos" in data["files"][0]
    assert data["files"][0]["todos"] == ["src/main.py (Line 1): TODO: Implement this"]