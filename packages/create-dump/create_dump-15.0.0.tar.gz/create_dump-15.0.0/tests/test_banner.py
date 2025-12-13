# tests/test_banner.py

import pytest
from unittest.mock import MagicMock, patch
import os
import random
from create_dump.banner import print_logo, lerp, blend

def test_global_lerp_and_blend():
    """Test the global lerp and blend functions."""
    assert lerp(0, 10, 0.5) == 5
    assert lerp(10, 20, 0.1) == 11

    # blend takes RGB tuples and t, returns hex string
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)
    # Just checking it returns a string starting with #
    result = blend(c1, c2, 0.5)
    assert result.startswith("#")
    assert len(result) == 7

def test_print_logo_no_env_var(mocker):
    """Test print_logo with no environment variable set (procedural generation)."""
    mocker.patch.dict(os.environ, {}, clear=True)

    # Patch rich.console.Console because print_logo imports it locally
    with patch("rich.console.Console") as MockConsole:
        mock_console_instance = MockConsole.return_value
        print_logo()
        assert mock_console_instance.print.called

def test_print_logo_valid_env_var(mocker):
    """Test print_logo with CREATE_DUMP_PALETTE set to a valid index."""
    mocker.patch.dict(os.environ, {"CREATE_DUMP_PALETTE": "0"})

    with patch("rich.console.Console") as MockConsole:
        mock_console_instance = MockConsole.return_value
        print_logo()
        assert mock_console_instance.print.called

def test_print_logo_invalid_env_var(mocker):
    """Test print_logo with CREATE_DUMP_PALETTE set to an invalid value."""
    mocker.patch.dict(os.environ, {"CREATE_DUMP_PALETTE": "999"})

    with patch("rich.console.Console") as MockConsole:
        mock_console_instance = MockConsole.return_value
        print_logo()
        assert mock_console_instance.print.called

def test_print_logo_non_numeric_env_var(mocker):
    """Test print_logo with CREATE_DUMP_PALETTE set to a non-numeric value."""
    mocker.patch.dict(os.environ, {"CREATE_DUMP_PALETTE": "abc"})

    with patch("rich.console.Console") as MockConsole:
        mock_console_instance = MockConsole.return_value
        print_logo()
        assert mock_console_instance.print.called

def test_print_logo_bias_branch(mocker):
    """Test the occasional bias branch in procedural generation."""
    mocker.patch.dict(os.environ, {}, clear=True)

    # We need to control the random generator.
    # banner.py uses `_sysrand = random.SystemRandom()`
    # Since SystemRandom is instantiated inside print_logo or at module level?
    # It is instantiated inside print_logo: `_sysrand = random.SystemRandom()`
    # AND imported inside print_logo: `import random`

    mock_random = MagicMock()
    # It needs to behave like random.SystemRandom instance.
    # The bias check is: `if _sysrand.random() < 0.25:`
    # We set it to return 0.1 which is < 0.25
    mock_random.random.return_value = 0.1
    # shuffle is also called
    mock_random.shuffle = MagicMock()

    # We patch random.SystemRandom where it is looked up.
    # Inside print_logo, `import random` is used, so we patch `random.SystemRandom`

    with patch("random.SystemRandom", return_value=mock_random):
        with patch("rich.console.Console") as MockConsole:
            mock_console_instance = MockConsole.return_value
            print_logo()
            assert mock_console_instance.print.called
