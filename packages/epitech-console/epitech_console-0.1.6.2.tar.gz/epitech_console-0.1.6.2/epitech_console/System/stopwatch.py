#############################
###                       ###
###    Epitech Console    ###
###  ----wtopwatch.py---- ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class StopWatch:
    """
        StopWatch class.

        StopWatch tool.
    """


    def __init__(
            self,
            start : bool = False,
        ) -> None:
        """
            Create a stopwatch.
        """

        self.start_time : float = 0.0
        self.time : float = 0.0

        if start:
            self.start()


    def __str__(
            self
        ) -> str :
        """
            Convert StopWatch object to string.

            Returns:
                str: StopWatch string
        """

        return str(self.elapsed())


    def start(
            self
        ) -> None:
        """
            Start the stopwatch.
        """

        from time import time

        self.start_time = time()


    def stop(
            self
        ) -> None:

        self.update()
        self.start_time = 0.0


    def update(
            self
        ) -> None:
        """
            Update the stopwatch.
        """

        from time import time

        if self.start_time:
            self.time = time() - self.start_time


    def elapsed(
            self,
            auto_update : bool = False
        ) -> float:
        """
            Get elapsed time.

            Parameters:
                auto_update (bool)(optional): Auto update. Defaults to False.

            Returns:
                float: Elapsed time.
        """

        if auto_update:
            self.update()

        return self.time


    def reset(
            self
        ) -> None:
        """
            Reset the stopwatch.
        """

        self.stop()
        self.start()
