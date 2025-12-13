# src/create_dump/cleanup.py

"""Safe, auditable cleanup of files/directories with dry-run and prompts."""

from __future__ import annotations

import shutil
from pathlib import Path
# ⚡ REFACTOR: Import AsyncGenerator, Union, and collections.abc
from typing import List, Tuple, AsyncGenerator, Union
import collections.abc

import anyio
# ⚡ REFACTOR: Import async finder and new async safe_is_within
from .path_utils import (
    confirm,
    find_matching_files, safe_is_within
)
from .logging import logger

# ⚡ REFACTOR: Removed safe_delete_paths and safe_cleanup
__all__ = ["safe_delete_paths", "safe_cleanup"]


# ⚡ REFACTOR: Removed synchronous safe_delete_paths function


async def safe_delete_paths(
    # ⚡ REFACTOR: Accept either a List (for existing callers) or an AsyncGenerator
    paths: Union[List[Path], AsyncGenerator[Path, None]], 
    root: Path, 
    dry_run: bool, 
    assume_yes: bool
) -> Tuple[int, int]:
    """Delete files or directories in a safe, async manner."""
    deleted_files = deleted_dirs = 0
    
    # ⚡ REFACTOR: Convert root to anyio.Path once
    anyio_root = anyio.Path(root)
    
    # ⚡ REFACTOR: Create a unified async iterator to handle both types
    async def async_iter(paths_iterable):
        if isinstance(paths_iterable, collections.abc.AsyncGenerator):
            async for p_gen in paths_iterable:
                yield p_gen
        else: # It's a List
            for p_list in paths_iterable:
                yield p_list

    # ⚡ REFACTOR: Use the unified iterator
    async for p in async_iter(paths):
        # 1. 🐞 FIX: Use the original anyio.Path object for all async I/O
        anyio_p = anyio.Path(p)

        # 2. 🐞 FIX: Use the new async safety check
        if not await safe_is_within(anyio_p, anyio_root):
            # Log using the original path for clarity
            logger.warning(f"Skipping path outside root: {p}")
            continue

        # 3. Use the original, async-capable anyio_p for I/O
        if await anyio_p.is_file():
            if dry_run:
                logger.info(f"[dry-run] would delete file: {p}")
            else:
                try:
                    await anyio_p.unlink()
                    logger.info(f"Deleted file: {p}")
                    deleted_files += 1
                # ⚡ REFACTOR: Narrow exception scope
                except OSError as e:
                    logger.error(f"Failed to delete file {p}: {e}")
                    
        elif await anyio_p.is_dir():
            if not assume_yes and not dry_run:
                ok = await anyio.to_thread.run_sync(
                    confirm, f"Remove directory tree: {p}?"
                )
                if not ok:
                    continue
            if dry_run:
                logger.info(f"[dry-run] would remove directory: {p}")
            else:
                try:
                    # 🐞 FIX: Wrap sync shutil.rmtree in thread pool (anyio.Path lacks rmtree)
                    await anyio.to_thread.run_sync(shutil.rmtree, anyio_p)
                    logger.info(f"Removed directory: {p}")
                    deleted_dirs += 1
                # ⚡ REFACTOR: Narrow exception scope
                except OSError as e:
                    logger.error(f"Failed to remove directory {p}: {e}")
    return deleted_files, deleted_dirs


# ⚡ REFACTOR: Removed synchronous safe_cleanup function


# ⚡ REFACTOR: New async version of safe_cleanup
async def safe_cleanup(root: Path, pattern: str, dry_run: bool, assume_yes: bool, verbose: bool) -> None:
    """Standalone async cleanup of matching paths."""
    # ⚡ REFACTOR: find_matching_files is now a generator
    matches_gen = find_matching_files(root, pattern)
    
    # ⚡ REFACTOR: We must 'peek' at the generator to see if it's empty
    try:
        first_match = await anext(matches_gen)
    except StopAsyncIteration:
        logger.info("No matching files found for cleanup.")
        return

    if verbose:
        # ⚡ REFACTOR: We can no longer give an exact count without memory cost.
        logger.info(f"Found paths to clean (starting with: {first_match.name}).")
    if dry_run:
        logger.info("Dry-run: Skipping deletions.")
        return

    user_confirmed = assume_yes or await anyio.to_thread.run_sync(
        confirm, "Delete all matching files?"
    )
    if user_confirmed:
        # ⚡ REFACTOR: Chain the peeked item back onto the generator
        async def final_gen() -> AsyncGenerator[Path, None]:
            yield first_match
            async for p in matches_gen:
                yield p

        deleted_files, deleted_dirs = await safe_delete_paths(
            final_gen(), root, dry_run=False, assume_yes=assume_yes
        )
        logger.info(f"Cleanup complete: {deleted_files} files, {deleted_dirs} dirs deleted")