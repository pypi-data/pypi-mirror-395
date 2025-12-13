import asyncio
import re
import blessed
from .config import config


_original_message = "Q -> Main Menu"
_current_message = _original_message

_ansi_escape_pattern = re.compile(r'\x1b\[[0-9;]*m')


def _strip_ansi(text: str) -> str:
    return _ansi_escape_pattern.sub('', text)


def _truncate_with_ansi(text: str, max_len: int) -> str:
    result = []
    visible_count = 0
    i = 0
    while i < len(text) and visible_count < max_len:
        match = _ansi_escape_pattern.match(text, i)
        if match:
            result.append(match.group())
            i = match.end()
        else:
            result.append(text[i])
            visible_count += 1
            i += 1
    while i < len(text):
        match = _ansi_escape_pattern.match(text, i)
        if match:
            result.append(match.group())
            i = match.end()
        else:
            break
    return ''.join(result)


async def input_handler():
    global _current_message
    _current_message = _original_message
    with config.terminal.cbreak():
        while config.current_mode in ("chart", "symbol", "interval", "orderbook"):
            clear_eol = blessed.Terminal().clear_eol
            term_width = config.terminal.width or 80
            if config.terminal.kbhit(timeout=0.1):
                key = config.terminal.inkey(timeout=0)

                if key == 'q':
                    _current_message = "Quitting..."
                    display_msg = _current_message[:term_width - 1] if len(
                        _current_message) >= term_width else _current_message
                    print(f"{display_msg}{clear_eol}",
                          end="\r", flush=True)
                    config.current_mode = "menu"
                    return
            visible_length = len(_strip_ansi(_current_message))
            if visible_length >= term_width:
                display_msg = _truncate_with_ansi(
                    _current_message, term_width - 1)
            else:
                display_msg = _current_message
            print(f"{display_msg}{clear_eol}",
                  end="\r", flush=True)
            await asyncio.sleep(0.05)


def set_current_message(message: str):
    global _current_message
    _current_message = message


def reset_current_message():
    global _current_message
    _current_message = _original_message
