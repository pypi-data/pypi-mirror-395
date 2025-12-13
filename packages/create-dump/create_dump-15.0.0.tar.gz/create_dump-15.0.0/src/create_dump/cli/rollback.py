# src/create_dump/cli/rollback.py

"""
'rollback' command implementation for the CLI.

Rehydrates a project structure from a specified .md dump file.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

import anyio
import typer

# ⚡ REFACTOR: Import setup_logging
from ..logging import logger, styled_print, setup_logging
from ..path_utils import confirm
from ..rollback.engine import RollbackEngine
from ..rollback.parser import MarkdownParser

# --- Rollback-specific Helpers ---

async def _calculate_sha256(file_path: anyio.Path) -> str:
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    async with await file_path.open("rb") as f:
        while True:
            chunk = await f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

async def _find_most_recent_dump(root: Path) -> Optional[Path]:
    """Finds the most recent .md dump file in the root."""
    latest_file: Optional[Path] = None
    latest_mtime: float = -1.0
    
    anyio_root = anyio.Path(root)
    # We use glob here, as find_matching_files is a generator
    # and we need to stat all files to find the latest.
    async for file in anyio_root.glob("*_all_create_dump_*.md"):
        try:
            stat = await file.stat()
            if stat.st_mtime > latest_mtime:
                latest_mtime = stat.st_mtime
                latest_file = Path(file) # Store as sync Path
        except OSError as e:
            logger.warning("Could not stat file", path=str(file), error=str(e))
            continue
    return latest_file

async def _verify_integrity(md_file: Path) -> bool:
    """Verifies the SHA256 hash of the .md file."""
    sha_file = md_file.with_suffix(".sha256")
    anyio_sha_path = anyio.Path(sha_file)
    anyio_md_path = anyio.Path(md_file)

    if not await anyio_sha_path.exists():
        logger.error(f"Integrity check failed: Missing checksum file for {md_file.name}")
        styled_print(f"[red]Error:[/red] Missing checksum file: [blue]{sha_file.name}[/blue]")
        return False
    
    try:
        # 1. Read the expected hash
        sha_content = await anyio_sha_path.read_text()
        expected_hash = sha_content.split()[0].strip()

        # 2. Calculate the actual hash
        actual_hash = await _calculate_sha256(anyio_md_path)

        # 3. Compare
        if actual_hash == expected_hash:
            logger.info("Integrity verified (SHA256 OK)", file=md_file.name)
            return True
        else:
            logger.error(
                "Integrity check FAILED: Hashes do not match",
                file=md_file.name,
                expected=expected_hash,
                actual=actual_hash
            )
            styled_print(f"[red]Error: Integrity check FAILED. File is corrupt.[/red]")
            styled_print(f"  Expected: {expected_hash}")
            styled_print(f"  Got:      {actual_hash}")
            return False
    except Exception as e:
        logger.error(f"Integrity check error: {e}", file=md_file.name)
        styled_print(f"[red]Error during integrity check:[/red] {e}")
        return False

# --- Async Main Logic ---

async def async_rollback(
    root: Path,
    file_to_use: Optional[Path],
    yes: bool,
    dry_run: bool,
    quiet: bool
):
    """The main async logic for the rollback command."""
    
    # 1. DISCOVERY
    md_file: Optional[Path] = None
    if file_to_use:
        if not await anyio.Path(file_to_use).exists():
            styled_print(f"[red]Error:[/red] Specified file not found: {file_to_use}")
            raise typer.Exit(code=1)
        md_file = file_to_use
    else:
        if not quiet:
            styled_print("[cyan]Scanning for most recent dump file...[/cyan]")
        md_file = await _find_most_recent_dump(root)
        if not md_file:
            styled_print("[red]Error:[/red] No `*_all_create_dump_*.md` files found in this directory.")
            raise typer.Exit(code=1)
    
    if not quiet:
        styled_print(f"Found dump file: [blue]{md_file.name}[/blue]")

    # 2. INTEGRITY VERIFICATION
    if not quiet:
        styled_print("Verifying file integrity (SHA256)...")
    is_valid = await _verify_integrity(md_file)
    if not is_valid:
        raise typer.Exit(code=1)
    
    if not quiet:
        styled_print("[green]Integrity verified.[/green]")

    # 3. PREPARATION & CONFIRMATION
    target_folder_name = md_file.stem
    # Your specified safe output directory
    output_dir = root.resolve() / "all_create_dump_rollbacks" / target_folder_name
    
    if not yes and not dry_run:
        prompt = f"Rehydrate project structure to [blue]./{output_dir.relative_to(root.resolve())}[/blue]?"
        user_confirmed = await anyio.to_thread.run_sync(confirm, prompt)
        if not user_confirmed:
            styled_print("[red]Rollback cancelled by user.[/red]")
            raise typer.Exit()
    elif dry_run and not quiet:
            styled_print(f"[cyan]Dry run:[/cyan] Would rehydrate files to [blue]./{output_dir.relative_to(root.resolve())}[/blue]")

    # 4. EXECUTION
    parser = MarkdownParser(md_file)
    engine = RollbackEngine(output_dir, dry_run=dry_run)
    created_files = await engine.rehydrate(parser)

    # 5. SUMMARY
    if not dry_run and not quiet:
        styled_print(f"[green]✅ Rollback complete.[/green] {len(created_files)} files created in [blue]{output_dir}[/blue]")
    elif dry_run and not quiet:
        styled_print(f"[green]✅ Dry run complete.[/green] Would have created {len(created_files)} files.")

# --- Typer Command Definition ---

# ⚡ REFACTOR: Removed 'rollback_app' Typer instance.
# The 'rollback' function is now a plain function to be registered in main.py.

def rollback(
    ctx: typer.Context,
    root: Path = typer.Argument(
        Path("."),
        help="Project root to scan for dumps and write rollback to.",
        show_default=True
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        help="Specify a dump file to use (e.g., my_dump.md). Default: find latest.",
        show_default=False
    ),
    # ⚡ REFACTOR: Add all 6 consistent flags in order
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Assume yes for prompts and deletions [default: false]."
    ),
    dry_run: bool = typer.Option(
        False,
        "-d",
        "--dry-run",
        help="Simulate without writing files (default: off)."
    ),
    no_dry_run: bool = typer.Option(
        False, 
        "-nd", 
        "--no-dry-run", 
        help="Run for real (disables simulation) [default: false]."
    ),
    verbose: Optional[bool] = typer.Option(
        None, 
        "-v", 
        "--verbose", 
        help="Enable debug logging."
    ),
    quiet: Optional[bool] = typer.Option(
        None, 
        "-q", 
        "--quiet", 
        help="Suppress output (CI mode)."
    ),
):
    """
    Rolls back a create-dump .md file to a full project structure.
    """
    # ⚡ REFACTOR: Add logic block from cli/single.py
    main_params = ctx.find_root().params
    
    effective_dry_run = dry_run and not no_dry_run

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

    # Re-run setup_logging in case 'rollback' was called directly
    setup_logging(verbose=verbose_val, quiet=quiet_val)
    
    try:
        anyio.run(
            async_rollback,
            root,
            file,
            yes,
            effective_dry_run, # Pass resolved value
            quiet_val          # Pass resolved value
        )
    except (FileNotFoundError, ValueError) as e:
        # These are caught by the parser/engine and logged
        styled_print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        # Catch any other unexpected error
        logger.error("Unhandled rollback error", error=str(e), exc_info=True)
        styled_print(f"[red]An unexpected error occurred:[/red] {e}")
        raise typer.Exit(code=1)