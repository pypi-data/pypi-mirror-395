# tests/writing/test_markdown.py

"""
Tests for Phase 3: src/create_dump/writing/markdown.py
"""

from __future__ import annotations
import pytest
import re
from pathlib import Path
from typing import Callable, Awaitable

import anyio

# Import the class to test
from create_dump.writing.markdown import MarkdownWriter
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
    """
    temp_dir = tmp_path_factory.mktemp("md_writer_temps")
    
    async def _create(
        file_path: str,
        content: str | None = None,
        error: str | None = None
    ) -> DumpFile:
        
        if error:
            return DumpFile(path=file_path, error=error)
        
        # Create the temp file
        temp_file = anyio.Path(temp_dir) / f"{file_path.replace('/', '_')}.tmp"
        await temp_file.write_text(content or "")
        
        return DumpFile(
            path=file_path,
            language=None, # Relies on get_language in prod, not needed here
            temp_path=Path(temp_file) # The writer expects a sync Path
        )
    
    return _create


async def test_write_standard_list_toc(
    test_project, temp_dumpfile_factory, mock_git_meta
):
    """
    Test Case 1: Standard write with a list ToC (default).
    Checks header, git meta, ToC entries, file content,
    error reporting, and code fence switching.
    """
    # 1. Setup
    outfile = test_project.path("dump.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/main.py", "print('hello')"
        ),
        await temp_dumpfile_factory(
            "src/backticks.md", "This file has ```backticks```"
        ),
        await temp_dumpfile_factory(
            "src/failed.py", error="File is unreadable"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=False, tree_toc=False)
    
    # 2. Act
    await writer.write(files, mock_git_meta, "8.0.0", total_files=3, total_loc=100)

    # 3. Assert
    assert await anyio.Path(outfile).exists()
    assert not await anyio.Path(outfile.with_suffix(".tmp")).exists()
    
    content = await anyio.Path(outfile).read_text()
    
    # Check Header
    assert "**Version:** 8.0.0" in content
    assert "**Git Branch:** main | **Commit:** abc1234" in content
    assert "**Total Files:** 3" in content
    assert "**Total Lines:** 100" in content
    
    # Check ToC (List format)
    assert "## Table of Contents" in content
    assert "1. [src/main.py](#src-main-py)" in content
    assert "2. [src/backticks.md](#src-backticks-md)" in content
    
    # 🐞 FIX: The error *is* in the content, just not the ToC.
    # This assertion was flawed. The error *section* must exist.
    assert "src/failed.py" in content
    assert "> ⚠️ **Failed:** File is unreadable" in content
    
    # Check File Content
    # (Using regex with re.DOTALL to span newlines)
    
    # File 1: Standard fence
    assert re.search(
        r"## src/main\.py\n\n<a id='src-main-py'></a>\n\n"
        r"```python\nprint\('hello'\)\n```",
        content,
        re.DOTALL
    )
    
    # File 2: Switched fence (~~~)
    assert re.search(
        r"## src/backticks\.md\n\n<a id='src-backticks-md'></a>\n\n"
        r"~~~markdown\nThis file has ```backticks```\n~~~",
        content,
        re.DOTALL
    )
    
    # File 3: Error reporting
    assert "## src/failed.py" in content
    assert "> ⚠️ **Failed:** File is unreadable" in content


async def test_write_tree_toc(test_project, temp_dumpfile_factory):
    """
    Test Case 2: Write with a tree-style ToC.
    Checks that the ToC is rendered as a sorted file tree.
    """
    # 1. Setup
    outfile = test_project.path("dump_tree.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/components/button.py", "pass"
        ),
        await temp_dumpfile_factory(
            "README.md", "# Title"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=False, tree_toc=True)
    
    # 2. Act
    await writer.write(files, None, "8.0.0", total_files=2, total_loc=2)
    
    # 3. Assert
    content = await anyio.Path(outfile).read_text()
    
    assert "## Table of Contents" in content
    
    # Check for the rendered tree structure.
    # 🐞 FIX: Use regular spaces to match the fix in markdown.py
    expected_tree = (
        "├── README.md ([link](#readme-md))\n"
        "└── src\n"
        "    └── components\n"
        "        └── button.py ([link](#src-components-button-py))"
    )
    
    assert expected_tree in content
    
    # Check that file content is still rendered
    assert "## README.md" in content
    assert "## src/components/button.py" in content


async def test_write_no_toc(test_project, temp_dumpfile_factory):
    """
    Test Case 3: Write with no_toc=True.
    Checks that the ToC section is completely omitted.
    """
    # 1. Setup
    outfile = test_project.path("dump_no_toc.md")
    
    files = [
        await temp_dumpfile_factory(
            "src/main.py", "pass"
        ),
    ]

    writer = MarkdownWriter(outfile, no_toc=True, tree_toc=False)
    
    # 2. Act
    await writer.write(files, None, "8.0.0", total_files=1, total_loc=1)
    
    # 3. Assert
    content = await anyio.Path(outfile).read_text()
    
    # Check that ToC is missing
    assert "## Table of Contents" not in content
    
    # 🐞 FIX: The anchor link *is* and *should be* present.
    # The assertion was flawed.
    assert "<a id='src-main-py'></a>" in content

    # Check that header and content are still present
    assert "**Version:** 8.0.0" in content
    assert "## src/main.py" in content
    assert "```python\npass\n```" in content


async def test_write_with_todo_summary(test_project, temp_dumpfile_factory):
    """
    Test Case: Write with a TODO summary.
    Checks that the ## 📝 Technical Debt Summary section is correctly rendered.
    """
    # 1. Setup
    outfile = test_project.path("dump_with_todos.md")

    files = [
        await temp_dumpfile_factory("src/main.py", "pass"),
    ]
    files[0].todos = ["src/main.py (Line 1): TODO: Implement this"]

    writer = MarkdownWriter(outfile, no_toc=False, tree_toc=False)

    # 2. Act
    await writer.write(files, None, "9.0.0", total_files=1, total_loc=1)

    # 3. Assert
    content = await anyio.Path(outfile).read_text()

    assert "## 📝 Technical Debt Summary" in content
    assert "Found 1 items:" in content
    assert "- src/main.py (Line 1): TODO: Implement this" in content
