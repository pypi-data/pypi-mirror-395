# tests/collector/test_git_ls.py

"""
Tests for src/create_dump/collector/git_ls.py
"""

from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch

# Import the class to test
from create_dump.collector.git_ls import GitLsCollector
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_get_git_ls_files(mocker) -> AsyncMock:
    """Mocks the system call to get_git_ls_files."""
    return mocker.patch(
        "create_dump.collector.git_ls.get_git_ls_files",
        new_callable=AsyncMock
    )


@pytest.fixture
def mock_filter_files(mocker) -> AsyncMock:
    """Mocks the base class's filter_files method."""
    return mocker.patch(
        "create_dump.collector.base.CollectorBase.filter_files",
        new_callable=AsyncMock
    )


class TestGitLsCollector:
    """Tests for the GitLsCollector."""

    async def test_collect_success(
        self,
        test_project,
        default_config: Config,
        mock_get_git_ls_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 1: (Happy Path)
        Validates that:
        1. get_git_ls_files is called.
        2. The raw list is passed to filter_files.
        3. The filtered list is returned.
        """
        raw_files = ["src/main.py", "README.md", "src/ignored.log"]
        filtered_files = ["src/main.py", "README.md"]
        
        mock_get_git_ls_files.return_value = raw_files
        mock_filter_files.return_value = filtered_files
        
        collector = GitLsCollector(config=default_config, root=test_project.root)
        result = await collector.collect()

        # Assertions
        mock_get_git_ls_files.assert_called_once_with(test_project.root)
        mock_filter_files.assert_called_once_with(raw_files)
        assert result == filtered_files

    async def test_collect_no_files_found(
        self,
        test_project,
        default_config: Config,
        mock_get_git_ls_files: AsyncMock,
        mock_filter_files: AsyncMock,
    ):
        """
        Test Case 2: (Empty Result)
        Validates that filter_files is NOT called if git ls-files returns empty.
        """
        mock_get_git_ls_files.return_value = []
        
        collector = GitLsCollector(config=default_config, root=test_project.root)
        result = await collector.collect()

        # Assertions
        mock_get_git_ls_files.assert_called_once_with(test_project.root)
        mock_filter_files.assert_not_called()
        assert result == []