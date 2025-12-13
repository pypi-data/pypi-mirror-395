# tests/archive/test_pruner.py

"""
Tests for Phase 3: src/create_dump/archive/pruner.py
"""

from __future__ import annotations
import pytest
from pathlib import Path

import anyio

# Import the class to test
from create_dump.archive.pruner import ArchivePruner
from create_dump.logging import setup_logging

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
async def archives_dir(test_project):
    """Provides the root path for the test project, acting as the archives_dir."""
    # Ensure logging is quiet for these tests
    setup_logging(quiet=True)
    return test_project.root


async def _create_test_archives(path: Path, archives: list[str]) -> list[str]:
    """
    Creates files with a small delay to ensure mtime sorting is predictable.
    Returns the list of names in the order they were created (oldest to newest).
    """
    # Create a subdir for the rglob test
    subdir = anyio.Path(path) / "subdir"
    await subdir.mkdir(exist_ok=True)

    created_order = []
    for i, name in enumerate(archives):
        # Place files in root and subdir to test rglob
        target_path = subdir if i % 2 == 0 else anyio.Path(path)
        await (target_path / name).write_text(f"content{i}")
        # Short sleep to make mtimes distinct and ensure order
        await anyio.sleep(0.01)
        created_order.append(name)

    return created_order


class TestArchivePruner:
    """Groups tests for the ArchivePruner."""

    async def test_prune_keep_last_is_none(self, archives_dir: Path):
        """Test Case 1: Pruner does nothing if keep_last is None."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",
            "archive_all_create_dump_20250101_000200.zip",
        ]
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=None, verbose=False)
        await pruner.prune()

        # Assert all files still exist
        assert await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert await anyio.Path(archives_dir / archive_names[1]).exists()

    async def test_prune_keep_last_gt_files(self, archives_dir: Path):
        """Test Case 2: Pruner does nothing if file count is <= keep_last."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",
            "archive_all_create_dump_20250101_000200.zip",
        ]
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=5, verbose=False)
        await pruner.prune()

        # Assert all files still exist
        assert await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert await anyio.Path(archives_dir / archive_names[1]).exists()

    async def test_prune_prunes_oldest_files(self, archives_dir: Path):
        """Test Case 3: Pruner correctly prunes the oldest files."""
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",  # Oldest
            "archive_all_create_dump_20250101_000200.zip",
            "archive_all_create_dump_20250101_000300.zip",
            "archive_all_create_dump_20250101_000400.zip",
            "archive_all_create_dump_20250101_000500.zip",  # Newest
        ]
        # Create files; the first 3 will be pruned
        await _create_test_archives(archives_dir, archive_names)

        pruner = ArchivePruner(archives_dir, keep_last=2, verbose=True)
        await pruner.prune()

        # Assert the OLDEST 3 files are GONE
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists()
        assert not await anyio.Path(archives_dir / archive_names[1]).exists()
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[2]).exists()

        # Assert the NEWEST 2 files REMAIN
        assert await anyio.Path(archives_dir / archive_names[3]).exists()
        assert await anyio.Path(archives_dir / "subdir" / archive_names[4]).exists()

    async def test_prune_ignores_non_matching_files(self, archives_dir: Path):
        """
        Test Case 4: Pruner ignores non-matching files but prunes *all* valid archive formats (.zip, .tar.gz) based on mtime.
        """
        archive_names = [
            "archive_all_create_dump_20250101_000100.zip",    # Oldest, to be pruned (mtime 1)
            "archive_all_create_dump_20250101_000200.zip",    # To be pruned (mtime 2)
            "not_a_dump.zip",                                 # Ignored (mtime 3)
            "archive_all_create_dump_20250101_000400.tar.gz"  # Newest, to keep (mtime 4)
        ]
        await _create_test_archives(archives_dir, archive_names)

        # ⚡ FIX: keep_last=1. The pruner will find 3 valid archives.
        pruner = ArchivePruner(archives_dir, keep_last=1, verbose=False)
        await pruner.prune()

        # ⚡ FIX: Assert the OLDEST 2 matching files are GONE
        # The .tar.gz is now correctly included in the logic.
        assert not await anyio.Path(archives_dir / "subdir" / archive_names[0]).exists() # pruned
        assert not await anyio.Path(archives_dir / archive_names[1]).exists() # pruned

        # ⚡ FIX: Assert the NON-MATCHING file REMAINS
        assert await anyio.Path(archives_dir / "subdir" / archive_names[2]).exists() # ignored

        # ⚡ FIX: Assert the NEWEST matching file REMAINS
        assert await anyio.Path(archives_dir / archive_names[3]).exists() # kept