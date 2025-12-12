#############################
###                       ###
###    Epitech Console    ###
###   ----cursor.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Cursor:
    """
        Cursor class.

        Manipulate the cursor's position.
    """

    from epitech_console.ANSI.ansi import ANSI


    @staticmethod
    def up(
            n: int = 1
        ) -> ANSI:
        """
            Bring the cursor up 'n' lines

            Parameters:
                n (int): number of lines up

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}A")


    @staticmethod
    def down(
            n: int = 1
        ) -> ANSI:
        """
            Bring the cursor down 'n' lines

            Parameters:
                n (int): number of lines down

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}B")


    @staticmethod
    def left(
            n: int = 1
        ) -> ANSI:
        """
            Bring the cursor left 'n' column

            Parameters:
                n (int): number of column left

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}D")


    @staticmethod
    def right(
            n: int = 1
        ) -> ANSI:
        """
            Bring the cursor right 'n' column

            Parameters:
                n (int): number of column right

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}C")


    @staticmethod
    def top(
        ) -> ANSI:
        """
            Move the cursor to the top left corner of the console

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}H")


    @staticmethod
    def previous(
            n: int = 1
        ) -> ANSI:
        """
            Move the cursor to the beginning of the 'n' previous line

            Parameters:
                n (int): number of column up

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}F")


    @staticmethod
    def next(
            n: int = 1
        ) -> ANSI:
        """
            Move the cursor to the beginning of the 'n' previous line

            Parameters:
                n (int): number of column right

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{n}E")


    @staticmethod
    def move(
            x : int = 0,
            y : int = 0
        ) -> ANSI:
        """
            Move the cursor to the column x and line y

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{y};{x}H")


    @staticmethod
    def move_column(
            x : int = 0
        ) -> ANSI:
        """
            Move the cursor to the column x and line y

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}{x}G")


    @staticmethod
    def set(
        ) -> ANSI:
        """
            Save the cursor's position

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}7")


    @staticmethod
    def reset(
        ) -> ANSI:
        """
            Move the cursor to the saved position

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}8")


    @staticmethod
    def show(
        ) -> ANSI:
        """
            Show the cursor

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}25h")


    @staticmethod
    def hide(
        ) -> ANSI:
        """
            Hide the cursor

            Returns:
                ANSI: ansi sequence
        """

        from epitech_console.ANSI.ansi import ANSI

        return ANSI(f"{ANSI.ESC}25l")
