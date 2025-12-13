# src/create_dump/collector/git_ls.py

"""The 'git ls-files' collection strategy."""

from __future__ import annotations

from typing import List

from ..logging import logger
from ..system import get_git_ls_files
from .base import CollectorBase


class GitLsCollector(CollectorBase):
    """Collects files using 'git ls-files'."""

    async def collect(self) -> List[str]:
        """Run 'git ls-files' and filter the results."""
        logger.debug("Collecting files via 'git ls-files'")
        raw_files_list = await get_git_ls_files(self.root)
        if not raw_files_list:
            logger.warning("'git ls-files' returned no files.")
            return []
        
        logger.debug(f"Git found {len(raw_files_list)} raw files. Applying filters...")
        return await self.filter_files(raw_files_list)