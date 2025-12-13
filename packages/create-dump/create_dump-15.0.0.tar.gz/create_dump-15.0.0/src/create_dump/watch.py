# src/create_dump/watch.py

"""File watcher and debouncing logic."""

from __future__ import annotations
from pathlib import Path
from typing import Callable, Awaitable

import anyio
from anyio import Event

from .logging import logger, styled_print


class FileWatcher:
    """Runs an async file watcher with debouncing."""
    
    DEBOUNCE_MS = 500  # 500ms debounce window 

    def __init__(self, root: Path, dump_func: Callable[[], Awaitable[None]], quiet: bool):
        self.root = root
        self.dump_func = dump_func
        self.quiet = quiet
        self.debounce_event = Event()

    async def _debouncer(self):
        """Waits for an event, then sleeps, then runs the dump."""
        while True:
            await self.debounce_event.wait()
            
            # 🐞 FIX: An anyio.Event is not cleared on wait().
            # We must re-create the event to reset its state and
            # prevent the loop from re-triggering immediately.
            self.debounce_event = Event()
            
            await anyio.sleep(self.DEBOUNCE_MS / 1000)
            
            if not self.quiet:
                styled_print(f"\n[yellow]File change detected, running dump...[/yellow]")
            try:
                await self.dump_func()
            except Exception as e:
                # Log error but don't kill the watcher 
                logger.error("Error in watched dump run", error=str(e))
                if not self.quiet:
                    styled_print(f"[red]Error in watched dump: {e}[/red]")

    async def start(self):
        """Starts the file watcher and debouncer."""
        try:
            async with anyio.create_task_group() as tg:
                tg.start_soon(self._debouncer)
                
                # Use anyio's native async watcher 
                async for _ in anyio.Path(self.root).watch(recursive=True):
                    self.debounce_event.set()
        except KeyboardInterrupt:
            if not self.quiet:
                styled_print("\n[cyan]Watch mode stopped.[/cyan]")