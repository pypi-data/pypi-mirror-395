# tests/test_archiver.py

"""
Tests for src/create_dump/archiver.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List, Optional, Tuple

import anyio

from create_dump.archiver import ArchiveManager
from create_dump.core import DEFAULT_DUMP_PATTERN
from create_dump.archive import ArchiveFinder, ArchivePackager, ArchivePruner

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config(mocker):
    """Mock load_config to return a dummy Config."""
    mock_cfg = MagicMock()
    mock_cfg.dump_pattern = DEFAULT_DUMP_PATTERN
    mocker.patch("create_dump.archiver.load_config", return_value=mock_cfg)
    return mock_cfg


@pytest.fixture
def mock_dirs(tmp_path: Path):
    """Ensure archives/quarantine dirs exist in tmp_path."""
    archives_dir = tmp_path / "archives"
    quarantine_dir = archives_dir / "quarantine"
    archives_dir.mkdir(exist_ok=True)
    quarantine_dir.mkdir(exist_ok=True)
    return archives_dir, quarantine_dir


class TestArchiveManagerInit:
    """Tests for ArchiveManager.__init__."""

    def test_init_defaults(self, tmp_path: Path, mock_config):
        """Test Case 1: Default params, dir creation, pattern fallback."""
        root = tmp_path / "root"
        root.mkdir()

        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            verbose=False,
            md_pattern=None,
        )

        assert manager.root == root.resolve()
        assert manager.archives_dir == root / "archives"
        assert manager.quarantine_dir == root / "archives" / "quarantine"
        assert manager.md_pattern == DEFAULT_DUMP_PATTERN
        assert manager.search is False
        assert manager.dry_run is False
        assert manager.yes is False

    def test_init_custom_pattern(self, tmp_path: Path, mock_config, mocker):
        """Test Case 2: Custom md_pattern, warning on loose format."""
        root = tmp_path / "root"
        root.mkdir()
        mock_logger = mocker.patch("create_dump.archiver.logger")

        loose_pattern = r".*\.md$"
        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            md_pattern=loose_pattern,
        )

        mock_logger.warning.assert_called_once()
        assert manager.md_pattern == DEFAULT_DUMP_PATTERN  # Enforced canonical

    def test_init_archive_all(self, tmp_path: Path):
        """Test Case 3: archive_all enables search."""
        root = tmp_path / "root"
        root.mkdir()

        manager = ArchiveManager(
            root=root,
            timestamp="20250101_000100",
            archive_all=True,
        )

        assert manager.search is True
        assert manager.archive_all is True


# ⚡ RENAMED: Class to match new function name
class TestArchiveManagerRun:
    """Tests for ArchiveManager.run orchestration."""

    @pytest.mark.parametrize("archive_all", [False, True])
    # ⚡ RENAMED: Function to match new API
    async def test_run_happy_path(self, tmp_path: Path, mock_config, mock_dirs, archive_all):
        """Test Case 4: Full flow with pairs, packaging, clean, prune."""
        root = tmp_path / "root"
        root.mkdir()
        archives_dir, quarantine_dir = mock_dirs

        # Mock components
        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [
            (root / "test.md", root / "test.sha256"),
        ]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_archive_paths = {"test": root / "archives/test.zip"}
        mock_to_delete = [root / "test.md"]
        if archive_all:
            mock_packager.group_pairs_by_prefix.return_value = {"group1": mock_pairs}
            mock_packager.handle_grouped_archives.return_value = (mock_archive_paths, mock_to_delete)
        else:
            mock_packager.handle_single_archive.return_value = (mock_archive_paths, mock_to_delete)
        mock_packager.group_pairs_by_prefix.return_value = {}  # Fallback

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        mock_delete = AsyncMock()
        mock_delete.return_value = (1, 0)

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths", new=mock_delete), \
             patch("create_dump.archiver.confirm", return_value=True):

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                archive_all=archive_all,
                clean_root=True,
                no_remove=False,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run()

        mock_finder.find_dump_pairs.assert_called_once()
        if archive_all:
            mock_packager.group_pairs_by_prefix.assert_called_once()
            mock_packager.handle_grouped_archives.assert_called_once()
        else:
            mock_packager.handle_single_archive.assert_called_once()
        mock_pruner.prune.assert_called_once()
        mock_delete.assert_called_once()  # Clean called
        assert result == mock_archive_paths

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_pairs(self, tmp_path: Path, mock_config, mocker):
        """Test Case 5: Early return if no pairs, prune still runs."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_finder.find_dump_pairs.return_value = []

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner):

            manager = ArchiveManager(root=root, timestamp="20250101_000100")
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run()

        mock_finder.find_dump_pairs.assert_called_once()
        mock_pruner.prune.assert_called_once()
        assert result == {}

    # ⚡ RENAMED: Function to match new API
    async def test_run_dry_run_skips_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 6: dry_run skips delete, no prompt."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.confirm") as mock_confirm, \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                dry_run=True,
                yes=False,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_confirm.assert_not_called()
        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 7: clean_root=False skips delete entirely."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=False,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_no_remove_skips_clean(self, tmp_path: Path, mock_config, mocker):
        """Test Case 8: no_remove=True skips delete despite clean_root."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete, \
             patch("create_dump.archiver.confirm") as mock_confirm:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                no_remove=True,
                dry_run=False,
                yes=True,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_confirm.assert_not_called()
        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_prompt_declined(self, tmp_path: Path, mock_config, mocker):
        """Test Case 9: User declines prompt, skips clean."""
        root = tmp_path / "root"
        root.mkdir()

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_pairs = [(root / "test.md", root / "test.sha256")]
        mock_finder.find_dump_pairs.return_value = mock_pairs

        mock_packager = AsyncMock(spec=ArchivePackager)
        mock_packager.handle_single_archive.return_value = ({}, [root / "test.md"])

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePackager", return_value=mock_packager), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner), \
             patch("create_dump.archiver.confirm", return_value=False), \
             patch("create_dump.archiver.safe_delete_paths") as mock_delete:

            manager = ArchiveManager(
                root=root,
                timestamp="20250101_000100",
                clean_root=True,
                dry_run=False,
                yes=False,
            )
            # ⚡ RENAMED: Call manager.run()
            await manager.run()

        mock_delete.assert_not_called()
        mock_pruner.prune.assert_called_once()

    # ⚡ RENAMED: Function to match new API
    async def test_run_current_outfile_noop(self, tmp_path: Path, mock_config, mocker):
        """Test Case 10: current_outfile passed but no symlink logic yet."""
        root = tmp_path / "root"
        root.mkdir()
        current_outfile = root / "current.md"

        mock_finder = AsyncMock(spec=ArchiveFinder)
        mock_finder.find_dump_pairs.return_value = []

        mock_pruner = AsyncMock(spec=ArchivePruner)
        mock_pruner.prune = AsyncMock()

        with patch("create_dump.archiver.ArchiveFinder", return_value=mock_finder), \
             patch("create_dump.archiver.ArchivePruner", return_value=mock_pruner):

            manager = ArchiveManager(root=root, timestamp="20250101_000100")
            # ⚡ RENAMED: Call manager.run()
            result = await manager.run(current_outfile=current_outfile)

        # No-op; no assertions fail on symlink absence
        assert result == {}