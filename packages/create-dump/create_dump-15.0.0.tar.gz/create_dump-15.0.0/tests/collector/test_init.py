# tests/collector/test_init.py

"""
Tests for the collector factory in src/create_dump/collector/__init__.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import the function to test
from create_dump.collector import get_collector
# Import dependencies to mock
from create_dump.core import Config


@pytest.fixture
def mock_config() -> Config:
    """Provides a default Config object."""
    return Config()


@pytest.fixture
def mock_collectors(mocker) -> dict[str, MagicMock]:
    """Mocks all collector classes and returns them."""
    # 🐞 FIX: Patch the names where they are *used* (in the __init__ module)
    mock_walk = mocker.patch("create_dump.collector.WalkCollector")
    mock_ls = mocker.patch("create_dump.collector.GitLsCollector")
    mock_diff = mocker.patch("create_dump.collector.GitDiffCollector")

    return {
        "WalkCollector": mock_walk,
        "GitLsCollector": mock_ls,
        "GitDiffCollector": mock_diff,
    }


class TestGetCollector:
    """Tests the get_collector factory function."""

    def test_get_collector_defaults_to_walk(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 1: (Default)
        Ensures WalkCollector is chosen when no flags are present.
        """
        get_collector(config=mock_config)

        mock_collectors["WalkCollector"].assert_called_once()
        mock_collectors["GitLsCollector"].assert_not_called()
        mock_collectors["GitDiffCollector"].assert_not_called()

    def test_get_collector_selects_git_ls(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 2: (git_ls_files flag)
        Ensures GitLsCollector is chosen when git_ls_files=True.
        """
        get_collector(config=mock_config, git_ls_files=True)

        mock_collectors["GitLsCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitDiffCollector"].assert_not_called()

    def test_get_collector_selects_git_diff(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 3: (diff_since flag)
        Ensures GitDiffCollector is chosen when diff_since is provided.
        """
        get_collector(config=mock_config, diff_since="main")

        mock_collectors["GitDiffCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitLsCollector"].assert_not_called()

    def test_get_collector_git_diff_has_precedence(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 4: (Precedence)
        Ensures GitDiffCollector is chosen even if git_ls_files is also True.
        """
        get_collector(
            config=mock_config,
            diff_since="main",
            git_ls_files=True  # This should be ignored
        )

        # GitDiffCollector should be called because it's checked first
        mock_collectors["GitDiffCollector"].assert_called_once()
        mock_collectors["WalkCollector"].assert_not_called()
        mock_collectors["GitLsCollector"].assert_not_called()

    def test_get_collector_passes_common_args(
        self, mock_config: Config, mock_collectors: dict
    ):
        """
        Test Case 5: (Argument Passthrough)
        Ensures all common arguments are passed to the chosen collector.
        """
        root_path = Path("/test/root")
        includes = ["*.py"]
        excludes = ["*.log"]

        get_collector(
            config=mock_config,
            includes=includes,
            excludes=excludes,
            use_gitignore=True,
            root=root_path,
            diff_since="main"  # Choose GitDiffCollector for this test
        )

        # Check that the correct collector was called with all args
        mock_collectors["GitDiffCollector"].assert_called_once_with(
            diff_since="main",
            config=mock_config,
            includes=includes,
            excludes=excludes,
            use_gitignore=True,
            root=root_path
        )