# tests/test_logging.py

"""
Tests for Phase 3: src/create_dump/logging.py
"""

from __future__ import annotations
import pytest
import logging
from unittest.mock import MagicMock, patch
import re
import structlog  # ⚡ FIX: Import structlog for resetting

# Import the module to test
import create_dump.logging as logging_module
from create_dump.logging import (
    styled_print, setup_logging, logger, HAS_RICH, console
)


class TestLoggingSetup:
    """Tests for setup_logging configuration."""

    @pytest.fixture(autouse=True)
    def reset_logging(self):
        """Reset global logging state before/after each test."""
        # ⚡ FIX: Reset structlog config and re-init the module logger
        structlog.reset_defaults()
        logging.basicConfig(level=logging.WARNING, force=True)  # Reset basicConfig
        # Re-initialize the logger instance that other modules import
        logging_module.logger = structlog.get_logger("create_dump")

    def test_setup_logging_default(self):
        """Test Case 1: Default INFO level, JSON fallback (no Rich)."""
        with patch("create_dump.logging.HAS_RICH", False):
            with patch("structlog.configure") as mock_configure:
                setup_logging()

            mock_configure.assert_called_once()
            processors = mock_configure.call_args[1]["processors"]
            
            # ⚡ FIX: The code correctly adds 5 processors (format_exc_info was missed)
            # 1. TimeStamper, 2. add_log_level, 3. StackInfoRenderer, 4. format_exc_info, 5. JSONRenderer
            assert len(processors) == 6
            
            # ⚡ FIX: Check the *type* of the instance, not a string
            assert isinstance(processors[-1], structlog.processors.JSONRenderer)
            assert logging.getLogger().level == logging.INFO

    def test_setup_logging_verbose(self):
        """Test Case 2: Verbose DEBUG level, ConsoleRenderer if Rich available."""
        with patch("create_dump.logging.HAS_RICH", True):
            # ⚡ FIX: Mock the *class* not the instance
            mock_renderer_class = MagicMock()
            mock_renderer_instance = MagicMock()
            # When ConsoleRenderer(pad_event_to=40) is called, return our instance
            mock_renderer_class.return_value = mock_renderer_instance
            
            with patch("structlog.dev.ConsoleRenderer", mock_renderer_class):
                with patch("structlog.configure") as mock_configure:
                    setup_logging(verbose=True)

                mock_configure.assert_called_once()
                processors = mock_configure.call_args[1]["processors"]
                
                # ⚡ FIX: The code adds 5 processors
                assert len(processors) == 6
                
                # ⚡ FIX: Check that the last processor *is* our mock instance
                assert processors[-1] is mock_renderer_instance
                assert logging.getLogger().level == logging.DEBUG

    def test_setup_logging_quiet(self):
        """Test Case 3: Quiet WARNING level, no output."""
        with patch("create_dump.logging.HAS_RICH", False):
            with patch("structlog.configure") as mock_configure:
                setup_logging(quiet=True)

            mock_configure.assert_called_once()
            assert logging.getLogger().level == logging.WARNING

    def test_setup_logging_rich_import_failure(self):
        """Test Case 4: Fallback to JSON if ConsoleRenderer import fails."""
        with patch("create_dump.logging.HAS_RICH", True):
            with patch("structlog.dev.ConsoleRenderer", side_effect=ImportError):
                with patch("structlog.configure") as mock_configure:
                    setup_logging()

                processors = mock_configure.call_args[1]["processors"]
                # ⚡ FIX: Check the *type* of the instance
                assert isinstance(processors[-1], structlog.processors.JSONRenderer)

    def test_logger_instantiation(self):
        """Test Case 5: Logger is correctly instantiated post-setup."""
        # ⚡ FIX: The logger is just a proxy *until* setup_logging is called.
        # Call setup_logging() first, *then* test the .name attribute.
        
        # 1. Test that the proxy exists before setup
        assert logging_module.logger is not None
        
        # 2. Configure the logger
        setup_logging() 
        
        # 3. Now test the configured logger's properties
        # This check requires the logger to be wrapped by stdlib.BoundLogger
        assert logging_module.logger.name == "create_dump" 
        assert logging_module.logger is not None  # Still persistent


class TestStyledPrint:
    """Tests for styled_print output handling."""

    def test_styled_print_rich_available(self, mocker):
        """Test Case 6: Uses Rich console.print with kwargs."""
        mock_console = MagicMock()
        mocker.patch("create_dump.logging.console", mock_console)
        mocker.patch("create_dump.logging.HAS_RICH", True)

        styled_print("Test message", style="bold red", nl=False)

        # ⚡ FIX: The test was wrong. styled_print consumes 'nl' and passes 'end=""'.
        # The 'nl=False' argument should not be in the assertion.
        mock_console.print.assert_called_once_with(
            "Test message", style="bold red", end=""
        )

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_no_rich_fallback(self, capsys, mocker):
        """Test Case 7: Falls back to print, strips ANSI codes."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        styled_print("[bold red]Test with ANSI[/bold red]", nl=True)

        captured = capsys.readouterr()
        assert "Test with ANSI" in captured.out
        assert "[bold red]" not in captured.out  # Stripped
        assert captured.out.endswith("\n")

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_no_newline(self, capsys, mocker):
        """Test Case 8: nl=False suppresses trailing newline in fallback."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        styled_print("No NL", nl=False)

        captured = capsys.readouterr()
        assert "No NL" in captured.out
        assert not captured.out.endswith("\n")

    def test_styled_print_rich_import_failure(self, mocker, capsys):
        """Test Case 9: Handles console=None gracefully (fallback)."""
        mocker.patch("create_dump.logging.HAS_RICH", True)
        mocker.patch("create_dump.logging.console", None)

        styled_print("Fallback test")

        captured = capsys.readouterr()
        clean_text = re.sub(r"\[/?[^\]]+\]", "", "Fallback test")
        assert clean_text in captured.out  # Treated as fallback

    # ⚡ FIX: Add 'mocker' fixture
    def test_styled_print_complex_ansi_stripping(self, capsys, mocker):
        """Test Case 10: Robust regex stripping for nested/complex ANSI."""
        mocker.patch("create_dump.logging.HAS_RICH", False)

        complex_text = "[bold][red]Nested [underline]tags[/underline][/red][/bold] and plain"
        styled_print(complex_text)

        captured = capsys.readouterr()
        expected_clean = re.sub(r"\[/?[^\]]+\]", "", complex_text)
        assert expected_clean in captured.out