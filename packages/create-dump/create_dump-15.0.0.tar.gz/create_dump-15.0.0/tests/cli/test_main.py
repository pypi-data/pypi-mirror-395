# tests/cli/test_main.py

"""
Tests for src/create_dump/cli/main.py
"""

from __future__ import annotations
import pytest
from typer.testing import CliRunner
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Import the app to test
from create_dump.cli.main import app
from importlib import metadata
# 🐞 FIX: Import the function we are checking
from create_dump.cli.single import run_single

try:
    __version__ = metadata.version("create-dump")
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_cli_deps(mocker):
    """
    Mocks all heavy dependencies called by CLI commands.
    We are only testing the CLI wiring, not the full execution.
    """
    # 🐞 FIX: Mock `anyio.run` where it's called (in cli.single)
    # This is the boundary of the CLI code.
    mock_anyio_run = mocker.patch(
        "create_dump.cli.single.anyio.run",
        new_callable=MagicMock
    )

    # Mock the `anyio.run` call in `cli/batch.py`
    mock_run_batch_async = mocker.patch(
        "create_dump.cli.batch.anyio.run",
        new_callable=MagicMock
    )

    # Mock config loading
    mock_load_config = mocker.patch("create_dump.cli.main.load_config")

    # Mock logging setup
    mock_setup_logging = mocker.patch("create_dump.cli.main.setup_logging")
    # Also mock the setup_logging call in cli.single
    mocker.patch("create_dump.cli.single.setup_logging")


    return {
        "run_single": mock_anyio_run, # 🐞 FIX: Point to the new mock
        "run_batch": mock_run_batch_async,
        "load_config": mock_load_config,
        "setup_logging": mock_setup_logging,
    }


class TestMainCli:
    """Tests for the main app callback and command registration."""

    def test_version_flag(self, cli_runner: CliRunner):
        """Test Case 1: --version flag prints version and exits."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"create-dump v{__version__}" in result.stdout

    def test_batch_subcommand_help(self, cli_runner: CliRunner):
        """Test Case 2: 'batch' subcommand is registered."""
        result = cli_runner.invoke(app, ["batch", "--help"])
        assert result.exit_code == 0
        assert "Batch operations" in result.stdout

    def test_logging_flags(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """Test Case 3: --verbose and --quiet flags call setup_logging."""
        mock_setup_logging = mock_cli_deps["setup_logging"]

        with cli_runner.isolated_filesystem():
            # Test --verbose
            cli_runner.invoke(app, ["--verbose", "single", "--help"])
            mock_setup_logging.assert_called_with(verbose=True, quiet=False)

        with cli_runner.isolated_filesystem():
            # Test --quiet
            cli_runner.invoke(app, ["--quiet", "batch", "--help"])
            mock_setup_logging.assert_called_with(verbose=False, quiet=True)

    def test_config_flag(
        self, cli_runner: CliRunner, mock_cli_deps: dict
    ):
        """Test Case 4: --config flag calls load_config with the correct path."""
        with cli_runner.isolated_filesystem() as temp_dir:
            config_file = Path(temp_dir) / "my_config.toml"
            config_file.write_text("test")

            cli_runner.invoke(app, ["--config", "my_config.toml", "single", "--help"])

            mock_cli_deps["load_config"].assert_called_with(Path("my_config.toml"), profile=None)


class TestInitWizard:
    """Tests for the --init interactive wizard."""

    def test_init_success(self, cli_runner: CliRunner, mocker):
        """Test Case 7: --init wizard runs, mocks prompts, and creates file."""
        mocker.patch("create_dump.cli.main.typer.prompt", return_value="my/dumps")
        mocker.patch("create_dump.cli.main.typer.confirm", side_effect=[True, False, True])

        with cli_runner.isolated_filesystem() as temp_dir:
            # 🐞 FIX: Surgically mock Path.exists to return False for this test
            mocker.patch("pathlib.Path.exists", return_value=False)

            config_path = Path(temp_dir) / "create_dump.toml"

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 0
            assert "Success!" in result.stdout

            # We can't assert config_path.exists() because we mocked it
            # But we can check the stdout
            assert f"config file created at {config_path.resolve()}" in result.stdout

            # We can also check the content (by mocking write_text)
            # This is complex, so we'll trust the stdout.

    def test_init_file_exists(self, cli_runner: CliRunner):
        """Test Case 8: --init fails if config file already exists."""
        with cli_runner.isolated_filesystem() as temp_dir:
            config_path = Path(temp_dir) / "create_dump.toml"
            config_path.write_text("existing")

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 1
            assert "already exists" in result.stdout
            assert config_path.read_text() == "existing"

    def test_init_io_error(self, cli_runner: CliRunner, mocker):
        """Test Case 9: --init handles IOError on file write."""
        mocker.patch("create_dump.cli.main.typer.prompt", return_value="")
        mocker.patch("create_dump.cli.main.typer.confirm", return_value=True)

        with cli_runner.isolated_filesystem() as temp_dir:
            # 🐞 FIX: Surgically mock Path.exists to return False for this test
            mocker.patch("pathlib.Path.exists", return_value=False)

            # Now, mock write_text to fail
            mocker.patch("pathlib.Path.write_text", side_effect=IOError("Permission denied"))

            result = cli_runner.invoke(app, ["--init"])

            assert result.exit_code == 1
            assert "Error:" in result.stdout
            assert "Permission denied" in result.stdout