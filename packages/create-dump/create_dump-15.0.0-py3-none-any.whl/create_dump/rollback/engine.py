# src/create_dump/rollback/engine.py

"""
Consumes a MarkdownParser and rehydrates the project structure to disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import anyio

from ..logging import logger
from .parser import MarkdownParser
# ✨ NEW: Import the robust, async-native path safety check
from ..path_utils import safe_is_within


class RollbackEngine:
    """
    Consumes a parser and writes the file structure to a target directory.
    """

    def __init__(self, root_output_dir: Path, dry_run: bool = False):
        """
        Initializes the engine.

        Args:
            root_output_dir: The *base* directory to write files into
                             (e.g., .../all_create_dump_rollbacks/my_dump_name_.../)
            dry_run: If True, will only log actions instead of writing.
        """
        self.root_output_dir = root_output_dir
        self.dry_run = dry_run
        self.anyio_root = anyio.Path(self.root_output_dir)

    async def rehydrate(self, parser: MarkdownParser) -> List[Path]:
        """
        Consumes the parser and writes files to the target directory.

        Args:
            parser: An initialized MarkdownParser instance.

        Returns:
            A list of the `pathlib.Path` objects that were created.
        """
        created_files: List[Path] = []
        
        logger.info(
            "Starting rehydration",
            target_directory=str(self.root_output_dir),
            dry_run=self.dry_run
        )

        async for rel_path_str, content in parser.parse_dump_file():
            try:
                # 🔒 SECURITY: Prevent path traversal attacks
                # ♻️ REFACTOR: Replaced weak ".." check with robust safe_is_within
                
                target_path = self.anyio_root / rel_path_str
                
                # The new, robust check handles symlinks and all traversal types
                # by resolving the path *before* checking if it's within the root.
                if not await safe_is_within(target_path, self.anyio_root):
                    logger.warning(
                        "Skipping unsafe path: Resolves outside root",
                        path=rel_path_str,
                        resolved_to=str(target_path)
                    )
                    continue
                
                # Ensure parent directory exists
                if not self.dry_run:
                    await target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the file
                if self.dry_run:
                    logger.info(f"[dry-run] Would rehydrate file to: {target_path}")
                else:
                    await target_path.write_text(content)
                    logger.debug(f"Rehydrated file: {target_path}")
                
                # ⚡ FIX: Append to created_files *only on success*
                created_files.append(Path(target_path))
                
            except Exception as e:
                logger.error(
                    "Failed to rehydrate file",
                    path=rel_path_str,
                    error=str(e)
                )
        
        logger.info(
            "Rehydration complete",
            files_created=len(created_files)
        )
        return created_files