import pytest


from epitech_console.Animation import Animation


def test_animation_initialization_with_list(
    ) -> None:
    frames = ["A", "B", "C"]
    anim = Animation(frames)
    assert anim.animation == frames
    assert anim.step == 0
    assert anim.render().replace("\033[0m", "") == "A"


def test_animation_initialization_with_string(
    ) -> None:
    anim = Animation("X\\Y\\Z")
    assert anim.animation == ["X", "Y", "Z"]
    assert anim.render().replace("\033[0m", "") == "X"


def test_animation_update_basic(
    ) -> None:
    anim = Animation(["A", "B", "C"])
    assert anim.render().replace("\033[0m", "") == "A"
    anim.update()
    assert anim.render().replace("\033[0m", "") == "B"
    anim.update()
    assert anim.render().replace("\033[0m", "") == "C"


def test_animation_update_auto_reset_enabled(
    ) -> None:
    anim = Animation(["A", "B"])
    anim.update()  # index 1
    anim.update()  # auto-reset to 0
    assert anim.render().replace("\033[0m", "") == "A"


def test_animation_update_auto_reset_disabled(
    ) -> None:
    anim = Animation(["A", "B"])
    anim.update(auto_reset=False)
    anim.update(auto_reset=False)
    # Stays on last frame
    assert anim.render().replace("\033[0m", "") == "B"


def test_animation_render_delete_flag(
    ) -> None:
    anim = Animation(["A"])
    output = anim.render(delete=True).replace("\033[0m", "")
    # Output MUST include delete sequence and frame
    assert isinstance(output, str)
    assert output == "\033[1F\033[2KA"


def test_animation_length_magic_method(
    ) -> None:
    anim = Animation(["A", "B", "C"])
    assert len(anim) == 3
