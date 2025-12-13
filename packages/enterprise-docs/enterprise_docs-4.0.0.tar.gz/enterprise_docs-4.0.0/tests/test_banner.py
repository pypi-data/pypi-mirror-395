# tests/test_banner.py


import pytest
import math
from unittest.mock import MagicMock
from enterprise_docs import banner

def test_lerp():
    assert banner.lerp(0, 10, 0.5) == 5.0
    assert banner.lerp(0, 10, 0.0) == 0.0
    assert banner.lerp(0, 10, 1.0) == 10.0
    assert banner.lerp(10, 20, 0.5) == 15.0

def test_blend():
    # Test blend functionality
    # blend(c1, c2, t) returns a hex string
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)

    # t=0 should be close to c1
    result_0 = banner.blend(c1, c2, 0.0)
    assert result_0 == "#000000"

    # t=1 is not directly testable easily because of the gamma correction and wave shaping in blend
    # but we can test that it returns a string starting with #
    result = banner.blend(c1, c2, 0.5)
    assert isinstance(result, str)
    assert result.startswith("#")
    assert len(result) == 7

def test_print_logo(mocker):
    # Mock console.print to verify it's called
    mock_console_print = mocker.patch.object(banner.console, 'print')

    banner.print_logo()

    # print_logo calls console.print multiple times (once for each line of the logo + 1 for the text)
    assert mock_console_print.call_count > 0

    # Verify the last call was the text
    args, _ = mock_console_print.call_args
    assert "[dim]🏗️ Enforce documentation standards and consistency across enterprise projects.[/dim]" in str(args[0])
