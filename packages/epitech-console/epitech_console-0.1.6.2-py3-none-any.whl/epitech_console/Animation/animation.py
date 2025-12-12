#############################
###                       ###
###    Epitech Console    ###
###  ----animation.py---- ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any
from epitech_console.Text.format import Format


class Animation(Format):
    """
        Animation class.

        Animation tool.
    """

    from epitech_console.ANSI.color import Color


    def __init__(
            self,
            animation : list[str | Any] | str = ""
        ) -> None:
        """
            Create an animation.

            Parameters:
                animation (list[str] | str): list of step
        """

        self.animation : list[str] = []

        if isinstance(animation, list):
            for step in animation:
                self.animation.append(str(step))

        else:
            self.animation = [animation]

        self.length : int = len(self.animation)
        self.step : int = 0


    def __add__(
            self,
            other : Any | str
        ) -> Any:
        """
            Add 2 Animations together.

            Parameters:
                other (Animation | ANSI | Text | StopWatch | str): Animation

            Returns:
                Animation: Animation
        """

        from epitech_console.Text.text import Text
        from epitech_console.ANSI.ansi import ANSI
        from epitech_console.System.stopwatch import StopWatch

        if type(other) in [Animation]:
            return Animation(self.animation + other.animation)

        elif type(other) in [Text, StopWatch, ANSI, str]:
            return Animation(self.animation + [str(other)])

        else:
            return Animation([])


    def __getitem__(
            self,
            item : int
        ) -> str :
        """
            Get the current step of the animation and convert it to a string.

            Returns:
                str: Animation string
        """

        if self.is_last():
            return str(self.animation[self.length - 1])

        return str(self.animation[item])


    def __str__(
            self,
            *,
            color : Any = Color.C_RESET
        ) -> str :
        """
            Convert Animation object to string.

            Returns:
                str: Animation string
        """

        from epitech_console.ANSI.color import Color

        return f"{color}{str(self[self.step])}{Color.color(Color.C_RESET)}"


    def __call__(
            self,
        ) -> None:
        """
            Do a step of the animation.
        """

        self.update(auto_reset=True)


    def __len__(
            self
        ) -> int:
        """
            Return the number of steps of the animation.
        """

        return self.length


    def update(
            self,
            *,
            auto_reset: bool = True
        ) -> None:
        """
            Add a step to the animation.

            Parameters:
                auto_reset (bool): Automatically reset the animation. Defaults to False.
        """

        self.step += 1

        if self.is_last() and auto_reset:
            self.reset()

        return None


    def render(
            self,
            *,
            delete : bool = False
        ) -> str:
        """
            Convert Animation object to string.

            Returns:
                str: Animation string
        """

        from epitech_console.ANSI.line import Line

        string : str = ""

        if delete:
            string += str(Line.clear_previous_line())

        string += str(self)

        return string


    def is_last(
            self
        ) -> bool:
        """
            Return whether it is or not the last step of the animation.

            Returns:
                bool: is the last step
        """

        return self.step >= self.length

    def reset(
            self
        ) -> None:
        """
            Reset the animation.
        """

        self.step = 0
