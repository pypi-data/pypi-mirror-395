# src/create_dump/collector/walk.py

"""The standard asynchronous directory walk collector."""

from __future__ import annotations

from pathlib import Path
from typing import AsyncGenerator, List

import anyio

from ..logging import logger
from .base import CollectorBase


class WalkCollector(CollectorBase):
    """Collects files using a recursive async walk."""

    async def _collect_recursive(self, rel_dir: Path) -> AsyncGenerator[Path, None]:
        """Recursive async generator for subdirs."""
        full_dir = anyio.Path(self.root / rel_dir)
        try:
            async for entry in full_dir.iterdir():
                if await entry.is_dir():
                    if entry.name in self.config.excluded_dirs:
                        continue
                    new_rel_dir = Path(entry).relative_to(self.root)
                    async for p in self._collect_recursive(new_rel_dir):
                        yield p
                elif await entry.is_file():
                    rel_path = Path(entry).relative_to(self.root)
                    if await self._matches(rel_path):
                        yield rel_path
        except OSError as e:
            logger.warning("Failed to scan directory", path=str(full_dir), error=str(e))

    async def collect(self) -> List[str]:
        """Walk and filter files efficiently."""
        logger.debug("Collecting files via standard async walk")
        files_list_internal: List[str] = []
        anyio_root = anyio.Path(self.root)
        
        try:
            async for entry in anyio_root.iterdir():
                if await entry.is_dir():
                    if entry.name in self.config.excluded_dirs:
                        continue
                    async for rel_path in self._collect_recursive(
                        Path(entry).relative_to(self.root)
                    ):
                        files_list_internal.append(rel_path.as_posix())
                elif await entry.is_file():
                    rel_path = Path(entry).relative_to(self.root)
                    if await self._matches(rel_path):
                        files_list_internal.append(rel_path.as_posix())
        except OSError as e:
            logger.error("Failed to scan root directory", path=str(self.root), error=str(e))
            return [] # Cannot proceed if root is unreadable

        files_list_internal.sort()
        return files_list_internal