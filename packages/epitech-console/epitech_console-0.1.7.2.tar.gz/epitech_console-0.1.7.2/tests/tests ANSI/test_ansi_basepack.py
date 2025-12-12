import pytest


from epitech_console.ANSI import BasePack
from epitech_console.ANSI import ANSI


def test_basepack_has_attributes(
    ) -> None:
    assert hasattr(BasePack, "P_ERROR")
    assert hasattr(BasePack, "P_WARNING")
    assert hasattr(BasePack, "P_OK")
    assert hasattr(BasePack, "P_INFO")


def test_basepack_types(
    ) -> None:
    assert isinstance(BasePack.P_ERROR, tuple)
    assert isinstance(BasePack.P_WARNING, tuple)
    assert isinstance(BasePack.P_OK, tuple)
    assert isinstance(BasePack.P_INFO, tuple)


def test_basepack_update(
    ) -> None:
    before = str(BasePack.P_ERROR)
    BasePack.update()
    after = str(BasePack.P_ERROR)
    assert isinstance(BasePack.P_ERROR[0], ANSI)
    assert "\033[41m" == BasePack.P_ERROR[0].sequence
    assert before == after
