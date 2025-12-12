#############################
###                       ###
###    Epitech Console    ###
###   ----spinner.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Spinner:
    """
        ProgressBar class.

        Progress-bar tool.
    """


    from epitech_console.Animation.animation import Animation
    from epitech_console.Animation.style import Style


    @staticmethod
    def stick(
            *,
            style : Any = Style("#", " ", "#", "#", "", "")
        ) -> Animation:
        """
            Stick spinner.

            Returns:
                Animation: Stick animation.
        """

        from epitech_console.Animation.animation import Animation

        return Animation(
            [
                f"{style.border_left}-{style.border_right}",
                f"{style.border_left}\\{style.border_right}",
                f"{style.border_left}|{style.border_right}",
                f"{style.border_left}/{style.border_right}"
            ]
        )


    @staticmethod
    def plus(
            *,
            style : Any = Style("#", " ", "#", "#", "", "")
        ) -> Animation:
        """
            Plus spinner.

            Returns:
                Animation: Plus animation.
        """

        from epitech_console.Animation.animation import Animation

        return Animation(
            [
                f"{style.border_left}-{style.border_right}",
                f"{style.border_left}|{style.border_right}"
            ]
        )


    @staticmethod
    def cross(
            *,
            style : Any = Style("#", " ", "#", "#", "", "")
        ) -> Animation:
        """
            Cross spinner.

            Returns:
                Animation: Cross animation.
        """

        from epitech_console.Animation.animation import Animation

        return Animation(
            [
                f"{style.border_left}/{style.border_right}",
                f"{style.border_left}\\{style.border_right}"
            ]
        )
