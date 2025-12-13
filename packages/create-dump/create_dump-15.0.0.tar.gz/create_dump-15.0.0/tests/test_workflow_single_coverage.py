# tests/test_workflow_single_coverage.py

import pytest
import shutil
import gzip
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import anyio
from typer import Exit

from create_dump.workflow.single import SingleRunOrchestrator

@pytest.fixture
def mock_root(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    return root

@pytest.mark.anyio
class TestWorkflowSingleCoverage:

    async def test_get_stats_sync(self, mock_root):
        file1 = mock_root / "f1.txt"
        file1.write_text("line1\nline2")
        file2 = mock_root / "f2.txt"
        file2.write_text("line1")

        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        count, loc = orch._get_stats_sync(["f1.txt", "f2.txt", "missing.txt"])
        assert count == 3
        assert loc == 3

    async def test_get_total_size_sync(self, mock_root):
        file1 = mock_root / "f1.txt"
        file1.write_text("123")

        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        size = orch._get_total_size_sync(["f1.txt", "missing.txt"])
        assert size == 3

    async def test_compress_file_sync(self, mock_root):
        in_file = mock_root / "in.txt"
        in_file.write_text("content")
        out_file = mock_root / "out.txt.gz"

        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        orch._compress_file_sync(in_file, out_file)

        assert out_file.exists()
        with gzip.open(out_file, "rt") as f:
            assert f.read() == "content"

    async def test_run_dest_outside_root(self, mock_root, tmp_path):
        # Target lines 202-207, 221-244
        dest = tmp_path / "outside"

        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False, dest=dest
        )

        # We need to mock collector to return files
        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        # Mock safe_is_within to return False to trigger the warning path
                        with patch("create_dump.workflow.single.safe_is_within", new=AsyncMock(return_value=False)):
                            await orch.run()

        assert dest.exists()

    async def test_run_user_cancel(self, mock_root):
        # Target lines 228-233
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=False, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("builtins.input", return_value="n"):
                with pytest.raises(Exit) as excinfo:
                    await orch.run()
                assert excinfo.value.exit_code == 1

    async def test_run_dry_run_output(self, mock_root):
        # Target lines 236-241
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=True, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with pytest.raises(Exit) as excinfo:
                await orch.run()
            assert excinfo.value.exit_code == 0

    async def test_run_json_format(self, mock_root):
        # Target lines 276
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="json", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.JsonWriter") as MockJW:
                    mock_jw_inst = MockJW.return_value
                    mock_jw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        await orch.run()

                        assert mock_jw_inst.write.called

    async def test_run_compression(self, mock_root):
        # Target lines 291-297
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=True, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        # Mock _compress_file_sync to not actually compress but create file
                        def mock_compress(src, dest):
                            Path(dest).touch()

                        with patch.object(orch, "_compress_file_sync", side_effect=mock_compress):
                            # Mock existing outfile before compression
                            with patch("anyio.Path.unlink", new=AsyncMock()):
                                 await orch.run()

                                 assert orch._compress_file_sync.called

    async def test_run_archiving(self, mock_root):
        # Target lines 311-330
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=True, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        with patch("create_dump.workflow.single.ArchiveManager") as MockAM:
                            mock_am_inst = MockAM.return_value
                            mock_am_inst.run = AsyncMock(return_value={"group": Path("archive.zip")})

                            await orch.run()

                            assert mock_am_inst.run.called

    async def test_run_archiving_no_results(self, mock_root):
        # Target lines 327-330
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=True, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        with patch("create_dump.workflow.single.ArchiveManager") as MockAM:
                            mock_am_inst = MockAM.return_value
                            mock_am_inst.run = AsyncMock(return_value={})

                            await orch.run()

                            assert mock_am_inst.run.called

    async def test_run_notification(self, mock_root):
        # Target lines 356-361
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False, notify_topic="mytopic"
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
            with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        with patch("create_dump.workflow.single.send_ntfy_notification", new=AsyncMock()) as mock_notify:
                            await orch.run()

                            assert mock_notify.called

    async def test_get_stats_sync_error(self, mock_root):
        # Target line 158: except (IOError, FileNotFoundError): pass
        orch = SingleRunOrchestrator(root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False, compress=False, format="md", exclude="", include="", max_file_size=None, use_gitignore=False, git_meta=False, progress=False, max_workers=1, archive=False, archive_all=False, archive_search=False, archive_include_current=True, archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None, archive_clean_root=False, archive_format="zip", allow_empty=True, metrics_port=0, verbose=False, quiet=False)

        file1 = mock_root / "locked.txt"
        file1.write_text("content")

        # Mock open to raise IOError
        with patch("builtins.open", side_effect=IOError("Locked")):
            count, loc = orch._get_stats_sync(["locked.txt"])
            assert count == 1 # still counted in total_files
            assert loc == 0 # no lines counted

    async def test_run_middleware_setup(self, mock_root):
        # Target lines 276-282 (middleware setup)
        orch = SingleRunOrchestrator(
            root=mock_root, dry_run=False, yes=True, no_toc=False, tree_toc=False,
            compress=False, format="md", exclude="", include="", max_file_size=None,
            use_gitignore=False, git_meta=False, progress=False, max_workers=1,
            archive=False, archive_all=False, archive_search=False, archive_include_current=True,
            archive_no_remove=False, archive_keep_latest=True, archive_keep_last=None,
            archive_clean_root=False, archive_format="zip", allow_empty=True,
            metrics_port=0, verbose=False, quiet=False, scan_secrets=True, scan_todos=True
        )

        mock_collector = AsyncMock()
        mock_collector.collect.return_value = ["f1.txt"]

        with patch("create_dump.workflow.single.get_collector", return_value=mock_collector):
             with patch("create_dump.workflow.single.FileProcessor") as MockFP:
                mock_fp_inst = MockFP.return_value
                mock_fp_inst.dump_concurrent = AsyncMock(return_value=[])

                with patch("create_dump.workflow.single.MarkdownWriter") as MockMW:
                    mock_mw_inst = MockMW.return_value
                    mock_mw_inst.write = AsyncMock()

                    with patch("create_dump.workflow.single.ChecksumWriter") as MockCW:
                        mock_cw_inst = MockCW.return_value
                        mock_cw_inst.write = AsyncMock(return_value="SHA256: ...")

                        await orch.run()

                        # Verify middlewares were passed to FileProcessor
                        args, kwargs = MockFP.call_args
                        middlewares = kwargs.get('middlewares')
                        assert len(middlewares) == 2
