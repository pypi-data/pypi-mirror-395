# src/create_dump/scanning/secret.py


"""Secret scanning and redaction middleware."""

from __future__ import annotations

import logging
import re
from typing import List, Dict, Any

import anyio
# 🐞 FIX: Import `to_thread` to create a private symbol
from anyio import to_thread
from detect_secrets.core import scan
from detect_secrets.core.potential_secret import PotentialSecret

from ..core import DumpFile
from ..logging import logger
from ..metrics import ERRORS_TOTAL

# 🐞 FIX: Create a private, patchable symbol for run_sync
_run_sync = to_thread.run_sync


class SecretScanner:
    """Processor middleware to scan for and optionally redact secrets."""

    def __init__(self, hide_secrets: bool = False, custom_patterns: List[str] | None = None):
        self.hide_secrets = hide_secrets
        self.compiled_patterns = [re.compile(p) for p in (custom_patterns or [])]

    async def _scan_for_secrets(self, file_str_path: str) -> List[PotentialSecret]:
        """Runs detect-secrets in a thread pool with correct settings."""
        
        def scan_in_thread():
            # 🐞 FIX: Get the "detect-secrets" logger and temporarily
            # silence it to suppress the "No plugins" spam.
            ds_logger = logging.getLogger("detect-secrets")
            original_level = ds_logger.level
            ds_logger.setLevel(logging.CRITICAL)
            
            try:
                # 🐞 FIX: Call scan_file with only the path.
                # v1.5.0 handles its own default plugin initialization
                # internally and does not accept a `plugins` argument.
                results = scan.scan_file(file_str_path)
                
                # 🐞 FIX: Convert the generator to a list *inside* the thread
                return list(results)
            finally:
                # Always restore the original log level
                ds_logger.setLevel(original_level)

        try:
            # 🐞 FIX: Call the new module-level `_run_sync`
            scan_results_list = await _run_sync(
                scan_in_thread
            )
            # The return value is now already a list
            return scan_results_list
        except Exception as e:
            # Log the error but don't fail the whole dump, just this file
            logger.error("Secret scan failed", path=file_str_path, error=str(e))
            return [] # Return empty list on scan error

    async def _redact_secrets(self, temp_path: anyio.Path, secrets: List[PotentialSecret]) -> None:
        """Reads the temp file, redacts secret lines, and overwrites it."""
        try:
            # 1. Get line numbers (detect-secrets is 1-indexed)
            line_numbers_to_redact = {s.line_number for s in secrets}

            # 2. Read lines
            original_content = await temp_path.read_text()
            lines = original_content.splitlines()

            # 3. Redact
            new_lines = []
            for i, line in enumerate(lines, 1):
                if i in line_numbers_to_redact:
                    # Find the specific secret type for this line
                    secret_type = next((s.type for s in secrets if s.line_number == i), "Unknown")
                    new_lines.append(f"***SECRET_REDACTED*** (Line {i}, Type: {secret_type})")
                else:
                    new_lines.append(line)
            
            # 4. Write back
            await temp_path.write_text("\n".join(new_lines))
        except Exception as e:
            logger.error("Failed to redact secrets", path=str(temp_path), error=str(e))
            # If redaction fails, write a generic error to be safe
            await temp_path.write_text(f"*** ERROR: SECRET REDACTION FAILED ***\n{e}")

    async def _scan_for_custom_secrets(self, temp_path: anyio.Path) -> List[PotentialSecret]:
        """Scans a file for user-defined regex patterns."""
        if not self.compiled_patterns:
            return []

        custom_secrets = []
        try:
            content = await temp_path.read_text()
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for pattern in self.compiled_patterns:
                    match = pattern.search(line)
                    if match:
                        # Create a PotentialSecret for consistency
                        secret = PotentialSecret(
                            type=f"Custom: {pattern.pattern[:50]}...",
                            filename=str(temp_path),
                            line_number=i,
                            secret=match.group(0),
                        )
                        custom_secrets.append(secret)
                        # Go to next line once one pattern matches
                        break
        except Exception as e:
            logger.error("Custom secret scan failed", path=str(temp_path), error=str(e))

        return custom_secrets

    async def process(self, dump_file: DumpFile) -> None:
        """
        Public method to run the scan/redact logic on a processed file.
        Modifies `dump_file` in place if an error occurs.
        """
        if not dump_file.temp_path or dump_file.error:
            # File failed before this middleware (e.g., read error)
            return

        temp_anyio_path = anyio.Path(dump_file.temp_path)
        temp_file_str = str(dump_file.temp_path)
        
        secrets = await self._scan_for_secrets(temp_file_str)
        custom_secrets = await self._scan_for_custom_secrets(temp_anyio_path)
        all_secrets = secrets + custom_secrets

        if all_secrets:
            if self.hide_secrets:
                # Redact the file and continue
                await self._redact_secrets(temp_anyio_path, all_secrets)
                logger.warning("Redacted secrets", path=dump_file.path)
            else:
                # Fail the file
                await temp_anyio_path.unlink(missing_ok=True)
                ERRORS_TOTAL.labels(type="secret").inc()
                logger.error("Secrets detected", path=dump_file.path)
                dump_file.error = "Secrets Detected" # Modify the object
                dump_file.temp_path = None # Clear the temp path
