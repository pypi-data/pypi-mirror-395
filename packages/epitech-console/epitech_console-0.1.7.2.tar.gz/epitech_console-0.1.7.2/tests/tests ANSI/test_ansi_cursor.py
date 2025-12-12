import pytest


from epitech_console.ANSI import Cursor


def test_cursor_up(
    ) -> None:
    assert str(Cursor.up(3)) == "\033[3A"


def test_cursor_down(
    ) -> None:
    assert str(Cursor.down(2)) == "\033[2B"


def test_cursor_left(
    ) -> None:
    assert str(Cursor.left(5)) == "\033[5D"


def test_cursor_right(
    ) -> None:
    assert str(Cursor.right(7)) == "\033[7C"


def test_cursor_top(
    ) -> None:
    assert str(Cursor.top()) == "\033[H"


def test_cursor_previous(
    ) -> None:
    assert str(Cursor.previous(2)) == "\033[2F"


def test_cursor_next(
    ) -> None:
    assert str(Cursor.next(4)) == "\033[4E"


def test_cursor_move(
    ) -> None:
    assert str(Cursor.move(5, 10)) == "\033[10;5H"


def test_cursor_move_column(
    ) -> None:
    assert str(Cursor.move_column(15)) == "\033[15G"


def test_cursor_save(
    ) -> None:
    assert str(Cursor.set()) == "\033[7"


def test_cursor_restore(
    ) -> None:
    assert str(Cursor.reset()) == "\033[8"


def test_cursor_hide():
    assert str(Cursor.hide()) == "\033[25l"


def test_cursor_show():
    assert str(Cursor.show()) == "\033[25h"
