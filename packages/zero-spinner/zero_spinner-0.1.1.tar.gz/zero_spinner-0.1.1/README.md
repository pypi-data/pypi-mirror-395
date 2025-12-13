# Zero Spinner 🌀

A minimal, dependency-free spinner for Python CLI applications with rich customization options.

[![Tests](https://github.com/matteozambon89/python-zero-spinner/actions/workflows/tests.yml/badge.svg)](https://github.com/matteozambon89/python-zero-spinner/actions/workflows/tests.yml)
[![PyPI Downloads](https://img.shields.io/pypi/dm/zero-spinner.svg)](https://pypi.org/project/zero-spinner/)
[![PyPI version](https://badge.fury.io/py/zero-spinner.svg)](https://badge.fury.io/py/zero-spinner)
[![Python Version](https://img.shields.io/pypi/pyversions/zero-spinner)](https://pypi.org/project/zero-spinner/)
[![License](https://img.shields.io/pypi/l/zero-spinner)](LICENSE)

## Features

- 🌈 **Rich Color Options** - 16 standard colors, RGB support, and special color cycles (rainbow, unicorn)
- 🎨 **Unicode & ASCII Support** - Automatically falls back to ASCII in incompatible terminals
- 🔄 **Context Manager** - Clean, Pythonic usage with automatic cleanup
- 🎯 **Multiple End States** - Success, failure, warning, and info completion states
- 🛠️ **Highly Customizable** - Prefix, suffix, indent, and custom symbols
- 🤖 **CI Aware** - Automatically disables in CI environments
- 🪶 **Zero Dependencies** - Lightweight with no external dependencies
- ⚡ **Thread Safe** - Non-blocking animation using threading

## Installation

Install from PyPI using pip:

```bash
pip install zero-spinner
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv add zero-spinner
```

Or using [poetry](https://python-poetry.org)

```bash
poetry add zero-spinner
```

## Quick Start

```python
from yeeti.zero_spinner import spinner

# Basic usage
spin = spinner('Loading...').start()
# ... do work ...
spin.succeed()

# Context manager (recommended)
with spinner('Processing'):
    # ... do work ...
    pass
```

## Detailed Usage

### Basic Spinner

```python
from yeeti.zero_spinner import spinner

# Simple spinner
with spinner('Loading data...'):
    # Your code here
    import time
    time.sleep(2)
```

### Custom Colors

```python
# Standard colors
with spinner('Processing...', color='red'):
    # ... work ...
    pass

# RGB colors
with spinner('RGB spinner...', color='rgb(255,105,180)'):
    # ... work ...
    pass

# Special color cycles
spin = spinner('Rainbow effect...')
spin.color = spin._colors.rainbow  # or rainbow_bright, rainbow_rgb, unicorn, unicorn_rgb
spin.start()
# ... work ...
spin.succeed()
```

### Completion States

```python
from yeeti.zero_spinner import spinner

spin = spinner('Processing...').start()

try:
    # ... work that might fail ...
    spin.succeed('Process completed successfully!')
except Exception as e:
    spin.fail(f'Process failed: {str(e)}')

# Other states
spin = spinner('Checking...').start()
spin.warn('This is just a warning')
# or
spin.info('For your information')
```

### Customization Options

```python
# All customization options
with spinner(
    text='Main text',
    prefix_text='[INFO] ',
    suffix_text=' (processing)',
    color='magenta',
    hide_cursor=True,
    indent=2,
    stream=sys.stdout,  # defaults to stdout
    disabled=False      # set to True to disable
):
    # ... work ...
    pass
```

### Context Manager Behavior

The spinner automatically ends with success if no exception occurs:

```python
# Automatically succeeds
with spinner('Task 1'):
    # ... work ...
    pass

# Automatically fails
with spinner('Task 2'):
    raise Exception('Something went wrong!')
```

## API Reference

### `spinner()` Function

Creates and returns a new Spinner instance.

```python
spinner(
    text='',
    prefix_text='',
    suffix_text='',
    color='cyan',
    hide_cursor=True,
    indent=0,
    stream=None,
    disabled=False,
    spinner=None,
    symbols=None,
    colors=None
) -> Spinner
```

**Parameters:**

- `text` (str): Main text displayed next to spinner
- `prefix_text` (str): Text before spinner
- `suffix_text` (str): Text after spinner and main text
- `color` (str): Spinner color (standard name or 'rgb(r,g,b)')
- `hide_cursor` (bool): Hide terminal cursor while spinning
- `indent` (int): Number of spaces to indent
- `stream` (TextIO): Output stream (defaults to stdout)
- `disabled` (bool): Disable spinner (useful for testing)
- `spinner` (SpinnerDefinition): Custom spinner frames/interval
- `symbols` (Symbols): Custom completion symbols
- `colors` (Colors): Custom color definitions

### `Spinner` Class

#### Methods

- `start(text=None)` - Start spinning
- `stop()` - Stop spinning
- `succeed(text=None)` - Stop with success symbol
- `fail(text=None)` - Stop with failure symbol
- `warn(text=None)` - Stop with warning symbol
- `info(text=None)` - Stop with info symbol
- `end(symbol, color=None, text=None)` - Stop with custom symbol

#### Properties

- `text` (str): Main text
- `color` (str): Current color

### Color Options

Standard colors:

- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- `bright_black`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`

Special color cycles:

- `random` - Randomly selected color
- `rainbow` - Standard rainbow colors
- `rainbow_bright` - Bright rainbow colors
- `rainbow_rgb` - Smooth RGB rainbow
- `unicorn` - Unicorn-themed colors
- `unicorn_rgb` - Smooth RGB unicorn colors

RGB colors: `rgb(255,0,0)` (red) format

### Symbols

Completion symbols automatically adapt to terminal capabilities:

- Success: ✔ (+ in ASCII mode)
- Failure: ✗ (X in ASCII mode)
- Warning: ⚠ (! in ASCII mode)
- Info: ℹ (i in ASCII mode)

## Advanced Examples

### Custom Spinner Animation

```python
from yeeti.zero_spinner import spinner, SpinnerDefinition

custom_spinner = SpinnerDefinition()
custom_spinner.frames = ['-', '=', '≡', '=', '-', ' ']
custom_spinner.interval = 100  # ms

# or simply
# custom_spinner = SpinnerDefinition(['-', '=', '≡', '=', '-', ' '], 100)

with spinner('Custom animation...', spinner=custom_spinner):
    # ... work ...
    pass
```

### Progress Updates

```python
spin = spinner('Processing items...').start()

for i, item in enumerate(items):
    spin.text = f'Processing items... ({i+1}/{len(items)})'
    # Process item
    time.sleep(0.1)

spin.succeed('All items processed!')
```

### Multiple Spinners

> _WARNING_ Currently not working!

```python
# Nested spinners
with spinner('Main process') as spin:
    with spinner('Subprocess 1', indent=2) as sub1:
        # ... work ...
        sub1.succeed()

    with spinner('Subprocess 2', indent=2) as sub2:
        # ... work ...
        sub2.succeed()

    spin.succeed()
```

## Compatibility

Zero Spinner works in:

- Unix terminals (Linux, macOS)
- Windows Command Prompt and PowerShell
- IDE terminals (VS Code, PyCharm, etc.)
- SSH sessions
- CI environments (automatically disabled)

The library automatically detects Unicode support and falls back to ASCII characters when needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Author

© 2025 Yeeti
