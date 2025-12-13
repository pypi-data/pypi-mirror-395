# src/create_dump/archiver.py

"""
Orchestrator for the archiving workflow.

Coordinates Finder, Packager, and Pruner components to manage the
archive lifecycle (find, zip, clean, prune).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import anyio  # ⚡ REFACTOR: Import anyio
# ⚡ REFACTOR: Import async cleanup
from .cleanup import safe_delete_paths
from .core import Config, load_config, DEFAULT_DUMP_PATTERN
from .path_utils import confirm
from .logging import logger  # ⚡ REFACTOR: Import from logging
# ⚡ REFACTOR: Import new SRP components
from .archive import ArchiveFinder, ArchivePackager, ArchivePruner

__all__ = ["ArchiveManager"]


class ArchiveManager:
    """Orchestrates finding, packaging, and pruning of archives."""

    def __init__(
        self,
        root: Path,
        timestamp: str,
        keep_latest: bool = True,
        keep_last: Optional[int] = None,
        clean_root: bool = False,
        search: bool = False,
        include_current: bool = True,
        no_remove: bool = False,
        dry_run: bool = False,
        yes: bool = False,
        verbose: bool = False,
        md_pattern: Optional[str] = None,
        archive_all: bool = False,
        archive_format: str = "zip",
    ):
        self.root = root.resolve()
        self.timestamp = timestamp
        self.search = search or archive_all
        self.archive_all = archive_all
        self.dry_run = dry_run
        self.yes = yes
        self.clean_root = clean_root
        self.no_remove = no_remove
        
        # Load and validate config (sync, fine)
        cfg = load_config()
        self.md_pattern = md_pattern or cfg.dump_pattern
        if md_pattern and not re.match(r'.*_all_create_dump_', self.md_pattern):
            logger.warning("Loose md_pattern provided; enforcing canonical: %s", DEFAULT_DUMP_PATTERN)
            self.md_pattern = DEFAULT_DUMP_PATTERN

        # Setup directories (sync, fine)
        self.archives_dir = self.root / "archives"
        self.archives_dir.mkdir(exist_ok=True)
        self.quarantine_dir = self.archives_dir / "quarantine"
        self.quarantine_dir.mkdir(exist_ok=True)
        
        # Instantiate SRP components (sync, fine)
        self.finder = ArchiveFinder(
            root=self.root,
            md_pattern=self.md_pattern,
            search=self.search,
            verbose=verbose,
            dry_run=dry_run,
            quarantine_dir=self.quarantine_dir,
        )
        
        self.packager = ArchivePackager(
            root=self.root,
            archives_dir=self.archives_dir,
            quarantine_dir=self.quarantine_dir,
            timestamp=self.timestamp,
            keep_latest=keep_latest,
            verbose=verbose,
            dry_run=dry_run,
            yes=yes,
            clean_root=clean_root,
            no_remove=no_remove,
            archive_format=archive_format,
         
        )
        
        self.pruner = ArchivePruner(
            archives_dir=self.archives_dir,
            keep_last=keep_last,
            verbose=verbose,
        )

    # ⚡ REFACTOR: Converted to async
    async def run(self, current_outfile: Optional[Path] = None) -> Dict[str, Optional[Path]]:
        """Orchestrate: find, package, clean, prune."""
        
        # 1. Find pairs
        # ⚡ REFACTOR: Await async finder
        pairs = await self.finder.find_dump_pairs()
        if not pairs:
            logger.info("No pairs for archiving.")
            await self.pruner.prune()  # Prune even if no new pairs
            return {}

        archive_paths: Dict[str, Optional[Path]] = {}
        all_to_delete: List[Path] = []

        # 2. Package pairs
        if not self.archive_all:
            # ⚡ REFACTOR: Await async packager
            archive_paths, to_delete = await self.packager.handle_single_archive(pairs)
            all_to_delete.extend(to_delete)
        else:
            groups = self.packager.group_pairs_by_prefix(pairs)
            # ⚡ REFACTOR: Await async packager
            archive_paths, to_delete = await self.packager.handle_grouped_archives(groups)
            all_to_delete.extend(to_delete)

        # 3. Clean (Deferred bulk delete)
        if self.clean_root and all_to_delete and not self.no_remove and not self.dry_run:
            prompt = f"Delete {len(all_to_delete)} archived files across groups?" if self.archive_all else f"Clean {len(all_to_delete)} root files post-archive?"
            
            # ⚡ REFACTOR: Run blocking 'confirm' in a thread
            user_confirmed = self.yes or await anyio.to_thread.run_sync(confirm, prompt)
            
            if user_confirmed:
                # ⚡ REFACTOR: Call async delete
                await safe_delete_paths(
                    all_to_delete, self.root, dry_run=False, assume_yes=self.yes
                )
                logger.info("Deferred delete: Cleaned %d files post-validation", len(all_to_delete))

        # 4. Prune
        # ⚡ REFACTOR: Await async pruner
        await self.pruner.prune()

        # 5. Handle symlink (no-op for now)
        if current_outfile:
            pass  # Logic for symlinking latest remains here if needed

        return archive_paths
    
    # ⚡ REFACTOR: Removed synchronous run method