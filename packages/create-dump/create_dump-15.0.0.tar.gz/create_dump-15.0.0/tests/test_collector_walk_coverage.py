# tests/test_collector_walk_coverage.py

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
import anyio
from create_dump.collector.walk import WalkCollector
from create_dump.core import Config

@pytest.fixture
def mock_root(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    return root

@pytest.mark.anyio
class TestWalkCollectorCoverage:

    async def test_collect_recursive_oserror(self, mock_root):
        # Create a directory
        subdir = mock_root / "subdir"
        subdir.mkdir()

        cfg = Config()
        collector = WalkCollector(config=cfg, includes=[], excludes=[], use_gitignore=False, root=mock_root)

        # Use a class-level patch for anyio.Path.iterdir with autospec=True so self is passed
        original_iterdir = anyio.Path.iterdir

        async def side_effect_iterdir(self):
            if self.name == "subdir":
                 raise OSError("Permission denied")
            if self.name == "project":
                yield anyio.Path(subdir)

        with patch.object(anyio.Path, "iterdir", side_effect=side_effect_iterdir, autospec=True):
             # Also mock is_dir to avoid disk checks on mock paths if needed, but here yield actual paths
             # is_dir call will happen on the yielded anyio.Path(subdir)
             # If side_effect_iterdir yields real anyio.Path objects, their methods work.

             files = await collector.collect()
             assert files == []

    async def test_collect_root_oserror(self, mock_root):
        cfg = Config()
        collector = WalkCollector(config=cfg, includes=[], excludes=[], use_gitignore=False, root=mock_root)

        with patch("anyio.Path.iterdir", side_effect=OSError("Root permission denied")):
            files = await collector.collect()
            assert files == []

    async def test_collect_matches_file(self, mock_root):
        file1 = mock_root / "file1.txt"
        file1.touch()

        cfg = Config()
        collector = WalkCollector(config=cfg, includes=[], excludes=[], use_gitignore=False, root=mock_root)

        files = await collector.collect()
        assert "file1.txt" in files

    async def test_collect_matches_recursive(self, mock_root):
        subdir = mock_root / "subdir"
        subdir.mkdir()
        file2 = subdir / "file2.txt"
        file2.touch()

        cfg = Config()
        collector = WalkCollector(config=cfg, includes=[], excludes=[], use_gitignore=False, root=mock_root)

        files = await collector.collect()
        assert "subdir/file2.txt" in files

    async def test_collect_excluded_dir(self, mock_root):
        # excluded_dirs in Config defaults to [".git", ...]
        dot_git = mock_root / ".git"
        dot_git.mkdir()
        file_hidden = dot_git / "hidden.txt"
        file_hidden.touch()

        cfg = Config()
        collector = WalkCollector(config=cfg, includes=[], excludes=[], use_gitignore=False, root=mock_root)

        files = await collector.collect()
        assert ".git/hidden.txt" not in files
