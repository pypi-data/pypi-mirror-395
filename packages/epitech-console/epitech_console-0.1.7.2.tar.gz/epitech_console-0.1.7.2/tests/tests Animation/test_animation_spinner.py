import pytest


from epitech_console.Animation import Animation
from epitech_console.Animation import Spinner


def test_spinner_stick(
    ) -> None:
    sp = Spinner.stick()
    assert isinstance(sp, Animation)
    assert len(sp.animation) > 0


def test_spinner_plus(
    ) -> None:
    sp = Spinner.plus()
    assert isinstance(sp, Animation)
    assert len(sp.animation) > 0


def test_spinner_cross(
    ) -> None:
    sp = Spinner.cross()
    assert isinstance(sp, Animation)
    assert len(sp.animation) > 0


def test_spinner_updates_correctly(
    ) -> None:
    sp = Spinner.stick()
    first = sp.render()
    sp.update()
    second = sp.render()
    assert first != second
