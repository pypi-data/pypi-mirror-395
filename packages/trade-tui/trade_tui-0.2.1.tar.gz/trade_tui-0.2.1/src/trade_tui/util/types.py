from typing import TypedDict
from datetime import datetime


class CandleData(TypedDict):
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    is_closed: bool
