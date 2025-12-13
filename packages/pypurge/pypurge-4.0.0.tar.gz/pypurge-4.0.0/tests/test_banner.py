
import pytest
from unittest.mock import patch
from pypurge.banner import print_logo, lerp, blend

def test_print_logo_default():
    with patch("rich.console.Console.print") as mock_print:
        print_logo()
        assert mock_print.call_count > 1

def test_lerp():
    assert lerp(0, 10, 0.5) == 5
    assert lerp(10, 20, 0) == 10
    assert lerp(10, 20, 1) == 20

def test_blend():
    c1 = (255, 105, 180)
    c2 = (147, 112, 219)

    assert blend(c1, c2, 0) == f"#{c1[0]:02x}{c1[1]:02x}{c1[2]:02x}"

    color = blend(c1, c2, 1)
    assert isinstance(color, str)
    assert color.startswith("#")
    assert len(color) == 7

    color_half = blend(c1, c2, 0.5)
    assert isinstance(color_half, str)
    assert color_half.startswith("#")
    assert len(color_half) == 7

    with patch("rich.console.Console.print") as mock_print:
        print_logo()
        assert mock_print.call_count > 1

def test_print_logo_fixed_palette(monkeypatch):
    """Test logo printing with a fixed palette index."""
    monkeypatch.setenv("CREATE_DUMP_PALETTE", "0")
    with patch("rich.console.Console.print") as mock_print:
        print_logo()
        assert mock_print.call_count > 1
