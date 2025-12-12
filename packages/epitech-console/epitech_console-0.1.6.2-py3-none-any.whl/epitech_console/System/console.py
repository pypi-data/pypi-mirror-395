#############################
###                       ###
###    Epitech Console    ###
###   ----console.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object, type
from typing import Any


class ConsoleMeta(type):
    """
        Metaclass for Console classe.
    """


    def __len__(
            cls
        ) -> int:
        """
            get length of the current terminal (number of columns)

            Returns:
                int: length of the terminal
        """

        from os import get_terminal_size

        return get_terminal_size().columns


class Console(metaclass=ConsoleMeta):
    """
        Console class.

        Console tool.
    """


    from sys import stdout


    @staticmethod
    def print(
            *args,
            separator: str = " ",
            start: str = "",
            end: str = "\n",
            file: Any = stdout,
            auto_reset: bool = True,
            sleep: int | float | None = None,
            cut_to_terminal_size: bool = False
        ) -> None:
        """
            Print on the console.

            WARNING : 'cut_to_terminal_size' does not work with ANSI sequence

            Parameters:
                *args: Any values to print.
                separator (str)(optional): Separator between values.
                start (str)(optional): String prepended before printing.
                end (str)(optional): String appended after printing.
                file (Any)(optional): File-like object to write into.
                auto_reset (bool)(optional): Automatically reset ANSI sequence.
                sleep (int | float | None)(optional): Delay in seconds after printing.
                cut_to_terminal_size (bool)(optional): Cut output to terminal width.
        """

        from epitech_console.System.time import Time
        from epitech_console.ANSI.color import Color

        string_list : list[str]
        string : str = f"{start}"

        for idx in range(len(args)):
            if idx and idx < len(args):
                string += separator
            string += str(args[idx])

        string += f"{end}"

        string_list = string.split("\n")

        for idx in range(len(string_list)):
            if cut_to_terminal_size and (len(string_list[idx]) - (string_list[idx].count("\033[") * 2)) > (len(Console) + 6):
                string_list[idx] = string_list[idx][:(len(Console) + 2 + string_list[idx].count("\033[") * 2)] + "..." + str(Color.color(Color.C_RESET))
            print(string_list[idx], file=file)

        if auto_reset:
            print(Color.color(Color.C_RESET), end="")

        if sleep:
            Time.wait(sleep)


    @staticmethod
    def input(
            msg : str = "Input",
            separator : str = " >>> ",
            wanted_type : type = str
        ) -> Any:
        """
            Get user text input from the console.

            Parameters:
                msg (str) : Message to show when user enters input.
                separator (str)(optional): Separator between message and input.
                wanted_type (type): Type of input to return.

            Returns:
                Any: User input as 'type' type.
        """

        return wanted_type(input(msg + separator))

    @staticmethod
    def flush(
            stream : Any = stdout,
        ) -> None:
        """
            Flush console output.

            Parameters:
                stream (Any)(optional) : Stream object to be flushed (generally stdin, stdout and stderr).
        """

        stream.flush()
