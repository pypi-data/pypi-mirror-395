# tests/scanning/test_todo.py

import anyio
import pytest
from create_dump.core import DumpFile
from create_dump.scanning.todo import TodoScanner

@pytest.fixture
def temp_dump_file(tmp_path):
    async def _create_temp_file(content):
        temp_file = tmp_path / "test_file.txt"
        await anyio.Path(temp_file).write_text(content)
        return DumpFile(path="test_file.txt", temp_path=temp_file)
    return _create_temp_file

@pytest.mark.asyncio
async def test_todo_scanner_finds_tags(temp_dump_file):
    dump_file = await temp_dump_file("TODO: Fix this\nFIXME: This is broken")
    scanner = TodoScanner()
    await scanner.process(dump_file)
    assert len(dump_file.todos) == 2
    assert "TODO: Fix this" in dump_file.todos[0]
    assert "FIXME: This is broken" in dump_file.todos[1]

@pytest.mark.asyncio
async def test_todo_scanner_no_tags(temp_dump_file):
    dump_file = await temp_dump_file("This is a clean file.")
    scanner = TodoScanner()
    await scanner.process(dump_file)
    assert len(dump_file.todos) == 0

@pytest.mark.asyncio
async def test_todo_scanner_does_not_fail(temp_dump_file):
    dump_file = await temp_dump_file("TODO: This is a todo")
    scanner = TodoScanner()
    await scanner.process(dump_file)
    assert dump_file.error is None
