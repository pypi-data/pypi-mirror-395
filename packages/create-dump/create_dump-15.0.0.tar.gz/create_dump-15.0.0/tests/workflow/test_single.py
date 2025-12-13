# tests/workflow/test_single.py

"""
Tests for src/create_dump/workflow/single.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call, ANY
from typer import Exit
from tempfile import TemporaryDirectory

import anyio

# Import the class to test
from create_dump.workflow.single import SingleRunOrchestrator
from create_dump.core import Config, DumpFile

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_config(mocker) -> Config:
    """Provides a mock Config object."""
    cfg = Config()
    mocker.patch("create_dump.workflow.single.load_config", return_value=cfg)
    return cfg


@pytest.fixture
def mock_orchestrator_deps(mocker, mock_config):
    """Mocks all external dependencies for SingleRunOrchestrator."""

    # 🐞 FIX: Mock the function and return its patch object
    mock_collector_instance = AsyncMock()
    mock_collector_instance.collect.return_value = ["src/main.py"]
    mock_get_collector_func = mocker.patch(
        "create_dump.workflow.single.get_collector",
        return_value=mock_collector_instance
    )

    # Mock Processor
    mock_processor = AsyncMock()
    mock_dump_file = DumpFile(path="src/main.py", temp_path=Path("/tmp/fake.tmp"))
    mock_processor.dump_concurrent.return_value = [mock_dump_file]
    mocker.patch(
        "create_dump.workflow.single.FileProcessor",
        return_value=mock_processor
    )

    # Mock Writers
    mock_md_writer = AsyncMock()
    mocker.patch(
        "create_dump.workflow.single.MarkdownWriter",
        return_value=mock_md_writer
    )
    mock_json_writer = AsyncMock()
    mocker.patch(
        "create_dump.workflow.single.JsonWriter",
        return_value=mock_json_writer
    )
    mock_checksum_writer = AsyncMock()
    mock_checksum_writer.write.return_value = "dummysha  dummyfile.md"
    mocker.patch(
        "create_dump.workflow.single.ChecksumWriter",
        return_value=mock_checksum_writer
    )

    # Mock ArchiveManager
    mock_archive_manager = AsyncMock()
    mock_archive_manager.run.return_value = {"default": Path("/tmp/archive.zip")}
    mocker.patch(
        "create_dump.workflow.single.ArchiveManager",
        return_value=mock_archive_manager
    )

    # 🐞 FIX: Mock the class and return its patch object
    mock_secret_scanner_class = mocker.patch(
        "create_dump.workflow.single.SecretScanner",
        return_value=MagicMock()  # Return a dummy instance
    )

    # Mock sync functions run in threads
    # 🐞 FIX: Mock _get_total_size_sync directly to avoid thread issues
    mocker.patch(
        "create_dump.workflow.single.SingleRunOrchestrator._get_total_size_sync",
        return_value=1024
    )
    mocker.patch(
        "create_dump.workflow.single.SingleRunOrchestrator._get_stats_sync",
        return_value=(1, 10)
    )
    
    # 🐞 FIX: Simplified the mock. The lambda's __name__ check conflicted with
    # the separate mock of _get_total_size_sync. This now just executes
    # the (already mocked) function it is given.
    mocker.patch(
        "anyio.to_thread.run_sync",
        side_effect=lambda func, *args: func(*args)
    )

    # Mock helpers and system functions
    mocker.patch(
        "create_dump.workflow.single._unique_path",
        side_effect=lambda p: p
    )
    mocker.patch(
        "create_dump.workflow.single.get_git_meta",
        return_value=None
    )
    
    # -----------------
    # 🐞 FIX: Capture the mock object here
    # -----------------
    mock_styled_print = mocker.patch("create_dump.workflow.single.styled_print")
    mocker.patch("create_dump.workflow.single.input", return_value="y")
    mocker.patch(
        "create_dump.workflow.single.TemporaryDirectory",
        MagicMock(spec=TemporaryDirectory)
    )
    
    # ⚡ FIX: Update DUMP_DURATION mock to handle .labels()
    mock_duration_ctx = MagicMock()
    mock_duration_ctx.__enter__ = MagicMock()
    mock_duration_ctx.__exit__ = MagicMock()
    mock_duration = mocker.patch("create_dump.workflow.single.DUMP_DURATION")
    mock_duration.labels.return_value.time.return_value = mock_duration_ctx
    
    mocker.patch(
        "create_dump.workflow.single.metrics_server",
        MagicMock()
    )

    # Return a dictionary of key mocks for assertions
    return {
        "get_collector": mock_get_collector_func, # 🐞 FIX: Return patch object
        "collector_instance": mock_collector_instance, # 🐞 FIX: Return instance for method calls
        "FileProcessor": mock_processor,
        "MarkdownWriter": mock_md_writer,
        "JsonWriter": mock_json_writer,
        "ChecksumWriter": mock_checksum_writer,
        "ArchiveManager": mock_archive_manager,
        "SecretScanner": mock_secret_scanner_class, # 🐞 FIX: Return patch object
        # -----------------
        # 🐞 FIX: Add the mock to the returned dictionary
        # -----------------
        "DUMP_DURATION": mock_duration, # ✨ NEW: Add this to the returned dict
        "styled_print": mock_styled_print,
    }
    
@pytest.fixture
def orchestrator_instance(test_project) -> SingleRunOrchestrator:
    """Provides a default instance of SingleRunOrchestrator."""
    return SingleRunOrchestrator(
        root=test_project.root,
        dry_run=False,
        yes=True,
        no_toc=False,
        tree_toc=False,
        compress=False,
        format="md",
        exclude="",
        include="",
        max_file_size=None,
        use_gitignore=True,
        git_meta=True,
        progress=False,
        max_workers=16,
        archive=False,
        archive_all=False,
        archive_search=False,
        archive_include_current=True,
        archive_no_remove=False,
        archive_keep_latest=True,
        archive_keep_last=None,
        archive_clean_root=False,
        archive_format="zip",
        allow_empty=False,
        metrics_port=0,
        verbose=False,
        quiet=False,
        dest=None,
        git_ls_files=False,
        diff_since=None,
        scan_secrets=False,
        hide_secrets=False,
    )


class TestSingleRunOrchestrator:
    """Tests for the SingleRunOrchestrator."""

    async def test_run_happy_path_md(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 1: Standard MD run, all steps called."""

        await orchestrator_instance.run()

        # Check that core components were called
        # 🐞 FIX: Assert against the returned instance's method
        mock_orchestrator_deps["collector_instance"].collect.assert_called_once()
        mock_orchestrator_deps["FileProcessor"].dump_concurrent.assert_called_once()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_called_once_with(
            ANY, ANY, ANY, total_files=1, total_loc=10
        )
        mock_orchestrator_deps["ChecksumWriter"].write.assert_called_once()
        
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

        # Check that non-default components were NOT called
        mock_orchestrator_deps["JsonWriter"].write.assert_not_called()
        mock_orchestrator_deps["ArchiveManager"].run.assert_not_called()
        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_not_called()

    async def test_run_dry_run_exits(self, orchestrator_instance, mock_orchestrator_deps):
        """Test Case 2: dry_run=True exits gracefully."""
        # 🐞 FIX: Add mock_orchestrator_deps to ensure collector returns files
        orchestrator_instance.dry_run = True

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()

        assert e.value.exit_code == 0
        
        # ⚡ FIX: Assert metric was NOT called
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_not_called()

    async def test_run_no_files_fail(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 3: No files found fails when allow_empty=False."""
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        orchestrator_instance.allow_empty = False

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()

        assert e.value.exit_code == 1

    async def test_run_no_files_allow_empty(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 4: No files found exits gracefully when allow_empty=True."""
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        orchestrator_instance.allow_empty = True

        await orchestrator_instance.run()

        # Ensure no processing or writing was attempted
        mock_orchestrator_deps["FileProcessor"].dump_concurrent.assert_not_called()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_not_called()
        
        # ⚡ FIX: Assert metric was NOT called
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_not_called()

    async def test_run_json_format(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 5: format='json' calls JsonWriter."""
        orchestrator_instance.format = "json"

        await orchestrator_instance.run()

        mock_orchestrator_deps["JsonWriter"].write.assert_called_once()
        mock_orchestrator_deps["MarkdownWriter"].write.assert_not_called()
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_archive(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 6: archive=True calls ArchiveManager."""
        orchestrator_instance.archive = True

        await orchestrator_instance.run()

        mock_orchestrator_deps["ArchiveManager"].run.assert_called_once()
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_scan_secrets(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 7: scan_secrets=True instantiates SecretScanner."""
        orchestrator_instance.scan_secrets = True
        orchestrator_instance.hide_secrets = False

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_called_once_with(
            hide_secrets=False,
            custom_patterns=[]
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_hide_secrets(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """Test Case 8: hide_secrets=True passes flag to SecretScanner."""
        orchestrator_instance.scan_secrets = True
        orchestrator_instance.hide_secrets = True

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the class patch object
        mock_orchestrator_deps["SecretScanner"].assert_called_once_with(
            hide_secrets=True,
            custom_patterns=[]
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_collector_flags(
        self, orchestrator_instance, mock_orchestrator_deps, mock_config
    ):
        """Test Case 9: Git flags are passed to get_collector."""
        orchestrator_instance.git_ls_files = True
        orchestrator_instance.diff_since = "main"

        await orchestrator_instance.run()

        # 🐞 FIX: Assert against the function patch object
        mock_orchestrator_deps["get_collector"].assert_called_once_with(
            config=mock_config,
            includes=[],
            excludes=[],
            use_gitignore=True,
            root=orchestrator_instance.root,
            git_ls_files=True,
            diff_since="main"
        )
        
        # ⚡ FIX: Assert metric label (diff_since takes precedence)
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="git_diff")
        

    async def test_run_no_files_logging_branches(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Action Plan 1 (Variation): Test logging branches for no_files.
        Covers verbose and quiet branches (lines 113-120).
        """
        mock_orchestrator_deps["collector_instance"].collect.return_value = []
        mock_styled_print = mock_orchestrator_deps["styled_print"]
        
        # 1. Test quiet=True (should not print)
        orchestrator_instance.allow_empty = True
        orchestrator_instance.quiet = True
        orchestrator_instance.verbose = False
        
        await orchestrator_instance.run()
        
        # Assert styled_print was NOT called
        mock_styled_print.assert_not_called()
        mock_styled_print.reset_mock()

        # 2. Test quiet=False (should print)
        orchestrator_instance.quiet = False
        orchestrator_instance.verbose = True # Also cover verbose branch
        
        await orchestrator_instance.run()

        # Assert styled_print WAS called
        mock_styled_print.assert_any_call("[yellow]⚠️ No matching files found; skipping dump.[/yellow]")

    async def test_run_user_prompt_cancel(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Action Plan 2: Test user prompt "n" (lines 177-182).
        Asserts that a "n" response to the prompt raises Exit(code=1).
        """
        # 1. Setup
        orchestrator_instance.yes = False
        orchestrator_instance.dry_run = False
        orchestrator_instance.quiet = False
        
        # 2. Mock: Override the default "y" mock for input
        mocker.patch("create_dump.workflow.single.input", return_value="n")
        mock_styled_print = mock_orchestrator_deps["styled_print"]

        # 3. Act & Assert
        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()
        
        assert e.value.exit_code == 1
        
        # 4. Assert cancellation message was printed
        mock_styled_print.assert_any_call("[red]Cancelled.[/red]")

    async def test_run_compress_true(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Action Plan 3: Test compress=True (lines 205-212).
        Asserts that compression is called and the final file is .gz.
        """
        # 1. Setup
        orchestrator_instance.compress = True
        
        # 2. Mock: Mock the sync compression function
        mock_compress_sync = mocker.patch.object(
            SingleRunOrchestrator, "_compress_file_sync"
        )
        
        # 3. Mock: Mock anyio.Path.unlink to verify the original .md is deleted
        mock_unlink = AsyncMock()
        mock_path_instance = MagicMock()
        mock_path_instance.unlink = mock_unlink
        mocker.patch("create_dump.workflow.single.anyio.Path", return_value=mock_path_instance)

        # 4. Act
        await orchestrator_instance.run()

        # 5. Assert
        # Assert compression was called
        mock_compress_sync.assert_called_once()
        
        # Assert the original file was unlinked
        mock_unlink.assert_called_once()
        
        # Assert the ChecksumWriter was called with the new .gz path
        mock_checksum_writer = mock_orchestrator_deps["ChecksumWriter"]
        final_path = mock_checksum_writer.write.call_args[0][0]
        assert str(final_path).endswith(".md.gz")
        
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")

    async def test_run_archive_no_results(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Action Plan 4: Test Archive 'Else' Branch (lines 263-268).
        Asserts the correct message is logged if archive=True but no
        archives are found/created.
        """
        # 1. Setup
        orchestrator_instance.archive = True
        orchestrator_instance.quiet = False # Ensure print is called

        # 2. Mock: Override ArchiveManager to return an empty/falsy value
        mock_archive_manager = mock_orchestrator_deps["ArchiveManager"]
        mock_archive_manager.run.return_value = {} # Empty dict
        
        mock_styled_print = mock_orchestrator_deps["styled_print"]
        
        # 3. Act
        await orchestrator_instance.run()

        # 4. Assert
        mock_archive_manager.run.assert_called_once()
        mock_styled_print.assert_any_call(
            "[yellow]ℹ️ No prior dumps found for archiving.[/yellow]"
        )
        # ⚡ FIX: Assert metric label
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="walk")
# [TEST_SKELETON_END]


    async def test_run_git_ls_collector_metric(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Covers line 234 (git_ls collector metric label).
        """
        orchestrator_instance.git_ls_files = True
        orchestrator_instance.diff_since = None # Ensure diff is not used

        await orchestrator_instance.run()
        
        mock_orchestrator_deps["DUMP_DURATION"].labels.assert_called_with(collector="git_ls")

    async def test_run_dry_run_prints_files(
        self, orchestrator_instance, mock_orchestrator_deps
    ):
        """
        Covers lines 190-198 (dry run prints files).
        """
        orchestrator_instance.dry_run = True
        orchestrator_instance.quiet = False
        mock_orchestrator_deps["collector_instance"].collect.return_value = ["a.py", "b.py"]
        mock_styled_print = mock_orchestrator_deps["styled_print"]

        with pytest.raises(Exit) as e:
            await orchestrator_instance.run()
        
        assert e.value.exit_code == 0
        mock_styled_print.assert_any_call("[green]✅ Dry run: Would process listed files.[/green]")
        mock_styled_print.assert_any_call(" - a.py")
        mock_styled_print.assert_any_call(" - b.py")

    async def test_run_dest_outside_root_warns(
        self, orchestrator_instance, mock_orchestrator_deps, mocker, test_project
    ):
        """
        Covers line 155 (dest outside root warning).
        """
        orchestrator_instance.dest = Path("/tmp/outside_dest")
        
        mock_logger = mocker.patch("create_dump.workflow.single.logger")
        # Mock safe_is_within to return False
        mocker.patch("create_dump.workflow.single.safe_is_within", new_callable=AsyncMock, return_value=False)

        await orchestrator_instance.run()
        
        mock_logger.warning.assert_called_once_with("Absolute dest outside root; proceeding with caution.")

    async def test_get_total_size_sync_handles_file_not_found(
        self, orchestrator_instance, mocker
    ):
        """
        Covers lines 124-125 (FileNotFoundError in _get_total_size_sync).
        """
        orchestrator_instance.root = Path("/fake/root") # Set a real path
        
        # Mock Path.stat to raise FileNotFoundError
        mock_stat = mocker.patch("pathlib.Path.stat", side_effect=FileNotFoundError)
        
        # Call the sync function directly (it's what run_sync does)
        size = orchestrator_instance._get_total_size_sync(["nonexistent.py"])
        
        assert size == 0
        mock_stat.assert_called_once()


    async def test_get_stats_sync(self, orchestrator_instance, test_project):
        """
        Tests the _get_stats_sync method.
        """
        # 1. Setup
        await test_project.create({
            "a.py": "print('hello')\nprint('world')",
            "b.py": "pass",
        })

        # 2. Act
        total_files, total_loc = orchestrator_instance._get_stats_sync(["a.py", "b.py"])

        # 3. Assert
        assert total_files == 2
        assert total_loc == 3


    async def test_run_sends_notify_on_success(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Tests that a notification is sent on successful run.
        """
        orchestrator_instance.notify_topic = "test"
        mock_send_ntfy = mocker.patch("create_dump.workflow.single.send_ntfy_notification")

        await orchestrator_instance.run()

        mock_send_ntfy.assert_called_once_with(
            "test",
            ANY,
            "✅ create-dump Success",
        )


    async def test_run_sends_notify_on_failure(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Tests that a notification is sent on failure.
        """
        orchestrator_instance.notify_topic = "test"
        mock_send_ntfy = mocker.patch("create_dump.workflow.single.send_ntfy_notification")
        mocker.patch(
            "create_dump.workflow.single.get_collector",
            side_effect=Exception("BOOM"),
        )

        with pytest.raises(Exception, match="BOOM"):
            await orchestrator_instance.run()

        mock_send_ntfy.assert_called_once_with(
            "test",
            "An unexpected error occurred: BOOM",
            "❌ create-dump Error",
        )


    async def test_run_sends_notify_on_dry_run(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Tests that a notification is sent on dry run.
        """
        orchestrator_instance.notify_topic = "test"
        orchestrator_instance.dry_run = True
        mock_send_ntfy = mocker.patch("create_dump.workflow.single.send_ntfy_notification")

        with pytest.raises(Exit):
            await orchestrator_instance.run()

        mock_send_ntfy.assert_called_once_with(
            "test",
            "Dry run completed.",
            "ℹ️ create-dump Dry Run",
        )


    async def test_run_no_notify_topic(
        self, orchestrator_instance, mock_orchestrator_deps, mocker
    ):
        """
        Tests that no notification is sent if notify_topic is None.
        """
        orchestrator_instance.notify_topic = None
        mock_send_ntfy = mocker.patch("create_dump.workflow.single.send_ntfy_notification")

        await orchestrator_instance.run()

        mock_send_ntfy.assert_not_called()