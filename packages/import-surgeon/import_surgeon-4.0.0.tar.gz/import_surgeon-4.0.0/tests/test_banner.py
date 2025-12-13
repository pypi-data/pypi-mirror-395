import pytest
from unittest.mock import patch, MagicMock
from import_surgeon import banner

def test_lerp():
    assert banner.lerp(0, 10, 0.5) == 5
    assert banner.lerp(10, 20, 0) == 10
    assert banner.lerp(10, 20, 1) == 20

def test_blend():
    color1 = (0, 0, 0)
    color2 = (255, 255, 255)
    assert banner.blend(color1, color2, 0.5).startswith("#")

@patch('import_surgeon.banner.console')
def test_print_logo_fixed_palette(mock_console, monkeypatch):
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "0")
    banner.print_logo()
    assert mock_console.print.call_count > 0

@patch('import_surgeon.banner.console')
def test_print_logo_procedural_palette(mock_console, monkeypatch):
    monkeypatch.delenv("CREATE_DUMP_PALETTE", raising=False)
    banner.print_logo()
    assert mock_console.print.call_count > 0

@patch('import_surgeon.banner.console')
def test_print_logo_invalid_palette(mock_console, monkeypatch):
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "invalid")
    banner.print_logo()
    assert mock_console.print.call_count > 0

@patch('import_surgeon.banner.console')
def test_print_logo_out_of_bounds_palette(mock_console, monkeypatch):
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "999")
    banner.print_logo()
    assert mock_console.print.call_count > 0