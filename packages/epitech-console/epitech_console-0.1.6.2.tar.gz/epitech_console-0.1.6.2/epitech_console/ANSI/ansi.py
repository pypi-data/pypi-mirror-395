#############################
###                       ###
###    Epitech Console    ###
###    ----ansi.py----    ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any
from epitech_console.Text.format import Format


class ANSI(Format):
    """
        ANSI class.

        ANSI string tool.

        Attributes:
            ESC (str) : ANSI escape (ANSI sequence starter).
    """


    ESC: str = "\033["


    def __init__(
            self,
            sequence : list[Any | str] | str = ""
        ) -> None:
        """
            Create an ANSI sequence.

            Parameters:
                sequence (list[ANSI | str] | str): ANSI sequence
        """

        self.sequence : str = ""

        if type(sequence) in [list]:
            for item in sequence:
                self.sequence += str(item)

        else:
            self.sequence = sequence


    def __add__(
            self,
            other : Any | str | int
        ) -> Any:
        """
            Add 2 ANSI sequences together.

            Parameters:
                other (ANSI | Animation | StopWatch | ProgressBar | Text | str): ANSI sequence

            Returns:
                ANSI: ANSI sequence
        """

        from epitech_console.Animation.animation import Animation
        from epitech_console.Animation.progressbar import ProgressBar
        from epitech_console.Text.text import Text
        from epitech_console.System.stopwatch import StopWatch

        if type(other) in [ANSI]:
            return ANSI(f"{self.sequence}{other.sequence}")

        elif type(other) in [Animation, StopWatch, ProgressBar, Text, str]:
            return ANSI(f"{self.sequence}{str(other)}")

        else:
            return ANSI("")


    def __str__(
            self
        ) -> str :
        """
            Convert ANSI object to string.

            Returns:
                str: ANSI string
        """

        return str(self.sequence)


    def __len__(
            self
        ) -> int:
        """
            Return the number of ANSI sequences.
        """

        return len(self.sequence)
