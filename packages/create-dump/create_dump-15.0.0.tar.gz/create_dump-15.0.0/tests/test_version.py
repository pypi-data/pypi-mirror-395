# tests/test_version.py

"""
Tests for version consistency.
"""

import re
import pytest
import toml
from pathlib import Path

def test_version_is_consistent():
    """Test Case 1: The version in pyproject.toml is readable and matches."""
    # Read version directly from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    pyproject_data = toml.load(pyproject_path)
    expected_version = pyproject_data["project"]["version"]

    # Assert that the version in pyproject.toml is the expected one
    assert expected_version == "15.0.0"

def test_version_format_semver():
    """Test Case 2: Version adheres to semantic versioning pattern."""
    # Read version directly from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    pyproject_data = toml.load(pyproject_path)
    __version__ = pyproject_data["project"]["version"]

    # 🐞 FIX: Update regex to be PEP 440-compliant, allowing for .devN suffixes
    semver_pattern = r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.dev\d+)?(?:-(?P<prerelease>[a-zA-Z0-9.-]+))?(?:\+(?P<build>[a-zA-Z0-9.-]+))?$"
    match = re.match(semver_pattern, __version__)
    assert match is not None, f"Version {__version__} does not match semver"
