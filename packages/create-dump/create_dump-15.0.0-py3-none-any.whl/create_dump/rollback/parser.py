# src/create_dump/rollback/parser.py

"""
Parses a create-dump Markdown file to extract file paths and content.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import AsyncGenerator, List, Tuple

import anyio

from ..logging import logger


class MarkdownParser:
    """
    Reads a .md dump file and parses it into a stream of
    (relative_path, content) tuples for rehydration.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        # Regex to find file headers, e.g., ## src/main.py
        self.header_regex = re.compile(r"^## (.*)$")
        # Regex to find code fences (both ``` and ~~~)
        self.fence_regex = re.compile(r"^(```|~~~)($|\w+)")
        # Regex to find and skip error blocks
        self.error_regex = re.compile(r"^> ⚠️ \*\*Failed:\*\*")

    async def parse_dump_file(self) -> AsyncGenerator[Tuple[str, str], None]:
        """
        Parses the dump file and yields tuples of (relative_path, content).
        """
        current_path: str | None = None
        content_lines: List[str] = []
        capturing = False
        current_fence: str | None = None

        try:
            async with await anyio.Path(self.file_path).open("r", encoding="utf-8") as f:
                async for line in f:
                    if capturing:
                        # Check for closing fence
                        if line.strip() == current_fence:
                            if current_path:
                                # Yield the complete file
                                yield (current_path, "".join(content_lines))
                            
                            # Reset state, wait for next header
                            capturing = False
                            current_path = None
                            content_lines = []
                            current_fence = None
                        else:
                            content_lines.append(line)
                    else:
                        # Not capturing, look for a new file header
                        header_match = self.header_regex.match(line.strip())
                        if header_match:
                            # Found a new file. Reset state and store path.
                            current_path = header_match.group(1).strip()
                            content_lines = []
                            capturing = False
                            current_fence = None
                            continue

                        # If we have a path, look for the opening fence
                        if current_path:
                            # Skip error blocks
                            if self.error_regex.match(line.strip()):
                                logger.warning(f"Skipping failed file in dump: {current_path}")
                                current_path = None # Reset, this file failed
                                continue

                            fence_match = self.fence_regex.match(line.strip())
                            if fence_match:
                                capturing = True
                                current_fence = fence_match.group(1) # Store fence type
                                # Do not append the fence line itself

        except FileNotFoundError:
            logger.error(f"Rollback failed: Dump file not found at {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"Rollback failed: Error parsing dump file: {e}")
            raise