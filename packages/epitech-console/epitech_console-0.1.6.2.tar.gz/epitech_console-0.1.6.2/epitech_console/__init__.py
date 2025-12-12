#############################
###                       ###
###    Epitech Console    ###
###  ----__init__.py----  ###
###                       ###
###=======================###
### by JARJARBIN's STUDIO ###
#############################


from epitech_console import Animation, ANSI, Error, System, Text
from epitech_console.System import Actions
from epitech_console.Text import Format

PATH = __file__.removesuffix("__init__.py")


Animation.basepack.BasePack.update(Animation.Style("#", " ", "#", "#", "", ""))
ANSI.basepack.BasePack.update()


__all__ : list[str] = [
    'Animation',
    'ANSI',
    'Error',
    'System',
    'Text',
    'PATH'
]


__author__ : str = 'Nathan Jarjarbin'
__email__ : str = 'nathan.epitech.eu'


def _banner(
        config
    ) -> None:
    """
        Show a simple banner.
    """

    from epitech_console import Animation as AN, ANSI as AS, Error as E, System as S, Text as T

    banner_size = 50

    epitech = AS.Color.epitech_fg()
    epitech_dark = AS.Color.epitech_dark_fg()
    reset = AS.Color.color(AS.Color.C_RESET)

    offset_t = T.Text("  ")
    title_t = epitech + T.Text(f"{config.get("PACKAGE", "name")}").bold().underline() + reset + "  " + T.Text.url_link(
        "https://github.com/Jarjarbin06/epitech_console", text="repository")
    version_t = T.Text(" " * 5) + epitech_dark + T.Text("version ").italic() + T.Text(
        f"{config.get("PACKAGE", "version")}").bold() + reset
    desc_t = T.Text("   Text • Animation • ANSI • Error • System   ").italic()
    line_t = epitech + ("─" * banner_size) + reset

    S.Console.print(line_t, offset_t + title_t + " " + version_t + offset_t, offset_t + desc_t + offset_t, line_t, separator="\n")


def _init(
    ) -> None:
    """
        _init() initializes the epitech console package and show a banner (if SETTING : show-banner = True in config.ini)
    """

    from epitech_console import Animation as AN, ANSI as AS, Error as E, System as S, Text as T

    Animation.BasePack.update()
    ANSI.basepack.BasePack.update()

    if not S.Config.exist(PATH):
        S.Config.create(PATH)

    config = S.Config.read(PATH)

    if config.getboolean("SETTING", "show-banner"):
        try:
            _banner(config)

        except Exception as error:
            if config.getboolean("SETTING", "debug"):
                print("\033[101m \033[0m \033[91m" + str(error) + "\033[0m\n")
            print(
                "\033[103m \033[0m \033[93mepitech_console imported with error\033[0m\n"
                "\033[103m \033[0m\n"
                "\033[103m \033[0m \033[93mPlease reinstall with :\033[0m\n"
                "\033[103m \033[0m \033[93m    'pip install --upgrade --force-reinstall epitech_console'\033[0m\n"
                "\033[103m \033[0m\n"
                "\033[103m \033[0m \033[93mPlease report the issue here : https://github.com/Jarjarbin06/epitech_console/issues\033[0m\n"
            )


_init()