# tests/cli/test_single.py

"""
Comprehensive tests for the 'single' command in src/create_dump/cli/single.py
"""

from __future__ import annotations
import pytest
from typer.testing import CliRunner
# 🐞 FIX: Import ANY and call
from unittest.mock import MagicMock, patch, AsyncMock, call, ANY
from pathlib import Path
from typer import Exit
# ⚡ REFACTOR: No longer importing BadParameter or SystemExit

# Import the main app to test the 'single' command in context
from create_dump.cli.main import app
# 🐞 FIX: Import the function we need to check the *identity* of
from create_dump.cli.single import run_single


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_cli_deps(mocker):
    """
    Mocks all downstream dependencies for cli.single, allowing us to
    test the CLI logic in isolation.
    """
    # 🐞 FIX: Mock anyio.run itself, not the async function
    # This is a more robust way to test the CLI boundary.
    mock_anyio_run = mocker.patch(
        "create_dump.cli.single.anyio.run",
        new_callable=MagicMock  # Use a standard mock, not AsyncMock
    )

    # Mock the logging setup function
    mock_setup_logging = mocker.patch("create_dump.cli.single.setup_logging")

    # Mock dependencies from cli.main to allow the app to load
    mocker.patch("create_dump.cli.main.load_config")
    # 🐞 FIX: Make the main setup_logging mock point to the same object
    # This ensures we can reliably test the *final* call from cli.single
    mocker.patch("create_dump.cli.main.setup_logging", new=mock_setup_logging)

    return {
        "anyio_run": mock_anyio_run, # 🐞 FIX: Return the new mock
        "setup_logging": mock_setup_logging,
    }


class TestSingleCli:
    """Tests for the 'single' command logic."""

    def test_invalid_root_is_file(self, cli_runner: CliRunner):
        """
        Test Case 1: (Validation)
        Fails with BadParameter if the root argument is a file, not a directory.
        """
        with cli_runner.isolated_filesystem() as temp_dir:
            file_path = Path(temp_dir) / "im_a_file.txt"
            file_path.write_text("content")

            # ⚡ REFACTOR: Let the runner catch the exception
            result = cli_runner.invoke(
                app, 
                ["single", str(file_path)]
                # Note: No catch_exceptions=False
            )
            
            # ⚡ REFACTOR: Assert the exit code is 2 (for BadParameter)
            assert result.exit_code == 2

    def test_flag_conflict_git_ls_and_diff(self, cli_runner: CliRunner):
        """
        Test Case 2: (Validation)
        Fails with BadParameter if --git-ls-files and --diff-since are used together.
        """
        # ⚡ REFACTOR: Let the runner catch the exception
        result = cli_runner.invoke(
            app, 
            ["single", ".", "--git-ls-files", "--diff-since", "main"]
        )
        
        # ⚡ REFACTOR: Assert the exit code is 2
        assert result.exit_code == 2

    def test_flag_conflict_hide_secrets(self, cli_runner: CliRunner):
        """
        Test Case 3: (Validation)
        Fails with BadParameter if --hide-secrets is used without --scan-secrets.
        """
        # ⚡ REFACTOR: Let the runner catch the exception
        result = cli_runner.invoke(
            app, 
            ["single", ".", "--hide-secrets"]
        )
        
        # ⚡ REFACTOR: Assert the exit code is 2
        assert result.exit_code == 2

    @pytest.mark.parametrize(
        "cli_flags, expected_dry_run_val",
        [
            (["-d"], True),
            (["--dry-run"], True),
            (["-nd"], False),
            (["--no-dry-run"], False),
            (["-d", "-nd"], False),
            ([], False),
        ],
    )
    def test_effective_dry_run_logic(
        self, cli_runner: CliRunner, mock_cli_deps: dict, cli_flags: list[str], expected_dry_run_val: bool
    ):
        """
        Test Case 5: (effective_dry_run)
        Tests all combinations of -d and -nd to ensure the correct
        boolean is passed to the async runner.
        """
        with cli_runner.isolated_filesystem():
            # ⚡ REFACTOR: We MUST use catch_exceptions=False for non-error tests
            cli_runner.invoke(app, ["single", "."] + cli_flags, catch_exceptions=False)

        mock_anyio_run = mock_cli_deps["anyio_run"] # 🐞 FIX: Get the right mock
        mock_anyio_run.assert_called_once()
        call_args = mock_anyio_run.call_args[0]
        # 🐞 FIX: Index is 2 (arg[0] is function, arg[1] is root)
        assert call_args[2] is expected_dry_run_val

    @pytest.mark.parametrize(
        "cli_flags, expected_verbose, expected_quiet, expected_progress",
        [
            # Default
            (["single", "."], False, False, True),
            # Main flags
            (["-v", "single", "."], True, False, True),
            (["-q", "single", "."], False, True, False),
            # Command flags
            (["single", "-v", "."], True, False, True),
            (["single", "-q", "."], False, True, False),
            # Command overrides Main
            (["-v", "single", "-q", "."], False, True, False),
            (["-q", "single", "-v", "."], True, False, True),
            # Progress flag interaction
            (["single", ".", "--no-progress"], False, False, False),
            (["single", "-q", ".", "--progress"], False, True, False), # Quiet wins
        ],
    )
    def test_verbose_quiet_progress_logic(
        self, cli_runner: CliRunner, mock_cli_deps: dict, cli_flags: list[str],
        expected_verbose: bool, expected_quiet: bool, expected_progress: bool
    ):
        """
        Test Case 6: (Logging & Progress)
        Tests the complex logic for verbose/quiet flags, including
        precedence of command flags over main flags, and how
        they interact with the progress flag.
        """
        with cli_runner.isolated_filesystem():
            cli_runner.invoke(app, cli_flags, catch_exceptions=False)

        mock_setup_logging = mock_cli_deps["setup_logging"]
        mock_anyio_run = mock_cli_deps["anyio_run"] # LIFIX: Get the right mock

        # 1. Check that setup_logging was called with the correct final values
        # The logic in single.py ensures it's called *last* with the final values.
        mock_setup_logging.assert_called_with(verbose=expected_verbose, quiet=expected_quiet)

        # 2. Check that the correct values were passed to the async runner
        mock_anyio_run.assert_called_once() # 🐞 FIX: Assert on anyio_run
        call_args = mock_anyio_run.call_args[0]
        # fargs...
        assert call_args[13] is expected_progress # arg[13] is 'effective_progress'
        assert call_args[26] is expected_verbose  # arg[26] is 'verbose_val'
        assert call_args[27] is expected_quiet    # arg[27] is 'quiet_val'

    def test_all_flags_passed_to_run_single(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 7: (Argument Passthrough)
        Verifies that *all* CLI flags are correctly processed and
        passed to the `anyio.run(run_single, ...)` call.
        """
        with cli_runner.isolated_filesystem() as temp_dir:
            dest_path = Path(temp_dir) / "my_dest"
            dest_path.mkdir()

            cli_args = [
                "single",
                ".",
                "--dest", str(dest_path),
                "--no-toc",
                "--tree-toc",
                "--format", "json",
                "-c", # compress
                "--allow-empty",
                "--metrics-port", "9090",
                "--exclude", "a,b",
                "--include", "c,d",
                "--max-file-size", "1024",
                "--no-use-gitignore",
                "--no-git-meta",
                "--max-workers", "8",
                "--watch",
                # "--git-ls-files", # Removed to avoid validation conflict
                "--diff-since", "main",
                "--scan-secrets",
                "--hide-secrets",
                "--scan-todos",
                "-a", # archive
                "--archive-all",
                "--archive-search",
                "--no-archive-include-current",
                "--archive-no-remove",
                "--no-archive-keep-latest",
                "--archive-keep-last", "5",
                "--archive-clean-root",
                "--archive-format", "tar.gz",
                "-y", # yes
            ]
            
            result = cli_runner.invoke(app, cli_args, catch_exceptions=False)
            assert result.exit_code == 0

            mock_anyio_run = mock_cli_deps["anyio_run"]
            mock_anyio_run.assert_called_once()

            call_args = mock_anyio_run.call_args[0]
            
            assert call_args[0] is run_single # Check function identity
            assert call_args[1] == Path('.')           # root
            assert call_args[2] is False           # effective_dry_run
            assert call_args[3] is True            # yes
            assert call_args[4] is True            # no_toc
            assert call_args[5] is True            # tree_toc
            assert call_args[6] is True            # compress
            assert call_args[7] == "json"          # format
            assert call_args[8] == "a,b"           # exclude
            assert call_args[9] == "c,d"           # include
            assert call_args[10] == 1024           # max_file_size
            assert call_args[11] is False          # use_gitignore
            assert call_args[12] is False          # git_meta
            assert call_args[13] is True           # effective_progress
            assert call_args[14] == 8              # max_workers
            assert call_args[15] is True           # archive
            assert call_args[16] is True           # archive_all
            assert call_args[17] is True           # archive_search
            assert call_args[18] is False          # archive_include_current
            assert call_args[19] is True           # archive_no_remove
            assert call_args[20] is False          # archive_keep_latest
            assert call_args[21] == 5              # archive_keep_last
            assert call_args[22] is True           # archive_clean_root
            assert call_args[23] == "tar.gz"       # archive_format
            assert call_args[24] is True           # allow_empty
            assert call_args[25] == 9090           # metrics_port
            assert call_args[26] is False          # verbose_val
            assert call_args[27] is False          # quiet_val
            assert call_args[28] == dest_path      # dest
            assert call_args[29] is True           # watch
            assert call_args[30] is False          # git_ls_files
            assert call_args[31] == "main"         # diff_since
            assert call_args[32] is True           # scan_secrets
            assert call_args[33] is True           # hide_secrets
            assert call_args[34] is None           # secret_patterns
            assert call_args[35] is True           # scan_todos

    def test_dry_run_exit_is_graceful(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 8: (Exception Handling)
        Ensures that if the async runner raises Exit(code=0) (e.g.,
        from its own dry_run check), the CLI exits gracefully with code 0.
        """
        mock_anyio_run = mock_cli_deps["anyio_run"] 
        mock_anyio_run.side_effect = Exit(code=0)

        # Pass -d to trigger the `if ... and dry_run` check in single.py
        result = cli_runner.invoke(app, ["single", ".", "-d"])

        assert result.exit_code == 0
        mock_anyio_run.assert_called_once()

    def test_real_exit_propagates(self, cli_runner: CliRunner, mock_cli_deps: dict):
        """
        Test Case 9: (Exception Handling)
        Ensures that if the async runner raises a real error (e.g.,
        Exit(code=1)), the CLI propagates that error.
        """
        mock_anyio_run = mock_cli_deps["anyio_run"]
        mock_anyio_run.side_effect = Exit(code=1)

        # Do NOT pass -d
        result = cli_runner.invoke(app, ["single", "."])

        assert result.exit_code == 1
        mock_anyio_run.assert_called_once()