import pytest
from sys import stderr


from epitech_console.System import Console


def test_console_print_basic(
        capsys
    ) -> None:
    assert str(Console.print("hello")) == "hello\033[0m\n"


def test_console_print_multiple_argument(
        capsys
    ) -> None:
    assert str(Console.print("hello", "world", "!!!")) == "hello world !!!\033[0m\n"


def test_console_print_with_start_end(
        capsys
    ) -> None:
    assert str(Console.print("world", start=">>> ", end=" !!!\n")) == ">>> world\033[0m !!!\n"


def test_console_print_custom_file(
    ) -> None:
    assert str(Console.print("test", file=stderr)) == "test\033[0m\n"
