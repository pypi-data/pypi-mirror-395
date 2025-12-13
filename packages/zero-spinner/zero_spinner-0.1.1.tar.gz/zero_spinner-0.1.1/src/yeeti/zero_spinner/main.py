# Copyright (C) 2025 Yeeti

"""Minimal spinner for Python CLI applications.

Usage:
    from yeeti.zero_spinner import spinner

    # Basic usage
    spin = spinner('Loading...').start()
    # ... do work ...
    spin.succeed()

    # Context manager
    with spinner('Processing'):
        # ... do work ...
        pass
"""

import os
import random
import re
import sys
import threading
import time
from itertools import cycle
from typing import Iterator, TextIO

# Check if Unicode is supported
try:
    '⠋'.encode(sys.stdout.encoding)
    UNICODE_SUPPORTED = True
except (UnicodeEncodeError, AttributeError):
    UNICODE_SUPPORTED = False


class Colors:
    """ANSI color codes."""

    _random: list[str] = [
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
        'bright_black',
        'bright_red',
        'bright_green',
        'bright_yellow',
        'bright_blue',
        'bright_magenta',
        'bright_cyan',
        'bright_white',
    ]
    _cycle_rainbow: Iterator[str] = cycle([
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ])
    _cycle_rainbow_bright: Iterator[str] = cycle([
        'bright_red',
        'bright_green',
        'bright_yellow',
        'bright_blue',
        'bright_magenta',
        'bright_cyan',
        'bright_white',
    ])
    _cycle_rainbow_rgb: Iterator[str] = cycle([
        'rgb(255,0,0)',
        'rgb(255,16,0)',
        'rgb(255,32,0)',
        'rgb(255,48,0)',
        'rgb(255,64,0)',
        'rgb(255,80,0)',
        'rgb(255,96,0)',
        'rgb(255,112,0)',
        'rgb(255,128,0)',
        'rgb(255,144,0)',
        'rgb(255,160,0)',
        'rgb(255,176,0)',
        'rgb(255,192,0)',
        'rgb(255,208,0)',
        'rgb(255,224,0)',
        'rgb(255,240,0)',
        'rgb(224,255,0)',
        'rgb(192,255,0)',
        'rgb(160,255,0)',
        'rgb(128,255,0)',
        'rgb(96,255,0)',
        'rgb(64,255,0)',
        'rgb(32,255,0)',
        'rgb(0,255,0)',
        'rgb(0,255,32)',
        'rgb(0,255,64)',
        'rgb(0,255,96)',
        'rgb(0,255,128)',
        'rgb(0,255,160)',
        'rgb(0,255,192)',
        'rgb(0,255,224)',
        'rgb(0,255,255)',
        'rgb(0,224,255)',
        'rgb(0,192,255)',
        'rgb(0,160,255)',
        'rgb(0,128,255)',
        'rgb(0,96,255)',
        'rgb(0,64,255)',
        'rgb(0,32,255)',
        'rgb(0,0,255)',
        'rgb(32,0,255)',
        'rgb(64,0,255)',
        'rgb(96,0,255)',
        'rgb(128,0,255)',
        'rgb(160,0,255)',
        'rgb(192,0,255)',
        'rgb(224,0,255)',
        'rgb(255,0,255)',
        'rgb(255,0,224)',
        'rgb(255,0,192)',
        'rgb(255,0,160)',
        'rgb(255,0,128)',
        'rgb(255,0,96)',
        'rgb(255,0,64)',
        'rgb(255,0,32)',
    ])
    _cycle_unicorn: Iterator[str] = cycle([
        'magenta',
        'bright_magenta',
        'cyan',
        'bright_cyan',
        'white',
        'bright_white',
    ])
    _cycle_unicorn_rgb: Iterator[str] = cycle([
        'rgb(255,105,180)',  # Hot Pink
        'rgb(255,20,147)',  # Deep Pink
        'rgb(219,112,147)',  # Pale Violet Red
        'rgb(199,21,133)',  # Medium Violet Red
        'rgb(218,112,214)',  # Orchid
        'rgb(186,85,211)',  # Medium Orchid
        'rgb(153,50,204)',  # Dark Orchid
        'rgb(147,112,219)',  # Medium Purple
        'rgb(138,43,226)',  # Blue Violet
        'rgb(148,0,211)',  # Dark Violet
        'rgb(123,104,238)',  # Medium Slate Blue
        'rgb(106,90,205)',  # Slate Blue
        'rgb(72,209,204)',  # Medium Turquoise
        'rgb(0,206,209)',  # Dark Turquoise
        'rgb(64,224,208)',  # Turquoise
        'rgb(127,255,212)',  # Aquamarine
        'rgb(102,205,170)',  # Medium Aquamarine
        'rgb(32,178,170)',  # Light Sea Green
        'rgb(0,191,255)',  # Deep Sky Blue
        'rgb(30,144,255)',  # Dodger Blue
        'rgb(65,105,225)',  # Royal Blue
        'rgb(135,206,250)',  # Light Sky Blue
        'rgb(173,216,230)',  # Light Blue
        'rgb(176,224,230)',  # Powder Blue
        'rgb(224,255,255)',  # Light Cyan
        'rgb(255,228,225)',  # Misty Rose
        'rgb(255,240,245)',  # Lavender Blush
        'rgb(255,245,238)',  # Seashell
        'rgb(255,250,240)',  # Floral White
        'rgb(255,255,240)',  # Ivory
        'rgb(240,255,240)',  # Honeydew
        'rgb(245,255,250)',  # Azure
        'rgb(240,248,255)',  # Alice Blue
        'rgb(230,230,250)',  # Lavender
        'rgb(216,191,216)',  # Thistle
        'rgb(221,160,221)',  # Plum
        'rgb(238,130,238)',  # Violet
        'rgb(255,130,255)',  # Magenta
        'rgb(255,105,180)',  # Hot Pink (repeated to connect)
    ])

    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    bright_black = '\033[90m'
    bright_red = '\033[91m'
    bright_green = '\033[92m'
    bright_yellow = '\033[93m'
    bright_blue = '\033[94m'
    bright_magenta = '\033[95m'
    bright_cyan = '\033[96m'
    bright_white = '\033[97m'
    reset = '\033[0m'
    hide_cursor = '\033[?25l'

    def rgb(self, r: int, g: int, b: int):
        """Return an ANSI escape sequence for RGB color.

        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).

        Returns:
            str: ANSI escape sequence for the RGB color.

        Raises:
            ValueError: If any of the RGB values are out of range.
        """
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError('RGB values must be between 0 and 255.')

        return f'\033[38;2;{r};{g};{b}m'

    def find(self, color: str) -> str:
        """Return the color code for a given color name.

        Args:
            color: The name of the color (e.g., 'red', 'green').

        Raises:
            ValueError: When color doesn't match a color code.

        Returns:
            The color code string.
        """

        rgb_pattern = re.compile(r'rgb\((\d+),(\d+),(\d+)\)')
        match = rgb_pattern.fullmatch(color)
        if match:
            r, g, b = map(int, match.groups())
            return self.rgb(r, g, b)

        color_code: str | None = getattr(self, color, None)
        if not color_code:
            raise ValueError(f"Color '{color}' not found")

        return color_code

    @property
    def random(self) -> str:
        """Return a randomly selected color code from the predefined list.

        Returns:
            str: A randomly selected ANSI color code.
        """
        color: str = random.choice(self._random)
        return self.find(color)

    @property
    def rainbow(self) -> str:
        """Return the next color in a standard rainbow cycle.

        Returns:
            str: The ANSI color code for the current rainbow color.
        """
        color: str = next(self._cycle_rainbow)
        return self.find(color)

    @property
    def rainbow_bright(self) -> str:
        """Return the next bright color in a rainbow cycle.

        Returns:
            str: The ANSI color code for the current bright rainbow color.
        """
        color: str = next(self._cycle_rainbow_bright)
        return self.find(color)

    @property
    def rainbow_rgb(self) -> str:
        """Return the next RGB color in a rainbow cycle.

        Returns:
            str: The ANSI escape sequence for the current RGB rainbow color.
        """
        color: str = next(self._cycle_rainbow_rgb)
        return self.find(color)

    @property
    def unicorn(self) -> str:
        """Return the next color in a unicorn cycle.

        Returns:
            str: The ANSI color code for the current unicorn color.
        """
        color: str = next(self._cycle_unicorn)
        return self.find(color)

    @property
    def unicorn_rgb(self) -> str:
        """Return the next RGB color in a unicorn cycle.

        Returns:
            str: The ANSI escape sequence for the current RGB unicorn color.
        """
        color: str = next(self._cycle_unicorn_rgb)
        return self.find(color)


class Symbols:
    """A class to hold symbols for the application."""

    success = '✔' if UNICODE_SUPPORTED else '+'
    success_color = 'green'

    fail = '✗' if UNICODE_SUPPORTED else 'X'
    fail_color = 'red'

    warn = '⚠' if UNICODE_SUPPORTED else '!'
    warn_color = 'yellow'

    info = 'ℹ' if UNICODE_SUPPORTED else 'i'
    info_color = 'blue'


class SpinnerDefinition:
    """A Spinner definition."""

    frames: list[str] = (
        ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'] if UNICODE_SUPPORTED else ['-', '\\', '|', '/']
    )
    interval: int = 80

    def __init__(self, frames: list[str] | None = None, interval: int | None = None):
        """Initialize a SpinnerDefinition.

        Args:
            frames (list[str]|None): The frames. If None it uses the SpinnerDefinition frames. Defaults to None.
            interval (int|None): The interval in milliseconds between each frame. If None it uses the SpinnerDefinition interval. Defaults to None.
        """  # noqa: E501

        self.frames = frames or self.frames
        self.interval = interval or self.interval

    @classmethod
    def from_dict(cls, data: dict):
        """Create a SpinnerDefinition from a dictionary.

        Args:
            cls (SpinnerDefinition): The class to create.
            data (dict): The data to fill the SpinnerDefinition.

        Raises:
           ValueError: If data is not a dictionary.

        Returns:
            SpinnerDefinition: A new SpinnerDefinition instance.
        """

        if not isinstance(data, dict):
            raise ValueError('data must be a dictionary.')

        frames = data.get('frames')
        if not frames:
            raise ValueError('data.frames is missing.')
        if not isinstance(frames, list):
            raise ValueError('data.frames is not a list.')
        if [isinstance(f, str) for f in frames].count(False) > 0:
            raise ValueError('data.frames[x] must contain only strings.')

        interval = data.get('interval')
        if not interval:
            raise ValueError('data.interval is missing.')
        if not isinstance(interval, int):
            raise ValueError('data.interval must be a int.')

        return cls(
            frames=frames,
            interval=interval,
        )


class Spinner:
    """A Spinner class."""

    _prefix_text: str
    _suffix_text: str
    _hide_cursor: bool
    _indent: int
    _thread: None | threading.Thread
    _stop: None | threading.Event
    _spinning: bool

    _spinner: SpinnerDefinition
    _frames: Iterator[str]
    _interval: int
    _steam: TextIO
    _disabled: bool
    _symbols: Symbols
    _colors: Colors

    text: str
    color: str

    def __init__(
        self,
        text='',
        prefix_text='',
        suffix_text='',
        color='cyan',
        hide_cursor=True,
        indent: int = 0,
        stream: TextIO | None = None,
        disabled: bool = False,
        spinner: SpinnerDefinition | None = None,
        symbols: Symbols | None = None,
        colors: Colors | None = None,
    ):
        """Initialize a spinner.

        Args:
            text (str): The main text to display next to the spinner. Defaults to ''.
            prefix_text (str): Text to display before the spinner. Defaults to ''.
            suffix_text (str): Text to display after the spinner and main text. Defaults to ''.
            color (str): Spinner color. Defaults to 'cyan'.
            hide_cursor (bool): Whether to hide the terminal cursor while spinning. Defaults to True.
            indent (int): Number of spaces to indent the spinner line. Defaults to 0.
            stream (TextIO | None): Output stream. If None, uses stdout. Defaults to None.
            disabled (bool): Whether the spinner is enabled or not. Defaults to False.
            spinner (SpinnerDefinition | None): Spinner definition. If None, uses the spinner's default. Defaults to None.
            symbols (Symbols | None): Custom symbols for spinner. If None, uses the spinner's default. Defaults to None.
            colors (Colors | None): Custom colors for spinner. If None, uses the spinner's default. Defaults to None.
        """  # noqa: E501

        self._spinner: SpinnerDefinition = spinner or SpinnerDefinition()
        self._frames = cycle(self._spinner.frames)
        self._interval = self._spinner.interval

        self.text = text
        self.color = color
        self._prefix_text = prefix_text
        self._suffix_text = suffix_text
        self._hide_cursor = hide_cursor
        self._indent = indent
        self._stream = stream or sys.stdout
        self._disabled = disabled or not self._stream.isatty() or self._is_ci_environment()
        self._thread = None
        self._stop = None
        self._spinning = False
        self._symbols = symbols or Symbols()
        self._colors = colors or Colors()

    def _is_ci_environment(self) -> bool:
        """Check if running in a CI environment like GitHub Actions.

        Returns:
           bool: True if running in a CI, False otherwise.
        """

        ci_env_vars = [
            'CI',  # Common CI environment variable
            'GITHUB_ACTIONS',  # GitHub Actions
            'GITLAB_CI',  # GitLab CI
            'TRAVIS',  # Travis CI
            'CIRCLECI',  # CircleCI
            'JENKINS_URL',  # Jenkins
            'TEAMCITY_VERSION',  # TeamCity
        ]
        return any(os.environ.get(var) for var in ci_env_vars)

    def start(self, text=None):
        """Start spinning, with text if provided.

        Args:
            text (str, optional): Text to display.

        Returns:
            Spinner: This spinner
        """

        if text:
            self.text = text

        if self._disabled:
            print(self.text, file=self._stream, flush=True)
            return self

        if self._spinning:
            return self

        self._spinning = True
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._animate)
        self._thread.daemon = True
        self._thread.start()
        return self

    def _format(
        self,
        symbol: str,
        color: str,
        text: str,
        indent: int = 0,
        prefix_text: str = '',
        suffix_text: str = '',
    ):
        color_code = self._colors.find(color)

        return '\r' + ''.join(
            (
                ' ' * indent,
                prefix_text,
                color_code,
                symbol,
                self._colors.reset,
                suffix_text,
                ' ',
                text,
            ),
        )

    def _animate(self):
        # Hide cursor
        if self._stream.isatty() and self._hide_cursor:
            print(self._colors.hide_cursor, file=self._stream, end='')

        if not self._stop:
            raise TypeError('_stop is not supposed to be None')

        while not self._stop.is_set():
            frame: str = next(self._frames)
            line: str = self._format(
                frame,
                self.color,
                self.text,
                self._indent,
                self._prefix_text,
                self._suffix_text,
            )
            print(line, file=self._stream, end='', flush=True)
            time.sleep(self._interval / 1000)

    def stop(self):
        """Stop spinning.

        Raises:
            TypeError: If something is misconfigured.

        Returns:
            Spinner: This spinner.
        """

        if self._disabled:
            return self

        if not self._stop:
            raise TypeError('_stop is not supposed to be None')
        if not self._thread:
            raise TypeError('_thread is not supposed to be None')

        if self._spinning:
            self._stop.set()
            self._thread.join()
            self._spinning = False
            if self._stream.isatty():
                print('\r\033[K\033[?25h', file=self._stream, end='')
        return self

    def end(self, symbol: str, color: str | None = None, text: str | None = None):
        """Stop spinning and persist the text with the symbol.

        If color is not provided, the current color will be used.
        If text is not provided, the current text will be used.

        Args:
            symbol (str): The symbol to display instead of the spinner.
            color (str|None): The color to use for the symbol. Defaults to None.
            text (str|None): The main text to display next to the spinner. Defaults to None.

        Returns:
            Spinner: This spinner.
        """

        self.stop()
        line: str = self._format(
            symbol,
            color or self.color,
            text or self.text,
            self._indent,
            self._prefix_text,
            self._suffix_text,
        )
        print(line, file=self._stream)
        return self

    def succeed(self, text: str | None = None):
        """Stop spinning and persist the text as success.

        If text is not provided, the current text will be used.

        Args:
            text (str|None): The main text to display next to the spinner. Defaults to None.

        Returns:
            Spinner: This spinner.
        """

        return self.end(
            self._symbols.success,
            self._symbols.success_color,
            text,
        )

    def fail(self, text: str | None = None):
        """Stop spinning and persist the text as failure.

        If text is not provided, the current text will be used.

        Args:
            text (str|None): The main text to display next to the spinner. Defaults to None.

        Returns:
            Spinner: This spinner.
        """

        return self.end(
            self._symbols.fail,
            self._symbols.fail_color,
            text,
        )

    def warn(self, text: str | None = None):
        """Stop spinning and persist the text as warning.

        If text is not provided, the current text will be used.

        Args:
            text (str|None): The main text to display next to the spinner. Defaults to None.

        Returns:
            Spinner: This spinner.
        """

        return self.end(
            self._symbols.warn,
            self._symbols.warn_color,
            text,
        )

    def info(self, text=None):
        """Stop spinning and persist the text as info.

        If text is not provided, the current text will be used.

        Args:
            text (str): The main text to display next to the spinner. Defaults to None.

        Returns:
            Spinner: This spinner.
        """

        return self.end(
            self._symbols.info,
            self._symbols.info_color,
            text,
        )

    def __enter__(self):
        """Start the spinner when entering a context.

        Returns:
            Spinner: This spinner.
        """

        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the spinner with either failure of success when exiting a context.

        Returns:
           bool: False to propagate any exception.
        """
        if exc_type:
            self.fail()
        else:
            self.succeed()
        return False


def spinner(
    text='',
    prefix_text='',
    suffix_text='',
    color='cyan',
    hide_cursor=True,
    indent: int = 0,
    stream: TextIO | None = None,
    disabled: bool = False,
    spinner: SpinnerDefinition | None = None,
    symbols: Symbols | None = None,
    colors: Colors | None = None,
) -> Spinner:
    """Create a new spinner instance.

    Args:
        text (str): The main text to display next to the spinner. Defaults to ''.
        prefix_text (str): Text to display before the spinner. Defaults to ''.
        suffix_text (str): Text to display after the spinner and main text. Defaults to ''.
        color (str): Spinner color. Defaults to 'cyan'.
        hide_cursor (bool): Whether to hide the terminal cursor while spinning. Defaults to True.
        indent (int): Number of spaces to indent the spinner line. Defaults to 0.
        stream (TextIO | None): Output stream. If None, uses stdout. Defaults to None.
        disabled (bool): Whether the spinner is enabled or not. Defaults to False.
        spinner (SpinnerDefinition | None): Spinner definition. If None, uses the spinner's default. Defaults to None.
        symbols (Symbols | None): Custom symbols for spinner. If None, uses the spinner's default. Defaults to None.
        colors (Colors | None): Custom colors for spinner. If None, uses the spinner's default. Defaults to None.

    Returns:
        Spinner: A new spinner instance.
    """  # noqa: E501

    return Spinner(
        text,
        prefix_text,
        suffix_text,
        color,
        hide_cursor,
        indent,
        stream,
        disabled,
        spinner,
        symbols,
        colors,
    )
