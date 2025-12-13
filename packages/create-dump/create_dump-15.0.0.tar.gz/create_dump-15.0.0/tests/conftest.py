# tests/conftest.py

"""
Global fixtures for the create-dump test suite.

This file provides common, reusable fixtures (like project setup,
config objects, and CLI runners) to all test modules.
"""

import os  # ⚡ FIXED: Import os for chdir
import pytest
import pytest_asyncio
from pathlib import Path
from typing import Dict, Callable, Awaitable

import anyio
from typer.testing import CliRunner

from create_dump.core import Config
from create_dump.cli.main import app as cli_app

# --- Session-Scoped Fixtures (Setup once) ---

# 🐞 FIX: Change scope from "session" to "function" to prevent test pollution
@pytest.fixture(scope="function")
def default_config() -> Config:
    """
    Provides a default, unaltered Config object.
    Tests should override specific fields as needed.
    """
    return Config()


@pytest.fixture(scope="session")
def cli_runner() -> CliRunner:
    """
    Provides a Typer CliRunner instance for invoking the CLI app.
    """
    return CliRunner()


@pytest.fixture(scope="session")
def cli_app_instance():
    """
    Provides the main Typer application instance.
    """
    return cli_app


# --- Function-Scoped Fixtures (Setup for each test) ---

class TestProjectFactory:
    """
    A factory for creating temporary project structures asynchronously.
    This is provided as a class to be instantiated by the fixture.
    """
    
    def __init__(self, tmp_path: Path):
        self.root = tmp_path
        # Ensure we're using anyio's Path for async I/O
        self.async_root = anyio.Path(self.root)

    async def create(self, structure: Dict[str, str | bytes | None]): # 🐞 FIX: Allow bytes and None
        """
        Creates files and directories from a dictionary structure.
        Keys are relative paths, values are file content.
        
        Example:
        await factory.create({
            "src/main.py": "print('hello')",
            "src/data.bin": b"binary_data",
            "empty_dir/": None
        })
        """
        for rel_path_str, content in structure.items():
            rel_path = Path(rel_path_str)
            full_path = self.async_root / rel_path
            
            # Ensure parent directories exist
            if not await (full_path.parent).exists():
                await full_path.parent.mkdir(parents=True, exist_ok=True)

            # 🐞 FIX: Handle content type
            if rel_path_str.endswith('/') or content is None:
                # It's explicitly a directory
                await full_path.mkdir(parents=True, exist_ok=True)
            elif isinstance(content, bytes):
                # It's binary content
                await full_path.write_bytes(content)
            else:
                # It's a text file
                await full_path.write_text(str(content)) # Cast content to str
 
    def path(self, rel_path: str) -> Path:
        """Helper to get a full pathlib.Path to a file in the test project."""
        return self.root / rel_path

@pytest_asyncio.fixture(scope="function")
async def test_project(tmp_path: Path): # ⚡ REMOVED: Type hint for factory
    """
    Provides an async factory fixture to create test project structures.
    
    Usage in a test:
    
    @pytest.mark.anyio
    async def test_my_feature(test_project: "TestProjectFactory"):
        # ... (docstring same as before) ...
    """
    # Change CWD to the temp path to simulate running from the project root
    # This is critical for collectors and path logic
    
    original_cwd = await anyio.to_thread.run_sync(Path.cwd)
    
    # ⚡ FIXED: Use os.chdir wrapped in run_sync
    await anyio.to_thread.run_sync(os.chdir, tmp_path)
    
    factory = TestProjectFactory(tmp_path)
    
    try:
        yield factory
    finally:
        # Teardown: change CWD back, guaranteed
        # ⚡ FIXED: Use os.chdir wrapped in run_sync
        await anyio.to_thread.run_sync(os.chdir, original_cwd)


