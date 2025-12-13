# trade-tui

Trade-TUI is a terminal-based user interface for trading with cryptocurrency. It offers charts, visualizations and more real-time monitoring and management of your trades.

**NOTE:** This project is highly optimized for the Kitty Terminal. Some features may not work properly in other terminals.

## Features

Trade-TUI features:

-   Real-time price charts for all charts supported by Binance API
-   Different tiemeframes (1m, 5m, 15m, 1h, 4h, 1d, 3d, 1M)
-   RSI and EMA calculations
-   Order book visualization
-   Customizable colors / themes
-   Image visualization in Kitty Terminal
-   ASCII art charts for other terminals

## Getting Started

Install the dependencies using venv and pip:

```bash
python3 -m venv tui
source tui/bin/activate
pip install -r requirements.txt
```

Run the TUI:

```bash
python3 main-kitty.py
```

Happy trading!

_Disclaimer: Trading with cryptocurrencies involves significant risk. Please trade responsibly. This project does not give any financial advice._
