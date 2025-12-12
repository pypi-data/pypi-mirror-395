import pytest
from epitech_console.ANSI import Line


def test_clear_line(
    ) -> None:
    assert str(Line.clear_line()) == "\033[2K"


def test_clear_start_line(
    ) -> None:
    assert str(Line.clear_start_line()) == "\033[1K"


def test_clear_end_line(
    ) -> None:
    assert str(Line.clear_end_line()) == "\033[K"


def test_clear_screen(
    ) -> None:
    assert str(Line.clear_screen()) == "\033[2J"


def test_clear(
    ) -> None:
    assert str(Line.clear()) == "\033[2J\033[H"


def test_clear_previous_line(
    ) -> None:
    assert str(Line.clear_previous_line()) == "\033[1F\033[2K"
