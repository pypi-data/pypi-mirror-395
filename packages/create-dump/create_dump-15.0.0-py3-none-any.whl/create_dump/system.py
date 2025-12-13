# src/create_dump/system.py

"""Handles system-level interactions: signals, subprocesses, cleanup."""

from __future__ import annotations

import atexit
import os
import signal
import subprocess
import sys
import tempfile
from contextlib import ExitStack
from pathlib import Path
# ⚡ REFACTOR: Import List and Tuple
from typing import Any, Optional, List, Tuple
import asyncio  # ⚡ NEW: Import asyncio

import tenacity
# ⚡ FIX: Removed all deprecated anyio subprocess imports

from .core import GitMeta
from .logging import logger

# Constants
DEFAULT_MAX_WORKERS = min(16, (os.cpu_count() or 4) * 2)

# Globals for cleanup (thread-safe via ExitStack)
_cleanup_stack = ExitStack()
_temp_dir: Optional[tempfile.TemporaryDirectory] = None


class CleanupHandler:
    """Graceful shutdown on signals."""

    def __init__(self):
        signal.signal(signal.SIGINT, self._handler)
        signal.signal(signal.SIGTERM, self._handler)
        atexit.register(self._cleanup)

    def _handler(self, signum: int, frame: Any) -> None:
        logger.info("Shutdown signal received", signal=signum)
        self._cleanup()
        sys.exit(130 if signum == signal.SIGINT else 143)

    def _cleanup(self) -> None:
        global _temp_dir
        if _temp_dir:
            _temp_dir.cleanup()
        _cleanup_stack.close()


handler = CleanupHandler()  # Global handler


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
def get_git_meta(root: Path) -> Optional[GitMeta]:
    """Fetch git metadata with timeout."""
    try:
        cmd_branch = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        cmd_commit = ["git", "rev-parse", "--short", "HEAD"]
        branch = (
            subprocess.check_output(
                cmd_branch, cwd=root, stderr=subprocess.DEVNULL, timeout=10
            )
            .decode()
            .strip()
        )
        commit = (
            subprocess.check_output(
                cmd_commit, cwd=root, stderr=subprocess.DEVNULL, timeout=10
            )
            .decode()
            .strip()
        )
        return GitMeta(branch=branch, commit=commit)
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        logger.debug("Git meta unavailable", root=root)
        return None


# ⚡ NEW: Internal helper for running asyncio subprocesses
async def _run_async_cmd(cmd: List[str], cwd: Path) -> Tuple[str, str, int]:
    """
    Run a command asynchronously and return (stdout, stderr, returncode).
    """
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=cwd,  # ⚡ Run in the specified root directory
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout_bytes, stderr_bytes = await proc.communicate()

    return (
        stdout_bytes.decode().strip(),
        stderr_bytes.decode().strip(),
        proc.returncode,
    )


# ⚡ REFACTOR: Rewritten to use asyncio.subprocess
async def get_git_ls_files(root: Path) -> List[str]:
    """Run 'git ls-files' asynchronously and return the file list."""
    cmd = ["git", "ls-files", "-co", "--exclude-standard"]
    try:
        stdout, stderr, code = await _run_async_cmd(cmd, cwd=root)
        
        if code != 0:
            logger.error(
                "git ls-files failed", 
                retcode=code, 
                error=stderr
            )
            return []
            
        return [line.strip() for line in stdout.splitlines() if line.strip()]

    except Exception as e:
        logger.error("Failed to run git ls-files", error=str(e))
        return []


# ⚡ REFACTOR: Rewritten to use asyncio.subprocess
async def get_git_diff_files(root: Path, ref: str) -> List[str]:
    """Run 'git diff --name-only' asynchronously and return the file list."""
    cmd = ["git", "diff", "--name-only", ref]
    try:
        stdout, stderr, code = await _run_async_cmd(cmd, cwd=root)
        
        if code != 0:
            logger.error(
                "git diff failed", 
                ref=ref,
                retcode=code, 
                error=stderr
            )
            return []

        return [line.strip() for line in stdout.splitlines() if line.strip()]
        
    except Exception as e:
        logger.error("Failed to run git diff", ref=ref, error=str(e))
        return []


async def get_git_diff_content(root: Path, ref: str, files: List[str]) -> str:
    """
    Run 'git diff' for specific files and return the content.
    """
    # Create the command: git diff <ref> -- <file1> <file2> ...
    cmd = ["git", "diff", ref, "--"] + files

    try:
        stdout, stderr, code = await _run_async_cmd(cmd, cwd=root)

        if code != 0:
            logger.error(
                "git diff content failed",
                ref=ref,
                retcode=code,
                error=stderr
            )
            # In case of failure, we might want to raise or return empty.
            # Returning empty string signals no diff or failure.
            return ""

        return stdout

    except Exception as e:
        logger.error("Failed to run git diff content", ref=ref, error=str(e))
        return ""