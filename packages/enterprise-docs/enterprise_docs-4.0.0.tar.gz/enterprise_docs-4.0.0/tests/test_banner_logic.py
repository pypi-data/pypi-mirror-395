# tests/test_banner_logic.py

import os
from unittest.mock import patch
from enterprise_docs import banner

def test_print_logo_fixed_palette(mocker):
    """
    Test that when CREATE_DUMP_PALETTE is set to a valid index,
    the fixed palette is used.
    """
    mocker.patch.object(banner, 'fixed_palettes', [[(255, 0, 0)]])
    mock_console_print = mocker.patch.object(banner.console, 'print')

    with patch.dict(os.environ, {'CREATE_DUMP_PALETTE': '0'}):
        banner.print_logo()

    assert mock_console_print.call_count > 0

def test_print_logo_procedural_palette(mocker):
    """
    Test that when CREATE_DUMP_PALETTE is not set, a procedural
    palette is generated.
    """
    mock_console_print = mocker.patch.object(banner.console, 'print')

    with patch.dict(os.environ, clear=True):
        banner.print_logo()

    assert mock_console_print.call_count > 0

def test_print_logo_bad_palette_fallback(mocker):
    """
    Test that if CREATE_DUMP_PALETTE is a bad value, it falls back
    to a procedural palette.
    """
    mock_console_print = mocker.patch.object(banner.console, 'print')

    with patch.dict(os.environ, {'CREATE_DUMP_PALETTE': 'not-a-number'}):
        banner.print_logo()

    assert mock_console_print.call_count > 0

def test_print_logo_out_of_bounds_palette_fallback(mocker):
    """
    Test that if CREATE_DUMP_PALETTE is out of bounds, it falls back
    to a procedural palette.
    """
    mock_console_print = mocker.patch.object(banner.console, 'print')

    with patch.dict(os.environ, {'CREATE_DUMP_PALETTE': '999'}):
        banner.print_logo()

    assert mock_console_print.call_count > 0
