# tests/test_single.py

"""
Tests for src/create_dump/single.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typer import Exit
import os

import anyio

# Import the function to test
from create_dump.single import run_single

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_deps(mocker):
    """Mocks all external dependencies for run_single."""

    # Mock Orchestrator
    mock_orchestrator_instance = AsyncMock()
    mock_orchestrator_instance.run = AsyncMock()
    mock_orchestrator_class = mocker.patch(
        "create_dump.single.SingleRunOrchestrator",
        return_value=mock_orchestrator_instance
    )

    # Mock Watcher
    mock_watcher_instance = AsyncMock()
    mock_watcher_instance.start = AsyncMock()
    mock_watcher_class = mocker.patch(
        "create_dump.single.FileWatcher",
        return_value=mock_watcher_instance
    )

    # Mock os.chdir
    mock_run_sync = mocker.patch(
        "create_dump.single.anyio.to_thread.run_sync",
        new_callable=AsyncMock
    )

    # Mock styled_print
    mock_styled_print = mocker.patch("create_dump.single.styled_print")

    return {
        "Orchestrator": mock_orchestrator_class,
        "orchestrator_instance": mock_orchestrator_instance,
        "Watcher": mock_watcher_class,
        "watcher_instance": mock_watcher_instance,
        "run_sync": mock_run_sync,
        "styled_print": mock_styled_print,
    }


@pytest.fixture
def default_run_args(test_project) -> dict:
    """Provides a default set of arguments for run_single."""
    return {
        "root": test_project.root,
        "dry_run": False,
        "yes": False,
        "no_toc": False,
        "tree_toc": False,
        "compress": False,
        "format": "md",
        "exclude": "",
        "include": "",
        "max_file_size": None,
        "use_gitignore": True,
        "git_meta": True,
        "progress": True,
        "max_workers": 16,
        "archive": False,
        "archive_all": False,
        "archive_search": False,
        "archive_include_current": True,
        "archive_no_remove": False,
        "archive_keep_latest": True,
        "archive_keep_last": None,
        "archive_clean_root": False,
        "archive_format": "zip",
        "allow_empty": False,
        "metrics_port": 8000,
        "verbose": False,
        "quiet": False,
        "dest": None,
        "watch": False,
        "git_ls_files": False,
        "diff_since": None,
        "scan_secrets": False,
        "hide_secrets": False,
    }


class TestRunSingle:
    """Tests for the run_single 'glue' function."""

    async def test_run_single_default_flow(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 1: (Happy Path)
        Validates the default (non-watch) flow.
        - Calls os.chdir
        - Instantiates Orchestrator with correct args (esp. effective_yes)
        - Calls orchestrator.run()
        - Does NOT instantiate FileWatcher
        """

        # Call the function
        await run_single(**default_run_args)

        # 1. Check os.chdir call
        mock_deps["run_sync"].assert_called_once_with(
            os.chdir, test_project.root
        )

        # 2. Check Orchestrator instantiation
        mock_deps["Orchestrator"].assert_called_once()
        call_kwargs = mock_deps["Orchestrator"].call_args[1]

        assert call_kwargs["root"] == test_project.root
        assert call_kwargs["yes"] is False  # effective_yes = False or False
        assert call_kwargs["git_ls_files"] is False
        assert call_kwargs["hide_secrets"] is False
        # 🐞 FIX: Remove incorrect assertion
        # assert call_kwargs["watch"] is False

        # 3. Check that orchestrator.run() was called
        mock_deps["orchestrator_instance"].run.assert_called_once()

        # 4. Check that FileWatcher was NOT called
        mock_deps["Watcher"].assert_not_called()

    async def test_run_single_watch_flow(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 2: (Watch Path)
        Validates the watch=True flow.
        - Instantiates Orchestrator with effective_yes=True
        - Calls orchestrator.run()
        - Instantiates FileWatcher
        - Calls watcher.start()
        """

        # Enable watch mode, keep yes=False to test effective_yes
        watch_args = default_run_args | {
            "watch": True,
            "yes": False,
            "quiet": False,
        }

        await run_single(**watch_args)

        # 1. Check Orchestrator instantiation
        mock_deps["Orchestrator"].assert_called_once()
        call_kwargs = mock_deps["Orchestrator"].call_args[1]

        # 🐞 FIX: Remove incorrect assertion
        # assert call_kwargs["watch"] is True
        assert call_kwargs["yes"] is True  # effective_yes = False or True

        # 2. Check that orchestrator.run() was called (for the initial run)
        mock_deps["orchestrator_instance"].run.assert_called_once()

        # 3. Check styled_print was called
        mock_deps["styled_print"].assert_any_call(
            "[green]Running initial dump...[/green]"
        )
        mock_deps["styled_print"].assert_any_call(
            f"\n[cyan]Watching for file changes in {test_project.root}... (Press Ctrl+C to stop)[/cyan]"
        )

        # 4. Check FileWatcher was instantiated and started
        mock_deps["Watcher"].assert_called_once_with(
            root=test_project.root,
            dump_func=mock_deps["orchestrator_instance"].run,
            quiet=False
        )
        mock_deps["watcher_instance"].start.assert_called_once()

    async def test_run_single_invalid_root(
        self, test_project, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 3: (Validation)
        Ensures a ValueError is raised if root is not a directory.
        """
        # Create a file to use as the invalid root
        file_path = test_project.root / "file.txt"
        await anyio.Path(file_path).write_text("content")

        invalid_args = default_run_args | {"root": file_path}

        # 🐞 FIX: Reset mock to ignore call from write_text
        mock_deps["run_sync"].reset_mock()

        with pytest.raises(ValueError, match="Invalid root"):
            await run_single(**invalid_args)

        # Ensure no mocks were called *by run_single*
        mock_deps["run_sync"].assert_not_called()
        mock_deps["Orchestrator"].assert_not_called()

    async def test_run_single_dry_run_exit_no_watch(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 4: (Exit Handling - No Watch)
        Ensures a graceful Exit(code=0) from orchestrator.run()
        is caught and handled (returns None).
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=0)

        dry_run_args = default_run_args | {"dry_run": True, "watch": False}

        # This should NOT raise an exception
        await run_single(**dry_run_args)

        mock_deps["orchestrator_instance"].run.assert_called_once()
        mock_deps["Watcher"].assert_not_called()

    async def test_run_single_dry_run_exit_with_watch(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 5: (Exit Handling - Watch)
        Ensures a graceful Exit(code=0) on the *initial* run
        is caught and stops execution (does not start watcher).
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=0)

        dry_run_args = default_run_args | {"dry_run": True, "watch": True}

        # This should NOT raise an exception
        await run_single(**dry_run_args)

        mock_deps["orchestrator_instance"].run.assert_called_once()
        # Ensure the watcher is never started
        mock_deps["Watcher"].assert_not_called()
        mock_deps["watcher_instance"].start.assert_not_called()

    async def test_run_single_real_exit_propagates(
        self, mock_deps: dict, default_run_args: dict
    ):
        """
        Test Case 6: (Exit Handling - Real Exit)
        Ensures a failing Exit(code=1) propagates up.
        """
        mock_deps["orchestrator_instance"].run.side_effect = Exit(code=1)

        fail_args = default_run_args | {"dry_run": False}

        with pytest.raises(Exit) as e:
            await run_single(**fail_args)

        assert e.value.exit_code == 1
        mock_deps["orchestrator_instance"].run.assert_called_once()