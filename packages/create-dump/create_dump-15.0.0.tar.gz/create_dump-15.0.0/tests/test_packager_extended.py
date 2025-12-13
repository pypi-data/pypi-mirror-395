# tests/test_packager_extended.py

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import os

from create_dump.archive.packager import ArchivePackager

@pytest.fixture
def mock_dirs(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    archives = root / "archives"
    archives.mkdir()
    quarantine = archives / "quarantine"
    quarantine.mkdir()
    return root, archives, quarantine

@pytest.mark.anyio
class TestPackagerExtended:

    async def test_handle_single_archive_sorting_fallback(self, mock_dirs):
        root, archives, quarantine = mock_dirs

        # Two files with same timestamp (or unparseable timestamp) but different mtime
        # Use > 1980 for ZIP compatibility (approx 315532800)
        t1 = 400000000
        t2 = 500000000
        f1 = root / "dump_invalid_ts_1.md"
        f1.touch()
        os.utime(f1, (t1, t1))

        f2 = root / "dump_invalid_ts_2.md"
        f2.touch()
        os.utime(f2, (t2, t2))

        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=True, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        # Mock extract_timestamp to return datetime.min to trigger mtime fallback
        # (Files have safe mtime > 1980)
        with patch("create_dump.archive.packager.extract_timestamp", return_value=datetime.min):
            pairs = [(f1, None), (f2, None)]
            archive_paths, to_delete = await packager.handle_single_archive(pairs)

            # f2 is newer (mtime 2000), so it should be kept (live_pair).
            # f1 is older (mtime 1000), so it should be archived.

            # Checking if f1 is in to_delete (archived files list)
            assert f1 in to_delete
            assert f2 not in to_delete

    async def test_handle_single_archive_no_historical(self, mock_dirs):
        root, archives, quarantine = mock_dirs

        f1 = root / "dump_1.md"
        f1.touch()

        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=True, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        # Only one pair, keep_latest=True -> No historical
        pairs = [(f1, None)]
        archive_paths, to_delete = await packager.handle_single_archive(pairs)

        assert len(to_delete) == 0
        assert len(archive_paths) == 0

    async def test_handle_single_archive_clean_root(self, mock_dirs):
        root, archives, quarantine = mock_dirs

        f1 = root / "dump_old.md"
        f1.touch()
        f2 = root / "dump_new.md"
        f2.touch()

        # Mock timestamps via sorting key or ensure filenames parse correctly?
        # Filenames don't match pattern "timestamp" exactly unless `extract_timestamp` handles it.
        # Let's mock `extract_timestamp`.

        def mock_extract(name):
            if "new" in name: return datetime(2025, 1, 2)
            return datetime(2025, 1, 1)

        with patch("create_dump.archive.packager.extract_timestamp", side_effect=mock_extract):
            # Mock safe_delete_paths to verify call
            with patch("create_dump.archive.packager.safe_delete_paths", new=AsyncMock()) as mock_delete:

                packager = ArchivePackager(
                    root=root, archives_dir=archives, quarantine_dir=quarantine,
                    timestamp="20250101", keep_latest=True, verbose=True, dry_run=False,
                    yes=True, clean_root=True, no_remove=False
                )

                pairs = [(f1, None), (f2, None)]

                # We need _create_archive to actually return archived files
                # Or mock it.
                with patch.object(packager, "_create_archive", new=AsyncMock(return_value=(Path("archive.zip"), [f1]))):
                     await packager.handle_single_archive(pairs)

                     # Should call safe_delete_paths for f1
                     args, _ = mock_delete.call_args
                     # args[0] is list of files
                     assert f1 in args[0]
                     assert f2 not in args[0]

    async def test_handle_grouped_archives_quarantine_dry_run(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        f1 = root / "dangling.md"
        f1.touch()

        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=True, verbose=True, dry_run=True,
            yes=True, clean_root=False, no_remove=False
        )

        groups = {'default': [(f1, None)]}

        await packager.handle_grouped_archives(groups)

        # Verify NO rename happened (dry run)
        assert f1.exists()
        assert not (quarantine / "dangling.md").exists()

    async def test_handle_grouped_archives_quarantine_real(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        f1 = root / "dangling.md"
        f1.write_text("content")

        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=True, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        groups = {'default': [(f1, None)]}

        await packager.handle_grouped_archives(groups)

        # Verify rename happened
        assert not f1.exists()
        assert (quarantine / "dangling.md").exists()
