def calculate_rsi(candles: list, period: int = 14) -> float:
    if len(candles) < period + 1:
        return 50.0

    closes = [c['close'] for c in candles if c is not None]
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]

    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_ema(candles: list, period: int = 20) -> float:
    if len(candles) < period:
        return 0.0
    closes = [c['close'] for c in candles if c is not None]
    multiplier = 2 / (period + 1)
    ema = closes[0]
    for price in closes[1:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    return ema
