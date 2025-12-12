import pytest


from epitech_console.Animation import Animation
from epitech_console.Animation import ProgressBar
from epitech_console.Animation import Spinner


def test_progressbar_initialization(
    ) -> None:
    pb = ProgressBar(10)
    assert pb.length == 10
    assert pb.percent == 0
    assert pb.style.on == "#"
    assert pb.style.off == "-"
    assert isinstance(pb.animation, Animation) or pb.animation is None


def test_progressbar_update_basic(
    ) -> None:
    pb = ProgressBar(10)
    pb.update(50)
    assert pb.percent == 50


def test_progressbar_update_spinner_flag(
    ) -> None:
    sp = Spinner.plus()
    pb = ProgressBar(10, spinner=sp)

    first = pb.spinner.render().replace("\033[0m", "")
    pb.update(20, update_spinner=True)
    second = pb.spinner.render().replace("\033[0m", "")

    assert first != second


def test_progressbar_update_no_spinner(
    ) -> None:
    sp = Spinner.plus()
    pb = ProgressBar(10, spinner=sp)

    first = pb.spinner.render().replace("\033[0m", "")
    pb.update(20, update_spinner=False)
    second = pb.spinner.render().replace("\033[0m", "")

    assert first == second


def test_progressbar_render_basic(
    ) -> None:
    pb = ProgressBar(10)
    pb.update(40)
    result = str(pb.render()).replace("\033[0m", "")
    assert isinstance(result, str)
    assert "|" in result and "#" in result and ">" in result and "-" in result


def test_progressbar_render_hide_spinner_at_end(
    ) -> None:
    sp = Spinner.stick()
    pb = ProgressBar(10, spinner=sp)

    pb.update(100)
    result = str(pb.render(hide_spinner_at_end=True))

    assert isinstance(result, str)
    assert sp.render().replace("\033[0m", "") not in result  # spinner hidden


def test_progressbar_render_delete_flag(
    ) -> None:
    pb = ProgressBar(10)
    result = str(pb.render(delete=True)).replace("\033[0m", "")
    assert isinstance(result, str)


def test_progressbar_percent_style_bar(
    ) -> None:
    pb = ProgressBar(10, percent_style="bar")
    pb.update(60)
    text = str(pb.render()).replace("\033[0m", "")
    # Expect filling using style.on
    assert "#" in text


def test_progressbar_percent_style_number(
    ) -> None:
    pb = ProgressBar(10, percent_style="num")
    pb.update(60)
    text = str(pb.render()).replace("\033[0m", "")
    # Expect percentage
    assert text.split()[-1] == "60%"


def test_progressbar_percent_style_mix(
    ) -> None:
    pb = ProgressBar(length=10, percent_style="mix")
    pb.update(60)
    text = str(pb.render()).replace("\033[0m", "")
    # Mix style includes both bar and percent digits
    assert "#" in text
    assert "%" in text
