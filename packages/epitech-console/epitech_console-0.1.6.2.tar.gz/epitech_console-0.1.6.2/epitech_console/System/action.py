#############################
###                       ###
###    Epitech Console    ###
###   ----action.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Action:
    """
        Action class.

        Action object to save a function and its arguments and call it later.
    """


    from collections.abc import Callable


    def __init__(
            self,
            name : str,
            function : Callable,
            *args : Any,
            **kwargs : Any
        ) -> None:
        """
            Save a function and its arguments.

            Parameters:
                name (str): Name of the call.
                function (Callable): Function to be saved.
                *args (Any): Function's args.
                **kwargs (Any): Function's kwargs.
        """

        from collections.abc import Callable

        self.name = name
        self.function : Callable = function
        self.args : list = list(args)
        self.kwargs : dict = dict(kwargs)


    def __str__(
            self
        ) -> str:
        """
            Return the string representation of the Action object.
        """

        return f"name = {self.name}  ;  function = {self.function}  ;  args = {self.args}  ;  kwargs = {self.kwargs}"


    def __add__(
            self,
            other
        ) -> Any:
        """
            Create Actions object with the 2 given actions.
        """

        return Actions([self, other])


    def __call__(
            self
        ) -> Any:
        """
            Call the saved function with its arguments.

        Returns:
            Any: Return of the function's call.
        """

        return self.function(*self.args, **self.kwargs)


class Actions:
    """
        Actions class.

        List of action to save.
    """


    def __init__(
            self,
            actions : list[Action] | Action
        ) -> None:
        """
            Save a list of actions.

            Parameters:
                actions (list[Action] | Action): list of actions to save.
        """

        self.actions : list[Action] = []

        if type(actions) in [list]:
            for action in actions:
                self.actions.append(action)

        else:
            self.actions = [actions]


    def __str__(
            self
        ) -> str:
        """
            Return the string representation of the Actions object.
        """

        string : str = ""

        for idx in range(len(self.actions)):
            string += f"{idx + 1} :\n"
            string += f"    name = {self.actions[idx].name}\n"
            string += f"    function = {self.actions[idx].function}\n"
            string += f"    args = {self.actions[idx].args}\n"
            string += f"    kwargs = {self.actions[idx].kwargs}\n\n"

        return string[:-2]


    def __call__(
            self
        ) -> dict[str, Any]:
        """
            Call the saved functions with their arguments.
        """

        returns : dict[str, Any] = {}

        for action in self.actions:
            returns[action.name] = action()

        return returns
