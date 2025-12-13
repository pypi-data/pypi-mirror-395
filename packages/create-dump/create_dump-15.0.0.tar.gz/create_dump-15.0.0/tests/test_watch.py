# tests/test_watch.py

"""
Tests for src/create_dump/watch.py
"""

from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import anyio
from anyio import Event

# Import the class to test
from create_dump.watch import FileWatcher

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


@pytest.fixture
def mock_dump_func() -> AsyncMock:
    """Provides a reusable AsyncMock for the dump_func callback."""
    return AsyncMock()


@pytest.fixture
def mock_sleep(mocker) -> AsyncMock:
    """Mocks anyio.sleep to prevent test delays."""
    return mocker.patch("anyio.sleep", new_callable=AsyncMock)


@pytest.fixture
def mock_styled_print(mocker) -> MagicMock:
    """Mocks styled_print to capture console output."""
    return mocker.patch("create_dump.watch.styled_print")


@pytest.fixture
def mock_logger(mocker) -> MagicMock:
    """Mocks the logger to capture error output."""
    return mocker.patch("create_dump.watch.logger")


class TestFileWatcher:
    """Tests for the FileWatcher class."""

    async def test_debouncer_logic(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print
    ):
        """
        Test Case 1: (Happy Path)
        Validates the _debouncer logic:
        1. Waits for an event.
        2. Clears the event.
        3. Sleeps for DEBOUNCE_MS.
        4. Calls styled_print (when not quiet).
        5. Calls the dump_func.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)
        
        # We need a completion event to know when the mock_dump_func has been
        # called, so we can safely exit the test's task group.
        completion_event = anyio.Event()
        mock_dump_func.side_effect = lambda: completion_event.set()

        async with anyio.create_task_group() as tg:
            # Start the debouncer in the background
            tg.start_soon(watcher._debouncer)
            
            # --- Test Execution ---
            # 1. Trigger the event
            watcher.debounce_event.set()
            
            # 2. Wait for the dump_func to be called
            with anyio.move_on_after(2):  # 2-second timeout
                await completion_event.wait()
            
            # 3. Cancel the debouncer's infinite loop to exit the test
            tg.cancel_scope.cancel()

        # --- Assertions ---
        # It slept for the correct debounce period
        mock_sleep.assert_called_once_with(watcher.DEBOUNCE_MS / 1000)
        # It printed to console
        mock_styled_print.assert_called_with(
            "\n[yellow]File change detected, running dump...[/yellow]"
        )
        # It called the dump function
        mock_dump_func.assert_called_once()

    async def test_debouncer_logic_quiet(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print
    ):
        """
        Test Case 2: (Quiet Mode)
        Validates that styled_print is NOT called when quiet=True.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)
        
        completion_event = anyio.Event()
        mock_dump_func.side_effect = lambda: completion_event.set()

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_sleep.assert_called_once()
        mock_dump_func.assert_called_once()
        # Key Assertion: Print was NOT called
        mock_styled_print.assert_not_called()

    async def test_debouncer_error_handling(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print, mock_logger
    ):
        """
        Test Case 3: (Error Handling)
        Validates that an exception in dump_func is caught, logged,
        and does not crash the debouncer. (Covers line 45->28)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)
        
        test_exception = Exception("Simulated dump error")
        completion_event = anyio.Event()

        # Configure mock to raise an error, but set the completion event
        # in a finally block so the test can exit.
        async def mock_side_effect():
            try:
                raise test_exception
            finally:
                completion_event.set()
        
        mock_dump_func.side_effect = mock_side_effect

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_dump_func.assert_called_once()
        # It logged the error
        mock_logger.error.assert_called_once_with(
            "Error in watched dump run", error=str(test_exception)
        )
        # It printed the error to console
        mock_styled_print.assert_any_call(
            f"[red]Error in watched dump: {test_exception}[/red]"
        )

    async def test_start_method_integration(self, test_project, mock_dump_func):
        """
        Test Case 4: (Integration)
        Validates that the `start` method:
        1. Launches the _debouncer.
        2. Calls anyio.Path.watch.
        3. Calls event.set() when the watcher yields.
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)

        # Mock the _debouncer method
        mock_debouncer = AsyncMock()
        watcher._debouncer = mock_debouncer

        # Mock the event to check .set()
        mock_event = AsyncMock(spec=Event)
        watcher.debounce_event = mock_event

        # Mock the watch generator to yield one value, then stop
        async def fake_watch_gen():
            yield "file_change_event"
        
        # Mock anyio.Path and its .watch() method
        with patch("anyio.Path") as mock_path_class:
            mock_path_instance = MagicMock()
            mock_path_instance.watch.return_value = fake_watch_gen()
            mock_path_class.return_value = mock_path_instance

            # Run the 'start' method, but cancel it immediately after
            # it's had time to process the single watch event.
            async with anyio.create_task_group() as tg:
                tg.start_soon(watcher.start)
                await anyio.sleep(0.01)  # Give time for the loop to run
                tg.cancel_scope.cancel() # Stop the start() method

        # --- Assertions ---
        # 1. _debouncer was started
        mock_debouncer.assert_called_once()
        # 2. anyio.Path(root) was called
        mock_path_class.assert_called_with(test_project.root)
        # 3. .watch(recursive=True) was called
        mock_path_instance.watch.assert_called_once_with(recursive=True)
        # 4. The event was set
        mock_event.set.assert_called_once()

    # --- NEW P2 TESTS ---
        
    async def test_debouncer_error_handling_quiet(
        self, test_project, mock_dump_func, mock_sleep, mock_styled_print, mock_logger
    ):
        """
        Test Case 5: (Error Handling - Quiet)
        Validates that an exception in dump_func is logged but NOT printed
        when in quiet mode. (Covers line 45->28 and skips 47)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)
        
        test_exception = Exception("Simulated dump error")
        completion_event = anyio.Event()

        async def mock_side_effect():
            try:
                raise test_exception
            finally:
                completion_event.set()
        
        mock_dump_func.side_effect = mock_side_effect

        async with anyio.create_task_group() as tg:
            tg.start_soon(watcher._debouncer)
            watcher.debounce_event.set()
            with anyio.move_on_after(2):
                await completion_event.wait()
            tg.cancel_scope.cancel()

        # --- Assertions ---
        mock_dump_func.assert_called_once()
        # It logged the error
        mock_logger.error.assert_called_once_with(
            "Error in watched dump run", error=str(test_exception)
        )
        # It did NOT print the error
        mock_styled_print.assert_not_called()

    async def test_start_keyboard_interrupt(
        self, test_project, mock_dump_func, mock_styled_print, mocker
    ):
        """
        Test Case 6: (KeyboardInterrupt)
        Validates that a KeyboardInterrupt during the watch loop is caught
        and printed. (Covers lines 57-59)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=False)

        # 🐞 FIX: Mock the create_task_group context manager to raise the interrupt
        # This simulates the interrupt happening *during* the watch.
        mock_task_group = mocker.patch(
            "anyio.create_task_group",
            side_effect=KeyboardInterrupt
        )

        # Run the 'start' method. It should catch the interrupt and exit.
        await watcher.start()

        # --- Assertions ---
        # Assert the task group was entered
        mock_task_group.assert_called_once()
        # Assert the final "stopped" message was printed
        mock_styled_print.assert_called_with("\n[cyan]Watch mode stopped.[/cyan]")
        
    async def test_start_keyboard_interrupt_quiet(
        self, test_project, mock_dump_func, mock_styled_print, mocker
    ):
        """
        Test Case 7: (KeyboardInterrupt - Quiet)
        Validates that a KeyboardInterrupt is caught but NOT printed
        when in quiet mode. (Covers line 58)
        """
        watcher = FileWatcher(test_project.root, mock_dump_func, quiet=True)

        mocker.patch(
            "anyio.create_task_group",
            side_effect=KeyboardInterrupt
        )

        await watcher.start()

        # Assert that the "stopped" message was NOT printed
        mock_styled_print.assert_not_called()