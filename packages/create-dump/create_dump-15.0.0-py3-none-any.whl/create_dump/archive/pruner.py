# src/create_dump/archive/pruner.py

"""Component responsible for pruning old archives based on retention policies."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, List

import anyio
from ..cleanup import safe_delete_paths
from ..logging import logger


class ArchivePruner:
    """Prunes old archives to enforce retention (e.g., keep last N)."""

    def __init__(
        self,
        archives_dir: Path,
        keep_last: Optional[int],
        verbose: bool,
    ):
        self.archives_dir = archives_dir
        self.keep_last = keep_last
        self.verbose = verbose

    async def prune(self) -> None:
        """Prune archives to last N by mtime in a non-blocking way."""
        if self.keep_last is None:
            return
        
        # ⚡ REFACTOR: Generalize pattern to match all supported archive formats
        archive_pattern = re.compile(
            r".*_all_create_dump_\d{8}_\d{6}(\.zip|\.tar\.gz|\.tar\.bz2)$"
        )
        anyio_archives_dir = anyio.Path(self.archives_dir)
        
        # Use async rglob for non-blocking directory traversal
        # ⚡ REFACTOR: Renamed variable for clarity
        archive_files: List[anyio.Path] = []
        async for p in anyio_archives_dir.rglob("*"):
            if archive_pattern.match(p.name):
                archive_files.append(p)
        
        num_to_keep = self.keep_last
        if len(archive_files) > num_to_keep:
            
            # Run blocking stat() calls in a thread pool for sorting
            async def get_mtime(p: anyio.Path) -> float:
                stat_res = await p.stat()
                return stat_res.st_mtime

            # Create a list of (mtime, path) tuples to sort
            path_mtimes = []
            # ⚡ REFACTOR: Use renamed variable
            for p in archive_files:
                path_mtimes.append((await get_mtime(p), p))
            
            # Sort by mtime (ascending: oldest first)
            path_mtimes.sort(key=lambda x: x[0])
            
            num_to_prune = max(0, len(path_mtimes) - num_to_keep)
            
            # Get original pathlib.Path objects for deletion compatibility
            to_prune_paths = [Path(p) for _, p in path_mtimes[:num_to_prune]]
            
            # Call async delete with safety guards
            deleted, _ = await safe_delete_paths(
                to_prune_paths, self.archives_dir, dry_run=False, assume_yes=True
            )
            
            logger.info("Pruned %d old archives (keeping last %d)", deleted, self.keep_last)
            if self.verbose:
                logger.debug("Pruned archives: %s", [p.name for p in to_prune_paths])