import aiohttp
from .config import config
from .types import CandleData
from datetime import datetime


async def fetch_historical_candles():
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": config.SYMBOL.upper(),
        "interval": config.INTERVAL,
        "limit": config.MAX_CANDLES
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()

    for kline in data:
        open_time = kline[0]
        candle: CandleData = {
            'time': datetime.fromtimestamp(open_time / 1000),
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5]),
            'is_closed': True
        }
        config.candles.append(candle)
        config.candle_dict[open_time] = len(config.candles) - 1
    return data
