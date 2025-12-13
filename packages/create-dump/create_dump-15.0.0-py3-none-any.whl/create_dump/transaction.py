# src/create_dump/transaction.py

"""
Transaction management for file operations.
"""

from __future__ import annotations

import sys
import shutil
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

import anyio

from .path_utils import safe_is_within
from .logging import logger
from .metrics import ROLLBACKS_TOTAL

class AtomicBatchTxn:
    """Atomic staging for batch outputs: commit/rollback via rename/rmtree."""

    def __init__(self, root: Path, dest: Optional[Path], run_id: str, dry_run: bool):
        self.root = root
        self.dest = dest
        self.run_id = run_id
        self.dry_run = dry_run
        self.staging: Optional[anyio.Path] = None

    async def __aenter__(self) -> Optional[anyio.Path]:
        if self.dry_run:
            self.staging = None
            return None

        staging_parent = self.root / "archives" if not self.dest else (
            self.dest.resolve() if self.dest.is_absolute() else self.root / self.dest
        )

        anyio_staging_parent = anyio.Path(staging_parent)
        anyio_root = anyio.Path(self.root)
        if not await safe_is_within(anyio_staging_parent, anyio_root):
            raise ValueError("Staging parent outside root boundary")

        self.staging = anyio.Path(staging_parent / f".staging-{self.run_id}")
        await self.staging.mkdir(parents=True, exist_ok=True)
        return self.staging

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.staging:
            return
        if exc_type is None:
            final_name = self.staging.name.replace(".staging-", "")
            final_path = self.staging.parent / final_name
            await self.staging.rename(final_path)
            logger.info("Batch txn committed: %s -> %s", self.staging, final_path)
        else:
            try:
                await anyio.to_thread.run_sync(shutil.rmtree, self.staging)
            except OSError:
                pass
            # ⚡ FIX: Call .labels() before .inc() for Prometheus
            ROLLBACKS_TOTAL.labels(reason=str(exc_val)[:100]).inc()
            logger.error("Batch txn rolled back due to: %s", exc_val)


@asynccontextmanager
async def atomic_batch_txn(root: Path, dest: Optional[Path], run_id: str, dry_run: bool):
    txn = AtomicBatchTxn(root, dest, run_id, dry_run)
    staging = await txn.__aenter__()
    try:
        yield staging
    finally:
        await txn.__aexit__(*sys.exc_info())
