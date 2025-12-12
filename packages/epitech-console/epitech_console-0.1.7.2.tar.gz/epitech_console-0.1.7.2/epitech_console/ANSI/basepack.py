#############################
###                       ###
###    Epitech Console    ###
###  ----basepack.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class BasePack:
    """
        BasePack class.

        Base animation pack ready for use.

        Attributes:
            P_ERROR (tuple): error tuple of color.
            P_WARNING (tuple): warning tuple of color.
            P_OK (tuple): validation tuple of color.
            P_INFO (tuple): information tuple of color.
    """


    P_ERROR = (0, 0)
    P_WARNING = (0, 0)
    P_OK = (0, 0)
    P_INFO = (0, 0)


    @staticmethod
    def update(
        ) -> None:
        """
            Initialise the BasePack class
        """

        from epitech_console.ANSI.color import Color

        BasePack.P_ERROR = (Color.color(Color.C_BG_DARK_RED), Color.color(Color.C_FG_DARK_RED))
        BasePack.P_WARNING = (Color.color(Color.C_BG_DARK_YELLOW), Color.color(Color.C_FG_DARK_YELLOW))
        BasePack.P_OK = (Color.color(Color.C_BG_DARK_GREEN), Color.color(Color.C_FG_DARK_GREEN))
        BasePack.P_INFO = (Color.color(Color.C_BG), Color.color(Color.C_RESET))
