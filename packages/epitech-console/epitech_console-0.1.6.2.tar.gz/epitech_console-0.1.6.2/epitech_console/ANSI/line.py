#############################
###                       ###
###    Epitech Console    ###
###     ----line.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Line:
    """
        Line class.

        Manipulate the lines of the console.
    """

    from epitech_console.ANSI.ansi import ANSI


    @staticmethod
    def clear_line(
        ) -> ANSI:
        """
            Clear the current line

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}2K")


    @staticmethod
    def clear_start_line(
        ) -> ANSI:
        """
            Clear the current line from the start to the cursor's position

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}1K")


    @staticmethod
    def clear_end_line(
        ) -> ANSI:
        """
            Clear the current line from the cursor's position to the end

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}K")


    @staticmethod
    def clear_screen(
        ) -> ANSI:
        """
            Clear the screen

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}2J")


    @staticmethod
    def clear(
        ) -> ANSI:
        """
            Clear the screen and bring the cursor to the top left corner

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.cursor import Cursor

        return Line.clear_screen() + Cursor.top()


    @staticmethod
    def clear_previous_line(
    ) -> ANSI:
        """
            Clear the previous line.

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.cursor import Cursor

        return Cursor.up(1) + Line.clear_end_line() + Cursor.move_column(0)
