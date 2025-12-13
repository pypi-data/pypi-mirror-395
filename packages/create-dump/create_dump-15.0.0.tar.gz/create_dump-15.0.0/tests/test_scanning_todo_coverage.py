# tests/test_scanning_todo_coverage.py

import pytest
from unittest.mock import AsyncMock, patch
from create_dump.scanning.todo import TodoScanner
from create_dump.core import DumpFile

@pytest.fixture
def mock_temp_dir(tmp_path):
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    return temp_dir

@pytest.mark.anyio
class TestTodoScannerCoverage:

    async def test_todo_scanner_with_matches(self, mock_temp_dir):
        scanner = TodoScanner()

        # Create a temp file with TODOs
        temp_file = mock_temp_dir / "test.py"
        temp_file.write_text("print('hello')\n# TODO: fix this\n# FIXME: broken\n")

        dump_file = DumpFile(path="test.py", temp_path=temp_file)

        await scanner.process(dump_file)

        assert len(dump_file.todos) == 2
        assert "TODO: fix this" in dump_file.todos[0]
        assert "FIXME: broken" in dump_file.todos[1]

    async def test_todo_scanner_no_temp_path(self):
        scanner = TodoScanner()

        dump_file = DumpFile(path="test.py", temp_path=None)

        await scanner.process(dump_file)

        assert len(dump_file.todos) == 0

    async def test_todo_scanner_exception(self, mock_temp_dir):
        scanner = TodoScanner()

        # Point to a directory so read_text fails
        dump_file = DumpFile(path="test.py", temp_path=mock_temp_dir)

        await scanner.process(dump_file)

        # Should catch exception and pass
        assert len(dump_file.todos) == 0
