#############################
###                       ###
###    Epitech Console    ###
###   ----config.py----   ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from builtins import object
from typing import Any


class Config:
    """
        Config class.

        Config file tool.
    """


    from configparser import ConfigParser


    @staticmethod
    def exist(
            path : str,
            *,
            file_name : str = "config.ini"
        ) -> bool:
        """
            Check if a config file config.ini is empty or doesn't exist

            Returns:
                bool: False if empty or not existing, True otherwise
                file_name (str)(optional): name of config file
        """

        empty_config : bool = True

        try :
            with open(path + file_name, 'r') as config_file:
                if config_file.read() == "":
                    empty_config = False
            config_file.close()

        except FileNotFoundError:
            empty_config = False

        return empty_config

    @staticmethod
    def create(
            path : str,
            data : dict | None = None,
            *,
            file_name : str = "config.ini"
        ) -> None:
        """
            Create a new config file

            Parameters:
                path (str): path to folder which you want your config file to be in
                data (dict | None): data to put in the config file
                file_name (str)(optional): name of config file
        """

        from configparser import ConfigParser

        if not data and file_name == "config.ini":
            data = {
                "PACKAGE" : {
                    "name": "None",
                    "version": "0.0.0",
                    "description": "None",
                    "repository": "None",
                },
                "SETTING" : {
                    "show-banner": "False",
                    "auto-color": "True",
                    "safe-mode": "False",
                    "minimal-mode": "False",
                    "debug": "False",
                    "log": "False"
                }
            }

        with open(path + file_name, 'w') as config_file:
            config = ConfigParser()
            for key in data:
                config[key] = data[key]

            config.write(config_file)

        config_file.close()

    @staticmethod
    def read(
            path: str,
            *,
            file_name : str = "config.ini"
        ) -> ConfigParser | None:
        """
            Read a config file

            Parameters:
                path (str): path to folder which contain your config file
                file_name (str)(optional): name of config file
        """

        from configparser import ConfigParser

        if Config.exist(path):
            config = ConfigParser()
            config.read(path + file_name)

            return config

        return None
