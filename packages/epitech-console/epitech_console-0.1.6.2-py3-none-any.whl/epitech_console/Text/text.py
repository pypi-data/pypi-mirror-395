#############################
###                       ###
###    Epitech Console    ###
###    ----text.py----    ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any
from epitech_console.Text.format import Format


class Text(Format):
    """
        Text class.

        Text tool.
    """


    def __init__(
            self,
            text : Any | str = ""
        ) -> None:
        """
            Create a text.

            Parameters:
                text (ANSI | str): text
        """

        from epitech_console.ANSI.ansi import ANSI

        self.text : str = ""

        if type(text) in [ANSI]:
            self.text = text.sequence

        else :
            self.text = str(text)


    def __add__(
            self,
            other : Any | str
        ) -> Any:
        """
            Add 2 Texts together.

            Parameters:
                other (ANSI | Text | str): text

            Returns:
                Text: text
        """

        return Text(str(self) + str(other))


    def __str__(
            self
        ) -> str :
        """
            Convert Text object to string.

            Returns:
                str: Text string
        """

        return str(self.text)


    def __len__(
            self
        ) -> int:
        """
            Get length of Text object.
        """

        return len(self.text)


    @staticmethod
    def url_link(
            url: str,
            text: str | None = None
        ) -> Any:
        """
            Get url link to line 'line' of the file 'path' (may not work in IDE's console).

            Parameters:
                url (str): URL to website.
                text (int): Text to show instead of the url (show the url if no text).

            Returns:
                str: url link.
        """

        if not text:
            text = url

        return Text(f'\033]8;;{url}\033\\{text}\033]8;;\033\\')


    @staticmethod
    def file_link(
            path: str,
            line: int | None = None
        ) -> Any:
        """
            Get file link to line 'line' of the file 'path' (needs CLion from JetBrains to work).

            Parameters:
                path (str): Path to the file.
                line (int): Line of the file.

            Returns:
                str: file link.
        """

        if line:
            return Text(f'\033]8;;jetbrains://clion/navigate/reference?file={path}&line={line}\033\\File "{path}", line {line}\033]8;;\033\\')
        else:
            return Text(f'\033]8;;jetbrains://clion/navigate/reference?file={path}\033\\"{path}"\033]8;;\033\\')
