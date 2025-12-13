from collections import deque
import blessed
from colorama import Fore
from typing import Optional
from .types import CandleData
import json
import os


class config:
    SYMBOL = str("btcusdt")
    INTERVAL = str("1s")  # 1s, 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, etc.
    MAX_CANDLES = 60
    UPDATE_EVERY = 1
    CHART_WIDTH = 14
    CHART_HEIGHT = 6
    CHART_BG = str("#1a1a2e")
    CHART_FG = str("#16213e")
    CANDLE_GAIN_COLOR = str("#00ff88")
    CANDLE_FALL_COLOR = str("#ff4444")
    TEXT_GAIN_COLOR = Fore.GREEN
    TEXT_FALL_COLOR = Fore.RED

    current_mode = 'chart'
    terminal = blessed.Terminal()

    candles: list[Optional[CandleData]] = [None] * MAX_CANDLES
    candle_dict = {}

    refresh_plot = False

    CONFIG_FILE = "config.json"

    @classmethod
    def save_to_file(cls):
        data = {
            "SYMBOL": cls.SYMBOL,
            "INTERVAL": cls.INTERVAL,
            "MAX_CANDLES": cls.MAX_CANDLES,
            "UPDATE_EVERY": cls.UPDATE_EVERY,
            "CHART_WIDTH": cls.CHART_WIDTH,
            "CHART_HEIGHT": cls.CHART_HEIGHT,
            "CHART_BG": cls.CHART_BG,
            "CHART_FG": cls.CHART_FG,
            "CANDLE_GAIN_COLOR": cls.CANDLE_GAIN_COLOR,
            "CANDLE_FALL_COLOR": cls.CANDLE_FALL_COLOR,
        }
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_file(cls):
        if os.path.exists(cls.CONFIG_FILE):
            with open(cls.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                cls.SYMBOL = data.get("SYMBOL", cls.SYMBOL)
                cls.INTERVAL = data.get("INTERVAL", cls.INTERVAL)
                cls.MAX_CANDLES = data.get("MAX_CANDLES", cls.MAX_CANDLES)
                cls.UPDATE_EVERY = data.get("UPDATE_EVERY", cls.UPDATE_EVERY)
                cls.CHART_WIDTH = data.get("CHART_WIDTH", cls.CHART_WIDTH)
                cls.CHART_HEIGHT = data.get("CHART_HEIGHT", cls.CHART_HEIGHT)
                cls.CHART_BG = data.get("CHART_BG", cls.CHART_BG)
                cls.CHART_FG = data.get("CHART_FG", cls.CHART_FG)
                cls.CANDLE_GAIN_COLOR = data.get(
                    "CANDLE_GAIN_COLOR", cls.CANDLE_GAIN_COLOR)
                cls.CANDLE_FALL_COLOR = data.get(
                    "CANDLE_FALL_COLOR", cls.CANDLE_FALL_COLOR)
