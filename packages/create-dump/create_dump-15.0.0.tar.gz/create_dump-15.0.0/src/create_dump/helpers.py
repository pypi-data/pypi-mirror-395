# src/create_dump/helpers.py

"""Stateless, general-purpose helper functions."""

from __future__ import annotations

import os
import re
import uuid
from os import scandir  # Explicit import
from pathlib import Path
from typing import Dict, List

import anyio  # ⚡ NEW: Import for async path operations
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError

from .logging import logger

# Constants
CHUNK_SIZE = 8192
BINARY_THRESHOLD = 0.05


def slugify(path: str) -> str:
    """Convert path to safe anchor slug."""
    p = Path(path)
    clean = p.as_posix().lstrip("./").lower()
    return re.sub(r"[^a-z0-9]+", "-", clean).strip("-")


def get_language(filename: str) -> str:
    """Detect file language from extension/basename."""
    # ⚡ FIX: Strip leading '.' from basename for special file matching
    basename = Path(filename).name.lower().lstrip('.')
    
    if basename == "dockerfile":
        return "dockerfile"
    if basename == "dockerignore":
        return "ini"
    
    ext = Path(filename).suffix.lstrip(".").lower()
    mapping: Dict[str, str] = {
        "py": "python", "sh": "bash", "yml": "yaml", "yaml": "yaml",
        "ini": "ini", "cfg": "ini", "toml": "toml", "json": "json",
        "txt": "text", "md": "markdown", "js": "javascript", "ts": "typescript",
        "html": "html", "css": "css", "jsx": "jsx", "tsx": "tsx", "vue": "vue",
        "sql": "sql", "go": "go", "rs": "rust", "java": "java", "c": "c",
        "cpp": "cpp", "rb": "ruby", "php": "php", "pl": "perl", "scala": "scala",
        "kt": "kotlin", "swift": "swift", "dart": "dart", "csv": "csv",
        "xml": "xml", "r": "r", "jl": "julia", "ex": "elixir", "exs": "elixir",
        "lua": "lua", "hs": "haskell", "ml": "ocaml", "scm": "scheme",
        "zig": "zig", "carbon": "carbon", "mojo": "mojo", "verse": "verse",
    }
    return mapping.get(ext, "text")


# ⚡ REFACTOR: Removed synchronous is_text_file function


# ⚡ NEW: Async version of is_text_file
async def is_text_file(path: anyio.Path) -> bool:
    """Async Heuristic: Check if file is text-based."""
    try:
        async with await path.open("rb") as f:
            chunk = await f.read(CHUNK_SIZE)
            if len(chunk) == 0:
                return True
            if b"\x00" in chunk:
                return False
            decoded = chunk.decode("utf-8", errors="replace")
            invalid_ratio = decoded.count("\ufffd") / len(decoded)
            return invalid_ratio <= BINARY_THRESHOLD
    except (OSError, UnicodeDecodeError):
        return False


def parse_patterns(patterns: List[str]) -> PathSpec:
    """Parse glob patterns safely."""
    try:
        return PathSpec.from_lines("gitwildmatch", patterns)
    except GitWildMatchPatternError as e:
        logger.error("Invalid pattern", patterns=patterns, error=str(e))
        raise ValueError(f"Invalid patterns: {patterns}") from e


def _unique_path(path: Path) -> Path:
    """Generate unique path with UUID suffix."""
    if not os.path.exists(path):
        return path

    stem, suffix = path.stem, path.suffix
    counter = 0
    while True:
        u = uuid.uuid4()
        hex_attr = getattr(u, "hex", "")
        hex_val = hex_attr() if callable(hex_attr) else hex_attr
        hex8 = str(hex_val)[:8]

        if counter == 0:
            unique_stem = f"{stem}_{hex8}"
        else:
            unique_stem = f"{stem}_{counter}_{hex8}"

        candidate = path.parent / f"{unique_stem}{suffix}"
        if not Path.exists(candidate):
            return candidate
        counter += 1