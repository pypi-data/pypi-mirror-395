# src/create_dump/scanning/todo.py

import re
from typing import List

import anyio

from create_dump.core import DumpFile
from create_dump.processor import ProcessorMiddleware


class TodoScanner(ProcessorMiddleware):
    def __init__(self) -> None:
        self.todo_regex = re.compile(r"(TODO|FIXME|HACK|TECH_DEBT):(.*)")

    async def process(self, dump_file: DumpFile) -> None:
        if not dump_file.temp_path:
            return

        try:
            content = await anyio.Path(dump_file.temp_path).read_text()
            lines = content.splitlines()
            for line_num, line in enumerate(lines, 1):
                if self.todo_regex.search(line):
                    finding = f"{dump_file.path} (Line {line_num}): {line.strip()}"
                    dump_file.todos.append(finding)
        except Exception:
            # This middleware does not set dump_file.error
            pass
