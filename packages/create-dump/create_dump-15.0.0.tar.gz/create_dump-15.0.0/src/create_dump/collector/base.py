# src/create_dump/collector/base.py

"""Base class for collection strategies."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncGenerator, List, Optional

import anyio
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

from ..core import Config
from ..helpers import is_text_file, parse_patterns
from ..logging import logger


class CollectorBase(ABC):
    """Abstract base class for file collection strategies."""

    def __init__(
        self,
        config: Config,
        includes: List[str] = None,
        excludes: List[str] = None,
        use_gitignore: bool = False,
        root: Path = Path("."),
    ):
        self.config = config
        self.root = root.resolve()
        self.includes = includes or []
        self.excludes = excludes or []
        self.use_gitignore = use_gitignore
        
        self._include_spec: Optional[PathSpec] = None
        self._exclude_spec: Optional[PathSpec] = None
        self._setup_specs()  # Sync setup is OK on init

    def _setup_specs(self) -> None:
        """Build include/exclude specs with defaults."""
        default_includes = self.config.default_includes + [
            "*.py", "*.sh", "*.ini", "*.txt", "*.md", "*.yml", "*.yaml",
            "*.toml", "*.cfg", "*.json", "Dockerfile", ".flake8",
            ".pre-commit-config.yaml",
        ]
        all_includes = default_includes + (self.includes or [])

        default_excludes = self.config.default_excludes + [
            "*.log", "*.pem", "*.key", "*.db", "*.sqlite", "*.pyc", "*.pyo",
            ".env*", "bot_config.json", "*config.json", "*secrets*",
            "__init__.py", "*_all_create_dump_*", "*_all_create_dump_*.md*",
            "*_all_create_dump_*.gz*", "*_all_create_dump_*.sha256",
            "*_all_create_dump_*.zip",
        ]
        all_excludes = default_excludes + (self.excludes or [])

        if self.use_gitignore:
            gitignore_path = self.root / ".gitignore"
            if gitignore_path.exists():
                with gitignore_path.open("r", encoding="utf-8") as f:
                    git_patterns = [
                        line.strip()
                        for line in f
                        if line.strip() and not line.startswith("#")
                    ]
                all_excludes.extend(git_patterns)
                logger.debug("Gitignore integrated", patterns=len(git_patterns))

        self._include_spec = parse_patterns(all_includes)
        self._exclude_spec = parse_patterns(all_excludes)

    async def _matches(self, rel_path: Path) -> bool:
        """Check include/exclude and filters."""
        rel_posix = rel_path.as_posix()
        
        if self._exclude_spec and self._exclude_spec.match_file(rel_posix):
            # ⚡ NEW: Add verbose logging
            logger.debug(f"File excluded by pattern: {rel_posix}")
            return False
        
        is_included = (
            not self._include_spec or
            self._include_spec.match_file(rel_posix) or 
            self._include_spec.match_file(rel_path.name)
        )
        if not is_included:
            # ⚡ NEW: Add verbose logging
            logger.debug(f"File not in include list: {rel_posix}")
            return False

        full_path = anyio.Path(self.root / rel_path)
        return await self._should_include(full_path, rel_posix)

    # ⚡ REFACTOR: Pass rel_posix for better logging
    async def _should_include(self, full_path: anyio.Path, rel_posix: str) -> bool:
        """Final size/text check."""
        try:
            if not await full_path.exists():
                logger.debug(f"Skipping non-existent file: {rel_posix}")
                return False
                
            stat = await full_path.stat()
            if (
                self.config.max_file_size_kb
                and stat.st_size > self.config.max_file_size_kb * 1024
            ):
                # ⚡ NEW: Add verbose logging
                logger.debug(f"File exceeds max size: {rel_posix}")
                return False
            
            is_text = await is_text_file(full_path)
            if not is_text:
                # ⚡ NEW: Add verbose logging
                logger.debug(f"File skipped (binary): {rel_posix}")
                return False
            
            # ⚡ NEW: Add verbose logging for success
            logger.debug(f"File included: {rel_posix}")
            return True

        except OSError as e:
            logger.warning(f"File check failed (OSError): {rel_posix}", error=str(e))
            return False

    async def filter_files(self, raw_files: List[str]) -> List[str]:
        """Shared filtering logic for git-based strategies."""
        filtered_files_list: List[str] = []
        for file_str in raw_files:
            try:
                rel_path = Path(file_str)
                if rel_path.is_absolute():
                    if not file_str.startswith(str(self.root)):
                         logger.warning("Skipping git path outside root", path=file_str)
                         continue
                    rel_path = rel_path.relative_to(self.root)
                
                if await self._matches(rel_path):
                    filtered_files_list.append(rel_path.as_posix())
            except Exception as e:
                logger.warning("Skipping file due to error", path=file_str, error=str(e))

        filtered_files_list.sort()
        return filtered_files_list

    @abstractmethod
    async def collect(self) -> List[str]:
        """Collect all raw file paths based on the strategy."""
        raise NotImplementedError