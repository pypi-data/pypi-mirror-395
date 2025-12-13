# tests/test_core.py

"""
Tests for Phase 1: src/create_dump/core.py
"""

from __future__ import annotations
import pytest
from pydantic import ValidationError
from pathlib import Path

from create_dump.core import (
    Config,
    load_config,
    DEFAULT_DUMP_PATTERN
)

# Mark all tests in this file as async-capable
# (needed for the test_project fixture)
pytestmark = pytest.mark.anyio


# --- Test Config Model (Validators) ---

def test_config_defaults(default_config: Config):
    """
    Tests the sane default values of the Config model.
    """
    assert default_config.git_meta is True
    assert default_config.use_gitignore is True
    assert default_config.max_file_size_kb is None
    assert default_config.dest is None
    assert "pyproject.toml" not in default_config.default_excludes
    assert ".git" in default_config.excluded_dirs


def test_config_validator_max_file_size():
    """
    Tests the 'max_file_size_kb' validator.
    """
    # Valid values
    assert Config(max_file_size_kb=1000).max_file_size_kb == 1000
    assert Config(max_file_size_kb=0).max_file_size_kb == 0
    assert Config(max_file_size_kb=None).max_file_size_kb is None
    
    # Invalid value
    with pytest.raises(ValidationError, match="must be non-negative"):
        Config(max_file_size_kb=-1)

def test_config_validator_dest():
    """
    Tests the 'dest' path validator.
    """
    # Valid values
    assert Config(dest="path/to/dumps").dest == Path("path/to/dumps")
    assert Config(dest="/abs/path").dest == Path("/abs/path")
    assert Config(dest=None).dest is None
    
    # Invalid (empty) value should become None
    assert Config(dest="").dest is None

def test_config_validator_dump_pattern():
    """
    Tests the 'dump_pattern' validator to ensure it enforces the
    canonical prefix.
    """
    # Default is valid
    assert Config().dump_pattern == DEFAULT_DUMP_PATTERN
    
    # Custom valid pattern is accepted
    custom_valid = r"my_prefix_all_create_dump_.*\.zip"
    assert Config(dump_pattern=custom_valid).dump_pattern == custom_valid
    
    # Invalid (loose) pattern is reset to default
    invalid_loose = r"some_other_pattern.*\.md"
    assert Config(dump_pattern=invalid_loose).dump_pattern == DEFAULT_DUMP_PATTERN
    
    # Empty pattern is reset to default
    assert Config(dump_pattern="").dump_pattern == DEFAULT_DUMP_PATTERN


# --- Test load_config() ---

async def test_load_config_no_file(test_project):
    """
    Tests that default Config is returned when no config file is found.
    We use test_project to ensure we are in a clean directory.
    """
    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)

    # 🐞 FIX: Robustly check for default values instead of brittle instance equality
    default_config = Config()
    assert config.dest == default_config.dest
    assert config.git_meta == default_config.git_meta
    assert config.max_file_size_kb == default_config.max_file_size_kb

async def test_load_config_from_pyproject(test_project):
    """
    Tests that config is correctly loaded from [tool.create-dump]
    in pyproject.toml.
    """
    await test_project.create({
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
git_meta = false
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    assert config.dest == Path("from_pyproject")
    assert config.git_meta is False
    # Defaults should still be present
    assert config.use_gitignore is True

async def test_load_config_from_dedicated_file(test_project):
    """
    Tests that config is correctly loaded from create_dump.toml.
    """
    await test_project.create({
        "create_dump.toml": """
[tool.create-dump]
dest = "from_dedicated_toml"
max_file_size_kb = 500
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    assert config.dest == Path("from_dedicated_toml")
    assert config.max_file_size_kb == 500
    assert config.git_meta is True # Default

async def test_load_config_precedence(test_project):
    """
    Tests that create_dump.toml takes precedence over pyproject.toml
    (based on the `possible_paths` order in core.py).
    """
    await test_project.create({
        "create_dump.toml": """
[tool.create-dump]
dest = "from_dedicated_toml"
""",
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
"""
    })

    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    config = load_config(_cwd=test_project.root)
    # 'create_dump.toml' is checked first in CWD, so it should win.
    assert config.dest == Path("from_dedicated_toml")

async def test_load_config_with_explicit_path(test_project):
    """
    Tests that loading from an explicit path works and
    ignores other config files.
    """
    await test_project.create({
        "config/my_config.toml": """
[tool.create-dump]
dest = "from_explicit_path"
""",
        "pyproject.toml": """
[tool.create-dump]
dest = "from_pyproject"
"""
    })
    
    explicit_path = test_project.path("config/my_config.toml")
    
    # 🐞 FIX: Pass the test_project's root as the explicit CWD
    # The explicit `path` argument will be used first, but we still
    # pass _cwd to be consistent and safe.
    config = load_config(path=explicit_path, _cwd=test_project.root)

    assert config.dest == Path("from_explicit_path")


async def test_load_config_with_profile(test_project):
    """
    Tests that a config profile correctly overrides base settings.
    """
    await test_project.create({
        "pyproject.toml": """
[tool.create-dump]
git_meta = true
[tool.create-dump.profile.ci]
git_meta = false
"""
    })

    config = load_config(_cwd=test_project.root, profile="ci")
    assert config.git_meta is False


async def test_load_config_with_nonexistent_profile(test_project, mocker):
    """
    Tests that a warning is logged when a nonexistent profile is requested.
    """
    await test_project.create({
        "pyproject.toml": """
[tool.create-dump]
git_meta = true
"""
    })

    mock_logger_warning = mocker.patch("create_dump.core.logger.warning")
    config = load_config(_cwd=test_project.root, profile="nonexistent")

    assert config.git_meta is True
    mock_logger_warning.assert_called_once_with(
        "Config profile not found, using base", profile="nonexistent"
    )


async def test_load_config_profile_merges_not_replaces(test_project):
    """
    Tests that a profile with one setting doesn't nullify other base settings.
    """
    await test_project.create({
        "pyproject.toml": """
[tool.create-dump]
git_meta = true
dest = "dumps"
[tool.create-dump.profile.ci]
git_meta = false
"""
    })

    config = load_config(_cwd=test_project.root, profile="ci")
    assert config.git_meta is False
    assert config.dest == Path("dumps")


def test_config_custom_secret_patterns():
    """
    Tests that the Config model correctly stores custom secret patterns.
    """
    patterns = ["API_KEY = '.*'"]
    config = Config(custom_secret_patterns=patterns)
    assert config.custom_secret_patterns == patterns
