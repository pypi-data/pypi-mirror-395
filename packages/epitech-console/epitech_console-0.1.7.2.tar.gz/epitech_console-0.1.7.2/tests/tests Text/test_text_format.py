import pytest


from epitech_console.Text import Text
from epitech_console.Text import Format



def test_format_reset():
    text = Text("hi")
    s = text.reset()
    assert isinstance(s, Text)
    assert str(s) == "\033[0mhi"


def test_format_bold():
    text = Text("hi")
    s = text.bold()
    assert isinstance(s, Text)
    assert str(s) == "\033[1mhi"


def test_format_italic():
    text = Text("hi")
    s = text.italic()
    assert isinstance(s, Text)
    assert str(s) == "\033[3mhi"


def test_format_underline():
    text = Text("hi")
    s = text.underline()
    assert isinstance(s, Text)
    assert str(s) == "\033[4mhi"


def test_format_hide():
    text = Text("hi")
    s = text.hide()
    assert isinstance(s, Text)
    assert str(s) == "\033[8mhi"


def test_format_strikethrough():
    text = Text("hi")
    s = text.strikethrough()
    assert isinstance(s, Text)
    assert str(s) == "\033[9mhi"


"""
def test_format_apply_to_text():
    t = Text("hi")
    result = Format.apply(t, sequence=Format.bold())
    assert "\033[" in result
    assert "hi" in result

def test_format_apply_to_str():
    result = Format.apply("hello", sequence=Format.italic())
    assert "\033[" in result
    assert "hello" in result


def test_format_apply_without_sequence_uses_reset():
    result = Format.apply("hello")
    assert "\033[" in result


def test_format_apply_invalid_target():
    with pytest.raises(TypeError):
        Format.apply(123, sequence=Format.bold())


def test_format_tree_dict():
    data = {
        "folder": {
            "file1": None,
            "subfolder": {"file2": None},
        }
    }
    tree_output = Format.tree(data, title="Project")

    # basic structure checks
    assert "Project" in tree_output
    assert "folder" in tree_output
    assert "file1" in tree_output
    assert "subfolder" in tree_output
    assert "file2" in tree_output


def test_format_tree_list():
    data = ["a", "b", "c"]
    tree_output = Format.tree(data, title="List")

    assert "List" in tree_output
    assert "a" in tree_output
    assert "b" in tree_output
    assert "c" in tree_output


def test_format_tree_string():
    tree_output = Format.tree("hello", title="String")

    assert "String" in tree_output
    assert "hello" in tree_output


def test_format_module_tree():
    output = Format.module_tree()

    # check that the tree contains the expected root
    assert "epitech_console" in output
"""
