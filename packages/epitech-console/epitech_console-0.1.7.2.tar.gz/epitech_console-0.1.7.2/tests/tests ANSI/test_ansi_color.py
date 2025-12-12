import pytest

from epitech_console.ANSI import Color
from epitech_console.ANSI import ANSI


def test_rgb_fg_valid(
    ) -> None:
    seq = Color.rgb_fg(10, 20, 30)
    assert str(seq) == "\033[38;2;10;20;30m"


def test_rgb_bg_valid(
    ) -> None:
    seq = Color.rgb_bg(100, 150, 200)
    assert str(seq) == "\033[48;2;100;150;200m"


def test_rgb_fg_invalid_range(
    ) -> None:
    assert str(Color.rgb_fg(-1, 10, 10)) == ""
    assert str(Color.rgb_fg(10, 256, 10)) == ""


def test_static_colors(
    ) -> None:
    color = Color.color(Color.C_RESET)
    assert isinstance(color, ANSI)
    assert str(color) == "\033[0m"


def test_epitech_fg(
    ) -> None:
    seq = Color.epitech_fg()
    assert str(seq) == "\033[38;2;0;145;211m"


def test_epitech_dark_fg(
    ) -> None:
    seq = Color.epitech_dark_fg()
    assert str(seq) == "\033[38;2;31;72;94m"


def test_len_color(
    ) -> None:
    assert len(Color.color_fg(Color.C_FG_RED)) == len("\033[38;5;31m")
