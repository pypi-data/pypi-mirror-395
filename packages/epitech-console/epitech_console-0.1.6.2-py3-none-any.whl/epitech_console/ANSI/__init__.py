#############################
###                       ###
###    Epitech Console    ###
###  ----__init__.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from epitech_console.ANSI.ansi import ANSI
from epitech_console.ANSI.cursor import Cursor
from epitech_console.ANSI.line import Line
from epitech_console.ANSI.color import Color
from epitech_console.ANSI.basepack import BasePack


__all__ : list[str] = [
    'ANSI',
    'Cursor',
    'Line',
    'Color',
    'BasePack'
]


__author__ : str = 'Nathan Jarjarbin'
__email__ : str = 'nathan.epitech.eu'
