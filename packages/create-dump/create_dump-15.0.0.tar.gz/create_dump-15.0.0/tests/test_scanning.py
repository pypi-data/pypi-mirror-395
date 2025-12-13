# tests/test_scanning.py

"""
Tests for Phase 3: src/create_dump/scanning.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
import logging # 🐞 FIX: Import logging
from unittest.mock import AsyncMock, MagicMock, patch, call, ANY

import anyio

# Import the class to test
from create_dump.scanning.secret import SecretScanner
# Import dependencies needed for testing
from create_dump.core import DumpFile
from detect_secrets.core.potential_secret import PotentialSecret
# 🐞 FIX: Import the *actual* dependencies to mock
from detect_secrets.core import scan


# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_potential_secret():
    """Creates a mock PotentialSecret object."""
    secret = MagicMock(spec=PotentialSecret)
    secret.type = "Generic Secret"
    secret.line_number = 2
    return secret


@pytest.fixture
async def temp_dump_file(tmp_path_factory):
    """
    Creates a real temporary file and a DumpFile object pointing to it.
    """
    # Create a persistent temp dir for the test session
    temp_dir = tmp_path_factory.mktemp("dump_files")

    # Create the content for the file
    content = (
        "line 1: this is safe\n"
        "line 2: this is a secret\n"
        "line 3: this is also safe\n"
    )

    # Use anyio to write the file
    temp_file_path = anyio.Path(temp_dir) / "test_file.tmp"
    await temp_file_path.write_text(content)

    # Create the DumpFile object
    dump_file = DumpFile(
        path="src/original/file.py",
        language="python",
        temp_path=Path(temp_file_path) # Store the sync path
    )

    return dump_file, anyio.Path(temp_file_path)


# 🐞 FIX: Updated fixture for the new implementation
@pytest.fixture
def mock_scanner_internals(mocker, mock_potential_secret):
    """
    Mocks the internal detect_secrets calls:
    - `scan.scan_file`
    - `logging.getLogger`
    """
    # 1. Mock the function that runs in the thread
    mock_scan_file_func = mocker.patch(
        "create_dump.scanning.secret.scan.scan_file", # Patched where it's called
        # 🐞 FIX: Return a list (or generator) instead of a dict
        return_value=[mock_potential_secret]
    )

    # 2. Mock the logger to verify it's being silenced
    mock_ds_logger = MagicMock()
    mock_get_logger = mocker.patch(
        "create_dump.scanning.secret.logging.getLogger",
        return_value=mock_ds_logger
    )

    return {
        "scan_file": mock_scan_file_func,
        "get_logger": mock_get_logger,
        "ds_logger": mock_ds_logger,
    }


class TestSecretScanner:
    """Groups tests for the SecretScanner middleware."""

    async def test_process_no_secrets(self, mocker, temp_dump_file, mock_scanner_internals):
        """
        Test Case 1: No secrets are found.
        """
        dump_file, temp_path = temp_dump_file
        original_content = await temp_path.read_text()

        # 🐞 FIX: Configure the mock to return an empty list
        mock_scanner_internals["scan_file"].return_value = []

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error is None
        assert await temp_path.read_text() == original_content

        # 🐞 FIX: Check logging was silenced and restored
        mock_scanner_internals["get_logger"].assert_called_with("detect-secrets")
        mock_ds_logger = mock_scanner_internals["ds_logger"]
        mock_ds_logger.setLevel.assert_has_calls([
            call(logging.CRITICAL), # Silenced
            call(mock_ds_logger.level) # Restored
        ])

        # 🐞 FIX: Check scan_file was called with just the path
        mock_scanner_internals["scan_file"].assert_called_once_with(
            str(dump_file.temp_path)
        )


    async def test_process_secrets_found_no_hide(
        self, mocker, temp_dump_file, mock_potential_secret, mock_scanner_internals
    ):
        """
        Test Case 2: Secrets found, hide_secrets=False.
        """
        dump_file, temp_path = temp_dump_file

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error == "Secrets Detected"
        assert dump_file.temp_path is None
        assert await temp_path.exists() is False

    async def test_process_secrets_found_with_hide(
        self, mocker, temp_dump_file, mock_potential_secret, mock_scanner_internals
    ):
        """
        Test Case 3: Secrets found, hide_secrets=True.
        """
        dump_file, temp_path = temp_dump_file

        scanner = SecretScanner(hide_secrets=True)
        await scanner.process(dump_file)

        # Assertions
        assert dump_file.error is None
        assert dump_file.temp_path is not None

        new_content = await temp_path.read_text()
        expected_content = (
            "line 1: this is safe\n"
            "***SECRET_REDACTED*** (Line 2, Type: Generic Secret)\n"
            "line 3: this is also safe"
        )
        assert new_content == expected_content


    async def test_process_scan_api_error(
        self, mocker, temp_dump_file, mock_scanner_internals
    ):
        """
        Test Case 4: A non-secret-related error during scan is logged and ignored.
        """
        dump_file, temp_path = temp_dump_file
        original_content = await temp_path.read_text()

        # 🐞 FIX: Patch the new, isolated `_run_sync` symbol
        mocker.patch(
            "create_dump.scanning.secret._run_sync",
            side_effect=Exception("Simulated API Error")
        )

        scanner = SecretScanner(hide_secrets=False)
        await scanner.process(dump_file)

        assert dump_file.error is None
        assert await temp_path.read_text() == original_content

    async def test_process_no_temp_path(self, mocker):
        """
        Test Case 5: process() returns early if dump_file has no temp_path.
        """
        dump_file = DumpFile(path="src/file.py", temp_path=None, error="Read error")
        mock_scan = mocker.patch("create_dump.scanning.secret.scan.scan_file")
        
        scanner = SecretScanner()
        await scanner.process(dump_file)
        
        mock_scan.assert_not_called()


    async def test_process_with_custom_patterns_no_hide(
        self, temp_dump_file
    ):
        """
        Tests that custom patterns are detected and fail the dump.
        """
        dump_file, _ = temp_dump_file
        scanner = SecretScanner(
            hide_secrets=False,
            custom_patterns=["secret"]
        )
        await scanner.process(dump_file)
        assert dump_file.error == "Secrets Detected"


    async def test_process_with_custom_patterns_with_hide(
        self, temp_dump_file
    ):
        """
        Tests that custom patterns are detected and redacted.
        """
        dump_file, temp_path = temp_dump_file
        scanner = SecretScanner(
            hide_secrets=True,
            custom_patterns=["secret"]
        )
        await scanner.process(dump_file)
        assert dump_file.error is None
        new_content = await temp_path.read_text()
        assert "***SECRET_REDACTED***" in new_content