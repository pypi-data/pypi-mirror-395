# src/create_dump/collector/git_diff.py

"""The 'git diff' collection strategy."""

from __future__ import annotations

from pathlib import Path
from typing import List

from ..logging import logger
from ..system import get_git_diff_files
from .base import CollectorBase


class GitDiffCollector(CollectorBase):
    """Collects files using 'git diff --name-only'."""

    def __init__(self, diff_since: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diff_since = diff_since

    async def collect(self) -> List[str]:
        """Run 'git diff' and filter the results."""
        logger.debug("Collecting files via 'git diff'", ref=self.diff_since)
        raw_files_list = await get_git_diff_files(self.root, self.diff_since)
        if not raw_files_list:
            logger.warning("'git diff' returned no files.", ref=self.diff_since)
            return []

        logger.debug(f"Git found {len(raw_files_list)} raw files. Applying filters...")
        return await self.filter_files(raw_files_list)