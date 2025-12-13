# tests/collector/test_walk.py

"""
Tests for Phase 2: src/create_dump/collector/walk.py
"""

from __future__ import annotations
import pytest
from pathlib import Path

# Import the class to test
from create_dump.collector.walk import WalkCollector
# Import dependencies needed for testing
from create_dump.core import Config

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


class TestWalkCollector:
    """Groups tests for the WalkCollector class."""

    @pytest.fixture
    async def project_structure(self, test_project):
        """Creates a standard file structure for walk tests."""
        await test_project.create({
            "src/main.py": "print('hello')",
            "src/utils.py": "def helper(): pass",
            "src/data/file.txt": "data",
            "src/__pycache__/cache.pyc": b"\x00",
            "src/logs/app.log": "this is a log",
            "README.md": "# Title",
            ".git/config": "fake git config"
        })

    async def test_collect_recursive(
        self, default_config: Config, test_project, project_structure
    ):
        """
        Tests the _collect_recursive() method directly.
        This method is responsible for walking subdirectories.
        """
        # We explicitly enable use_gitignore=False to ensure
        # only default_excludes (like __pycache__) are used.
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=False
        )

        # Start the recursive collector from the 'src' directory
        collected_files_gen = collector._collect_recursive(Path("src"))
        
        # Collect results into a set for easy comparison
        collected_files = {p.as_posix() async for p in collected_files_gen}

        # Define what we expect to find *within* 'src'
        expected = {
            "src/main.py",
            "src/utils.py",
            "src/data/file.txt",
            # 'src/logs/app.log' is excluded by default_excludes
            # 'src/__pycache__/cache.pyc' is excluded by excluded_dirs
        }

        assert collected_files == expected

    async def test_collect_full(
        self, default_config: Config, test_project, project_structure
    ):
        """
        Tests the main collect() method, which scans the root
        and then calls the recursive collector.
        """
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=False  # Keep test predictable
        )

        # Run the full collection
        files_list = await collector.collect()

        # Expected list is sorted, as per the collector's implementation
        expected = [
            "README.md",
            "src/data/file.txt",
            "src/main.py",
            "src/utils.py",
        ]
        
        assert files_list == expected

    async def test_collect_with_gitignore(
        self, default_config: Config, test_project
    ):
        """
        Tests that the collector correctly uses .gitignore
        when use_gitignore=True.
        """
        await test_project.create({
            "src/main.py": "print('hello')",
            "src/ignored.py": "ignore me",
            "README.md": "# Title",
            ".gitignore": "src/ignored.py"
        })
        
        collector = WalkCollector(
            config=default_config,
            root=test_project.root,
            use_gitignore=True  # Explicitly enable
        )

        files_list = await collector.collect()

        # src/ignored.py should be missing
        expected = [
            "README.md",
            "src/main.py",
        ]
        
        assert files_list == expected
