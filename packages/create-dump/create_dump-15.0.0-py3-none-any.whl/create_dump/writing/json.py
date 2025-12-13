# src/create_dump/writing/json.py

"""JSON writing logic.
Consumes processed files and formats them as JSON.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

import anyio

from ..core import DumpFile, GitMeta
from ..helpers import CHUNK_SIZE
from ..logging import logger


class JsonWriter:
    """Streams JSON output from processed temp files."""

    def __init__(self, outfile: Path):
        self.outfile = outfile
        self.files: List[DumpFile] = []  # Stored for metrics

    async def write(
        self,
        files: List[DumpFile],
        git_meta: Optional[GitMeta],
        version: str,
        total_files: int,
        total_loc: int,
    ) -> None:
        """Writes the final JSON file from the list of processed files."""
        self.files = files  # Store for metrics
        
        data: Dict[str, Any] = {
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "version": version,
            "git_meta": git_meta.model_dump() if git_meta else None,
            "total_files": total_files,
            "total_lines_of_code": total_loc,
            "files": []
        }

        for df in self.files:
            if df.error:
                data["files"].append({
                    "path": df.path,
                    "language": df.language,
                    "error": df.error,
                    "content": None,
                    "todos": df.todos,
                })
            elif df.temp_path or df.content:
                try:
                    content = df.content
                    if not content and df.temp_path:
                         content = await self._read_temp_file(df.temp_path)

                    data["files"].append({
                        "path": df.path,
                        "language": df.language,
                        "error": None,
                        "content": content,
                        "todos": df.todos,
                    })
                except Exception as e:
                    logger.error("Failed to read content for JSON dump", path=df.path, error=str(e))
                    data["files"].append({
                        "path": df.path,
                        "language": df.language,
                        "error": f"Failed to read content: {e}",
                        "content": None
                    })

        await self._write_json(data)

    async def _read_temp_file(self, temp_path: Path) -> str:
        """Reads the raw content from a temp file."""
        return await anyio.Path(temp_path).read_text(encoding="utf-8", errors="replace")

    async def _write_json(self, data: Dict[str, Any]) -> None:
        """Writes the data dictionary to the output file atomically."""
        temp_out = anyio.Path(self.outfile.with_suffix(".tmp"))
        try:
            # Run blocking json.dumps in a thread
            # 🐞 FIX: Wrap the call in a lambda to pass the keyword argument
            json_str = await anyio.to_thread.run_sync(
                lambda: json.dumps(data, indent=2)
            )
            
            async with await temp_out.open("w", encoding="utf-8") as f:
                await f.write(json_str)
            
            await temp_out.rename(self.outfile)
            logger.info("JSON written atomically", path=self.outfile)
        except Exception:
            if await temp_out.exists():
                await temp_out.unlink()
            raise