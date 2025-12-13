# src/create_dump/writing/markdown.py

"""Markdown writing logic.
Consumes processed files and formats them as Markdown.
"""

from __future__ import annotations

import datetime
import uuid
from datetime import timezone
from pathlib import Path
from typing import List, Optional, Dict, Any
from importlib import metadata

import anyio

from ..core import DumpFile, GitMeta
from ..helpers import CHUNK_SIZE, get_language, slugify
from ..logging import logger

try:
    __version__ = metadata.version("create-dump")
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"


class MarkdownWriter:
    """Streams Markdown output from processed temp files."""

    def __init__(
        self,
        outfile: Path,
        no_toc: bool,
        tree_toc: bool,
    ):
        self.outfile = outfile
        self.no_toc = no_toc
        self.tree_toc = tree_toc
        self.files: List[DumpFile] = []  # Stored for metrics
        self.git_meta: Optional[GitMeta] = None
        self.version: str = __version__
        self.total_files: int = 0
        self.total_loc: int = 0

    async def write(
        self,
        files: List[DumpFile],
        git_meta: Optional[GitMeta],
        version: str,
        total_files: int,
        total_loc: int,
    ) -> None:
        """Writes the final Markdown file from the list of processed files."""
        self.files = files
        self.git_meta = git_meta
        self.version = version
        self.total_files = total_files
        self.total_loc = total_loc
        
        await self._write_md_streamed()

    async def _write_md_streamed(self) -> None:
        """Stream final MD from temps atomically."""
        temp_out = anyio.Path(self.outfile.with_suffix(".tmp"))
        try:
            async with await temp_out.open("w", encoding="utf-8") as out:
                now = datetime.datetime.now(timezone.utc)
                
                await out.write("# 🗃️ Project Code Dump\n\n")
                await out.write(f"**Generated:** {now.isoformat(timespec='seconds')} UTC\n")
                await out.write(f"**Version:** {self.version}\n")
                await out.write(f"**Total Files:** {self.total_files}\n")
                await out.write(f"**Total Lines:** {self.total_loc}\n")
                if self.git_meta:
                    await out.write(
                        f"**Git Branch:** {self.git_meta.branch} | **Commit:** {self.git_meta.commit}\n"
                    )
                await out.write("\n---\n\n")

                if not self.no_toc:
                    await out.write("## Table of Contents\n\n")
                    
                    valid_files = [df for df in self.files if not df.error and (df.temp_path or df.content)]
                    
                    if self.tree_toc:
                        file_tree: Dict[str, Any] = {}
                        for df in valid_files:
                            parts = df.path.split('/')
                            current_level = file_tree
                            for part in parts[:-1]:
                                current_level = current_level.setdefault(part, {})
                            current_level[parts[-1]] = df
                        
                        await self._render_tree_level(out, file_tree)
                    else:
                        for idx, df in enumerate(valid_files, 1):
                            anchor = slugify(df.path)
                            await out.write(f"{idx}. [{df.path}](#{anchor})\n")
                            
                    await out.write("\n---\n\n")

                for df in self.files:
                    if df.error:
                        await out.write(
                            f"## {df.path}\n\n> ⚠️ **Failed:** {df.error}\n\n---\n\n"
                        )
                    elif df.temp_path or df.content:
                        lang = get_language(df.path)
                        has_backtick = False  # Check content for backticks
                        
                        if df.content:
                            temp_content = df.content
                        elif df.temp_path:
                             # Read temp file to check for backticks
                            temp_content = await anyio.Path(df.temp_path).read_text(encoding="utf-8", errors="replace")
                        else:
                            temp_content = ""

                        if "```" in temp_content:
                            has_backtick = True
                        
                        fence = "~~~" if has_backtick else "```"
                        
                        anchor = slugify(df.path)
                        await out.write(f"## {df.path}\n\n<a id='{anchor}'></a>\n\n")
                        
                        # Write fence and content
                        await out.write(f"{fence}{lang}\n")
                        await out.write(temp_content)
                        await out.write(f"\n{fence}\n\n---\n\n")

                all_todos = [todo for df in self.files if df.todos for todo in df.todos]
                if all_todos:
                    await out.write("## 📝 Technical Debt Summary\n\n")
                    await out.write(f"Found {len(all_todos)} items:\n\n")
                    await out.write("```text\n")
                    for item in all_todos:
                        await out.write(f"- {item}\n")
                    await out.write("```\n\n---\n\n")

            await temp_out.rename(self.outfile)
            logger.info("MD written atomically", path=self.outfile)
        except Exception:
            if await temp_out.exists():
                await temp_out.unlink()
            raise
        finally:
            # NOTE: Final temp file cleanup is handled by the `temp_dir`
            # context manager in `single.py`.
            pass

    async def _render_tree_level(
        self,
        out_stream: anyio.abc.Stream,
        level_dict: dict,
        prefix: str = "",
    ):
        """Recursively writes the file tree to the output stream."""
        
        # Sort items so files appear before sub-directories
        sorted_items = sorted(level_dict.items(), key=lambda item: isinstance(item[1], dict))
        
        for i, (name, item) in enumerate(sorted_items):
            is_last = (i == len(sorted_items) - 1)
            connector = "└── " if is_last else "├── "
            line = f"{prefix}{connector}{name}"
            
            if isinstance(item, dict):  # It's a directory
                await out_stream.write(f"{line}\n")
                # 🐞 FIX: Use regular spaces, not non-breaking spaces
                new_prefix = prefix + ("    " if is_last else "│   ")
                await self._render_tree_level(out_stream, item, new_prefix)
            else:  # It's a DumpFile
                anchor = slugify(item.path)
                await out_stream.write(f"{line} ([link](#{anchor}))\n")