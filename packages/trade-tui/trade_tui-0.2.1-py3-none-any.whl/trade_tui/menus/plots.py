from datetime import datetime
import asyncio
import websockets
import json
import matplotlib.pyplot as plt
import matplotlib
from ..util.ui import draw_candlesticks, display_in_kitty
from matplotlib.ticker import FuncFormatter
from ..util.config import config
from ..util.types import CandleData
from ..util.backfill import fetch_historical_candles
from ..util.input import set_current_message
from ..util.indicators import calculate_rsi, calculate_ema
from colorama import Fore
import os

TERM = os.environ.get('TERM', '')
IS_KITTY = "kitty" in TERM

if IS_KITTY:
    matplotlib.use('module://matplotlib-backend-kitty')
else:
    import matplotlib_terminal

WS_URL = ""

update_count = 0


async def connect_and_plot():
    WS_URL = f"wss://stream.binance.com:9443/ws/{config.SYMBOL}@kline_{config.INTERVAL}"

    data = await fetch_historical_candles()
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

    if config.candles is not None and len(config.candles) > 0 and config.candles[-1] is not None:
        await show_plot(config.candles[-1], open_time=config.candles[-1]['time'].timestamp() * 1000)

    async with websockets.connect(WS_URL) as ws:
        set_current_message(
            f"Q -> Main Menu | {config.TEXT_GAIN_COLOR}Connected{Fore.RESET} | {config.SYMBOL.upper()} @ {config.INTERVAL} | {WS_URL}")

        while (not config.refresh_plot) and config.current_mode == "chart":
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.1)
                data = json.loads(msg)

                kline = data['k']
                open_time = kline['t']
                candle_data: CandleData = {
                    'time': datetime.fromtimestamp(open_time / 1000),
                    'open': float(kline['o']),
                    'high': float(kline['h']),
                    'low': float(kline['l']),
                    'close': float(kline['c']),
                    'volume': float(kline['v']),
                    'is_closed': kline['x']
                }
                await show_plot(candle_data=candle_data, open_time=open_time)

                rsi = calculate_rsi(config.candles, 14)
                rsi_string = ""
                if rsi >= 80:
                    rsi_string = config.TEXT_FALL_COLOR
                elif rsi <= 20:
                    rsi_string = config.TEXT_GAIN_COLOR
                else:
                    rsi_string = Fore.RESET
                rsi_string += str(int(rsi * 100) / 100.0) + Fore.RESET
                set_current_message(
                    f"Q -> Main Menu | RSI -> {rsi_string} | EMA -> {int(calculate_ema(config.candles, 20) * 100) / 100} | {config.TEXT_GAIN_COLOR}Connected{Fore.RESET} | {config.SYMBOL.upper()} @ {config.INTERVAL} | {WS_URL}")

            except asyncio.TimeoutError:
                continue
            except websockets.ConnectionClosed:
                print("Connection closed, reconnecting...")
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                plt.close()
                return
            except Exception as e:
                print(f"Error: {e}")
                continue

    plt.close()
    if config.refresh_plot:
        config.refresh_plot = False
        await connect_and_plot()


async def show_plot(candle_data: CandleData, open_time):
    global update_count
    fig, ax = plt.subplots(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
    fig.set_facecolor(config.CHART_BG)
    ax.set_facecolor(config.CHART_FG)

    try:
        if open_time in config.candle_dict:
            idx = config.candle_dict[open_time]
            config.candles[idx] = candle_data
        else:
            config.candles.append(candle_data)
            config.candle_dict[open_time] = len(config.candles) - 1

            if len(config.candles) > config.MAX_CANDLES:
                config.candles = config.candles[-config.MAX_CANDLES:]
                config.candle_dict = {
                    k: i for i, (k, _) in enumerate(
                        sorted(config.candle_dict.items()
                               )[-config.MAX_CANDLES:]
                    )
                }

        update_count += 1

        if len(config.candles) >= 2 and update_count >= config.UPDATE_EVERY:
            update_count = 0

            ax.clear()
            ax.set_facecolor(config.CHART_FG)

            candles_list = [c for c in config.candles if c is not None]
            draw_candlesticks(
                ax, candles_list, offset=config.MAX_CANDLES - len(candles_list))

            current_price = candles_list[-1]['close']
            price_change = current_price - candles_list[-1]['open']
            change_pct = (
                price_change / candles_list[-1]['open']) * 100
            change_symbol = '+' if price_change >= 0 else ''

            ax.set_title(
                f'{config.SYMBOL.upper()} ({config.INTERVAL}) - ${current_price:,.2f} '
                f'({change_symbol}{price_change:,.2f} / {change_symbol}{change_pct:.2f}%)',
                fontsize=14, color='white'
            )
            ax.set_xlabel('Candles', color='white')
            ax.set_ylabel('Price (USD)', color='white')

            ax.set_xlim(-1, config.MAX_CANDLES)

            all_highs = [c['high'] for c in candles_list]
            all_lows = [c['low'] for c in candles_list]
            min_price = min(all_lows)
            max_price = max(all_highs)
            price_range = max_price - min_price
            padding = max(price_range * 0.1, 10)
            ax.set_ylim(min_price - padding, max_price + padding)

            ax.yaxis.set_major_formatter(
                FuncFormatter(lambda x, p: f'${x:,.0f}'))

            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.grid(True, alpha=0.3, color='gray')

            fig.canvas.draw()
            fig.tight_layout()
            if IS_KITTY:
                display_in_kitty(fig)
            else:
                plt.show()

    except KeyboardInterrupt:
        print("\nExiting...")
        return
    except Exception as e:
        print(f"Error: {e}")
    finally:
        plt.close(fig)
