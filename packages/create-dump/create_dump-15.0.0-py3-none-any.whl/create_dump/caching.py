# src/create_dump/caching.py

"""
Smart Caching Strategy.

Implements persistent caching to avoid reprocessing unchanged files
during watch mode or repeated runs.
"""

from __future__ import annotations

import os
import shutil
import hashlib
from pathlib import Path
from typing import Optional, Dict
import json
import anyio

from .logging import logger

class CacheManager:
    """
    Manages a directory-based cache for processed file content.

    Structure:
    cache_dir/
      metadata.json  -> {config_hash: str, entries: {file_abs_path: {mtime, size, blob_name}}}
      blobs/
        <uuid>.tmp
    """

    def __init__(self, cache_dir: Path, config_hash: str):
        self.cache_dir = cache_dir
        self.blobs_dir = self.cache_dir / "blobs"
        self.metadata_file = self.cache_dir / "metadata.json"
        self.config_hash = config_hash
        self.entries: Dict[str, dict] = {}

        # Initialize
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)
        if not self.blobs_dir.exists():
            self.blobs_dir.mkdir()

        self._load_metadata()

    def _load_metadata(self):
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    stored_hash = data.get("config_hash")
                    if stored_hash == self.config_hash:
                        self.entries = data.get("entries", {})
                    else:
                        logger.info("Cache config mismatch, invalidating cache", old=stored_hash, new=self.config_hash)
                        self.entries = {}
                        # Optionally clean up blobs here or just let them be orphaned until explicit clean
                        # For now, let's just reset entries.
                        # Ideally we should clear blobs too to avoid disk leak.
                        self._clear_blobs()
        except Exception as e:
            logger.warning("Failed to load cache metadata", error=str(e))
            self.entries = {}

    def _clear_blobs(self):
        """Removes all cached blobs."""
        if self.blobs_dir.exists():
             shutil.rmtree(self.blobs_dir)
             self.blobs_dir.mkdir()

    async def save(self):
        """Persists metadata to disk."""
        try:
            data = {
                "config_hash": self.config_hash,
                "entries": self.entries
            }
            # Use async file writing or thread offloading
            await anyio.to_thread.run_sync(self._write_json_sync, data)
        except Exception as e:
            logger.error("Failed to save cache metadata", error=str(e))

    def _write_json_sync(self, data):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    async def get(self, file_path: str, stat: os.stat_result) -> Optional[Path]:
        """
        Retrieves path to cached content if valid.

        Args:
            file_path: Absolute path to the source file.
            stat: Current os.stat_result of the source file.

        Returns:
            Path to the cached content file, or None if miss.
        """
        key = str(Path(file_path).resolve())
        entry = self.entries.get(key)

        if not entry:
            return None

        # Validate mtime and size
        if entry["mtime"] != stat.st_mtime or entry["size"] != stat.st_size:
            return None

        cached_file = self.blobs_dir / entry["blob_name"]
        if not cached_file.exists():
            # Inconsistency found
            del self.entries[key]
            return None

        return cached_file

    async def put(self, file_path: str, stat: os.stat_result, content_path: Path) -> None:
        """
        Stores content in cache (in-memory update).

        Args:
            file_path: Absolute path to source file.
            stat: Current os.stat_result.
            content_path: Path to the temp file containing processed content.
        """
        key = str(Path(file_path).resolve())

        # Generate a unique blob name
        blob_name = hashlib.md5(key.encode()).hexdigest() + "_" + str(stat.st_mtime)
        dest_path = self.blobs_dir / blob_name

        # Copy content to cache
        await anyio.to_thread.run_sync(shutil.copy2, content_path, dest_path)

        self.entries[key] = {
            "mtime": stat.st_mtime,
            "size": stat.st_size,
            "blob_name": blob_name
        }
        # Note: We do NOT save metadata here. Call save() at end of batch.

    async def clear(self):
        """Clears the cache."""
        if self.cache_dir.exists():
            await anyio.to_thread.run_sync(shutil.rmtree, self.cache_dir)
        self.entries = {}
