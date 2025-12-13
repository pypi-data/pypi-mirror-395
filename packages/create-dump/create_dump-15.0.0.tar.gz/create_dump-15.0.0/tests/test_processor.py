# tests/test_processor.py

"""
Tests for Phase 3: src/create_dump/processor.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call

import anyio
# 🐞 FIX: Import TimeoutError from asyncio, not anyio
from asyncio import TimeoutError
# ✨ NEW: Import the real anyio.Path for spec-ing
from anyio import Path as RealAnyIOPath

# Import the class to test
from create_dump.processor import FileProcessor, ProcessorMiddleware
from create_dump.core import DumpFile

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def temp_dir(tmp_path: Path) -> str:
    """Provides a string path to a real temp directory."""
    return str(tmp_path)


@pytest.fixture
def mocked_metrics(mocker):
    """Mocks metrics and returns the mocks."""
    m_files_processed = mocker.patch("create_dump.processor.FILES_PROCESSED")
    m_errors_total = mocker.patch("create_dump.processor.ERRORS_TOTAL")
    return m_files_processed, m_errors_total


@pytest.fixture(autouse=True)
def mocked_deps(mocker):
    """Mocks non-critical dependencies."""
    mocker.patch("create_dump.processor.get_language", return_value="python")
    # Make the UUID predictable for temp file path assertion
    mocker.patch("create_dump.processor.uuid.uuid4", MagicMock(hex="test-uuid"))


@pytest.fixture
def mock_paths(mocker, temp_dir: str):
    """
    Mocks anyio.Path for both reading and writing.
    Returns the mock objects for assertion.
    """
    # 1. Mock the file-to-be-read
    mock_read_file = AsyncMock()
    # Simulate streaming read (peek + chunk + end)
    mock_read_file.read.side_effect = ["hello", " world", ""]
    mock_read_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_read_file))
    # 🐞 FIX: Use the real class for the spec
    mock_read_path = AsyncMock(spec=RealAnyIOPath)
    mock_read_path.open = AsyncMock(return_value=mock_read_context)

    # 2. Mock the temp-file-to-be-written
    mock_write_file = AsyncMock()
    mock_write_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_write_file))
    # 🐞 FIX: Use the real class for the spec
    mock_write_path = AsyncMock(spec=RealAnyIOPath)
    mock_write_path.open = AsyncMock(return_value=mock_write_context)
    mock_write_path.unlink = AsyncMock()

    # The expected path of the temp file
    temp_file_path_str = str(Path(temp_dir) / "test-uuid.tmp")

    mock_write_path.__fspath__ = MagicMock(return_value=temp_file_path_str)
    mock_write_path.__str__ = MagicMock(return_value=temp_file_path_str)


    # Mock for anyio.Path(temp_dir)
    # 🐞 FIX: Use the real class for the spec
    mock_temp_dir_path = AsyncMock(spec=RealAnyIOPath)
    # Mock the "/" operator to return the final write path
    mock_temp_dir_path.__truediv__ = MagicMock(return_value=mock_write_path)

    # 3. Mock the anyio.Path constructor to return the correct mock
    def path_side_effect(path_arg):
        path_str = str(path_arg)
        if path_str == "src/main.py":
            return mock_read_path
        if path_str == temp_dir:
            return mock_temp_dir_path

        # ✨ NEW: Add case for empty file test
        if path_str == "src/empty.py":
            mock_empty_read = AsyncMock()
            mock_empty_read.read.side_effect = ["", ""] # First read is empty
            mock_empty_context = AsyncMock(__aenter__=AsyncMock(return_value=mock_empty_read))
            # 🐞 FIX: Use the real class for the spec
            mock_empty_path = AsyncMock(spec=RealAnyIOPath)
            mock_empty_path.open = AsyncMock(return_value=mock_empty_context)
            return mock_empty_path

        # Fallback
        # 🐞 FIX: Use the real class for the spec
        return AsyncMock(spec=RealAnyIOPath)

    mocker.patch("create_dump.processor.anyio.Path", side_effect=path_side_effect)

    return mock_read_path, mock_write_path, mock_write_file


@pytest.fixture
def mock_middleware():
    """Returns a simple, successful mock middleware."""
    return AsyncMock(spec=ProcessorMiddleware)


class TestFileProcessor:
    """Groups tests for the FileProcessor."""

    async def test_process_file_success(
        self, temp_dir, mock_paths, mock_middleware, mocked_metrics
    ):
        """
        Test Case 1: process_file() success.
        Checks streaming, middleware call, and success metric.
        """
        _, _, mock_write_file = mock_paths
        m_files_processed, _ = mocked_metrics

        processor = FileProcessor(temp_dir, middlewares=[mock_middleware])
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert dump_file.error is None
        assert dump_file.path == "src/main.py"
        assert dump_file.language == "python"
        assert dump_file.temp_path == Path(temp_dir) / "test-uuid.tmp"

        # Check that streaming occurred (peek + chunk)
        assert mock_write_file.write.call_args_list == [
            call("hello"),
            call(" world"),
        ]

        # Check middleware and metrics
        mock_middleware.process.assert_called_once_with(dump_file)
        m_files_processed.labels.assert_called_once_with(status="success")
        m_files_processed.labels.return_value.inc.assert_called_once()

    async def test_process_file_read_error(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 2: process_file() fails on file read."""
        mock_read_path, mock_write_path, _ = mock_paths
        _, m_errors_total = mocked_metrics

        # Simulate a read error
        mock_read_path.open.side_effect = OSError("Permission denied")

        processor = FileProcessor(temp_dir)
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert "Permission denied" in dump_file.error
        assert dump_file.temp_path is None

        mock_write_path.unlink.assert_called_once_with(missing_ok=True)
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_process_file_write_error(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 3: process_file() fails on temp file write."""
        _, mock_write_path, _ = mock_paths
        _, m_errors_total = mocked_metrics

        # Simulate a write error
        mock_write_path.open.side_effect = OSError("Disk full")

        processor = FileProcessor(temp_dir)
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert "Disk full" in dump_file.error
        assert dump_file.temp_path is None

        mock_write_path.unlink.assert_called_once()
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_middleware_chain_execution(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 4: Middleware chain executes in order."""
        m_files_processed, _ = mocked_metrics
        mock_mw_1 = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_2 = AsyncMock(spec=ProcessorMiddleware)

        # Use mock_calls to check order
        manager = MagicMock()
        manager.attach_mock(mock_mw_1, "mw1")
        manager.attach_mock(mock_mw_2, "mw2")

        processor = FileProcessor(temp_dir, middlewares=[mock_mw_1, mock_mw_2])
        dump_file = await processor.process_file("src/main.py")

        # Check calls
        assert dump_file.error is None
        assert manager.mock_calls == [
            call.mw1.process(dump_file),
            call.mw2.process(dump_file),
        ]
        m_files_processed.labels.return_value.inc.assert_called_once()

    async def test_middleware_chain_short_circuits(
        self, temp_dir, mock_paths, mocked_metrics
    ):
        """Test Case 5: Middleware chain stops on first failure."""
        m_files_processed, _ = mocked_metrics

        mock_mw_1 = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_fail = AsyncMock(spec=ProcessorMiddleware)
        mock_mw_2 = AsyncMock(spec=ProcessorMiddleware)

        # Configure the failing middleware
        def fail_side_effect(df: DumpFile):
            df.error = "Middleware Fail"
        mock_mw_fail.process.side_effect = fail_side_effect

        processor = FileProcessor(
            temp_dir, middlewares=[mock_mw_1, mock_mw_fail, mock_mw_2]
        )
        dump_file = await processor.process_file("src/main.py")

        # Check DumpFile state
        assert dump_file.error == "Middleware Fail"

        # Check call chain
        mock_mw_1.process.assert_called_once()
        mock_mw_fail.process.assert_called_once()
        mock_mw_2.process.assert_not_called() # Should be skipped

        # Success metric should NOT be incremented
        m_files_processed.labels.return_value.inc.assert_not_called()

    async def test_dump_concurrent_respects_semaphore(self, mocker, temp_dir):
        """Test Case 6: dump_concurrent() respects max_workers via Semaphore."""
        mock_semaphore_cls = mocker.patch("create_dump.processor.anyio.Semaphore")
        mock_semaphore_instance = AsyncMock()
        mock_semaphore_cls.return_value = mock_semaphore_instance

        # Mock the method that runs inside the semaphore
        mock_process_file = mocker.patch.object(
            FileProcessor, "process_file", new_callable=AsyncMock
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py", "b.py", "c.py"]
        await processor.dump_concurrent(files_list, progress=False, max_workers=2)

        # Check that semaphore was created with max_workers
        mock_semaphore_cls.assert_called_once_with(2)

        # Check that it was acquired for each file
        assert mock_semaphore_instance.__aenter__.call_count == 3
        assert mock_process_file.call_count == 3

    async def test_dump_concurrent_timeout(self, mocker, temp_dir, mocked_metrics):
        """
        Test Case 7: dump_concurrent() wrapper handles Timeouts.
        Covers lines 139-141.
        """
        _, m_errors_total = mocked_metrics

        # Mock fail_after to immediately raise a TimeoutError
        mocker.patch(
            "create_dump.processor.anyio.fail_after", side_effect=TimeoutError
        )
        # Mock process_file, though it won't be fully called
        mocker.patch.object(FileProcessor, "process_file", new_callable=AsyncMock)

        processor = FileProcessor(temp_dir)
        files_list = ["a.py"]
        results = await processor.dump_concurrent(files_list, progress=False)

        # Check that a failure DumpFile was returned
        assert len(results) == 1
        assert results[0].path == "a.py"
        assert results[0].error == "Timeout"

        # Check metrics
        m_errors_total.labels.assert_called_once_with(type="timeout")
        m_errors_total.labels.return_value.inc.assert_called_once()

    # --- NEW TESTS TO COVER MISSED LINES ---
        
    async def test_dump_concurrent_generic_exception(self, mocker, temp_dir, mocked_metrics):
        """
        Test Case 8: dump_concurrent() wrapper handles generic Exceptions.
        Covers lines 142-143.
        """
        _, m_errors_total = mocked_metrics
        test_exception = Exception("Unhandled generic error")

        # Mock process_file to raise the exception
        mocker.patch.object(
            FileProcessor, "process_file", side_effect=test_exception
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py"]
        results = await processor.dump_concurrent(files_list, progress=False)

        # Check that a failure DumpFile was returned
        assert len(results) == 1
        assert results[0].path == "a.py"
        assert results[0].error == f"Unhandled exception: {test_exception}"

        # Check metrics
        m_errors_total.labels.assert_called_once_with(type="process")
        m_errors_total.labels.return_value.inc.assert_called_once()

    async def test_dump_concurrent_no_progress(self, mocker, temp_dir):
        """
        Test Case 9: dump_concurrent() with progress=False.
        Covers lines 130-132 (else branch) and 135 (finally branch).
        """
        # Mock the Progress bar to ensure it's not called
        mock_progress_cls = mocker.patch("create_dump.processor.Progress")
        
        # Mock process_file to check it's still called
        mock_process_file = mocker.patch.object(
            FileProcessor, "process_file", new_callable=AsyncMock
        )

        processor = FileProcessor(temp_dir)
        files_list = ["a.py", "b.py"]
        await processor.dump_concurrent(files_list, progress=False)

        # Assert Progress bar was not used
        mock_progress_cls.assert_not_called()
        
        # Assert files were still processed
        assert mock_process_file.call_count == 2

    async def test_process_file_empty(
        self, temp_dir, mock_paths, mock_middleware, mocked_metrics
    ):
        """
        Test Case 10: process_file() with an empty file.
        Covers line 71 (if peek:) being false.
        """
        _, _, mock_write_file = mock_paths
        m_files_processed, _ = mocked_metrics

        processor = FileProcessor(temp_dir, middlewares=[mock_middleware])
        # "src/empty.py" is configured in mock_paths to return "" on first read
        dump_file = await processor.process_file("src/empty.py")

        # Check DumpFile state
        assert dump_file.error is None
        assert dump_file.path == "src/empty.py"
        assert dump_file.temp_path is not None

        # Check that write was NOT called
        mock_write_file.write.assert_not_called()

        # Check middleware and metrics (still a success)
        mock_middleware.process.assert_called_once_with(dump_file)
        m_files_processed.labels.assert_called_once_with(status="success")
        m_files_processed.labels.return_value.inc.assert_called_once()