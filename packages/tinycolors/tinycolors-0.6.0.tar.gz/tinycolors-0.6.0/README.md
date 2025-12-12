# tinycolors

A tiny, useful, and readable color library for terminal output. Perfect for fast, simple ANSI color formatting in Python applications.

## Installation

Install from PyPI:

```bash
pip install tinycolors
```

## Quick Start

### Basic Colorization

```python
from tinycolors import colorize, cprint, cinput

# Colorize text with ANSI codes
red_text = colorize("Hello", color="red")
print(red_text)

# Print colored text directly
cprint("Success!", color="green")
cprint("Warning", color="yellow", style="bold")

# Input with colored prompt
name = cinput("Enter your name: ", color="blue")
```

### Using Color Classes

```python
from tinycolors import color, clib

# Basic colors
print(color.red + "Red text" + color.reset)
print(clib.green + "Green text" + clib.reset)

# Bright colors
print(color.bright.cyan + "Bright cyan" + color.reset)

# Background colors
print(color.bg.yellow + "Yellow background" + color.reset)
print(color.bg.bright.blue + "Bright blue background" + color.reset)

# Text styles
print(color.bold.red + "Bold red" + color.reset)
print(color.underline.blue + "Underlined blue" + color.reset)
print(color.italic.green + "Italic green" + color.reset)
```

## Features

- **Simple API**: Easy-to-use functions for colorizing text
- **ANSI Support**: Full support for foreground and background colors
- **Styles**: Bold, dim, italic, underline, and more
- **Tiny**: Minimal overhead, no external dependencies
- **Readable**: Clean, intuitive class structure
- **Fast**: Pure Python with no dependencies

## Available Colors

- Basic: black, red, green, yellow, blue, magenta, cyan, white
- Bright variants: bright black, bright red, bright green, bright yellow, bright blue, bright magenta, bright cyan, bright white
- Background colors available for all variants

## Available Styles

- bold
- dim
- italic
- underline
- blink
- fast_blink
- inverse
- hidden
- strike

## License

MIT License - See LICENSE file for details
