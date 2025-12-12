#############################
###                       ###
###    Epitech Console    ###
###    ----style.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Style:
    """
        Style class.

        Progress-bar style.
    """


    def __init__(
            self,
            on : str = "#",
            off : str = "-",
            arrow_left : str = "<",
            arrow_right : str = ">",
            border_left : str = "|",
            border_right : str = "|"
        ) -> None:
        """
        """

        self.on = on
        self.off = off
        self.arrow_left = arrow_left
        self.arrow_right = arrow_right
        self.border_left = border_left
        self.border_right = border_right


    def __str__(
            self
        ) -> str:
        """
        """

        return (
            f'on="{self.on}";off="{self.off}";' +
            f'arrow_left="{self.arrow_left}";arrow_right"{self.arrow_right}";' +
            f'border_left="{self.border_left}";border_right"{self.border_right}"' +
            f'\n\nExample:' +
            f'\n"{self.border_left}{self.on}{self.on}{self.arrow_right}{self.off}{self.off}{self.off}{self.border_right}"'
        )