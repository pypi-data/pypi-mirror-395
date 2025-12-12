import pytest


from epitech_console.ANSI import ANSI


def test_ansi_empty_init(
    ) -> None:
    a = ANSI()
    assert str(a) == ""


def test_ansi_string_init(
    ) -> None:
    a = ANSI("\033[31m")
    assert str(a) == "\033[31m"


def test_ansi_addition(
    ) -> None:
    a = ANSI("\033[31m")
    b = ANSI("\033[1m")
    c = a + b
    assert str(c) == "\033[31m\033[1m"


def test_ansi_len(
    ) -> None:
    a = ANSI("\033[31m")
    assert len(a) == len("\033[31m")


def test_ansi_repr(
    ) -> None:
    a = ANSI("\033[32m")
    r = repr(a)
    assert r == "ANSI(\"\033[32m\")"


def test_ansi_add_with_str(
    ) -> None:
    a = ANSI("\033[31m")
    c = a + "hello"
    assert str(c) == "\033[31mhello"


def test_ansi_invalid_add(
    ) -> None:
    a = ANSI("\033[31m")
    b = a + 123
    assert str(b) == str(a)
