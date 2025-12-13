# src/create_dump/cli/main.py

"""
Main CLI Entry Point.

Defines the main 'app' and orchestrates the 'single' and 'batch' commands.
"""

from __future__ import annotations

import typer
from typing import Optional
from pathlib import Path

from importlib import metadata

# ⚡ REFACTOR: Removed generate_default_config import
from ..core import load_config
# ⚡ REFACTOR: Corrected imports from new modules
from ..logging import setup_logging, styled_print

# ⚡ REFACTOR: Import commands and command groups from submodules
from .single import single
from .batch import batch_app

from .rollback import rollback

from ..banner import print_logo

print_logo()

try:
    __version__ = metadata.version("create-dump")
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"


app = typer.Typer(
    name="create-dump",
    add_completion=True,
    pretty_exceptions_enable=True,
    help="Enterprise-grade code dump utility for projects and monorepos.",
    context_settings={"help_option_names": ["-h", "--help"]},
)


# ⚡ NEW: Helper function for the interactive --init wizard
def _run_interactive_init() -> str:
    """Runs an interactive wizard to build the config file content."""
    styled_print("\n[bold]Welcome to the `create-dump` interactive setup![/bold]")
    styled_print("This will create a `create_dump.toml` file in your current directory.\n")
    
    # Header for the TOML file
    lines = [
        "# Configuration for create-dump",
        "# You can also move this content to [tool.create-dump] in pyproject.toml",
        "[tool.create-dump]",
        ""
    ]
    
    # 1. Ask for 'dest' path
    dest_path = typer.prompt(
        "Default output destination? (e.g., './dumps'). [Press Enter to skip]",
        default="",
        show_default=False,
    )
    if dest_path:
        # Ensure path is formatted for TOML (forward slashes)
        sane_path = Path(dest_path).as_posix()
        lines.append(f'# Default output destination. Overridden by --dest.')
        lines.append(f'dest = "{sane_path}"')
        lines.append("")

    # 2. Ask for 'use_gitignore'
    use_gitignore = typer.confirm(
        "Use .gitignore to automatically exclude files?", 
        default=True
    )
    lines.append("# Use .gitignore files to automatically exclude matching files.")
    lines.append(f"use_gitignore = {str(use_gitignore).lower()}")
    lines.append("")

    # 3. Ask for 'git_meta'
    git_meta = typer.confirm(
        "Include Git branch and commit hash in the header?", 
        default=True
    )
    lines.append("# Include Git branch and commit hash in the header.")
    lines.append(f"git_meta = {str(git_meta).lower()}")
    lines.append("")

    # 4. Ask for 'scan_secrets'
    scan_secrets = typer.confirm(
        "Enable secret scanning? (Recommended: false, unless you configure --hide-secrets)", 
        default=False
    )
    lines.append("# Enable secret scanning. Add 'hide_secrets = true' to redact them.")
    lines.append(f"scan_secrets = {str(scan_secrets).lower()}")
    lines.append("")

    return "\n".join(lines)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    # --- App Controls ---
    version: bool = typer.Option(False, "-V", "--version", help="Show version and exit."),
    init: bool = typer.Option(
        False, 
        "--init", 
        help="Run interactive wizard to create 'create_dump.toml'.",
        is_eager=True,  # Handle this before any command
    ),
    config: Optional[str] = typer.Option(None, "--config", help="Path to TOML config file."),
    profile: Optional[str] = typer.Option(None, "--profile", help="Config profile (e.g., 'ci') to merge from pyproject.toml."),
    
    # --- ⚡ REFACTOR: Grouped SRE/Control Flags ---
    yes: bool = typer.Option(False, "-y", "--yes", help="Assume yes for prompts and deletions [default: false]."),
    dry_run: bool = typer.Option(False, "-d", "--dry-run", help="Simulate without writing files (default: off)."),
    no_dry_run: bool = typer.Option(False, "-nd", "--no-dry-run", help="Run for real (disables simulation) [default: false]."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable debug logging [default: false]."),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Suppress output (CI mode) [default: false]."),
    
    # --- Default Command ('single') Flags ---
    dest: Optional[Path] = typer.Option(None, "--dest", help="Destination dir for output (default: root)."),
    no_toc: bool = typer.Option(False, "--no-toc", help="Omit table of contents."),
    tree_toc: bool = typer.Option(False, "--tree-toc", help="Render Table of Contents as a file tree."),
    format: str = typer.Option("md", "--format", help="Output format (md or json)."),
    compress: bool = typer.Option(False, "-c", "--compress", help="Gzip the output file."),
    progress: bool = typer.Option(True, "-p", "--progress/--no-progress", help="Show processing progress."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Succeed on 0 files (default: fail)."),
    metrics_port: int = typer.Option(8000, "--metrics-port", help="Prometheus export port [default: 8000]."),
    exclude: str = typer.Option("", "--exclude", help="Comma-separated exclude patterns."),
    include: str = typer.Option("", "--include", help="Comma-separated include patterns."),
    max_file_size: Optional[int] = typer.Option(None, "--max-file-size", help="Max file size in KB."),
    use_gitignore: bool = typer.Option(True, "--use-gitignore/--no-use-gitignore", help="Incorporate .gitignore excludes [default: true]."),
    git_meta: bool = typer.Option(True, "--git-meta/--no-git-meta", help="Include Git branch/commit [default: true]."),
    max_workers: int = typer.Option(16, "--max-workers", help="Concurrency level [default: 16]."),
    watch: bool = typer.Option(False, "--watch", help="Run in live-watch mode, redumping on file changes."),
    git_ls_files: bool = typer.Option(False, "--git-ls-files", help="Use 'git ls-files' for file collection (fast, accurate)."),
    diff_since: Optional[str] = typer.Option(None, "--diff-since", help="Only dump files changed since a specific git ref (e.g., 'main')."),
    scan_secrets: bool = typer.Option(False, "--scan-secrets", help="Scan files for secrets. Fails dump if secrets are found."),
    hide_secrets: bool = typer.Option(False, "--hide-secrets", help="Redact found secrets (requires --scan-secrets)."),
    scan_todos: bool = typer.Option(False, "--scan-todos", help="Scan files for TODO/FIXME tags and append a summary."),
    notify_topic: Optional[str] = typer.Option(None, "--notify-topic", help="ntfy.sh topic for push notification on completion."),
    archive: bool = typer.Option(False, "-a", "--archive", help="Archive prior dumps into ZIP (unified workflow)."),
    archive_all: bool = typer.Option(False, "--archive-all", help="Archive dumps grouped by prefix (e.g., src_, tests_) into separate ZIPs."),
    archive_search: bool = typer.Option(False, "--archive-search", help="Search project-wide for dumps."),
    archive_include_current: bool = typer.Option(True, "--archive-include-current/--no-archive-include-current", help="Include this run in archive [default: true]."),
    archive_no_remove: bool = typer.Option(False, "--archive-no-remove", help="Preserve originals post-archiving."),
    archive_keep_latest: bool = typer.Option(True, "--archive-keep-latest/--no-archive-keep-latest", help="Keep latest dump live or archive all (default: true; use =false to disable)."),
    archive_keep_last: Optional[int] = typer.Option(None, "--archive-keep-last", help="Keep last N archives."),
    archive_clean_root: bool = typer.Option(False, "--archive-clean-root", help="Clean root post-archive."),
    archive_format: str = typer.Option("zip", "--archive-format", help="Archive format (zip, tar.gz, tar.bz2)."),
):
    """Create Markdown code dumps from source files.

    Defaults to 'single' mode if no subcommand provided.
    """
    # Setup logging immediately
    setup_logging(verbose=verbose, quiet=quiet)

    if version:
        styled_print(f"create-dump v{__version__}")
        raise typer.Exit()

    if init:
        config_path = Path("create_dump.toml")
        if config_path.exists():
            styled_print(f"[yellow]⚠️ Config file 'create_dump.toml' already exists.[/yellow]")
            raise typer.Exit(code=1)
        
        try:
            config_content = _run_interactive_init()
            config_path.write_text(config_content)
            styled_print(f"\n[green]✅ Success![/green] Default config file created at [blue]{config_path.resolve()}[/blue]")
        except IOError as e:
            styled_print(f"[red]❌ Error:[/red] Could not write config file: {e}")
            raise typer.Exit(code=1)
        
        raise typer.Exit(code=0)  # Exit after creating file

    load_config(Path(config) if config else None, profile=profile)
    
    if ctx.invoked_subcommand is None:
        root_arg = ctx.args[0] if ctx.args else Path(".")
        
        # ⚡ FIX: Must pass ALL duplicated flags to the invoked command
        ctx.invoke(
            single, 
            ctx=ctx,  
            root=root_arg, 
            dest=dest,
            no_toc=no_toc,
            tree_toc=tree_toc,
            format=format,
            compress=compress,
            progress=progress,
            allow_empty=allow_empty,
            metrics_port=metrics_port,
            exclude=exclude,
            include=include,
            max_file_size=max_file_size,
            use_gitignore=use_gitignore,
            git_meta=git_meta,
            max_workers=max_workers,
            watch=watch,
            git_ls_files=git_ls_files,
            diff_since=diff_since,
            scan_secrets=scan_secrets,
            hide_secrets=hide_secrets,
            scan_todos=scan_todos,
            notify_topic=notify_topic,
            archive=archive,
            archive_all=archive_all,
            archive_search=archive_search,
            archive_include_current=archive_include_current,
            archive_no_remove=archive_no_remove,
            archive_keep_latest=archive_keep_latest,
            archive_keep_last=archive_keep_last,
            archive_clean_root=archive_clean_root,
            archive_format=archive_format,
            yes=yes,
            dry_run=dry_run,
            no_dry_run=no_dry_run,
            verbose=verbose,
            quiet=quiet
        )


# ⚡ REFACTOR: Register the imported 'single' command
app.command()(single)

# ⚡ REFACTOR: Register the imported 'batch' app
app.add_typer(batch_app, name="batch")

# ✨ NEW: Register the rollback function as a standard command
app.command(name="rollback", help="Rehydrate a project structure from a create-dump file.")(rollback)