import pytest


from epitech_console.System import Config


def test_config_exist_returns_false(
    ) -> None:
    assert not Config.exist("tests")


def test_config_create_and_dont_exist(
    ) -> None:
    data = {"SECTION1": {"key11": "value11", "key12": "value12"}, "SECTION2": {"key21": "value21", "key22": "value22"}}
    Config("tests", data)

    assert Config.exist("tests")


def test_config_create_and_exist(
    ) -> None:
    data = {"SECTION1": {"key11": "value11", "key12": "value12"}, "SECTION2": {"key21": "value21", "key22": "value22"}}
    Config("tests", data)

    assert Config.exist("tests")


def test_config_read(
    ) -> None:
    result = Config("tests")
    assert result.get("SECTION1", "key11") == "value11"
    assert result.get("SECTION1", "key12") == "value12"
    assert result.get("SECTION2", "key21") == "value21"
    assert result.get("SECTION2", "key22") == "value22"


def test_config_delete_cached(
    ) -> None:
    config = Config("tests")
    config.delete("tests", cached=True)
    assert config.config
    assert not Config.exist("tests")


def test_config_delete_not_cached(
    ) -> None:
    config = Config("tests")
    config.delete("tests")
    assert not config.config
    assert not Config.exist("tests")
