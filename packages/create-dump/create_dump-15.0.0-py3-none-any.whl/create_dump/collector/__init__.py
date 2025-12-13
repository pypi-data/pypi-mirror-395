# src/create_dump/collector/__init__.py
"""
File Collection Factory.

This module provides a factory function (`get_collector`) that instantiates
the correct collection strategy based on the provided arguments.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..core import Config
from ..logging import logger
# ⚡ REFACTOR: Import strategies
from .base import CollectorBase
from .walk import WalkCollector
from .git_ls import GitLsCollector
# ⚡ FIX: Add missing import for GitDiffCollector
from .git_diff import GitDiffCollector


def get_collector(
    config: Config,
    includes: List[str] = None,
    excludes: List[str] = None,
    use_gitignore: bool = False,
    root: Path = Path("."),
    # ⚡ NEW: v8 feature flags
    git_ls_files: bool = False,
    diff_since: Optional[str] = None,
) -> CollectorBase:
    """
    Factory function to select the appropriate file collector strategy.
    """
    
    # Common arguments for all collectors
    common_args = {
        "config": config,
        "includes": includes,
        "excludes": excludes,
        "use_gitignore": use_gitignore,
        "root": root,
    }

    if diff_since:
        logger.debug("Using GitDiffCollector strategy.")
        return GitDiffCollector(diff_since=diff_since, **common_args)
    
    if git_ls_files:
        logger.debug("Using GitLsCollector strategy.")
        return GitLsCollector(**common_args)
    
    logger.debug("Using WalkCollector (default) strategy.")
    return WalkCollector(**common_args)

# ⚡ NEW: Make strategies importable from the package
__all__ = [
    "CollectorBase",
    "WalkCollector",
    "GitLsCollector",
    "GitDiffCollector",
    "get_collector",
]