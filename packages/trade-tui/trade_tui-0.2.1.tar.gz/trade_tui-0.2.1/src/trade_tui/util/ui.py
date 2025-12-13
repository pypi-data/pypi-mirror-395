from matplotlib.patches import Rectangle
import base64
import io
import sys
from .config import config


def draw_candlesticks(ax, candles_list, offset=0):
    width = 0.6

    for i, candle in enumerate(candles_list):
        x = i + offset
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']

        if close_price >= open_price:
            color = config.CANDLE_GAIN_COLOR
            body_bottom = open_price
            body_height = close_price - open_price
        else:
            color = config.CANDLE_FALL_COLOR
            body_bottom = close_price
            body_height = open_price - close_price

        ax.plot([x, x], [low_price, high_price], color=color, linewidth=1)

        if body_height == 0:
            body_height = 0.01
        rect = Rectangle((x - width / 2, body_bottom), width, body_height,
                         facecolor=color, edgecolor=color, linewidth=1)
        ax.add_patch(rect)


def display_in_kitty(fig, image_id=1):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100,
                bbox_inches='tight', facecolor='#1a1a2e')
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('ascii')

    sys.stdout.write('\033[?2026h')
    sys.stdout.write('\033[H')

    sys.stdout.write(f'\033_Ga=d,d=i,i={image_id},q=2\033\\')

    chunk_size = 4096
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    for i, chunk in enumerate(chunks):
        if i == 0:
            if len(chunks) == 1:
                sys.stdout.write(
                    f'\033_Ga=T,f=100,i={image_id},q=2;{chunk}\033\\')
            else:
                sys.stdout.write(
                    f'\033_Ga=T,f=100,i={image_id},m=1,q=2;{chunk}\033\\')
        elif i == len(chunks) - 1:
            sys.stdout.write(f'\033_Gm=0,q=2;{chunk}\033\\')
        else:
            sys.stdout.write(f'\033_Gm=1,q=2;{chunk}\033\\')

    sys.stdout.write('\n')
    sys.stdout.write('\033[?2026l')
    sys.stdout.flush()
    buf.close()
