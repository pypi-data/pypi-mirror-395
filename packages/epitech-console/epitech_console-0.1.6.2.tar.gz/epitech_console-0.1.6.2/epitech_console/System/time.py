#############################
###                       ###
###    Epitech Console    ###
###    ----time.py----    ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Time:
    """
        Time class.

        Time tool.
    """

    @staticmethod
    def wait(
            sleep : int | float
        ) -> float:
        """
            Wait for 'sleep' seconds and return the exact elapsed time during the wait function.

            Parameters:
                sleep (int | float) : Time to wait

            Returns:
                float : Exact elapsed time
        """

        from epitech_console.System.stopwatch import StopWatch

        watch = StopWatch(True)

        while watch.elapsed() < sleep:
            watch.update()

        return watch.elapsed()


    @staticmethod
    def pause(
            msg : str = "Press enter to continue..."
        ) -> float:
        """
            Pause the program and print a message and return the exact elapsed time during the pause function.

            Parameters:
                msg (str) : Message to be displayed

            Returns:
                float : Exact elapsed time
        """

        from epitech_console.System.stopwatch import StopWatch

        watch = StopWatch(True)
        input(msg)

        return watch.elapsed(True)
