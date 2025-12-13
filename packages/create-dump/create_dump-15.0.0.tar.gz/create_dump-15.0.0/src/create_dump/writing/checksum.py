# src/create_dump/writing/checksum.py

"""Checksum generation and writing logic."""

from __future__ import annotations

import hashlib
from pathlib import Path
import tenacity
import anyio  # ⚡ REFACTOR: Import anyio
from ..helpers import CHUNK_SIZE  # Refactored import


class ChecksumWriter:
    """Secure checksum with retries."""

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(1))
    # ⚡ REFACTOR: Converted to async
    async def write(self, path: Path) -> str:
        """
        Calculates the SHA256 checksum of a file and writes it to a .sha256 file.
        
        NOTE: Doctest was removed as it does not support async functions.
        This logic must be tested with pytest-anyio.
        """
        sha = hashlib.sha256()
        anyio_path = anyio.Path(path)
        
        # ⚡ REFACTOR: Use async file open and read
        async with await anyio_path.open("rb") as f:
            while True:
                chunk = await f.read(CHUNK_SIZE)
                if not chunk:
                    break
                sha.update(chunk)
                
        checksum = f"{sha.hexdigest()}  {path.name}"
        
        # ⚡ REFACTOR: Use async file write
        anyio_checksum_file = anyio.Path(path.with_suffix(".sha256"))
        await anyio_checksum_file.write_text(checksum + "\n")
        
        return checksum