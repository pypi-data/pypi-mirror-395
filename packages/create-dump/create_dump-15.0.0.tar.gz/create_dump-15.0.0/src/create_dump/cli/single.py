# src/create_dump/cli/single.py

"""'single' command implementation for the CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List

import typer
from typer import Exit
import anyio  # ⚡ REFACTOR: Import anyio

# ⚡ REFACTOR: Import the new ASYNC workflow function
from ..single import run_single
# ⚡ REFACTOR: Import from new logging module
from ..logging import setup_logging


def single(
    ctx: typer.Context,  # 🐞 FIX: Add Context argument
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root directory to scan [default: . (cwd)]."),

    # Output & Format
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    tree_toc: bool = typer.Option(False, "--tree-toc", help="Render Table of Contents as a file tree."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),

    # Processing
    progress: Optional[bool] = typer.Option(None, "-p", "--progress/--no-progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
    metrics_port: int = typer.Option(8000, "--metrics-port", help="Prometheus export port [default: 8000]."),

    # Filtering & Collection
    exclude: str = typer.Option("", "--exclude", help="Comma-separated exclude patterns."),
    include: str = typer.Option("", "--include", help="Comma-separated include patterns."),
    max_file_size: Optional[int] = typer.Option(None, "--max-file-size", help="Max file size in KB."),
    use_gitignore: bool = typer.Option(True, "--use-gitignore/--no-use-gitignore", help="Incorporate .gitignore excludes [default: true]."),
    git_meta: bool = typer.Option(True, "--git-meta/--no-git-meta", help="Include Git branch/commit [default: true]."),
    max_workers: int = typer.Option(16, "--max-workers", help="Concurrency level [default: 16]."),
    
    # ⚡ NEW: v8 feature flags
    watch: bool = typer.Option(False, "--watch", help="Run in live-watch mode, redumping on file changes."),
    git_ls_files: bool = typer.Option(False, "--git-ls-files", help="Use 'git ls-files' for file collection (fast, accurate)."),
    diff_since: Optional[str] = typer.Option(None, "--diff-since", help="Generate a git diff/patch file for changes since a specific git ref (e.g., 'main')."),
    scan_secrets: bool = typer.Option(False, "--scan-secrets", help="Scan files for secrets. Fails dump if secrets are found."),
    hide_secrets: bool = typer.Option(False, "--hide-secrets", help="Redact found secrets (requires --scan-secrets)."),
    secret_patterns: Optional[List[str]] = typer.Option(None, "--secret-patterns", help="Custom regex patterns for secret scanning."),
    scan_todos: bool = typer.Option(False, "--scan-todos", help="Scan files for TODO/FIXME tags and append a summary."),
    notify_topic: Optional[str] = typer.Option(None, "--notify-topic", help="ntfy.sh topic for push notification on completion."),

    # ⚡ NEW: ChatOps Flags
    notify_slack: Optional[str] = typer.Option(None, "--notify-slack", help="Slack webhook URL."),
    notify_discord: Optional[str] = typer.Option(None, "--notify-discord", help="Discord webhook URL."),
    notify_telegram_chat: Optional[str] = typer.Option(None, "--notify-telegram-chat", help="Telegram chat ID."),
    notify_telegram_token: Optional[str] = typer.Option(None, "--notify-telegram-token", help="Telegram bot token."),

    # ⚡ NEW: Database Dump Flags
    db_provider: Optional[str] = typer.Option(None, "--db-provider", help="Database provider (postgres, mysql)."),
    db_name: Optional[str] = typer.Option(None, "--db-name", help="Database name."),
    db_host: str = typer.Option("localhost", "--db-host", help="Database host [default: localhost]."),
    db_port: Optional[int] = typer.Option(None, "--db-port", help="Database port."),
    db_user: Optional[str] = typer.Option(None, "--db-user", help="Database user."),
    db_pass_env: Optional[str] = typer.Option(None, "--db-pass-env", help="Env var containing database password."),

    # Archiving (Unified)
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this run in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
):
    """Create a single code dump in the specified directory.
    ...
    """
    if not root.is_dir():
        raise typer.BadParameter(f"Root '{root}' is not a directory. Use '.' for cwd or a valid path.")

    # ⚡ NEW: Validation for v8 flags
    if git_ls_files and diff_since:
        raise typer.BadParameter("--git-ls-files and --diff-since are mutually exclusive.")
    
    if hide_secrets and not scan_secrets:
        raise typer.BadParameter("--hide-secrets requires --scan-secrets to be enabled.")

    effective_dry_run = dry_run and not no_dry_run
    
    # 🐞 FIX: Get verbose/quiet values from the *main* context
    # This ensures `create-dump -v` (no command) works
    main_params = ctx.find_root().params
    
    # 🐞 FIX: Logic to correctly determine verbosity, giving command-level precedence
    # and ensuring quiet wins.
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else: # Neither was set at the command level, so inherit from main
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        
        # Final sanity check if inheriting: quiet wins
        if quiet_val:
            verbose_val = False

    # 🐞 FIX: Re-run setup_logging in case 'single' was called directly
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    # 🐞 FIX: Add logic to correctly determine progress, mirroring verbose/quiet
    if progress is True:
        progress_val = True
    elif progress is False:
        progress_val = False
    else: # Not set at command level, inherit from main
        progress_val = main_params.get('progress', True) # Default to True from main
    
    effective_progress = progress_val and not quiet_val

    # ⚡ REFACTOR: Call the async function using anyio.run
    try:
        anyio.run(
            run_single,
            root,
            effective_dry_run,
            yes,
            no_toc,
            tree_toc,
            compress,
            format,
            exclude,
            include,
            max_file_size,
            use_gitignore,
            git_meta,
            effective_progress,
            max_workers,
            archive,
            archive_all,
            archive_search,
            archive_include_current,
            archive_no_remove,
            archive_keep_latest,
            archive_keep_last,
            archive_clean_root,
            archive_format,
            allow_empty,
            metrics_port,
            verbose_val,  # 🐞 FIX: Pass the correct flag value
            quiet_val,    # 🐞 FIX: Pass the correct flag value
            dest,
            # ⚡ NEW: Pass v8 flags to the orchestrator
            watch,
            git_ls_files,
            diff_since,
            scan_secrets,
            hide_secrets,
            secret_patterns,
            scan_todos,
            notify_topic,
            notify_slack,
            notify_discord,
            notify_telegram_chat,
            notify_telegram_token,
            db_provider,
            db_name,
            db_host,
            db_port,
            db_user,
            db_pass_env,
        )
    except Exit as e:
        if getattr(e, "exit_code", None) == 0 and dry_run:
            return  # Graceful exit for dry run
        raise