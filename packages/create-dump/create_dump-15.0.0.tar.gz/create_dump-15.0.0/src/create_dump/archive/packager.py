# src/create_dump/archive/packager.py

"""Component responsible for grouping, sorting, and packaging (zipping) archives."""

from __future__ import annotations

import zipfile
import tarfile  # ⚡ NEW: Import tarfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import anyio
from ..cleanup import safe_delete_paths
from ..path_utils import confirm
from ..helpers import _unique_path
from ..logging import logger
from .core import ArchiveError, extract_group_prefix, extract_timestamp, _safe_arcname


class ArchivePackager:
    """Handles logic for grouping, sorting by date, and creating ZIP archives."""

    def __init__(
        self,
        root: Path,
        archives_dir: Path,
        quarantine_dir: Path,
        timestamp: str,
        keep_latest: bool,
        verbose: bool,
        dry_run: bool,
        yes: bool,
        clean_root: bool,
        no_remove: bool,
        archive_format: str = "zip",  # ⚡ NEW: Add format
    ):
        self.root = root
        self.archives_dir = archives_dir
        self.quarantine_dir = quarantine_dir
        self.timestamp = timestamp
        self.keep_latest = keep_latest
        self.verbose = verbose
        self.dry_run = dry_run
        self.yes = yes
        self.clean_root = clean_root
        self.no_remove = no_remove
        
        # ⚡ NEW: Store format and get correct extension
        self.archive_format = archive_format
        if archive_format == "tar.gz":
            self.archive_ext = ".tar.gz"
        elif archive_format == "tar.bz2":
            self.archive_ext = ".tar.bz2"
        else:
            self.archive_format = "zip"  # Default to zip
            self.archive_ext = ".zip"

    # ⚡ REFACTOR: Renamed to _create_archive_sync
    # 🐞 FIX: Corrected type hint from Path to str
    def _create_archive_sync(self, files_to_archive: List[Path], zip_name: str) -> Tuple[Optional[Path], List[Path]]:
        """Create archive; dedupe, compression-aware, unique naming; validate integrity."""
        if not files_to_archive:
            logger.info("No files to archive for %s", zip_name)
            return None, []

        valid_files = [p for p in files_to_archive if p is not None]
        if not valid_files:
            logger.info("No valid files to archive after filtering orphans for %s", zip_name)
            return None, []

        base_archive = self.archives_dir / zip_name
        archive_name = _unique_path(base_archive)
        to_archive = sorted(list(set(valid_files)))

        try:
            # ⚡ REFACTOR: Branch logic based on format
            if self.archive_format == "zip":
                with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                    for p in to_archive:
                        arcname = _safe_arcname(p, self.root)
                        comp_type = zipfile.ZIP_STORED if p.suffix in {".gz", ".zip", ".bz2"} else zipfile.ZIP_DEFLATED
                        z.write(p, arcname=arcname, compress_type=comp_type)
                
                # ⚡ REFACTOR: Validation is zip-specific
                with zipfile.ZipFile(archive_name, 'r') as z:
                    badfile = z.testzip()
                    if badfile is not None:
                        raise ArchiveError(f"Corrupt file in ZIP: {badfile}")
                logger.info("ZIP integrity validated successfully for %s", zip_name)

            else:  # Handle 'tar.gz' and 'tar.bz2'
                tar_mode = "w:gz" if self.archive_format == "tar.gz" else "w:bz2"
                with tarfile.open(archive_name, tar_mode) as tar:
                    for p in to_archive:
                        arcname = _safe_arcname(p, self.root)
                        tar.add(p, arcname=arcname)
                logger.info("TAR integrity validated (creation successful) for %s", zip_name)
        
        except (ArchiveError, tarfile.TarError, zipfile.BadZipFile, Exception) as e:
            logger.error("Archive creation/validation failed for %s: %s. Rolling back.", zip_name, e)
            archive_name.unlink(missing_ok=True)
            raise

        size = archive_name.stat().st_size
        logger.info("Archive %s created: %s (%d bytes, %d files)", self.archive_format.upper(), archive_name, size, len(to_archive))
        return archive_name, to_archive

    async def _create_archive(
        self, files_to_archive: List[Path], zip_name: str
    ) -> Tuple[Optional[Path], List[Path]]:
        """Runs the sync _create_archive_sync in a thread pool to avoid blocking."""
        # ⚡ REFACTOR: Call renamed sync method
        return await anyio.to_thread.run_sync(
            self._create_archive_sync, files_to_archive, zip_name
        )

    def group_pairs_by_prefix(self, pairs: List[Tuple[Path, Optional[Path]]]) -> Dict[str, List[Tuple[Path, Optional[Path]]]]:
        groups: Dict[str, List[Tuple[Path, Optional[Path]]]] = {}
        for pair in pairs:
            prefix = extract_group_prefix(pair[0].name)
            if prefix:
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(pair)
            else:
                if 'default' not in groups:
                    groups['default'] = []
                groups['default'].append(pair)
        if self.verbose:
            for group, group_pairs in groups.items():
                logger.debug("Grouped %d pairs under '%s'", len(group_pairs), group)
        return groups

    async def handle_single_archive(
        self, pairs: List[Tuple[Path, Optional[Path]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        live_pair = None
        historical = pairs
        if self.keep_latest:
            def key_func(p):
                ts = extract_timestamp(p[0].name)
                if ts == datetime.min:
                    ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                    if self.verbose:
                        logger.debug("Fallback to mtime for sorting: %s", p[0].name)
                return (-ts.timestamp(), p[0].name)
            sorted_pairs = sorted(pairs, key=key_func)
            
            if not sorted_pairs:
                return archive_paths, to_delete 
                
            live_pair = sorted_pairs[0]
            historical = sorted_pairs[1:]
            if self.verbose:
                logger.info(
                    "Retained latest pair (ts=%s): %s",
                    extract_timestamp(live_pair[0].name),
                    live_pair[0].name,
                )

        if len(historical) == 0:
            return archive_paths, to_delete
        
        files_to_archive = [p for pair in historical for p in pair if p is not None]
        num_historical_pairs = len(historical)
        num_files = len(files_to_archive)
        if self.verbose:
            logger.info("Archiving %d pairs (%d files)", num_historical_pairs, num_files)

        # ⚡ REFACTOR: Use self.archive_ext for the correct file extension
        base_archive_name = f"{self.root.name}_dumps_archive_{self.timestamp}{self.archive_ext}"

        if self.dry_run:
            logger.info("[dry-run] Would create archive: %s", base_archive_name)
            archive_path = None
        else:
            archive_path, archived_files = await self._create_archive(
                files_to_archive, base_archive_name
            )
            to_delete.extend(archived_files)

        archive_paths['default'] = archive_path
 
        if self.clean_root and not self.no_remove:
            to_clean = files_to_archive
            if self.keep_latest and live_pair:
                live_paths = [live_pair[0]]
                if live_pair[1] is not None:
                    live_paths.append(live_pair[1])
                to_clean = [p for p in files_to_archive if p not in live_paths]
            prompt = f"Clean {len(to_clean)} root files post-archive?"
            
            user_confirmed = self.yes or await anyio.to_thread.run_sync(confirm, prompt)
            
            if user_confirmed:
                await safe_delete_paths(
                    to_clean, self.root, dry_run=self.dry_run, assume_yes=self.yes
                )
                if not self.dry_run:
                    logger.info("Cleaned %d root files", len(to_clean))


        return archive_paths, to_delete

    async def handle_grouped_archives(
        self, groups: Dict[str, List[Tuple[Path, Optional[Path]]]]
    ) -> Tuple[Dict[str, Optional[Path]], List[Path]]:
        
        archive_paths: Dict[str, Optional[Path]] = {}
        to_delete: List[Path] = []

        for group, group_pairs in groups.items():
            if self.verbose:
                logger.info("Processing group: %s (%d pairs)", group, len(group_pairs))

            if group == 'default' and len(group_pairs) > 0:
                logger.warning("Skipping 'default' group (%d pairs): Quarantining unmatchable MDs", len(group_pairs))
                for pair in group_pairs:
                    md, sha_opt = pair[0], pair[1]
                    if not self.dry_run:
                        await anyio.Path(self.quarantine_dir).mkdir(exist_ok=True)
                        if await anyio.Path(md).exists():
                            quarantine_md = self.quarantine_dir / md.name
                            await anyio.to_thread.run_sync(md.rename, quarantine_md)
                            logger.debug("Quarantined unmatchable MD: %s -> %s", md, quarantine_md)
                        if sha_opt and await anyio.Path(sha_opt).exists() and sha_opt != md:
                            quarantine_sha = self.quarantine_dir / sha_opt.name
                            await anyio.to_thread.run_sync(sha_opt.rename, quarantine_sha)
                            logger.debug("Quarantined unmatchable SHA: %s -> %s", sha_opt, quarantine_sha)
                    else:
                        logger.warning("[dry-run] Would quarantine unmatchable pair: %s / %s", md, sha_opt)
                continue
            
            live_pair = None
            historical = group_pairs
            if self.keep_latest:
                def key_func(p):
                    ts = extract_timestamp(p[0].name)
                    if ts == datetime.min:
                        ts = datetime.fromtimestamp(p[0].stat().st_mtime)
                        if self.verbose:
                            logger.debug("Fallback to mtime for sorting in %s: %s", group, p[0].name)
                    return (-ts.timestamp(), p[0].name)
                sorted_pairs = sorted(group_pairs, key=key_func)
                
                if not sorted_pairs:
                    continue 
                
                live_pair = sorted_pairs[0]
                historical = sorted_pairs[1:]
                if self.verbose and live_pair:
                    logger.info(
                        "Retained latest pair in %s (ts=%s): %s",
                        group,
                        extract_timestamp(live_pair[0].name),
                        live_pair[0].name,
                    )

            if len(historical) == 0:
                logger.info("No historical pairs for group %s.", group)
                continue
            
            files_to_archive = [p for pair in historical for p in pair if p is not None]
            num_historical_pairs = len(historical)
            num_files = len(files_to_archive)
            if self.verbose:
                logger.info("Archiving %d pairs (%d files) for group %s", num_historical_pairs, num_files, group)

            # ⚡ REFACTOR: Use self.archive_ext for the correct file extension
            base_archive_name = f"{group}_all_create_dump_{self.timestamp}{self.archive_ext}"
            
            if self.dry_run:
                logger.info("[dry-run] Would create archive for %s: %s", group, base_archive_name)
                archive_path = None
            else:
                archive_path, archived_files = await self._create_archive(
                    files_to_archive, base_archive_name
                )
                to_delete.extend(archived_files)

            archive_paths[group] = archive_path

        return archive_paths, to_delete