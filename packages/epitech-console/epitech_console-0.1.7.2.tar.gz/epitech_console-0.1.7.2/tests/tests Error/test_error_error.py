import pytest


from epitech_console.Error import Error


def test_error_default_constructor(
    ) -> None:
    err = Error()
    assert err.message == "an error occurred"
    assert err.error == "Error"
    assert err.link is None
    assert isinstance(err, Error)


def test_error_full_constructor(
    ) -> None:
    err = Error("Something broke", error="SystemError", link=("path/file.py", 42))
    assert err.message == "Something broke"
    assert err.error == "SystemError"
    assert str(err.link) == '\033]8;;jetbrains://clion/navigate/reference?file=path/file.py&line=42\033\\File "path/file.py", line 42\033]8;;\033\\'


def test_error_str_without_link(
    ) -> None:
    err = Error("Broken", error="RuntimeError")
    s = str(err)

    assert "RuntimeError" in s
    assert "Broken" in s
    assert "File" not in s
    assert "line" not in s


def test_error_str_with_link(
    ) -> None:
    err = Error("Crash detected", error="FatalError", link=("engine.py", 88))
    s = str(err)

    assert "FatalError" in s
    assert "Crash detected" in s
    assert "engine.py" in s
    assert "88" in s
    assert "File" in s
    assert "line" in s


def test_error_str_formatting_clean(
    ) -> None:
    err = Error("X", error="Y", link=("a.py", 5))
    output = str(err).replace("\n", " ").strip()

    assert "Y" in output
    assert "X" in output
    assert "a.py" in output
    assert "5" in output


def test_link_negative_line_number_disallowed(
    ) -> None:
    err = Error("msg", error="Err", link=("file.py", -1))
    assert not err.link


def test_empty_message_and_error_are_allowed(
    ) -> None:
    err = Error("", error="")
    assert err.message == ""
    assert err.error == ""
