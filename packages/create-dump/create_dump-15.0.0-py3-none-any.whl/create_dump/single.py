# src/create_dump/single.py

"""
Single dump runner.

This file is the "glue" layer that connects the CLI flags
from `cli/single.py` to the core orchestration logic.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List

import anyio
from typer import Exit

# ⚡ REFACTOR: Import new orchestration and watch modules
from .workflow.single import SingleRunOrchestrator
from .watch import FileWatcher
from .logging import styled_print


async def run_single(
    root: Path,
    dry_run: bool,
    yes: bool,
    no_toc: bool,
    tree_toc: bool,
    compress: bool,
    format: str,
    exclude: str,
    include: str,
    max_file_size: Optional[int],
    use_gitignore: bool,
    git_meta: bool,
    progress: bool,
    max_workers: int,
    archive: bool,
    archive_all: bool,
    archive_search: bool,
    archive_include_current: bool,
    archive_no_remove: bool,
    archive_keep_latest: bool,
    archive_keep_last: Optional[int],
    archive_clean_root: bool,
    archive_format: str,
    allow_empty: bool,
    metrics_port: int,
    verbose: bool,
    quiet: bool,
    dest: Optional[Path] = None,
    # ⚡ NEW: v8 feature flags
    watch: bool = False,
    git_ls_files: bool = False,
    diff_since: Optional[str] = None,
    scan_secrets: bool = False,
    hide_secrets: bool = False,
    secret_patterns: Optional[List[str]] = None,
    scan_todos: bool = False,
    notify_topic: Optional[str] = None,
    # ⚡ NEW: ChatOps flags
    notify_slack: Optional[str] = None,
    notify_discord: Optional[str] = None,
    notify_telegram_chat: Optional[str] = None,
    notify_telegram_token: Optional[str] = None,
    # ⚡ NEW: Database flags
    db_provider: Optional[str] = None,
    db_name: Optional[str] = None,
    db_host: str = "localhost",
    db_port: Optional[int] = None,
    db_user: Optional[str] = None,
    db_pass_env: Optional[str] = None,
) -> None:
    
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Invalid root: {root}")

    # Normalize cwd once at the start
    await anyio.to_thread.run_sync(os.chdir, root)
    
    # ⚡ REFACTOR: Handle `yes` logic for watch mode
    # If --watch is on, we don't want prompts on subsequent runs.
    effective_yes = yes or watch

    # ⚡ REFACTOR: Instantiate the orchestrator
    orchestrator = SingleRunOrchestrator(
        root=root,
        dry_run=dry_run,
        yes=effective_yes, # Pass the combined value
        no_toc=no_toc,
        tree_toc=tree_toc,
        compress=compress,
        format=format,
        exclude=exclude,
        include=include,
        max_file_size=max_file_size,
        use_gitignore=use_gitignore,
        git_meta=git_meta,
        progress=progress,
        max_workers=max_workers,
        archive=archive,
        archive_all=archive_all,
        archive_search=archive_search,
        archive_include_current=archive_include_current,
        archive_no_remove=archive_no_remove,
        archive_keep_latest=archive_keep_latest,
        archive_keep_last=archive_keep_last,
        archive_clean_root=archive_clean_root,
        archive_format=archive_format,
        allow_empty=allow_empty,
        metrics_port=metrics_port,
        verbose=verbose,
        quiet=quiet,
        dest=dest,
        git_ls_files=git_ls_files,
        diff_since=diff_since,
        scan_secrets=scan_secrets,
        hide_secrets=hide_secrets,
        secret_patterns=secret_patterns,
        scan_todos=scan_todos,
        notify_topic=notify_topic,
        notify_slack=notify_slack,
        notify_discord=notify_discord,
        notify_telegram_chat=notify_telegram_chat,
        notify_telegram_token=notify_telegram_token,
        db_provider=db_provider,
        db_name=db_name,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_pass_env=db_pass_env,
    )

    # ⚡ REFACTOR: Top-level control flow
    if watch:
        # ⚡ SMART CACHING: Enable caching for watch mode
        orchestrator.enable_caching()

        if not quiet:
            styled_print("[green]Running initial dump...[/green]")
        
        try:
            await orchestrator.run()
        except Exit as e:
            if getattr(e, "exit_code", None) == 0 and dry_run:
                 # Handle dry_run exit for the *initial* run
                 return
            raise # Re-raise other exits
        
        if not quiet:
            styled_print(f"\n[cyan]Watching for file changes in {root}... (Press Ctrl+C to stop)[/cyan]")
        
        watcher = FileWatcher(root=root, dump_func=orchestrator.run, quiet=quiet)
        await watcher.start()
    else:
        try:
            await orchestrator.run()
        except Exit as e:
            if getattr(e, "exit_code", None) == 0 and dry_run:
                # Handle dry_run exit
                return
            raise
