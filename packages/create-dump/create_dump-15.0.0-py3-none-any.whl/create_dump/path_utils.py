# src/create_dump/path_utils.py

"""Shared utilities for path safety, discovery, and user confirmation."""

from __future__ import annotations

import logging
import re
from pathlib import Path
# ⚡ REFACTOR: Import AsyncGenerator
from typing import List, AsyncGenerator

import anyio  # ⚡ REFACTOR: Import anyio
from .logging import logger  # ⚡ REFACTOR: Import from logging

# ⚡ REFACTOR: Removed safe_is_within and find_matching_files
__all__ = ["safe_is_within", "confirm", "find_matching_files"]


# ⚡ REFACTOR: Removed synchronous safe_is_within function


# ⚡ NEW: Async version of safe_is_within for anyio.Path
async def safe_is_within(path: anyio.Path, root: anyio.Path) -> bool:
    """
    Async check if path is safely within root (relative/escape-proof).
    Handles anyio.Path objects by awaiting .resolve().
    """
    try:
        # 1. Await resolution for both paths
        resolved_path = await path.resolve()
        resolved_root = await root.resolve()
        
        # 2. Perform the check on the resulting sync pathlib.Path objects
        return resolved_path.is_relative_to(resolved_root)
    except AttributeError:
        # Fallback for Python < 3.9
        resolved_path = await path.resolve()
        resolved_root = await root.resolve()
        return str(resolved_path).startswith(str(resolved_root) + "/")


# ⚡ REFACTOR: Removed synchronous find_matching_files function


# ⚡ REFACTOR: New async version of find_matching_files
async def find_matching_files(root: Path, regex: str) -> AsyncGenerator[Path, None]:
    """Async glob files matching regex within root."""
    pattern = re.compile(regex)
    anyio_root = anyio.Path(root)
    # ⚡ REFACTOR: Yield paths directly instead of building a list
    async for p in anyio_root.rglob("*"):
        if pattern.search(p.name):
            yield Path(p)  # Yield as pathlib.Path


def confirm(prompt: str) -> bool:
    """Prompt user for yes/no; handles interrupt gracefully."""
    try:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
    except KeyboardInterrupt:
        print()
        return False
    return ans in ("y", "yes")