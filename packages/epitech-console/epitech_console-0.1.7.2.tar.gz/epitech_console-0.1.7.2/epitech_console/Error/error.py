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
                message (str, optional): The error message.
                error (str, optional): The error type (title).
                link (tuple[str, int], optional): The link to where the error comes from (file and line).
        """

        from epitech_console.Text.text import Text

        self.message : str = message
        self.error : str = error
        self.link : str | None = None

        if link:
            if len(link) == 1 and type(link[0]) in [str]:
                self.link = Text.file_link(link[0])
            if len(link) == 2 and type(link[0]) in [str] and type(link[1]) in [int]:
                if link[1] > 0:
                    self.link = Text.file_link(link[0], link[1])


    def __str__(
            self
        ) -> str:
        """
            Get string representation of the error.

            Returns:
                str: String representation of the error.
        """

        return f'{self.error}:\n    {self.message}\n\n{self.link if self.link else ""}'
