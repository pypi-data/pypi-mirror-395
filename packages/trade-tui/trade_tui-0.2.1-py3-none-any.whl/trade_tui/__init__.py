import os
from .util.config import config
from .menus.main_menu import main_menu


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    config.load_from_file()
    await main_menu()
