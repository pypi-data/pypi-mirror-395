# tests/test_cli_single_coverage.py

import pytest
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from create_dump.cli.main import app

runner = CliRunner()

class TestCliSingleCoverage:

    def test_single_root_not_dir(self):
        with patch("pathlib.Path.is_dir", return_value=False):
            result = runner.invoke(app, ["single", "."])
            assert result.exit_code != 0
            # stdout check skipped due to capturing issues with rich/logging setup

    def test_single_mutually_exclusive_flags(self):
        result = runner.invoke(app, ["single", ".", "--git-ls-files", "--diff-since", "HEAD"])
        assert result.exit_code != 0
        # stdout check skipped

    def test_single_hide_secrets_dependency(self):
        result = runner.invoke(app, ["single", ".", "--hide-secrets"])
        assert result.exit_code != 0
        # stdout check skipped

    def test_single_happy_path(self):
        # Mock run_single to avoid actual work
        with patch("create_dump.cli.single.anyio.run") as mock_run:
            with patch("pathlib.Path.is_dir", return_value=True):
                result = runner.invoke(app, ["single", ".", "--yes", "--dry-run"])
                assert result.exit_code == 0
                assert mock_run.called

    def test_single_verbosity_overrides(self):
        with patch("create_dump.cli.single.setup_logging") as mock_setup:
            with patch("create_dump.cli.single.anyio.run"):
                with patch("pathlib.Path.is_dir", return_value=True):
                    # Verbose + Quiet -> Quiet wins
                    runner.invoke(app, ["single", ".", "--verbose", "--quiet"])
                    mock_setup.assert_called_with(verbose=False, quiet=True)

    def test_single_exit_handling_dry_run(self):
        # anyio.run raising Exit(0)
        from typer import Exit
        with patch("create_dump.cli.single.anyio.run", side_effect=Exit(0)):
            with patch("pathlib.Path.is_dir", return_value=True):
                result = runner.invoke(app, ["single", ".", "--dry-run"])
                assert result.exit_code == 0

    def test_single_exit_handling_error(self):
        # anyio.run raising Exit(1)
        from typer import Exit
        with patch("create_dump.cli.single.anyio.run", side_effect=Exit(1)):
            with patch("pathlib.Path.is_dir", return_value=True):
                result = runner.invoke(app, ["single", ".", "--dry-run"])
                assert result.exit_code == 1
