# src/create_dump/archive/finder.py

"""Component responsible for finding valid MD/SHA dump pairs."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, AsyncGenerator

import anyio
# ⚡ REFACTOR: Import the async version of the safety check
from ..path_utils import safe_is_within
from ..logging import logger


class ArchiveFinder:
    """Finds valid dump pairs, respecting search scope and quarantining orphans."""

    def __init__(
        self,
        root: Path,
        md_pattern: str,
        search: bool,
        verbose: bool,
        dry_run: bool,
        quarantine_dir: Path,
    ):
        self.root = root
        self.md_pattern = md_pattern
        self.search = search
        self.verbose = verbose
        self.dry_run = dry_run
        self.quarantine_dir = quarantine_dir
        
        # ⚡ REFACTOR: Store anyio.Path versions for async checks
        self.anyio_root = anyio.Path(self.root)
        self.anyio_quarantine_dir = anyio.Path(self.quarantine_dir)

    # ⚡ REFACTOR: Converted to async generator
    async def _walk_files(self) -> AsyncGenerator[anyio.Path, None]:
        """
        Walks root directory and yields all file Paths.
        Respects self.search (recursive) vs. flat (scandir).
        """
        # ⚡ REFACTOR: Use instance-level anyio_root
        if self.search:
            # Recursive search
            async for p in self.anyio_root.rglob("*"):
                if await p.is_file():
                    yield p
        else:
            # Flat search
            async for p in self.anyio_root.iterdir():
                if await p.is_file():
                    yield p

    # ⚡ REFACTOR: Converted to async
    async def find_dump_pairs(self) -> List[Tuple[Path, Optional[Path]]]:
        """Find MD/SHA pairs; search if enabled; quarantine orphans."""
        md_regex = re.compile(self.md_pattern)
        pairs = []

        # ⚡ REFACTOR: Renamed 'p' to 'anyio_p' for clarity
        async for anyio_p in self._walk_files():
            # Create a sync pathlib.Path for non-I/O operations
            p_pathlib = Path(anyio_p)
            
            # 🐞 FIX: Prevent recursive loop by ignoring the quarantine dir
            # ⚡ REFACTOR: (Target 1) Use await and async check
            if await safe_is_within(anyio_p, self.anyio_quarantine_dir):
                continue

            if not md_regex.search(p_pathlib.name):
                continue
            
            # 🐞 FIX: This check is critical. Only process .md files.
            if not p_pathlib.name.endswith('.md'):
                if self.verbose:
                    logger.debug("Skipping non-MD match: %s", p_pathlib.name)
                continue
            
            # ⚡ REFACTOR: (Target 2) Use await and async check
            if not await safe_is_within(anyio_p, self.anyio_root):
                continue
            
            # Use pathlib for sync suffix logic
            sha_pathlib = p_pathlib.with_suffix(".sha256")
            
            # ⚡ REFACTOR: Use anyio.Path for async .exists() check
            anyio_sha = anyio.Path(sha_pathlib)
            sha_exists = await anyio_sha.exists()
            
            # ⚡ REFACTOR: (Target 3) Re-structured logic for async check
            sha_path = None  # Default to None
            if sha_exists:
                if await safe_is_within(anyio_sha, self.anyio_root):
                    sha_path = sha_pathlib  # Success, store the sync path
                else:
                    logger.debug("Ignoring .sha256 file outside root", path=str(sha_pathlib))

            if not sha_path:
                if not self.dry_run:
                    # Ensure quarantine dir exists before moving
                    await self.anyio_quarantine_dir.mkdir(exist_ok=True)
                    quarantine_path = self.quarantine_dir / p_pathlib.name
                    # ⚡ REFACTOR: Use async rename on the anyio.Path object 'anyio_p'
                    await anyio_p.rename(quarantine_path)
                    logger.warning("Quarantined orphan MD: %s -> %s", p_pathlib, quarantine_path)
                else:
                    logger.warning("[dry-run] Would quarantine orphan MD: %s", p_pathlib)
                continue
            
            # Store the sync pathlib.Path in the list
            pairs.append((p_pathlib, sha_path))

        if self.verbose:
            logger.debug("Found %d pairs (recursive=%s)", len(pairs), self.search)
        return sorted(pairs, key=lambda x: x[0].name)