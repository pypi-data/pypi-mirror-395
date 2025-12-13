# src/create_dump/processor.py

"""
File Processing Component.

Reads all source files and saves their raw content to temporary files
for later consumption by formatters (Markdown, JSON, etc.).
"""

from __future__ import annotations

import uuid
from pathlib import Path
# ⚡ REFACTOR: Import List, Optional, Callable, Awaitable, Protocol
from typing import List, Optional, Any, Callable, Awaitable, Protocol

import anyio
from anyio.abc import TaskStatus

# ⚡ REFACTOR: Removed all detect-secrets imports

from .core import DumpFile
from .helpers import CHUNK_SIZE, get_language
from .logging import (
    HAS_RICH, Progress, SpinnerColumn, TextColumn, console, logger
)
from .metrics import FILES_PROCESSED, ERRORS_TOTAL
from .system import DEFAULT_MAX_WORKERS


# ⚡ NEW: Define a simple Protocol for middleware
class ProcessorMiddleware(Protocol):
    async def process(self, dump_file: DumpFile) -> None:
        """Processes a DumpFile. Can modify it in-place."""
        ...

# ⚡ NEW: Import CacheManager Protocol
class CacheManagerProtocol(Protocol):
    async def get(self, file_path: str, stat: Any) -> Optional[Path]: ...
    async def put(self, file_path: str, stat: Any, content_path: Path) -> None: ...


class FileProcessor:
    """
    Reads source files concurrently and stores their content in temp files.
    """

    # ⚡ REFACTOR: Update __init__ to accept middleware and cache_manager
    def __init__(
        self, 
        temp_dir: str, 
        middlewares: List[ProcessorMiddleware] | None = None,
        cache_manager: Optional[CacheManagerProtocol] = None
    ):
        self.temp_dir = temp_dir
        self.files: List[DumpFile] = []
        self.middlewares = middlewares or []
        self.cache_manager = cache_manager
        
    # ⚡ REFACTOR: Removed _scan_for_secrets
    # ⚡ REFACTOR: Removed _redact_secrets

    async def process_file(self, file_path: str) -> DumpFile:
        """Concurrently read and write file content to temp (streamed)."""
        temp_anyio_path: Optional[anyio.Path] = None
        dump_file: Optional[DumpFile] = None
        
        try:
            lang = get_language(file_path)

            # ⚡ SMART CACHING START
            if self.cache_manager:
                # We need blocking stat for now or use anyio.to_thread
                # anyio.Path.stat is async
                stat = await anyio.Path(file_path).stat()
                cached_path = await self.cache_manager.get(file_path, stat)
                if cached_path:
                    # Cache Hit!
                    logger.debug("Cache hit for file", path=file_path)
                    FILES_PROCESSED.labels(status="cached").inc()
                    return DumpFile(path=file_path, language=lang, temp_path=cached_path)
            # ⚡ SMART CACHING END

            temp_filename = f"{uuid.uuid4().hex}.tmp"
            temp_anyio_path = anyio.Path(self.temp_dir) / temp_filename
            
            async with await anyio.Path(file_path).open("r", encoding="utf-8", errors="replace") as src, \
                       await temp_anyio_path.open("w", encoding="utf-8") as tmp:
                
                peek = await src.read(CHUNK_SIZE)
                if peek:
                    # ⚡ REFACTOR: Write only the raw content.
                    await tmp.write(peek)
                    while chunk := await src.read(CHUNK_SIZE):
                        await tmp.write(chunk)
            
            # Create the successful DumpFile object
            dump_file = DumpFile(path=file_path, language=lang, temp_path=Path(temp_anyio_path))

            # ⚡ NEW: Run middleware chain
            for middleware in self.middlewares:
                await middleware.process(dump_file)
                if dump_file.error:
                    # Middleware failed this file (e.g., secrets found)
                    # The middleware is responsible for logging and metrics
                    if temp_anyio_path:
                         await temp_anyio_path.unlink(missing_ok=True)
                    return dump_file

            # ⚡ SMART CACHING UPDATE
            if self.cache_manager and not dump_file.error:
                 # Re-fetch stat to be sure we have the latest one associated with what we read
                 # (Technically there's a race condition if file changed during read, but this is best effort)
                 stat = await anyio.Path(file_path).stat()
                 await self.cache_manager.put(file_path, stat, Path(temp_anyio_path))

            FILES_PROCESSED.labels(status="success").inc()
            return dump_file
        
        except Exception as e:
            if temp_anyio_path is not None:
                await temp_anyio_path.unlink(missing_ok=True)
            
            ERRORS_TOTAL.labels(type="process").inc()
            
            logger.error("File process error", path=file_path, error=str(e))
            # Return an error DumpFile
            return DumpFile(path=file_path, error=str(e))

    async def dump_concurrent(
        self,
        files_list: List[str],
        progress: bool = False,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ) -> List[DumpFile]:
        """
        Parallel temp file creation with progress.
        
        Returns the list of processed DumpFile objects.
        """
        
        limiter = anyio.Semaphore(max_workers)
        self.files = [] # Ensure list is fresh for this run

        async def _process_wrapper(
            file_path: str, 
            prog: Optional[Progress] = None, 
            task_id: Optional[TaskStatus] = None
        ):
            """Wrapper to handle timeouts, limiting, and progress bar."""
            async with limiter:
                try:
                    with anyio.fail_after(60):  # 60-second timeout
                        result = await self.process_file(file_path)
                        self.files.append(result)
                except TimeoutError:
                    ERRORS_TOTAL.labels(type="timeout").inc()
                    self.files.append(DumpFile(path=file_path, error="Timeout"))
                except Exception as e:
                    ERRORS_TOTAL.labels(type="process").inc()
                    self.files.append(DumpFile(path=file_path, error=f"Unhandled exception: {e}"))
                finally:
                    if prog and task_id is not None:
                        prog.advance(task_id)

        async with anyio.create_task_group() as tg:
            if progress and HAS_RICH and console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as prog:
                    task_id = prog.add_task("Processing files...", total=len(files_list))
                    for f in files_list:
                        tg.start_soon(_process_wrapper, f, prog, task_id)
            else:
                for f in files_list:
                    tg.start_soon(_process_wrapper, f, None, None)
        
        # Return the processed files list
        return self.files
