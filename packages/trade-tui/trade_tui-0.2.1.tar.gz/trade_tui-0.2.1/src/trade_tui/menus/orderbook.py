import asyncio
import json
import aiohttp
import websockets
from collections import OrderedDict
from typing import Optional
from ..util.config import config
from ..util.input import _current_message
from colorama import Fore

# https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#how-to-manage-a-local-order-book-correctly


class OrderBook:

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.bids: OrderedDict[str, str] = OrderedDict()
        self.asks: OrderedDict[str, str] = OrderedDict()
        self.last_update_id: int = 0
        self.buffer: list = []
        self.initialized: bool = False
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@depth"
        self.snapshot_url = f"https://api.binance.com/api/v3/depth?symbol={self.symbol.upper()}&limit=5000"

    def _sort_bids(self):
        self.bids = OrderedDict(
            sorted(self.bids.items(), key=lambda x: float(x[0]), reverse=True))

    def _sort_asks(self):
        self.asks = OrderedDict(
            sorted(self.asks.items(), key=lambda x: float(x[0])))

    def apply_update(self, price: str, quantity: str, side: str):
        book = self.bids if side == 'bid' else self.asks

        if float(quantity) == 0:
            book.pop(price, None)
        else:
            book[price] = quantity

    def process_event(self, event: dict) -> bool:
        event_first_id: int = event.get('U', 0)
        event_last_id: int = event.get('u', 0)

        if event_last_id <= self.last_update_id:
            return True

        if event_first_id > self.last_update_id + 1:
            return False

        for bid in event.get('b', []):
            price, quantity = bid[0], bid[1]
            self.apply_update(price, quantity, 'bid')

        for ask in event.get('a', []):
            price, quantity = ask[0], ask[1]
            self.apply_update(price, quantity, 'ask')

        self.last_update_id = event_last_id

        self._sort_bids()
        self._sort_asks()

        return True

    async def fetch_snapshot(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.snapshot_url) as response:
                return await response.json()

    async def initialize_from_snapshot(self, snapshot: dict, first_event_u: int) -> bool:
        last_update_id = snapshot.get('lastUpdateId', 0)

        if last_update_id < first_event_u:
            return False

        self.bids.clear()
        self.asks.clear()

        for bid in snapshot.get('bids', []):
            price, quantity = bid[0], bid[1]
            if float(quantity) > 0:
                self.bids[price] = quantity

        for ask in snapshot.get('asks', []):
            price, quantity = ask[0], ask[1]
            if float(quantity) > 0:
                self.asks[price] = quantity

        self._sort_bids()
        self._sort_asks()

        self.last_update_id = last_update_id
        return True

    def get_top_bids(self, n: int = 10) -> list:
        return list(self.bids.items())[:n]

    def get_top_asks(self, n: int = 10) -> list:
        return list(self.asks.items())[:n]

    def get_best_bid(self) -> tuple:
        if self.bids:
            price = next(iter(self.bids))
            return (price, self.bids[price])
        return (None, None)

    def get_best_ask(self) -> tuple:
        if self.asks:
            price = next(iter(self.asks))
            return (price, self.asks[price])
        return (None, None)

    def get_spread(self) -> float:
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid[0] and best_ask[0]:
            return float(best_ask[0]) - float(best_bid[0])
        return 0.0

    def get_mid_price(self) -> float:
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid[0] and best_ask[0]:
            return (float(best_bid[0]) + float(best_ask[0])) / 2
        return 0.0


orderbook: Optional[OrderBook] = None


async def connect_orderbook():
    global orderbook

    orderbook = OrderBook(config.SYMBOL)

    while config.current_mode == "orderbook":
        try:
            async with websockets.connect(orderbook.ws_url) as ws:
                print(
                    f"Connected to order book stream for {config.SYMBOL.upper()}")

                first_event_u = None
                orderbook.buffer = []
                orderbook.initialized = False

                while config.current_mode == "orderbook":
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        event = json.loads(msg)

                        if not orderbook.initialized:
                            orderbook.buffer.append(event)

                            if first_event_u is None:
                                first_event_u = event.get('U')

                                snapshot = await orderbook.fetch_snapshot()

                                while snapshot.get('lastUpdateId', 0) < first_event_u:
                                    await asyncio.sleep(0.1)
                                    snapshot = await orderbook.fetch_snapshot()

                                await orderbook.initialize_from_snapshot(snapshot, first_event_u)

                                orderbook.buffer = [
                                    e for e in orderbook.buffer
                                    if e.get('u') > orderbook.last_update_id
                                ]

                                for buffered_event in orderbook.buffer:
                                    if not orderbook.process_event(buffered_event):
                                        orderbook.initialized = False
                                        break
                                else:
                                    orderbook.initialized = True
                                    orderbook.buffer = []
                        else:
                            if not orderbook.process_event(event):
                                print(
                                    "Missed events, restarting order book sync...")
                                orderbook.initialized = False
                                first_event_u = None
                                orderbook.buffer = []

                    except asyncio.TimeoutError:
                        continue
                    except websockets.ConnectionClosed:
                        print("Order book connection closed, reconnecting...")
                        break

        except Exception as e:
            print(f"Order book error: {e}")
            await asyncio.sleep(1)

    print("Order book mode ended")


def get_orderbook_data(levels: int = 10) -> dict:
    global orderbook

    if orderbook is None or not orderbook.initialized:
        return {
            'initialized': False,
            'symbol': config.SYMBOL.upper(),
            'bids': [],
            'asks': [],
            'spread': 0.0,
            'mid_price': 0.0,
            'best_bid': (None, None),
            'best_ask': (None, None),
        }

    return {
        'initialized': True,
        'symbol': orderbook.symbol.upper(),
        'bids': orderbook.get_top_bids(levels),
        'asks': orderbook.get_top_asks(levels),
        'spread': orderbook.get_spread(),
        'mid_price': orderbook.get_mid_price(),
        'best_bid': orderbook.get_best_bid(),
        'best_ask': orderbook.get_best_ask(),
        'last_update_id': orderbook.last_update_id,
    }


async def display_orderbook():
    LEVELS = 20
    COL_WIDTH = 30

    while config.current_mode == "orderbook":
        data = get_orderbook_data(levels=LEVELS)

        if data['initialized'] and orderbook:
            print("\033[2J\033[H", end="")

            symbol = data['symbol']
            mid_price = data['mid_price']
            spread = data['spread']
            ws_protocol = orderbook.ws_url.split("://")[1].split(":")[0]
            print(
                f"{symbol}@{ws_protocol} | Mid: ${mid_price:,.2f} | Spread: ${spread:,.2f}")
            print()

            bid_header = "BUY".center(COL_WIDTH)
            ask_header = "SELL".center(COL_WIDTH)
            print(f"{bid_header}|{ask_header}")
            print("-" * COL_WIDTH + "|" + "-" * COL_WIDTH)

            bids = data['bids']
            asks = data['asks']

            max_bid_qty = max((float(q) for _, q in bids), default=1)
            max_ask_qty = max((float(q) for _, q in asks), default=1)
            max_qty = max(max_bid_qty, max_ask_qty)

            for i in range(LEVELS):
                if i < len(bids):
                    bid_price, bid_qty = bids[i]
                    bid_qty_f = float(bid_qty)
                    bar_len = int((bid_qty_f / max_qty) * (COL_WIDTH - 12))
                    bid_bar = "=" * bar_len
                    bid_text = f"[{bid_bar}{float(bid_price):,.1f}]"
                    padding = COL_WIDTH - len(bid_text)
                    bid_cell = " " * padding + \
                        f"[{config.TEXT_GAIN_COLOR}{bid_bar}{float(bid_price):,.1f}{Fore.RESET}]"
                else:
                    bid_cell = " " * COL_WIDTH

                if i < len(asks):
                    ask_price, ask_qty = asks[i]
                    ask_qty_f = float(ask_qty)
                    bar_len = int((ask_qty_f / max_qty) * (COL_WIDTH - 12))
                    ask_bar = "=" * bar_len
                    ask_text = f"[{float(ask_price):,.1f}{ask_bar}]"
                    padding = COL_WIDTH - len(ask_text)
                    ask_cell = f"[{config.TEXT_FALL_COLOR}{float(ask_price):,.1f}{ask_bar}{Fore.RESET}]" + \
                        " " * padding
                else:
                    ask_cell = " " * COL_WIDTH

                print(f"{bid_cell}|{ask_cell}")
            print(_current_message, end="\r")
        else:
            print("Syncing order book...", end="\r")

        await asyncio.sleep(0.1)
