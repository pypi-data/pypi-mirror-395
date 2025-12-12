#############################
###                       ###
###    Epitech Console    ###
###  ----__init__.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from epitech_console.Animation.animation import Animation
from epitech_console.Animation.basepack import BasePack
from epitech_console.Animation.progressbar import ProgressBar
from epitech_console.Animation.style import Style
from epitech_console.Animation.spinner import Spinner


__all__ : list[str] = [
    'Animation',
    'BasePack',
    'ProgressBar',
    'Style',
    'Spinner'
]


__author__ : str = 'Nathan Jarjarbin'
__email__ : str = 'nathan.epitech.eu'


BasePack.update()
