# tests/rollback/test_parser.py

"""
Tests for src/create_dump/rollback/parser.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import anyio

# Import the class to test
from create_dump.rollback.parser import MarkdownParser

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestMarkdownParser:
    """Tests for the MarkdownParser class."""

    async def test_parse_valid_file_simple(self, tmp_path: Path):
        """
        Test Case 1: Valid file with one entry.
        """
        dump_file = tmp_path / "simple.md"
        content = (
            "# Dump\n\n"
            "## src/main.py\n\n"
            "```python\n"
            "print('hello world')\n"
            "```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 1
        assert results[0] == ("src/main.py", "print('hello world')\n")

    async def test_parse_valid_file_multiple_mixed_fences(self, tmp_path: Path):
        """
        Test Case 2: Multiple files, different fences (``` and ~~~).
        """
        dump_file = tmp_path / "mixed.md"
        content = (
            "## file1.py\n"
            "```python\ncontent1\n```\n\n"
            "## file2.md\n"
            "~~~markdown\ncontent with ```backticks``` inside\n~~~\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0] == ("file1.py", "content1\n")
        assert results[1] == ("file2.md", "content with ```backticks``` inside\n")

    async def test_parse_empty_file(self, tmp_path: Path):
        """
        Test Case 3: Empty file yields nothing.
        """
        dump_file = tmp_path / "empty.md"
        await anyio.Path(dump_file).touch()

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 0

    async def test_parse_ignores_preamble_and_mixed_content(self, tmp_path: Path):
        """
        Test Case 4: Text outside of file blocks is ignored.
        """
        dump_file = tmp_path / "noisy.md"
        content = (
            "# Project Dump\n"
            "This is some preamble text.\n\n"
            "## valid/file.txt\n"
            "```text\nreal content\n```\n"
            "This text between files should also be ignored.\n"
            "## another/file.txt\n"
            "```\nmore content\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0] == ("valid/file.txt", "real content\n")
        assert results[1] == ("another/file.txt", "more content\n")

    async def test_parse_malformed_headers_ignored(self, tmp_path: Path):
        """
        Test Case 5: Headers that don't match `## ` are ignored.
        """
        dump_file = tmp_path / "malformed.md"
        content = (
            "# Too Top Level (Ignored)\n"
            "```\nignore me\n```\n"
            "### Too Deep Level (Ignored)\n"
            "```\nignore me too\n```\n"
            "## just_right.txt\n"
            "```\ncontent\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 1
        assert results[0] == ("just_right.txt", "content\n")

    async def test_parse_unclosed_fence_skipped(self, tmp_path: Path):
        """
        Test Case 6: If EOF is reached while capturing, the last file is dropped.
        """
        dump_file = tmp_path / "incomplete.md"
        content = (
            "## good.txt\n"
            "```\ngood content\n```\n"
            "## bad.txt\n"
            "```\nmissing closing fence..."
            # EOF here
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        # Should only get the one that finished
        assert len(results) == 1
        assert results[0] == ("good.txt", "good content\n")

    async def test_parse_skips_error_blocks(self, tmp_path: Path):
        """
        Test Case 7: Standard error blocks are identified and skipped.
        """
        dump_file = tmp_path / "errors.md"
        content = (
            "## good.py\n"
            "```python\nprint('ok')\n```\n"
            "\n"
            "## secret.py\n"
            "\n> ⚠️ **Failed:** Secrets Detected\n\n"
            "---\n\n"
            "## also_good.py\n"
            "```python\nprint('also ok')\n```\n"
        )
        await anyio.Path(dump_file).write_text(content)

        parser = MarkdownParser(dump_file)
        results = [r async for r in parser.parse_dump_file()]

        assert len(results) == 2
        assert results[0][0] == "good.py"
        assert results[1][0] == "also_good.py"

    async def test_file_not_found_re_raises(self, tmp_path: Path, mocker):
        """
        Test Case 8: FileNotFoundError is logged and re-raised.
        """
        missing_file = tmp_path / "ghost.md"
        parser = MarkdownParser(missing_file)
        mock_logger = mocker.patch("create_dump.rollback.parser.logger")

        with pytest.raises(FileNotFoundError):
             # Consume the generator to trigger execution
             [r async for r in parser.parse_dump_file()]

        mock_logger.error.assert_called_once_with(
            f"Rollback failed: Dump file not found at {missing_file}"
        )

    async def test_generic_exception_re_raises(self, tmp_path: Path, mocker):
        """
        Test Case 9: Generic exceptions during read are logged and re-raised.
        """
        dump_file = tmp_path / "broken.md"
        await anyio.Path(dump_file).touch()

        parser = MarkdownParser(dump_file)
        mock_logger = mocker.patch("create_dump.rollback.parser.logger")

        # Mock anyio.Path.open to fail
        mocker.patch.object(anyio.Path, "open", side_effect=PermissionError("Access denied"))

        with pytest.raises(PermissionError):
             [r async for r in parser.parse_dump_file()]

        mock_logger.error.assert_called_once_with(
            "Rollback failed: Error parsing dump file: Access denied"
        )