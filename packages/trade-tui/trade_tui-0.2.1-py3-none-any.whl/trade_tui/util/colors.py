from colorama import Fore


def fore_from_name(name: str):
    # BLACK           = 30
    # RED             = 31
    # GREEN           = 32
    # YELLOW          = 33
    # BLUE            = 34
    # MAGENTA         = 35
    # CYAN            = 36
    # WHITE           = 37
    # RESET           = 39
    color_map = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "reset": Fore.RESET,
    }

    return color_map.get(name.lower(), Fore.RESET)
