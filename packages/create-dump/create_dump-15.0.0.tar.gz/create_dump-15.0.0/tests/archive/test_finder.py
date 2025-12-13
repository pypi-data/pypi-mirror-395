# tests/archive/test_finder.py

"""
Tests for Phase 3: src/create_dump/archive/finder.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging

import anyio

# Import the class to test
from create_dump.archive.finder import ArchiveFinder
from create_dump.core import DEFAULT_DUMP_PATTERN
# 🐞 FIX: Import the logging setup function
from create_dump.logging import setup_logging

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def quarantine_dir(test_project) -> Path:
    """Creates and returns a quarantine directory inside the test project."""
    q_dir = test_project.root / "quarantine"
    # test_project.create handles async mkdir
    return q_dir


@pytest.fixture
async def project_with_dumps(test_project, quarantine_dir):
    """Creates a standard file structure for finder tests."""
    # 🐞 FIX: Add valid timestamps (e.g., _20250101_000100) to all filenames
    # so they match DEFAULT_DUMP_PATTERN.
    await test_project.create({
        # Valid pair in root
        "root_pair_all_create_dump_20250101_000100.md": "content1",
        "root_pair_all_create_dump_20250101_000100.sha256": "hash1",

        # Orphan in root
        "root_orphan_all_create_dump_20250101_000200.md": "content2",

        # Valid pair in subdir
        "subdir/sub_pair_all_create_dump_20250101_000300.md": "content3",
        "subdir/sub_pair_all_create_dump_20250101_000300.sha256": "hash3",

        # Orphan in subdir
        "subdir/sub_orphan_all_create_dump_20250101_000400.md": "content4",

        # Non-MD file matching pattern
        "root_sha_only_all_create_dump_20250101_000500.sha256": "hash5",

        # Other file to be ignored
        "README.md": "readme",
    })
    # Ensure quarantine_dir exists
    await anyio.Path(quarantine_dir).mkdir(exist_ok=True)


class TestArchiveFinder:
    """Groups tests for the ArchiveFinder."""

    async def test_find_dump_pairs_recursive(
        self, test_project, quarantine_dir, project_with_dumps
    ):
        """
        Test Case 1: search=True (Recursive)
        Should find pairs in root and subdirs, and quarantine all orphans.
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,  # Recursive
            verbose=False,
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs
        assert len(pairs) == 2
        pair_paths = {p[0].name for p in pairs}
        # 🐞 FIX: Check for the new, valid filenames
        assert "root_pair_all_create_dump_20250101_000100.md" in pair_paths
        assert "sub_pair_all_create_dump_20250101_000300.md" in pair_paths

        # Assertions for quarantining
        # 🐞 FIX: Check for the new, valid filenames
        assert await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        # 🐞 FIX: The test was wrong. Quarantine is flat, it doesn't replicate subdirs.
        assert await (anyio.Path(quarantine_dir) / "sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert originals are gone
        assert not await (test_project.async_root / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert not await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert valid pair was not moved
        assert await (test_project.async_root / "root_pair_all_create_dump_20250101_000100.md").exists()

    async def test_find_dump_pairs_flat(
        self, test_project, quarantine_dir, project_with_dumps
    ):
        """
        Test Case 2: search=False (Flat)
        Should find pairs in root ONLY, and quarantine orphans in root ONLY.
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=False,  # Flat
            verbose=False,
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs
        assert len(pairs) == 1
        pair_paths = {p[0].name for p in pairs}
        # 🐞 FIX: Check for the new, valid filenames
        assert "root_pair_all_create_dump_20250101_000100.md" in pair_paths
        # Subdir pair should be ignored
        assert "sub_pair_all_create_dump_20250101_000300.md" not in pair_paths

        # Assertions for quarantining (only root orphan)
        # 🐞 FIX: Check for the new, valid filenames
        assert await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        # Subdir orphan should be ignored
        assert not await (anyio.Path(quarantine_dir) / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert subdir orphan was NOT moved
        assert await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

    async def test_find_dump_pairs_dry_run(
        self, test_project, quarantine_dir, project_with_dumps, capsys
    ):
        """
        Test Case 3: dry_run=True
        Should find pairs but NOT quarantine orphans, logging instead.
        """
        # 🐞 FIX: Call setup_logging to configure structlog so logs emit to stderr
        setup_logging(verbose=False)

        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,  # Recursive
            verbose=False,
            dry_run=True, # Dry run
            quarantine_dir=quarantine_dir,
        )

        pairs = await finder.find_dump_pairs()

        # Assertions for found pairs (same as recursive)
        assert len(pairs) == 2

        # Assertions for quarantining (NOTHING should be moved)
        # 🐞 FIX: Check for the new, valid filenames
        assert not await (anyio.Path(quarantine_dir) / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert not await (anyio.Path(quarantine_dir) / "sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert originals are STILL present
        assert await (test_project.async_root / "root_orphan_all_create_dump_20250101_000200.md").exists()
        assert await (test_project.async_root / "subdir/sub_orphan_all_create_dump_20250101_000400.md").exists()

        # Assert logging via capsys (captures structlog stderr)
        out, err = capsys.readouterr()
        assert err.count("[dry-run] Would quarantine orphan MD") == 2
        assert err.count("root_orphan_all_create_dump_20250101_000200.md") == 1
        assert err.count("sub_orphan_all_create_dump_20250101_000400.md") == 1

    async def test_ignores_non_md_files(
        self, test_project, quarantine_dir # 🐞 FIX: Removed project_with_dumps
    ):
        """
        Test Case 4: Ignores files matching pattern but not ending in .md
        """
        finder = ArchiveFinder(
            root=test_project.root,
            md_pattern=DEFAULT_DUMP_PATTERN,
            search=True,
            verbose=True, # Enable verbose to check debug logs
            dry_run=False,
            quarantine_dir=quarantine_dir,
        )

        # 🐞 FIX: This test now runs on a CLEAN directory
        # It no longer inherits files from the project_with_dumps fixture.
        await test_project.create({
            "non_md_all_create_dump_20250101_000100.sha256": "hash",
        })

        pairs = await finder.find_dump_pairs()

        # No pairs should be found
        assert len(pairs) == 0

        # 🐞 FIX: Ensure the quarantine dir exists *before* iterating it
        # The finder correctly doesn't create it if there's nothing to quarantine.
        await anyio.Path(quarantine_dir).mkdir(exist_ok=True)

        # Nothing should be quarantined
        async for _ in anyio.Path(quarantine_dir).iterdir():
            assert False, "Quarantine directory should be empty"
