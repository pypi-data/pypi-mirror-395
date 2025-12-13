# tests/archive/test_core.py

"""
Tests for Phase 1: src/create_dump/archive/core.py
"""

from __future__ import annotations
import pytest
from datetime import datetime
from pathlib import Path
import anyio

from create_dump.archive.core import (
    extract_group_prefix,
    extract_timestamp,
    _safe_arcname
)

# Mark all tests in this file as async-capable
# (needed for the test_project fixture)
pytestmark = pytest.mark.anyio


# --- Test extract_group_prefix() ---

@pytest.mark.parametrize(
    "filename, expected_prefix",
    [
        # Standard cases
        ("src_all_create_dump_20250101_120000.md", "src"),
        ("tests_all_create_dump_20250101_120000.md", "tests"),
        ("my-group-1_all_create_dump_20250101_120000.md", "my-group-1"),

        # Non-matching cases
        ("default_all_create_dump_20250101_120000.zip", None), # Not .md
        ("all_create_dump_20250101_120000.md", None), # No prefix
        ("_all_create_dump_20250101_120000.md", None), # No prefix
        ("src_all_create_dump_20250101_120000.txt", None), # Not .md
        ("src_all_create_dump.md", None), # No timestamp
        ("src_all_create_dump_20250101_1200.md", None), # Invalid timestamp

        # Invalid prefix characters (should not match)
        ("src/path_all_create_dump_20250101_120000.md", None),
        ("src.._all_create_dump_20250101_120000.md", None),
    ]
)
def test_extract_group_prefix(filename: str, expected_prefix: str | None):
    """
    Tests the regex logic for extracting group prefixes from dump filenames.
    """
    assert extract_group_prefix(filename) == expected_prefix


# --- Test extract_timestamp() ---

@pytest.mark.parametrize(
    "filename, expected_dt",
    [
        # Standard cases
        ("src_all_create_dump_20250101_123005.md", datetime(2025, 1, 1, 12, 30, 5)),
        ("archive_20241225_090000.zip", datetime(2024, 12, 25, 9, 0, 0)),
        ("prefix_with_numbers_123_20250202_030405.txt", datetime(2025, 2, 2, 3, 4, 5)),

        # Non-matching cases
        ("no_timestamp.md", datetime.min),
        ("invalid_timestamp_20250101_1230.zip", datetime.min),
        ("malformed_20259999_999999.zip", datetime.min),
    ]
)
def test_extract_timestamp(filename: str, expected_dt: datetime):
    """
    Tests the regex logic for extracting timestamps from various filenames.
    """
    assert extract_timestamp(filename) == expected_dt


# --- Test _safe_arcname() ---

async def test_safe_arcname_success(test_project):
    """
    Tests that a valid file path is correctly made relative.
    """
    await test_project.create({
        "src/main.py": "pass"
    })
    root = test_project.root
    file_path = test_project.path("src/main.py")

    arcname = _safe_arcname(file_path, root)
    assert arcname == "src/main.py"

async def test_safe_arcname_raises_for_directory(test_project):
    """
    Tests that _safe_arcname() raises a ValueError if the path is a
    directory, not a file.
    """
    # ⚡ FIX: Use `create({"src/mydir": None})` to create a directory
    await test_project.create({"src/mydir": None})
    root = test_project.root
    dir_path = test_project.path("src/mydir")

    with pytest.raises(ValueError, match="not a file"):
        _safe_arcname(dir_path, root)

async def test_safe_arcname_raises_for_traversal(test_project):
    """
    Tests that _safe_arcname() raises a ValueError for path traversal.
    This is the core "Zip-Slip" security test.
    """
    root = test_project.root

    # We don't even need to create the file, just the path object
    # 1. Simple traversal
    malicious_path_1 = root / "../secret.txt"
    # 2. Complex traversal
    malicious_path_2 = root / "src/../../etc/passwd"

    # We test against the *unresolved* path, as `relative_to`
    # will catch this.
    with pytest.raises(ValueError, match="Invalid arcname with traversal"):
        _safe_arcname(malicious_path_1, root)

    with pytest.raises(ValueError, match="Invalid arcname with traversal"):
        _safe_arcname(malicious_path_2, root)

async def test_safe_arcname_raises_for_absolute(test_project):
    """
    Tests that _safe_arcname() raises a ValueError for absolute paths.
    """
    # ⚡ FIX: This test was logically flawed.
    # We must test a path that is *actually* outside the root,
    # not just an absolute path that points *inside* the root.
    root = test_project.root
    
    # Create a dummy external file to get a real, absolute, external path
    external_path = Path("/tmp/external_test_file.txt")
    await anyio.Path(external_path).write_text("external")

    # `relative_to` will fail because /tmp/external_test_file.txt
    # is not in the subpath of our test_project root.
    with pytest.raises(ValueError, match="is not in the subpath"):
        _safe_arcname(external_path, root)

    # Cleanup
    await anyio.Path(external_path).unlink(missing_ok=True)


