from ..util.config import config
from ..util.hex import validate_hex
from ..util.colors import fore_from_name
from ..util.clear import clear
from ..util.banner import print_banner
from colorama import Fore
import threading
import os
import platform
import subprocess


def open_settings():
    while True:
        clear()
        print_banner()
        print()
        print("Which setting would you like to change?")
        print("---------------------- CHARTS ----------------------")
        print(f"1. SYMBOL ({config.SYMBOL})")
        print(f"2. INTERVAL ({config.INTERVAL})")
        print("---------------------- COLORS ----------------------")
        print(
            f"11. CANDLE COLORS ({config.CANDLE_GAIN_COLOR} / {config.CANDLE_FALL_COLOR})")
        print(f"12. CHART COLORS ({config.CHART_BG} / {config.CHART_FG})")
        print(
            f"13. TEXT COLORS GAIN / FALL ({config.TEXT_GAIN_COLOR}+$100{Fore.RESET} / {config.TEXT_FALL_COLOR}-$100{Fore.RESET})")
        print("----------------------- MISC -----------------------")
        print("98. Export")
        print("99. Back")

        setting = input("[num] > ")

        if setting == "1":
            symbol = input("[sym] > ")
            config.SYMBOL = symbol.lower()
            config.candle_dict.clear()
            config.candles.clear()
        elif setting == "2":
            interval = input("[int] > ")
            if interval not in ("1s", "1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d", "3d", "1w", "1M"):
                print(
                    f"Interval not allowed. {interval} != ('1s', '1m', '3m', '5m', '15m', '30m', '1h', '4h', '1d', '3d', '1w', '1M')")
                return
            config.INTERVAL = interval

        elif setting == "11":
            print("Leave blank to keep as-is")
            print("Gain:")
            gain = input("[hex] > #")
            if validate_hex(gain):
                config.CANDLE_GAIN_COLOR = f"#{gain}"
            print("Fall:")
            fall = input("[hex] > #")
            if validate_hex(fall):
                config.CANDLE_FALL_COLOR = f"#{fall}"

        elif setting == "12":
            print("Leave blank to keep as-is")
            print("Foreground:")
            fg = input("[hex] > #")
            if validate_hex(fg):
                config.CHART_FG = f"#{fg}"
            print("Background:")
            bg = input("[hex] > #")
            if validate_hex(bg):
                config.CHART_BG = f"#{bg}"

        elif setting == "13":
            print("Leave blank to keep as-is; allowed colors: ('BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'RESET')")

            print("Gain:")
            gain = input("[col] > ")
            if gain != "":
                gain_fore = fore_from_name(gain)
                if gain_fore != "":
                    config.TEXT_GAIN_COLOR = gain_fore
                else:
                    print("Invalid color")
            print("Fall:")
            fall = input("[col] > ")
            if fall != "":
                fall_fore = fore_from_name(fall)
                if fall_fore != "":
                    config.TEXT_FALL_COLOR = fall_fore
                else:
                    print("Invalid color")

        elif setting == "98":
            threading.Thread(
                target=open_in_file_manager,
                args=(config.CONFIG_FILE,),
                daemon=True
            ).start()

        elif setting == "99":
            config.save_to_file()
            break


def open_in_file_manager(path):
    path = os.path.abspath(path)

    system = platform.system()

    if system == "Windows":
        subprocess.Popen(["explorer", "/select,", path])
        return

    path = os.path.dirname(path)

    if system == "Darwin":
        subprocess.Popen(
            ["open", "-R", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    else:
        try:
            subprocess.Popen(
                ["xdg-open", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return
        except FileNotFoundError:
            pass
