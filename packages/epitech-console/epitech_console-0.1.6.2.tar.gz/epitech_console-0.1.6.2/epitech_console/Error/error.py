#############################
###                       ###
###    Epitech Console    ###
###    ----error.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Error(Exception):
    """
    Error class.

    Error for epitech_console.
    """


    def __init__(
            self,
            message : str = "an error occurred",

            *,
            error : str = "Error",
            link : tuple[str, int] | None = None
        ) -> None:
        """
            Create an Error.

            Parameters:
                message (str): The error message.
                link (tuple[str, int]): The link to where the error comes from (file and line).
        """

        from epitech_console.Text.text import Text

        self.message : str = message
        self.error : str = error
        self.link : str | None = None

        if link:
            self.link = Text.file_link(link[0], link[1])


    def __str__(
            self
        ) -> str:
        """
            Get string representation of the error.

            Returns:
                str: String representation of the error.
        """

        return f"{self.error}:\n    {self.message}" + (f"\n\n{self.link}" if self.link else "")
