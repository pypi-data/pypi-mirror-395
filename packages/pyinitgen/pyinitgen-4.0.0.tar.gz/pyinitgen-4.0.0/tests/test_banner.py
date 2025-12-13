# tests/test_banner.py

import pytest
from pyinitgen.banner import lerp, blend, print_logo

# Use the 'mocker' fixture from pytest-mock

def test_lerp():
    assert lerp(0, 10, 0.5) == 5.0
    assert lerp(10, 20, 0.5) == 15.0
    assert lerp(0, 100, 0.0) == 0.0
    assert lerp(0, 100, 1.0) == 100.0

def test_blend():
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)

    # Test t=0
    result = blend(c1, c2, 0)
    assert result == "#000000"

    # Test t=1
    result = blend(c1, c2, 1)
    assert result.startswith("#")
    assert len(result) == 7

def test_blend_edge_cases():
    """
    Test the blend function with edge-case t values.
    """
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)
    assert blend(c1, c2, 0.0) == "#000000"

    result = blend(c1, c2, 1.0)
    assert result.startswith("#")
    assert result != "#ffffff"

def test_print_logo(mocker):
    # Mock 'console' object in pyinitgen.banner
    mock_console = mocker.patch("pyinitgen.banner.console")

    print_logo()

    assert mock_console.print.called
    assert mock_console.print.call_count > 1

    # Verify the footer by checking the last call
    # call_args_list returns a list of Call objects (which are tuples)
    last_call = mock_console.print.call_args_list[-1]
    # args is the first element of the Call object
    last_call_args = last_call[0]
    expected_footer = "[dim]🐍 Automatically generate __init__.py files for Python packages.[/dim]\\n"
    assert last_call_args[0] == expected_footer

def test_print_logo_procedural_palette(mocker, monkeypatch):
    """
    Test that print_logo can generate a procedural palette
    when no fixed palette is specified.
    """
    mock_console = mocker.patch("pyinitgen.banner.console")
    # Ensure env var is unset (though conftest handles this, being explicit is safe)
    monkeypatch.delenv("CREATE_DUMP_PALETTE", raising=False)

    print_logo()
    assert mock_console.print.called
    assert mock_console.print.call_count > 1

def test_print_logo_with_fixed_palette(mocker, monkeypatch):
    """
    Test that print_logo uses a fixed palette when the env var is set.
    """
    mock_console = mocker.patch("pyinitgen.banner.console")
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "0")

    print_logo()
    assert mock_console.print.called
    assert mock_console.print.call_count > 1

def test_print_logo_with_invalid_palette_fallback(mocker, monkeypatch):
    """
    Test that print_logo falls back to procedural generation
    if an invalid palette index is provided.
    """
    mock_console = mocker.patch("pyinitgen.banner.console")
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "invalid")

    print_logo()
    assert mock_console.print.called
    assert mock_console.print.call_count > 1

def test_print_logo_with_large_invalid_palette_fallback(mocker, monkeypatch):
    """
    Test fallback for an out-of-range integer palette index.
    """
    mock_console = mocker.patch("pyinitgen.banner.console")
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "9999")

    print_logo()
    assert mock_console.print.called
    assert mock_console.print.call_count > 1
