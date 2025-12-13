# tests/test_packager_coverage.py

import pytest
import tarfile
import zipfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from create_dump.archive.packager import ArchivePackager, ArchiveError

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
class TestPackagerCoverage:

    async def test_create_archive_formats(self, mock_dirs):
        root, archives, quarantine = mock_dirs

        file1 = root / "file1.txt"
        file1.write_text("content")

        # Test zip (default)
        packager_zip = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False, archive_format="zip"
        )
        archive_path_zip, archived_zip = packager_zip._create_archive_sync([file1], "test_archive.zip")
        assert archive_path_zip.exists()
        assert str(archive_path_zip).endswith(".zip")
        assert zipfile.is_zipfile(archive_path_zip)

        # Test tar.gz
        packager_tar_gz = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False, archive_format="tar.gz"
        )

        archive_path, archived = packager_tar_gz._create_archive_sync([file1], "test_archive.tar.gz")
        assert archive_path.exists()
        assert str(archive_path).endswith(".tar.gz")
        assert tarfile.is_tarfile(archive_path)

        # Test tar.bz2
        packager_tar_bz2 = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False, archive_format="tar.bz2"
        )
        archive_path_bz2, archived_bz2 = packager_tar_bz2._create_archive_sync([file1], "test_archive.tar.bz2")
        assert archive_path_bz2.exists()
        assert str(archive_path_bz2).endswith(".tar.bz2")
        assert tarfile.is_tarfile(archive_path_bz2)

    async def test_create_archive_error_handling(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        file1 = root / "file1.txt"
        file1.write_text("content")

        # Force an error during zip writing
        with patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Test Error")):
            with pytest.raises(zipfile.BadZipFile):
                packager._create_archive_sync([file1], "bad.zip")

    async def test_handle_grouped_archives_quarantine(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        # Create dummy files
        md_file = root / "dangling.md"
        md_file.write_text("md")
        sha_file = root / "dangling.sha256"
        sha_file.write_text("sha")

        groups = {
            'default': [(md_file, sha_file)]
        }

        archive_paths, to_delete = await packager.handle_grouped_archives(groups)

        # Verify files were moved to quarantine
        assert (quarantine / "dangling.md").exists()
        assert (quarantine / "dangling.sha256").exists()
        assert not md_file.exists()
        assert not sha_file.exists()

    async def test_handle_grouped_archives_dry_run_quarantine(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=True,
            yes=True, clean_root=False, no_remove=False
        )

        md_file = root / "dangling_dry.md"
        md_file.write_text("md")

        groups = {
            'default': [(md_file, None)]
        }

        await packager.handle_grouped_archives(groups)

        # Files should NOT move in dry run
        assert md_file.exists()
        assert not (quarantine / "dangling_dry.md").exists()

    async def test_handle_grouped_archives_normal_flow(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        file1 = root / "group1_1.md"
        file1.write_text("content")
        file2 = root / "group1_2.md"
        file2.write_text("content")

        groups = {
            'group1': [(file1, None), (file2, None)]
        }

        archive_paths, to_delete = await packager.handle_grouped_archives(groups)

        assert 'group1' in archive_paths
        assert archive_paths['group1'] is not None
        assert archive_paths['group1'].exists()

    async def test_create_archive_sync_tar_error(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False, archive_format="tar.gz"
        )

        file1 = root / "file1.txt"
        file1.write_text("content")

        # Force an error during tar writing
        with patch("tarfile.open", side_effect=tarfile.TarError("Test Error")):
            with pytest.raises(tarfile.TarError):
                packager._create_archive_sync([file1], "bad.tar.gz")

    async def test_handle_grouped_archives_quarantine_missing_sha(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        md_file = root / "dangling.md"
        md_file.write_text("md")
        # SHA file does not exist

        groups = {
            'default': [(md_file, root / "dangling.sha256")]
        }

        await packager.handle_grouped_archives(groups)

        assert (quarantine / "dangling.md").exists()
        assert not md_file.exists()
        # SHA should not be quarantined because it didn't exist
        assert not (quarantine / "dangling.sha256").exists()

    async def test_handle_grouped_archives_quarantine_same_file(self, mock_dirs):
        root, archives, quarantine = mock_dirs
        packager = ArchivePackager(
            root=root, archives_dir=archives, quarantine_dir=quarantine,
            timestamp="20250101", keep_latest=False, verbose=True, dry_run=False,
            yes=True, clean_root=False, no_remove=False
        )

        md_file = root / "dangling.md"
        md_file.write_text("md")

        groups = {
            'default': [(md_file, md_file)] # SHA is same as MD
        }

        await packager.handle_grouped_archives(groups)

        assert (quarantine / "dangling.md").exists()
        assert not md_file.exists()
