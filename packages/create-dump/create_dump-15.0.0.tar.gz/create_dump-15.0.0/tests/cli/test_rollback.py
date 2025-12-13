# tests/cli/test_rollback.py

"""
Comprehensive test suite for src/create_dump/cli/rollback.py.
This directly addresses the P0 coverage plan to unblock CI.
"""

from __future__ import annotations
import pytest
from pathlib import Path
# 🐞 FIX: Import ANY for flexible mock call assertion
from unittest.mock import AsyncMock, MagicMock, patch, ANY
import hashlib

import anyio
from typer.testing import CliRunner
from typer import Exit

# Import the main app to test the command
from create_dump.cli.main import app

# Import the module to test its internal helpers
from create_dump.cli import rollback as rollback_module
from create_dump.rollback.engine import RollbackEngine

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provides a Typer CliRunner instance."""
    return CliRunner()


@pytest.fixture
def mock_deps(mocker):
    """
    Mocks all downstream async dependencies called by the
    `async_rollback` function.
    """
    # Mock the helper functions in the module
    mock_find = mocker.patch(
        "create_dump.cli.rollback._find_most_recent_dump",
        new_callable=AsyncMock
    )
    mock_verify = mocker.patch(
        "create_dump.cli.rollback._verify_integrity",
        new_callable=AsyncMock
    )

    # Mock the downstream classes
    mock_engine_instance = AsyncMock(spec=RollbackEngine)
    mock_engine_instance.rehydrate = AsyncMock(return_value=[Path("file1.py")]) # Default success
    mock_engine_class = mocker.patch(
        "create_dump.cli.rollback.RollbackEngine",
        return_value=mock_engine_instance
    )

    mock_parser_class = mocker.patch("create_dump.cli.rollback.MarkdownParser")

    # Mock the sync confirm function run in a thread
    mock_confirm_thread = mocker.patch(
        "create_dump.cli.rollback.anyio.to_thread.run_sync",
        return_value=True # Default to "yes"
    )

    # Mock logging/printing
    mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")
    mock_logger = mocker.patch("create_dump.cli.rollback.logger")

    # Mock anyio.Path.exists for the --file check
    mock_path_exists = mocker.patch("anyio.Path.exists", new_callable=AsyncMock, return_value=True)

    return {
        "find": mock_find,
        "verify": mock_verify,
        "engine_class": mock_engine_class,
        "engine_instance": mock_engine_instance,
        "parser_class": mock_parser_class,
        "confirm": mock_confirm_thread,
        "styled_print": mock_styled_print,
        "logger": mock_logger,
        "path_exists": mock_path_exists,
    }


class TestCliRollbackCommand:
    """Tests the `rollback` command wiring and logic flow."""

    def test_happy_path_find_latest(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 1: Happy Path (Find Latest)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 0
        mock_deps["find"].assert_called_once_with(test_project.root)
        mock_deps["verify"].assert_called_once_with(mock_dump_path)
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[green]Integrity verified.[/green]")
        mock_deps["styled_print"].assert_any_call(
            f"[green]✅ Rollback complete.[/green] 1 files created in [blue]{test_project.root.resolve() / 'all_create_dump_rollbacks' / 'dump_2025'}[/blue]"
        )

    def test_happy_path_with_file(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 2: Happy Path (--file)."""
        mock_dump_path = test_project.path("mydump.md")
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--file", str(mock_dump_path)])

        assert result.exit_code == 0
        mock_deps["find"].assert_not_called()
        mock_deps["path_exists"].assert_called_once()
        mock_deps["verify"].assert_called_once_with(mock_dump_path)
        mock_deps["engine_instance"].rehydrate.assert_called_once()

    def test_dry_run(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 3: Dry Run."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--dry-run"])

        assert result.exit_code == 0
        mock_deps["engine_class"].assert_called_with(
            test_project.root.resolve() / 'all_create_dump_rollbacks' / 'dump_2025',
            dry_run=True
        )
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[green]✅ Dry run complete.[/green] Would have created 1 files.")

    def test_user_cancellation(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 4: User Cancellation."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["confirm"].return_value = False  # User says "no"

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        # 🐞 FIX: typer.Exit() on user cancel is exit_code 1
        assert result.exit_code == 1
        
        # 🐞 FIX: Assert *any* call, because conftest.py also uses run_sync
        mock_deps["confirm"].assert_any_call(rollback_module.confirm, ANY)
        
        mock_deps["engine_instance"].rehydrate.assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Rollback cancelled by user.[/red]")

    def test_failure_file_not_found(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 5: Failure (File Not Found)."""
        mock_deps["path_exists"].return_value = False

        result = cli_runner.invoke(app, ["rollback", str(test_project.root), "--file", "nonexistent.md"])

        assert result.exit_code == 1
        mock_deps["path_exists"].assert_called_once()
        mock_deps["verify"].assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] Specified file not found: nonexistent.md")

    def test_failure_no_dumps_found(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 6: Failure (No Dumps Found)."""
        mock_deps["find"].return_value = None

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["find"].assert_called_once()
        mock_deps["verify"].assert_not_called()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] No `*_all_create_dump_*.md` files found in this directory.")

    def test_failure_integrity_check(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 7: Failure (Integrity Check)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = False  # Verification fails

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["find"].assert_called_once()
        mock_deps["verify"].assert_called_once()
        mock_deps["engine_instance"].rehydrate.assert_not_called()

    def test_failure_engine_error(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 10: Failure (Engine Error - ValueError)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["engine_instance"].rehydrate.side_effect = ValueError("Engine Failed")

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["styled_print"].assert_any_call("[red]Error:[/red] Engine Failed")

    def test_failure_unexpected_error(self, cli_runner: CliRunner, mock_deps: dict, test_project):
        """Test Case 11: Failure (Unexpected Error)."""
        mock_dump_path = test_project.path("dump_2025.md")
        mock_deps["find"].return_value = mock_dump_path
        mock_deps["verify"].return_value = True
        mock_deps["engine_instance"].rehydrate.side_effect = TypeError("Unexpected")

        result = cli_runner.invoke(app, ["rollback", str(test_project.root)])

        assert result.exit_code == 1
        mock_deps["engine_instance"].rehydrate.assert_called_once()
        mock_deps["logger"].error.assert_any_call("Unhandled rollback error", error="Unexpected", exc_info=True)
        mock_deps["styled_print"].assert_any_call("[red]An unexpected error occurred:[/red] Unexpected")


class TestRollbackHelpers:
    """Tests the async helper functions in rollback.py."""

    async def test_calculate_sha256(self, test_project):
        """Tests the SHA256 calculation."""
        content = "hello world"
        expected_hash = hashlib.sha256(content.encode()).hexdigest()

        await test_project.create({"file.txt": content})
        file_path = test_project.async_root / "file.txt"

        hash_val = await rollback_module._calculate_sha256(file_path)

        assert hash_val == expected_hash

    async def test_find_most_recent_dump_success(self, test_project):
        """Tests finding the latest file by mtime."""
        await test_project.create({"dump_old_all_create_dump_20240101_000000.md": "old"})
        await anyio.sleep(0.02) # Ensure mtime difference
        await test_project.create({"dump_new_all_create_dump_20250101_000000.md": "new"})

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is not None
        assert latest_file.name == "dump_new_all_create_dump_20250101_000000.md"

    async def test_find_most_recent_dump_empty(self, test_project):
        """Tests that None is returned when no dumps are found."""
        await test_project.create({"not_a_dump.txt": "content"})

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is None

    async def test_find_most_recent_dump_stat_error(self, test_project, mocker):
        """Tests that an OSError during stat is caught and logged."""
        await test_project.create({"dump_file_all_create_dump_20250101_000000.md": "content"})

        mock_logger = mocker.patch("create_dump.cli.rollback.logger")

        # Mock Path.stat to raise an error
        mock_stat = AsyncMock(side_effect=OSError("Permission denied"))
        mocker.patch.object(anyio.Path, "stat", mock_stat)

        latest_file = await rollback_module._find_most_recent_dump(test_project.root)

        assert latest_file is None
        mock_logger.warning.assert_called_once()
        assert "Could not stat file" in mock_logger.warning.call_args[0][0]

    async def test_verify_integrity_success(self, test_project):
        """Tests successful integrity verification."""
        content = "test content"
        hash_val = hashlib.sha256(content.encode()).hexdigest()

        await test_project.create({
            "test_all_create_dump_20250101_000000.md": content,
            "test_all_create_dump_20250101_000000.sha256": f"{hash_val}  test_all_create_dump_20250101_000000.md"
        })

        md_path = test_project.path("test_all_create_dump_20250101_000000.md")
        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is True

    async def test_verify_integrity_sha_missing(self, test_project, mocker):
        """Test Case 8: Failure (SHA Missing)."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({"dump.md": "content"})
        md_path = test_project.path("dump.md")

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with("Integrity check failed: Missing checksum file for dump.md")
        mock_styled_print.assert_any_call("[red]Error:[/red] Missing checksum file: [blue]dump.sha256[/blue]")

    async def test_verify_integrity_sha_mismatch(self, test_project, mocker):
        """Test Case 9: Failure (SHA Mismatch)."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({
            "dump.md": "content",
            "dump.sha256": "badhash  dump.md"
        })
        md_path = test_project.path("dump.md")

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with(
            "Integrity check FAILED: Hashes do not match",
            file="dump.md",
            expected="badhash",
            actual=hashlib.sha256(b"content").hexdigest()
        )
        mock_styled_print.assert_any_call("[red]Error: Integrity check FAILED. File is corrupt.[/red]")

    async def test_verify_integrity_read_error(self, test_project, mocker):
        """Tests that an exception during hash calculation is caught."""
        # 🐞 FIX: Add local mocks for logger and styled_print
        mock_logger = mocker.patch("create_dump.cli.rollback.logger")
        mock_styled_print = mocker.patch("create_dump.cli.rollback.styled_print")

        await test_project.create({
            "dump.md": "content",
            "dump.sha256": "hash  dump.md"
        })
        md_path = test_project.path("dump.md")

        # Mock _calculate_sha256 to raise an error
        mocker.patch(
            "create_dump.cli.rollback._calculate_sha256",
            side_effect=Exception("Read Error")
        )

        is_valid = await rollback_module._verify_integrity(md_path)

        assert is_valid is False
        # 🐞 FIX: Use local mock variable
        mock_logger.error.assert_called_once_with("Integrity check error: Read Error", file="dump.md")
        mock_styled_print.assert_any_call("[red]Error during integrity check:[/red] Read Error")