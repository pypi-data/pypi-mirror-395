# src/create_dump/workflow/single.py

"""The core single-run orchestration logic."""

from __future__ import annotations

import gzip
import os
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional
from typer import Exit
from importlib import metadata

import anyio

# Local project imports
from ..archiver import ArchiveManager
from ..collector import get_collector
from ..core import Config, GitMeta, load_config
# ⚡ REFACTOR: Import the async safety check
from ..path_utils import safe_is_within
from ..helpers import _unique_path
from ..logging import logger, styled_print
from ..metrics import DUMP_DURATION, metrics_server
from ..system import get_git_meta, get_git_diff_content
from ..processor import FileProcessor, ProcessorMiddleware
from ..writing import ChecksumWriter, MarkdownWriter, JsonWriter
from ..scanning.secret import SecretScanner
from ..scanning.todo import TodoScanner
from ..notifications import (
    send_ntfy_notification,
    send_slack_notification,
    send_discord_notification,
    send_telegram_notification,
)
from ..caching import CacheManager # ⚡ IMPORT CacheManager
from ..database import DatabaseDumper # ⚡ IMPORT DatabaseDumper

try:
    __version__ = metadata.version("create-dump")
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"


class SingleRunOrchestrator:
    """Orchestrates a complete, single dump run."""

    def __init__(
        self,
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
        watch: bool = False, # Pass watch explicitly
    ):
        # Store all parameters as instance attributes
        self.root = root
        self.dry_run = dry_run
        self.yes = yes
        self.no_toc = no_toc
        self.tree_toc = tree_toc
        self.compress = compress
        self.format = format
        self.exclude = exclude
        self.include = include
        self.max_file_size = max_file_size
        self.use_gitignore = use_gitignore
        self.git_meta = git_meta
        self.progress = progress
        self.max_workers = max_workers
        self.archive = archive
        self.archive_all = archive_all
        self.archive_search = archive_search
        self.archive_include_current = archive_include_current
        self.archive_no_remove = archive_no_remove
        self.archive_keep_latest = archive_keep_latest
        self.archive_keep_last = archive_keep_last
        self.archive_clean_root = archive_clean_root
        self.archive_format = archive_format
        self.allow_empty = allow_empty
        self.metrics_port = metrics_port
        self.verbose = verbose
        self.quiet = quiet
        self.dest = dest
        self.git_ls_files = git_ls_files
        self.diff_since = diff_since
        self.scan_secrets = scan_secrets
        self.hide_secrets = hide_secrets
        self.secret_patterns = secret_patterns or []
        self.scan_todos = scan_todos
        self.notify_topic = notify_topic
        self.notify_slack = notify_slack
        self.notify_discord = notify_discord
        self.notify_telegram_chat = notify_telegram_chat
        self.notify_telegram_token = notify_telegram_token
        self.db_provider = db_provider
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass_env = db_pass_env
        
        # ⚡ REFACTOR: Store anyio.Path version of root
        self.anyio_root = anyio.Path(self.root)

        self.cache_manager: Optional[CacheManager] = None

        # Calculate config hash for cache safety
        self.config_hash = self._calculate_config_hash()

    def _calculate_config_hash(self) -> str:
        """Generates a stable hash of the processing configuration."""
        # Include all flags that affect file processing or content
        config_items = [
            str(self.max_file_size),
            str(self.use_gitignore),
            str(self.git_ls_files),
            str(self.scan_secrets),
            str(self.hide_secrets),
            ",".join(sorted(self.secret_patterns)),
            str(self.scan_todos),
            str(self.exclude),
            str(self.include),
             # Note: format/compress/archive options don't affect *intermediate* processing
             # (FileProcessor output is raw content + metadata).
             # But if middleware changes content (redaction), it matters.
        ]
        return hashlib.md5("".join(config_items).encode("utf-8")).hexdigest()

    def enable_caching(self):
        """Enables the smart caching strategy."""
        cache_dir = self.root / ".create_dump_cache"
        self.cache_manager = CacheManager(cache_dir, self.config_hash)
        if not self.quiet:
            logger.info("Smart caching enabled", cache_dir=str(cache_dir))


    def _get_stats_sync(self, files: List[str]) -> tuple[int, int]:
        """Calculates total files and lines of code."""
        total_files = len(files)
        total_loc = 0
        for f in files:
            try:
                with open(self.root / f, "r", encoding="utf-8", errors="ignore") as in_f:
                    total_loc += sum(1 for _ in in_f)
            except (IOError, FileNotFoundError):
                pass  # File might have vanished, skip
        return total_files, total_loc
    
    # ⚡ FIX: Removed 'async' keyword. This must be a sync function.
    def _get_total_size_sync(self, files: List[str]) -> int:
        """Helper to run blocking stat() calls in a thread."""
        size = 0
        for f in files:
            try:
                # This is a blocking call, which is why the func is run in a thread
                size += (self.root / f).stat().st_size
            except FileNotFoundError:
                pass  # File may have vanished, skip
        return size

    def _compress_file_sync(self, in_file: Path, out_file: Path):
        """Blocking helper to gzip a file."""
        with open(in_file, "rb") as f_in, gzip.open(out_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    async def run(self):
        """The core logic for a single dump run."""
        status_title = "✅ create-dump Success"
        status_message = "Dump completed."
        try:
            # Load config on each run, in case it changed
            cfg = load_config()
            if self.max_file_size is not None:
                cfg.max_file_size_kb = self.max_file_size

            # Apply config defaults for new flags
            # CLI flags take precedence (if True), otherwise use config file

            effective_git_ls_files = self.git_ls_files or cfg.git_ls_files
            effective_scan_secrets = self.scan_secrets or cfg.scan_secrets
            effective_hide_secrets = self.hide_secrets or cfg.hide_secrets

            # Combine custom secret patterns from CLI and Config
            combined_secret_patterns = self.secret_patterns + cfg.custom_secret_patterns
            # Deduplicate patterns while preserving order
            combined_secret_patterns = list(dict.fromkeys(combined_secret_patterns))

            includes = [p.strip() for p in self.include.split(",") if p.strip()]
            excludes = [p.strip() for p in self.exclude.split(",") if p.strip()]

            # ⚡ FIX: Use the 'get_collector' factory function
            collector = get_collector(
                config=cfg,
                includes=includes,
                excludes=excludes,
                use_gitignore=self.use_gitignore,
                root=self.root,
                git_ls_files=effective_git_ls_files,
                diff_since=self.diff_since, # diff_since is CLI-only, not in config
            )
            files_list = await collector.collect()

            if not files_list:
                msg = "⚠️ No matching files found; skipping dump."
                logger.warning(msg)
                if self.verbose:
                    logger.debug("Excludes: %s, Includes: %s", excludes, includes)
                if not self.quiet:
                    styled_print(f"[yellow]{msg}[/yellow]")
                if not self.allow_empty:
                    raise Exit(code=1)
                return

            total_files, total_loc = await anyio.to_thread.run_sync(self._get_stats_sync, files_list)
            total_size = await anyio.to_thread.run_sync(self._get_total_size_sync, files_list)

            logger.info(
                "Collection complete",
                count=len(files_list),
                total_size_kb=total_size / 1024,
                root=str(self.root),
            )
            if not self.quiet:
                styled_print(
                    f"[green]📄 Found {total_files} files ({total_loc} lines, {total_size / 1024:.1f} KB total).[/green]"
                )

            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            foldername = self.root.name or "project"
            
            if self.diff_since:
                file_ext = "diff"
            else:
                file_ext = "json" if self.format == "json" else "md"

            branded_name = Path(f"{foldername}_all_create_dump_{timestamp}.{file_ext}")

            output_dest = self.root
            if self.dest:
                output_dest = self.dest.resolve()
                if not output_dest.is_absolute():
                    output_dest = self.root / self.dest

                # ⚡ REFACTOR: (Target 1) Use await and async check
                anyio_output_dest = anyio.Path(output_dest)
                if not await safe_is_within(anyio_output_dest, self.anyio_root):
                    logger.warning("Absolute dest outside root; proceeding with caution.")
                await anyio_output_dest.mkdir(parents=True, exist_ok=True)

            base_outfile = output_dest / branded_name

            prompt_outfile = await anyio.to_thread.run_sync(_unique_path, base_outfile)

            if not self.yes and not self.dry_run and not self.quiet:
                styled_print(
                    f"Proceed with dump to [blue]{prompt_outfile}[/blue]? [yellow](y/n)[/yellow]",
                    nl=False,
                )
                user_input = await anyio.to_thread.run_sync(input, "")
                if not user_input.lower().startswith("y"):
                    styled_print("[red]Cancelled.[/red]")
                    raise Exit(code=1)

            if self.dry_run:
                styled_print("[green]✅ Dry run: Would process listed files.[/green]")
                if not self.quiet:
                    for p in files_list:
                        styled_print(f" - {p}")
                raise Exit(code=0)


            outfile = await anyio.to_thread.run_sync(_unique_path, base_outfile)
            gmeta = await anyio.to_thread.run_sync(get_git_meta, self.root) if self.git_meta else None

            temp_dir = TemporaryDirectory()
            try:
                processed_files: List[DumpFile] = []
                
                # ⚡ FIX: Determine collector label BEFORE starting timer
                if self.diff_since:
                    collector_label = "git_diff"
                elif effective_git_ls_files: # Use the same var as collector
                    collector_label = "git_ls"
                else:
                    collector_label = "walk"
                
                with metrics_server(port=self.metrics_port):
                    # ⚡ FIX: Apply the label to the metric
                    with DUMP_DURATION.labels(collector=collector_label).time():
                        
                        if self.diff_since:
                            # ⚡ NEW: Git Diff Dump Mode
                            logger.info("Generating git diff dump", ref=self.diff_since)
                            diff_content = await get_git_diff_content(self.root, self.diff_since, files_list)

                            async with await anyio.open_file(outfile, "w", encoding="utf-8") as f:
                                await f.write(diff_content)

                            # Fake processed files list for success summary (metrics might be slightly off)
                            # Or we can leave it empty, but success_count uses it.
                            # Let's populate it with dummy success entries for the files we diffed?
                            # No, processed_files is List[DumpFile]. We don't have DumpFile objects here.
                            # We can just skip processed_files population.

                        else:
                            # Standard Dump Mode
                            # ⚡ REFACTOR: Step 1 - Build middleware
                            middlewares: List[ProcessorMiddleware] = []
                            if effective_scan_secrets:
                                middlewares.append(
                                    SecretScanner(
                                        hide_secrets=effective_hide_secrets,
                                        custom_patterns=combined_secret_patterns,
                                    )
                                )
                            if self.scan_todos:
                                middlewares.append(TodoScanner())

                            # ⚡ REFACTOR: Step 2 - Process files
                            processor = FileProcessor(
                                temp_dir.name,
                                middlewares=middlewares, # Pass middleware list
                                cache_manager=self.cache_manager # Pass cache manager
                            )
                            processed_files = await processor.dump_concurrent(
                                files_list, self.progress, self.max_workers
                            )

                            # ⚡ NEW: Database Dump Integration
                            if self.db_provider and self.db_name:
                                try:
                                    dumper = DatabaseDumper(
                                        provider=self.db_provider,
                                        db_name=self.db_name,
                                        host=self.db_host,
                                        port=self.db_port,
                                        user=self.db_user,
                                        password_env=self.db_pass_env,
                                    )
                                    db_file = await dumper.dump()
                                    processed_files.append(db_file)
                                    if not self.quiet:
                                        styled_print(f"[green]✔ Database dump added: {db_file.path}[/green]")
                                except Exception as e:
                                    logger.error("Database dump failed", error=str(e))
                                    if not self.quiet:
                                        styled_print(f"[red]❌ Database dump failed: {e}[/red]")
                                    # We don't fail the whole dump, just log error?
                                    # Or should we fail? Roadmap doesn't say.
                                    # Let's treat it as an error file.
                                    processed_files.append(DumpFile(path="database_dump_error", error=f"Database dump failed: {str(e)}"))

                            # ⚡ CACHE UPDATE: Save metadata if caching is enabled
                            if self.cache_manager:
                                await self.cache_manager.save()

                            # Step 3 - Format output
                            if self.format == "json":
                                writer = JsonWriter(outfile)
                                await writer.write(processed_files, gmeta, __version__, total_files=total_files, total_loc=total_loc)
                            else:
                                writer = MarkdownWriter(
                                    outfile,
                                    self.no_toc,
                                    self.tree_toc,
                                )
                                await writer.write(processed_files, gmeta, __version__, total_files=total_files, total_loc=total_loc)

                # Step 4 - Compress
                if self.compress:
                    gz_outfile = outfile.with_suffix(f".{file_ext}.gz")
                    await anyio.to_thread.run_sync(self._compress_file_sync, outfile, gz_outfile)
                    
                    await anyio.Path(outfile).unlink()
                    outfile = gz_outfile
                    logger.info("Output compressed", path=str(outfile))

                # Step 5 - Checksum
                checksum_writer = ChecksumWriter()
                checksum = await checksum_writer.write(outfile)
                if not self.quiet:
                    styled_print(f"[blue]{checksum}[/blue]")

                # Step 6 - Archive
                if self.archive or self.archive_all:
                    manager = ArchiveManager(
                        root=self.root,
                        timestamp=timestamp,
                        keep_latest=self.archive_keep_latest,
                        keep_last=self.archive_keep_last,
                        clean_root=self.archive_clean_root,
                        search=self.archive_search,
                        include_current=self.archive_include_current,
                        no_remove=self.archive_no_remove,
                        dry_run=self.dry_run,
                        yes=self.yes,
                        verbose=self.verbose,
                        md_pattern=cfg.dump_pattern,
                        archive_all=self.archive_all,
                        archive_format=self.archive_format, 
                    )
                    archive_results = await manager.run(current_outfile=outfile)
                    if archive_results:
                        groups = ', '.join(k for k, v in archive_results.items() if v)
                        if not self.quiet:
                            styled_print(f"[green]Archived groups: {groups}[/green]")
                        logger.info("Archiving complete", groups=groups)
                    else:
                        msg = "ℹ️ No prior dumps found for archiving."
                        if not self.quiet:
                            styled_print(f"[yellow]{msg}[/yellow]")
                        logger.info(msg)

                # Final metrics
                if self.diff_since:
                     # For diff mode, we assume success if we reached here
                    success_count = len(files_list)
                    error_count = 0
                else:
                    success_count = sum(1 for f in processed_files if not f.error)
                    error_count = len(processed_files) - success_count

                logger.info(
                    "Dump summary",
                    success=success_count,
                    errors=error_count,
                    output=str(outfile),
                )
                status_message = f"Successfully created: {outfile.name}"
            finally:
                await anyio.to_thread.run_sync(temp_dir.cleanup)
        except Exit as e:
            if e.exit_code == 0:
                status_title = "ℹ️ create-dump Dry Run"
                status_message = "Dry run completed."
            else:
                status_title = "❌ create-dump Failed"
                status_message = f"Failed with exit code {e.exit_code}"
            raise e
        except Exception as e:
            status_title = "❌ create-dump Error"
            status_message = f"An unexpected error occurred: {str(e)}"
            raise e
        finally:
            # ⚡ NOTIFICATIONS: Send all configured notifications
            async with anyio.create_task_group() as tg:
                if self.notify_topic:
                    tg.start_soon(send_ntfy_notification, self.notify_topic, status_message, status_title)

                if self.notify_slack:
                    tg.start_soon(send_slack_notification, self.notify_slack, f"{status_title}\n{status_message}")

                if self.notify_discord:
                    tg.start_soon(send_discord_notification, self.notify_discord, f"{status_title}\n{status_message}")

                if self.notify_telegram_chat and self.notify_telegram_token:
                    tg.start_soon(send_telegram_notification, self.notify_telegram_chat, self.notify_telegram_token, f"{status_title}\n{status_message}")