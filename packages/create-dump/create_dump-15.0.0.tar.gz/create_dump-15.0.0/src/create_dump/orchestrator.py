# src/create_dump/orchestrator.py

"""Batch orchestration: Multi-subdir dumps, centralization, compression, cleanup."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple, Union

import anyio

from .archiver import ArchiveManager
# ⚡ FIX: Import the renamed async function
from .cleanup import safe_delete_paths
from .core import Config, load_config, has_local_config, DEFAULT_DUMP_PATTERN
# ⚡ FIX: Import the renamed async functions
from .path_utils import confirm, find_matching_files, safe_is_within
# ⚡ FIX: Import the renamed async function
from .single import run_single
from .logging import logger, styled_print
from .metrics import DUMP_DURATION
from .transaction import atomic_batch_txn

# ⚡ FIX: Renamed __all__
__all__ = ["run_batch"]


# ⚡ RENAMED: Function
async def _centralize_outputs(
    dest_path: Union[anyio.Path, Path],
    root: Path,
    successes: List[Path],
    compress: bool,
    yes: bool,
    dump_pattern: str
) -> None:
    if isinstance(dest_path, Path):
        dest_path = anyio.Path(dest_path)
    await dest_path.mkdir(parents=True, exist_ok=True)
    moved = 0
    
    # ⚡ FIX: This regex must match *all* artifacts, not just .md
    # We'll use the .md pattern to find the *base* and then move its .sha256
    md_regex = re.compile(dump_pattern)
    anyio_root = anyio.Path(root)

    for sub_root in successes:
        anyio_sub_root = anyio.Path(sub_root)
        # Find only the .md files first
        all_md_files = [
            f async for f in anyio_sub_root.glob("*.md") 
            if await f.is_file() and md_regex.match(f.name)
        ]

        for md_file_path in all_md_files:
            sha_file_path = md_file_path.with_suffix(".sha256")
            
            # Create a list of files to move for this pair
            files_to_move = [md_file_path]
            if await sha_file_path.exists():
                files_to_move.append(sha_file_path)
            else:
                # This check is now redundant because validate_batch_staging will catch it,
                # but it's good practice to log here.
                logger.warning("Missing SHA256 for dump, moving .md only", path=str(md_file_path))

            for file_path in files_to_move:
                if not await safe_is_within(file_path, anyio_root):
                    logger.warning("Skipping unsafe dump artifact: %s", file_path)
                    continue

                target = dest_path / file_path.name
                if await target.exists():
                    await target.unlink()
                await file_path.rename(target)
                
                if file_path.suffix == ".md":
                    moved += 1 # Count pairs
                
                to_type = "staging" if "staging" in str(dest_path) else "dest"
                logger.info("Moved dump artifact to %s: %s -> %s", to_type, file_path, target)

    logger.info("Centralized %d dump pairs to %s", moved, dest_path)


async def validate_batch_staging(staging: anyio.Path, pattern: str) -> bool:
    """Validate: All MD have SHA, non-empty."""
    dump_regex = re.compile(pattern)
    md_files = []
    async for f in staging.rglob("*"):
        if await f.is_file() and dump_regex.match(f.name) and f.suffix == ".md":
            md_files.append(f)
    if not md_files:
        return False
    has_sha = True
    for f in md_files:
        sha_path = f.with_suffix(".sha256")
        if not await sha_path.exists():
            has_sha = False
            logger.error("Validation failed: Missing SHA256", md_file=str(f))
            break
    return has_sha


# ⚡ RENAMED: Function
async def run_batch(
    root: Path,
    subdirs: List[str],
    pattern: str,
    dry_run: bool,
    yes: bool,
    accept_prompts: bool,
    compress: bool,
    max_workers: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,
    archive: bool = False,
    archive_all: bool = False,
    archive_search: bool = False,
    archive_include_current: bool = True,
    archive_no_remove: bool = False,
    archive_keep_latest: bool = True,
    archive_keep_last: Optional[int] = None,
    archive_clean_root: bool = False,
    atomic: bool = True,
    format: str = "md", # Added
    archive_format: str = "zip", # Added
) -> None:
    root = root.resolve()
    cfg = load_config()

    if not re.match(r'.*_all_create_dump_', pattern):
        logger.warning("Enforcing canonical pattern: %s", cfg.dump_pattern)
        pattern = cfg.dump_pattern

    atomic = not dry_run and atomic

    # Common: Resolve sub_roots & pre-cleanup
    sub_roots = []
    for sub in subdirs:
        sub_path = root / sub
        if await anyio.Path(sub_path).exists():
            sub_roots.append(sub_path)
    if not sub_roots:
        logger.warning("No valid subdirs: %s", subdirs)
        return

    # ⚡ FIX: Consume the async generator from find_matching_files into a list.
    matches = [p async for p in find_matching_files(root, pattern)]
    
    if matches and not dry_run and not archive_all:
        if yes or await anyio.to_thread.run_sync(confirm, "Delete old dumps?"):
            # ⚡ FIX: Call renamed async function
            deleted, _ = await safe_delete_paths(matches, root, dry_run, yes)
            if verbose:
                logger.info("Pre-cleanup: %d deleted", deleted)

    successes: List[Path] = []
    failures: List[Tuple[Path, str]] = []

    async def _run_single_wrapper(sub_root: Path):
        try:
            # Determine configuration for this subdirectory
            # If local config exists, use it; otherwise fallback to root config
            use_cfg = cfg
            if has_local_config(sub_root):
                use_cfg = load_config(_cwd=sub_root)
                logger.debug(f"Using local config for {sub_root}")

            # ⚡ FIX: Call renamed async function
            await run_single(
                root=sub_root, dry_run=dry_run, yes=accept_prompts or yes, no_toc=False,
                tree_toc=False, format=format, archive_format=archive_format, # Added these arguments
                compress=compress, exclude="", include="", max_file_size=use_cfg.max_file_size_kb,
                use_gitignore=use_cfg.use_gitignore, git_meta=use_cfg.git_meta, progress=False,
                max_workers=16, archive=False, archive_all=False, archive_search=False,
                archive_include_current=archive_include_current, archive_no_remove=archive_no_remove,
                archive_keep_latest=archive_keep_latest, archive_keep_last=archive_keep_last,
                archive_clean_root=archive_clean_root, allow_empty=True, metrics_port=0,
                verbose=verbose, quiet=quiet,
            )
            successes.append(sub_root)
            if not quiet:
                styled_print(f"[green]✅ Dumped {sub_root}[/green]")
        except Exception as e:
            failures.append((sub_root, str(e)))
            logger.error("Subdir failed", subdir=sub_root, error=str(e))
            if not quiet:
                styled_print(f"[red]❌ Failed {sub_root}: {str(e).split('from e')[-1].strip()}[/red]")

    # ⚡ FIX: Add 'collector' label for metrics
    with DUMP_DURATION.labels(collector="batch").time():
        limiter = anyio.Semaphore(max_workers)
        async with anyio.create_task_group() as tg:
            for sub_root in sub_roots:
                async def limited_wrapper(sub_root=Path(sub_root)):
                    async with limiter:
                        await _run_single_wrapper(sub_root)
                tg.start_soon(limited_wrapper)

    if not successes:
        logger.info("No successful dumps.")
        return

    run_id = uuid.uuid4().hex[:8]
    if atomic:
        async with atomic_batch_txn(root, dest, run_id, dry_run) as staging:
            if staging is None:
                return  # Dry run complete

            await _centralize_outputs(staging, root, successes, compress, yes, pattern)
            
            if not await validate_batch_staging(staging, pattern):
                # Raise validation error *before* archiving
                raise ValueError("Validation failed: Incomplete dumps")

            if archive or archive_all:
                timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
                staging_path = Path(staging)
                manager = ArchiveManager(
                    root=staging_path,
                    timestamp=timestamp, keep_latest=archive_keep_latest, keep_last=archive_keep_last,
                    clean_root=archive_clean_root, search=archive_search,
                    include_current=archive_include_current, no_remove=archive_no_remove,
                    dry_run=dry_run, yes=yes, verbose=verbose, md_pattern=pattern, archive_all=archive_all,
                )
                archive_results = await manager.run()
                if verbose:
                    logger.debug("Archiving in staging: search=%s, all=%s", archive_search, archive_all)
                if archive_results and any(archive_results.values()):
                    groups = ', '.join(k for k, v in archive_results.items() if v)
                    logger.info("Archived: %s", groups)
                    if not quiet:
                        styled_print(f"[green]📦 Archived: {groups}[/green]")
                else:
                    logger.info("No dumps for archiving.")
            
    else: # Not atomic
        if dry_run:
            logger.info("[dry-run] Would centralize files to non-atomic dest.")
            return

        central_dest = dest or root / "archives"
        await _centralize_outputs(central_dest, root, successes, compress, yes, pattern)
        
        if not await validate_batch_staging(anyio.Path(central_dest), pattern):
            logger.warning("Validation failed: Incomplete dumps in non-atomic destination.")
            # Do not raise, as this is non-transactional

        if archive or archive_all:
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            manager = ArchiveManager(
                root=root, timestamp=timestamp, keep_latest=archive_keep_latest, keep_last=archive_keep_last,
                clean_root=archive_clean_root, search=archive_search, include_current=archive_include_current,
                no_remove=archive_no_remove, dry_run=dry_run, yes=yes, verbose=verbose,
                md_pattern=pattern, archive_all=archive_all,
            )
            archive_results = await manager.run()
            if archive_results and any(archive_results.values()):
                groups = ', '.join(k for k, v in archive_results.items() if v)
                logger.info("Archived: %s", groups)
                if not quiet:
                    styled_print(f"[green]📦 Archived: {groups}[/green]")
            else:
                logger.info("No dumps for archiving.")

    logger.info("Batch complete: %d/%d successes", len(successes), len(sub_roots))
    if failures and verbose:
        for sub_root, err in failures:
            logger.error("Failure: %s - %s", sub_root, err)
    if not quiet:
        styled_print(f"[green]✅ Batch: {len(successes)}/{len(sub_roots)}[/green]")