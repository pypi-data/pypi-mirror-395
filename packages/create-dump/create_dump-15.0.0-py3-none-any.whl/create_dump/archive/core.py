# src/create_dump/archive/core.py

"""Core utilities and exceptions for the archive components."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..logging import logger  # ⚡ FIX: Added missing logger import

class ArchiveError(ValueError):
    """Custom error for archive operations."""


def extract_group_prefix(filename: str) -> Optional[str]:
    """Extract group prefix from filename, e.g., 'tests' from 'tests_all_create_dump_*.md'."""
    match = re.match(r'^(.+?)_all_create_dump_\d{8}_\d{6}\.md$', filename)
    if match:
        group = match.group(1)
        if re.match(r'^[a-zA-Z0-9_-]+$', group):
            return group
    return None


def extract_timestamp(filename: str) -> datetime:
    """Extract timestamp from filename (e.g., _20251028_041318)."""
    match = re.search(r'_(\d{8}_\d{6})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
        except ValueError:
            logger.warning("Malformed timestamp in filename: %s", filename)
    return datetime.min


def _safe_arcname(path: Path, root: Path) -> str:
    """Sanitize arcname to prevent zip-slip."""
    try:
        rel = path.relative_to(root).as_posix()
        if ".." in rel.split("/") or rel.startswith("/"):
            raise ValueError(f"Invalid arcname with traversal: {rel}")
        if not path.is_file():
            raise ValueError(f"Invalid arcname: not a file - {path}")
        return rel
    except ValueError as e:
        if "is not in the subpath" in str(e):
            raise ValueError(f"Invalid arcname: {str(e)}") from e
        logger.warning("Skipping unsafe path for ZIP: %s (%s)", path, e)
        raise