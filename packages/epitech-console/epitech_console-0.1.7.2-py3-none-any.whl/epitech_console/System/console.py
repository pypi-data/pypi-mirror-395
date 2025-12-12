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
    from epitech_console.Text.text import Text


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
        ) -> Text:
        """
            Print on the console.

            WARNING : 'cut_to_terminal_size' does not work with ANSI sequence
            WARNING : 'cut_to_terminal_size' does not work properly when changing terminal size

            Parameters:
                *args: Any values to print.
                separator (str, optional): Separator between values.
                start (str, optional): String prepended before printing.
                end (str, optional): String appended after printing.
                file (Any, optional): File-like object to write into.
                auto_reset (bool, optional): Automatically reset ANSI sequence.
                sleep (int | float | None, optional): Delay in seconds after printing.
                cut_to_terminal_size (bool, optional): Cut output to terminal width.
        """

        from epitech_console.System.time import Time
        from epitech_console.ANSI.color import Color
        from epitech_console.Text.text import Text

        string_list : list[str]
        string : str = ""
        final_string : Text = Text("")

        for idx in range(len(args)):
            if idx and idx < len(args):
                string += separator
            string += str(args[idx])

        string_list = string.split("\n")

        for idx in range(len(string_list)):
            if cut_to_terminal_size and (len(string_list[idx]) - (string_list[idx].count("\033[") * 2)) > (len(Console) + 6):
                string_list[idx] = string_list[idx][:(len(Console) + 2 + string_list[idx].count("\033[") * 2)] + "..." + str(Color.color(Color.C_RESET))
            final_string += Text(string_list[idx]) + (Text("\n") if len(string_list) > 1 else Text(""))

        final_string = Text(start) + final_string + (Color.color(Color.C_RESET) if auto_reset else Text("")) + Text(end)

        print(final_string, file=file)

        if sleep:
            Time.wait(sleep)

        return final_string


    @staticmethod
    def input(
            msg : str = "Input",
            separator : str = " >>> ",
            wanted_type : type = str
        ) -> Any:
        """
            Get user text input from the console.

            Parameters:
                msg (str, optional) : Message to show when user enters input.
                separator (str, optional): Separator between message and input.
                wanted_type (type, optional): Type of input to return.

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
                stream (Any, optional) : Stream object to be flushed (generally stdin, stdout and stderr).
        """

        stream.flush()
