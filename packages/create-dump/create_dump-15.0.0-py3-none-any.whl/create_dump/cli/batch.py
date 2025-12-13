# src/create_dump/cli/batch.py

"""'batch' command group implementation for the CLI."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import typer
import anyio  # ⚡ REFACTOR: Import anyio

# ⚡ REFACTOR: Import async versions of cleanup and orchestrator
from ..cleanup import safe_cleanup
from ..core import DEFAULT_DUMP_PATTERN
from ..orchestrator import run_batch
# ⚡ REFACTOR: Import from new logging module
from ..logging import setup_logging
from ..archiver import ArchiveManager


# Create a separate Typer for the batch group
batch_app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]})


@batch_app.callback()
def batch_callback(
    # Controls (Standardized; dry-run default ON for safety)
    dry_run: bool = typer.Option(True, "-d", "--dry-run", help="Perform a dry-run (default: ON for batch)."),
    dest: Optional[Path] = typer.Option(None, "--dest", help="Global destination dir for outputs (default: root)."),
):
    """Batch operations: Run dumps across subdirectories with cleanup and centralization.

    Examples:
        $ create-dump batch run --dirs src,tests --archive-all -y  # Batch dumps + grouped archive, skip prompts
        $ create-dump batch clean --pattern '.*dump.*' -y -nd  # Real cleanup of olds
    """
    # Logging is now set by the main_callback or the subcommand.
    pass


def split_dirs(dirs_str: str) -> List[str]:
    """Split comma-separated dirs string into list, stripping whitespace."""
    if not dirs_str:
        return [".", "packages", "services"]
    split = [d.strip() for d in dirs_str.split(',') if d.strip()]
    if not split:
        return [".", "packages", "services"]
    return split


@batch_app.command()
def run(
    ctx: typer.Context,  # Inject ctx to access callback params
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),

    # Output & Processing
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for centralized outputs (default: root; inherits from batch)."),
    dirs: str = typer.Option(".,packages,services", "--dirs", help="Subdirectories to process (comma-separated, relative to root) [default: .,packages,services]."),
    pattern: str = typer.Option(DEFAULT_DUMP_PATTERN, "--pattern", help="Regex to identify dump files [default: canonical pattern]."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    accept_prompts: bool = typer.Option(True, "--accept-prompts/--no-accept-prompts", help='Auto-answer "y" to single-dump prompts [default: true].'),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip outputs [default: false]."),
    max_workers: int = typer.Option(4, "--max-workers", help="Workers per subdir dump (global concurrency limited) [default: 4]."),

    # Archiving (Unified)
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this batch in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for deletions and prompts [default: false]."),
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
):
    """Run dumps in multiple subdirectories, cleanup olds, and centralize files.

    Examples:
        $ create-dump batch run src/ --dest central/ --dirs api,web -c -y -nd  # Real batch to central dir
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params
    
    # 2. Resolve dry_run (safe by default)
    # Start with the batch-level default
    effective_dry_run = parent_params.get('dry_run', True)
    # If the *command* flag is set, it wins
    if dry_run is True:
        effective_dry_run = True
    # --no-dry-run always wins
    if no_dry_run is True:
        effective_dry_run = False

    # 3. Resolve verbose/quiet (inheriting from root)
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else: # Neither was set at the command level, so inherit from main
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False

    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    subdirs = split_dirs(dirs)
    
    # 5. Call async function
    anyio.run(
        run_batch,
        root,
        subdirs,
        pattern,
        effective_dry_run,
        yes, # 'yes' is simple, just pass it
        accept_prompts,
        compress,
        max_workers,
        verbose_val, # Pass resolved value
        quiet_val,   # Pass resolved value
        dest or parent_params.get('dest'), # Pass inherited value
        archive,
        archive_all,
        archive_search,
        archive_include_current,
        archive_no_remove,
        archive_keep_latest,
        archive_keep_last,
        archive_clean_root,
        format, # Added
        archive_format, # Added
    )


@batch_app.command()
def clean(
    ctx: typer.Context,
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(DEFAULT_DUMP_PATTERN, help="Regex for old dumps to delete [default: canonical pattern]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations for deletions [default: false]."),
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables inherited dry-run) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
) -> None:
    """Cleanup old dump files/directories without running new dumps.

    Examples:
        $ create-dump batch clean . '.*old_dump.*' -y -nd -v  # Real verbose cleanup
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params

    # 2. Resolve dry_run
    effective_dry_run = parent_params.get('dry_run', True)
    if dry_run is True:
        effective_dry_run = True
    if no_dry_run is True:
        effective_dry_run = False

    # 3. Resolve verbose/quiet
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else:
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False

    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    # 5. Call async function
    anyio.run(
        safe_cleanup,
        root,
        pattern,
        effective_dry_run,
        yes,
        verbose_val # Pass resolved value
    )


@batch_app.command()
def archive(
    ctx: typer.Context,
    # Core Arguments
    root: Path = typer.Argument(Path("."), help="Root project path."),
    pattern: str = typer.Argument(r".*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?)$", help="Regex for MD dumps [default: canonical MD subset]."),

    # Archiving (Unified; elevated as primary focus)
    archive_search: bool = typer.Option(False, "--archive-search", help="Recursive search for dumps [default: false]."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs [default: false]."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives (unified flag)."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive (unified flag) [default: false]."),

    # Controls (Standardized)
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmations [default: false]."),
    dry_run: Optional[bool] = typer.Option(None, "-d", "--dry-run", help="Simulate without writing files (overrides batch default)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: Optional[bool] = typer.Option(None, "-v", "--verbose", help="Enable debug logging."),
    quiet: Optional[bool] = typer.Option(None, "-q", "--quiet", help="Suppress output (CI mode)."),
) -> None:
    """Archive existing dump pairs into ZIP; optional clean/prune (unified with single mode).

    Examples:
        $ create-dump batch archive monorepo/ '.*custom' --archive-all -y -v  # Grouped archive, verbose, skip prompts
    """
    # 1. Get flags from all 3 levels
    parent_params = ctx.parent.params
    main_params = ctx.find_root().params
    
    # Get archive_format from root
    inherited_archive_format = main_params.get('archive_format', 'zip')

    # 2. Resolve dry_run
    effective_dry_run = parent_params.get('dry_run', True)
    if dry_run is True:
        effective_dry_run = True
    if no_dry_run is True:
        effective_dry_run = False
    
    # 3. Resolve verbose/quiet
    if quiet is True:
        verbose_val = False
        quiet_val = True
    elif verbose is True:
        verbose_val = True
        quiet_val = False
    else:
        verbose_val = main_params.get('verbose', False)
        quiet_val = main_params.get('quiet', False)
        if quiet_val:
            verbose_val = False
    
    # 4. Re-run logging setup
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    manager = ArchiveManager(
        root, timestamp, archive_keep_latest, archive_keep_last, archive_clean_root,
        search=archive_search,
        dry_run=effective_dry_run, 
        yes=yes, 
        verbose=verbose_val, # Pass resolved value
        md_pattern=pattern,
        archive_all=archive_all,
        archive_format=inherited_archive_format # Pass inherited format
    )
    
    # 5. Call async function
    anyio.run(manager.run)  # No current_outfile for batch