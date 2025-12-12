"""
tinycolors v0.6.0:
A tiny, useful, and readable color library for fast colors, and a large library.
Having a very large library of colorization and super readable syntax, tinycolors is
the color library you were looking for.
"""

from sys import platform
from typing import Any, Literal, TypedDict

if platform == "win32":
    from os import system
    system('')

# ---------------------------------------------------------
# Node wrapper
# ---------------------------------------------------------

class NodeProxy:
    def __init__(self, cls) -> None:
        self._cls = cls

    def __getattr__(self, item):
        attr = getattr(self._cls, item)
        if isinstance(attr, type):
            return NodeProxy(attr)
        return attr

    def __repr__(self):
        return f"<colornode {self._cls.__name__} with code {self._cls.value!r}>"

    def __str__(self):
        return getattr(self._cls, "value", "\033[0m")

def stylenode(cls):
    return NodeProxy(cls)

# ---------------------------------------------------------
# Color class with ANSI escape codes
# ---------------------------------------------------------

class clib:
    """Basic color library class with ANSI escape codes."""
    black       = "\033[30m"
    red         = "\033[31m"
    green       = "\033[32m"
    yellow      = "\033[33m"
    blue        = "\033[34m"
    magenta     = "\033[35m"
    cyan        = "\033[36m"
    white       = "\033[37m"
    gray        = "\033[90m"
    default     = "\033[39m"
    reset       = "\033[0m"

    palette     = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white"
    ]

class color:
    """The elegant color class with classic ANSI codes."""
    reset       = "\033[0m"
    black       = "\033[30m"
    red         = "\033[31m"
    green       = "\033[32m"
    yellow      = "\033[33m"
    blue        = "\033[34m"
    magenta     = "\033[35m"
    cyan        = "\033[36m"
    white       = "\033[37m"
    gray        = "\033[90m"
    default     = "\033[39m"
    class bright:
        """Bright color variants"""
        black       = "\033[90m"
        red         = "\033[91m"
        green       = "\033[92m"
        yellow      = "\033[93m"
        blue        = "\033[94m"
        magenta     = "\033[95m"
        cyan        = "\033[96m"
        white       = "\033[97m"
        reset       = "\033[0m"

    class bg:
        """Background colors"""
        black       = "\033[40m"
        red         = "\033[41m"
        green       = "\033[42m"
        yellow      = "\033[43m"
        blue        = "\033[44m"
        magenta     = "\033[45m"
        cyan        = "\033[46m"
        white       = "\033[47m"
        gray        = "\033[100m"
        default     = "\033[49m"
        reset       = "\033[0m"

        class bright:
            """Bright background color variants"""
            black       = "\033[100m"
            red         = "\033[101m"
            green       = "\033[102m"
            yellow      = "\033[103m"
            blue        = "\033[104m"
            magenta     = "\033[105m"
            cyan        = "\033[106m"
            white       = "\033[107m"
            reset       = "\033[0m"

    @stylenode
    class bold:
        """Bold style"""
        value = "\033[1m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class dim:
        """Dim style"""
        value = "\033[2m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class italic:
        """Italic style"""
        value = "\033[3m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class underline:
        """Underline style"""
        value = "\033[4m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class blinking:
        """Blinking style"""
        value = "\033[5m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class fast_blinking:
        """Blinking style, but faster"""
        value = "\033[6m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class inverted:
        """Inverted background and foreground colors style"""
        value = "\033[7m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class hidden:
        # This class was purposely not have given a docstring, because it's hidden. (get it)
        value = "\033[8m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"

    @stylenode
    class striked:
        """Your text is striked (struck) in the chest!"""
        value = "\033[9m"

        for color_name in clib.palette:
            locals()[color_name] = value + getattr(clib, color_name)
        reset = "\033[0m"


    class style:
        """Basic style library"""
        reset       = "\033[0m"
        bold        = "\033[1m"
        dim         = "\033[2m"
        italic      = "\033[3m"
        underline   = "\033[4m"
        blink       = "\033[5m"
        fast_blink  = "\033[6m"
        inverse     = "\033[7m"
        hidden      = "\033[8m"
        strike      = "\033[9m"

# ---------------------------------------------------------
# Type definitions
# ---------------------------------------------------------

COLOR_NAMES = Literal[
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "gray",
    "default",

    "bright black",
    "bright red",
    "bright green",
    "bright yellow",
    "bright blue",
    "bright magenta",
    "bright cyan",
    "bright white",

    "reset",
]

STYLE_NAMES = Literal[
    "dim",
    "bold",
    "italic",
    "underline",
    "strike",
    "blink",
    "fast_blink",
    "inverse",
    "hidden",

    "reset",
]

COLOR_MAP = {
    "black": clib.black,
    "red": clib.red,
    "green": clib.green,
    "yellow": clib.yellow,
    "blue": clib.blue,
    "magenta": clib.magenta,
    "cyan": clib.cyan,
    "white": clib.white,
    "gray": clib.gray,
    "default": clib.default,

    "bright black": color.bright.black,
    "bright red": color.bright.red,
    "bright green": color.bright.green,
    "bright yellow": color.bright.yellow,
    "bright blue": color.bright.blue,
    "bright magenta": color.bright.magenta,
    "bright cyan": color.bright.cyan,
    "bright white": color.bright.white,

    "reset": clib.reset,
}

STYLE_MAP = {
    "dim": color.style.dim,
    "bold": color.style.bold,
    "italic": color.style.italic,
    "underline": color.style.underline,
    "strike": color.style.strike,
    "blink": color.style.blink,
    "fast_blink": color.style.fast_blink,
    "inverse": color.style.inverse,
    "hidden": color.style.hidden,

    "reset": color.style.reset,
}

BG_COLOR_MAP = {
    "black": color.bg.black,
    "red": color.bg.red,
    "green": color.bg.green,
    "yellow": color.bg.yellow,
    "blue": color.bg.blue,
    "magenta": color.bg.magenta,
    "cyan": color.bg.cyan,
    "white": color.bg.white,
    "gray": color.bg.gray,
    "default": color.bg.default,
    "bright black": color.bg.bright.black,
    "bright red": color.bg.bright.red,
    "bright green": color.bg.bright.green,
    "bright yellow": color.bg.bright.yellow,
    "bright blue": color.bg.bright.blue,
    "bright magenta": color.bg.bright.magenta,
    "bright cyan": color.bg.bright.cyan,
    "bright white": color.bg.bright.white,

    "reset": color.bg.reset,
}

# ---------------------------------------------------------
# Combined style maps for simplified API
# ---------------------------------------------------------

# Generate all style + color combinations programmatically
_STYLES_DICT = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "fast_blink": "\033[6m",
    "inverse": "\033[7m",
    "hidden": "\033[8m",
    "strike": "\033[9m",
}

_COLORS_DICT = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
    "default": "\033[39m",
    "bright black": "\033[90m",
    "bright red": "\033[91m",
    "bright green": "\033[92m",
    "bright yellow": "\033[93m",
    "bright blue": "\033[94m",
    "bright magenta": "\033[95m",
    "bright cyan": "\033[96m",
    "bright white": "\033[97m",
}

_BG_COLORS_DICT = {
    "black": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
    "gray": "\033[100m",
    "default": "\033[49m",
    "bright black": "\033[100m",
    "bright red": "\033[101m",
    "bright green": "\033[102m",
    "bright yellow": "\033[103m",
    "bright blue": "\033[104m",
    "bright magenta": "\033[105m",
    "bright cyan": "\033[106m",
    "bright white": "\033[107m",
}

# COMBINED_STYLES: All style + color combinations (162 total: 9 styles × 18 colors)
COMBINED_STYLES = {}
for style_name, style_code in _STYLES_DICT.items():
    for color_name, color_code in _COLORS_DICT.items():
        key = f"{style_name} {color_name}"
        COMBINED_STYLES[key] = style_code + color_code

# COMBINED_STYLES_WITH_BG: Practical style + foreground + background combinations
# Focus on high contrast and commonly used patterns
COMBINED_STYLES_WITH_BG = {
    # Bold combinations (most common)
    "bold red on black": "\033[1m\033[31m\033[40m",
    "bold red on white": "\033[1m\033[31m\033[47m",
    "bold white on red": "\033[1m\033[37m\033[41m",
    "bold white on blue": "\033[1m\033[37m\033[44m",
    "bold white on green": "\033[1m\033[37m\033[42m",
    "bold white on black": "\033[1m\033[37m\033[40m",
    "bold black on white": "\033[1m\033[30m\033[47m",
    "bold black on yellow": "\033[1m\033[30m\033[43m",
    "bold yellow on black": "\033[1m\033[33m\033[40m",
    "bold yellow on blue": "\033[1m\033[33m\033[44m",
    "bold green on black": "\033[1m\033[32m\033[40m",
    "bold blue on black": "\033[1m\033[34m\033[40m",
    "bold cyan on black": "\033[1m\033[36m\033[40m",
    "bold magenta on black": "\033[1m\033[35m\033[40m",
    "bold bright white on red": "\033[1m\033[97m\033[41m",
    "bold bright white on blue": "\033[1m\033[97m\033[44m",
    "bold bright white on green": "\033[1m\033[97m\033[42m",
    "bold bright white on black": "\033[1m\033[97m\033[40m",
    "bold bright red on black": "\033[1m\033[91m\033[40m",
    "bold bright green on black": "\033[1m\033[92m\033[40m",
    "bold bright blue on black": "\033[1m\033[94m\033[40m",
    "bold bright yellow on black": "\033[1m\033[93m\033[40m",
    "bold bright cyan on black": "\033[1m\033[96m\033[40m",
    "bold bright magenta on black": "\033[1m\033[95m\033[40m",

    # Italic combinations
    "italic cyan on black": "\033[3m\033[36m\033[40m",
    "italic bright cyan on black": "\033[3m\033[96m\033[40m",
    "italic blue on black": "\033[3m\033[34m\033[40m",
    "italic green on black": "\033[3m\033[32m\033[40m",
    "italic white on blue": "\033[3m\033[37m\033[44m",
    "italic white on black": "\033[3m\033[37m\033[40m",
    "italic gray on black": "\033[3m\033[90m\033[40m",

    # Underline combinations
    "underline red on black": "\033[4m\033[31m\033[40m",
    "underline blue on black": "\033[4m\033[34m\033[40m",
    "underline cyan on black": "\033[4m\033[36m\033[40m",
    "underline white on blue": "\033[4m\033[37m\033[44m",
    "underline white on red": "\033[4m\033[37m\033[41m",
    "underline bright cyan on black": "\033[4m\033[96m\033[40m",

    # Dim combinations
    "dim white on black": "\033[2m\033[37m\033[40m",
    "dim green on black": "\033[2m\033[32m\033[40m",
    "dim red on black": "\033[2m\033[31m\033[40m",
    "dim yellow on black": "\033[2m\033[33m\033[40m",
    "dim cyan on black": "\033[2m\033[36m\033[40m",
    "dim gray on black": "\033[2m\033[90m\033[40m",

    # Inverse combinations
    "inverse red on white": "\033[7m\033[31m\033[47m",
    "inverse white on black": "\033[7m\033[37m\033[40m",
    "inverse black on white": "\033[7m\033[30m\033[47m",
    "inverse blue on white": "\033[7m\033[34m\033[47m",

    # Strike combinations
    "strike red on black": "\033[9m\033[31m\033[40m",
    "strike white on red": "\033[9m\033[37m\033[41m",
    "strike gray on black": "\033[9m\033[90m\033[40m",

    # Blink combinations (for warnings/alerts)
    "blink red on black": "\033[5m\033[31m\033[40m",
    "blink white on red": "\033[5m\033[37m\033[41m",
    "blink yellow on black": "\033[5m\033[33m\033[40m",

    # Fast blink combinations
    "fast_blink red on black": "\033[6m\033[31m\033[40m",
    "fast_blink white on red": "\033[6m\033[37m\033[41m",

    # Hidden combinations (for sensitive data)
    "hidden white on black": "\033[8m\033[37m\033[40m",
    "hidden black on black": "\033[8m\033[30m\033[40m",

    # Additional high-contrast combinations
    "bold black on cyan": "\033[1m\033[30m\033[46m",
    "bold black on green": "\033[1m\033[30m\033[42m",
    "bold black on magenta": "\033[1m\033[30m\033[45m",
    "bold red on yellow": "\033[1m\033[31m\033[43m",
    "bold blue on white": "\033[1m\033[34m\033[47m",
    "bold green on white": "\033[1m\033[32m\033[47m",
    "bold magenta on white": "\033[1m\033[35m\033[47m",

    # Bright background combinations
    "bold black on bright white": "\033[1m\033[30m\033[107m",
    "bold black on bright yellow": "\033[1m\033[30m\033[103m",
    "bold black on bright cyan": "\033[1m\033[30m\033[106m",
    "bold black on bright green": "\033[1m\033[30m\033[102m",
    "bold white on bright red": "\033[1m\033[37m\033[101m",
    "bold white on bright blue": "\033[1m\033[37m\033[104m",
    "bold white on bright magenta": "\033[1m\033[37m\033[105m",
    "bold bright white on bright red": "\033[1m\033[97m\033[101m",
    "bold bright white on bright blue": "\033[1m\033[97m\033[104m",

    # Common UI patterns
    "italic white on gray": "\033[3m\033[37m\033[100m",
    "underline green on black": "\033[4m\033[32m\033[40m",
    "underline yellow on black": "\033[4m\033[33m\033[40m",
    "dim blue on black": "\033[2m\033[34m\033[40m",
    "dim magenta on black": "\033[2m\033[35m\033[40m",
}

# Type literal for all combined styles
COMBINED_STYLES_LITERAL = Literal[
    # All style + color combinations (162 entries)
    "bold black", "bold red", "bold green", "bold yellow", "bold blue", "bold magenta",
    "bold cyan", "bold white", "bold gray", "bold default", "bold bright black",
    "bold bright red", "bold bright green", "bold bright yellow", "bold bright blue",
    "bold bright magenta", "bold bright cyan", "bold bright white",

    "dim black", "dim red", "dim green", "dim yellow", "dim blue", "dim magenta",
    "dim cyan", "dim white", "dim gray", "dim default", "dim bright black",
    "dim bright red", "dim bright green", "dim bright yellow", "dim bright blue",
    "dim bright magenta", "dim bright cyan", "dim bright white",

    "italic black", "italic red", "italic green", "italic yellow", "italic blue", "italic magenta",
    "italic cyan", "italic white", "italic gray", "italic default", "italic bright black",
    "italic bright red", "italic bright green", "italic bright yellow", "italic bright blue",
    "italic bright magenta", "italic bright cyan", "italic bright white",

    "underline black", "underline red", "underline green", "underline yellow", "underline blue", "underline magenta",
    "underline cyan", "underline white", "underline gray", "underline default", "underline bright black",
    "underline bright red", "underline bright green", "underline bright yellow", "underline bright blue",
    "underline bright magenta", "underline bright cyan", "underline bright white",

    "blink black", "blink red", "blink green", "blink yellow", "blink blue", "blink magenta",
    "blink cyan", "blink white", "blink gray", "blink default", "blink bright black",
    "blink bright red", "blink bright green", "blink bright yellow", "blink bright blue",
    "blink bright magenta", "blink bright cyan", "blink bright white",

    "fast_blink black", "fast_blink red", "fast_blink green", "fast_blink yellow", "fast_blink blue", "fast_blink magenta",
    "fast_blink cyan", "fast_blink white", "fast_blink gray", "fast_blink default", "fast_blink bright black",
    "fast_blink bright red", "fast_blink bright green", "fast_blink bright yellow", "fast_blink bright blue",
    "fast_blink bright magenta", "fast_blink bright cyan", "fast_blink bright white",

    "inverse black", "inverse red", "inverse green", "inverse yellow", "inverse blue", "inverse magenta",
    "inverse cyan", "inverse white", "inverse gray", "inverse default", "inverse bright black",
    "inverse bright red", "inverse bright green", "inverse bright yellow", "inverse bright blue",
    "inverse bright magenta", "inverse bright cyan", "inverse bright white",

    "hidden black", "hidden red", "hidden green", "hidden yellow", "hidden blue", "hidden magenta",
    "hidden cyan", "hidden white", "hidden gray", "hidden default", "hidden bright black",
    "hidden bright red", "hidden bright green", "hidden bright yellow", "hidden bright blue",
    "hidden bright magenta", "hidden bright cyan", "hidden bright white",

    "strike black", "strike red", "strike green", "strike yellow", "strike blue", "strike magenta",
    "strike cyan", "strike white", "strike gray", "strike default", "strike bright black",
    "strike bright red", "strike bright green", "strike bright yellow", "strike bright blue",
    "strike bright magenta", "strike bright cyan", "strike bright white",

    # All style + foreground + background combinations from COMBINED_STYLES_WITH_BG
    "bold red on black", "bold red on white", "bold white on red", "bold white on blue",
    "bold white on green", "bold white on black", "bold black on white", "bold black on yellow",
    "bold yellow on black", "bold yellow on blue", "bold green on black", "bold blue on black",
    "bold cyan on black", "bold magenta on black", "bold bright white on red", "bold bright white on blue",
    "bold bright white on green", "bold bright white on black", "bold bright red on black", "bold bright green on black",
    "bold bright blue on black", "bold bright yellow on black", "bold bright cyan on black", "bold bright magenta on black",

    "italic cyan on black", "italic bright cyan on black", "italic blue on black", "italic green on black",
    "italic white on blue", "italic white on black", "italic gray on black",

    "underline red on black", "underline blue on black", "underline cyan on black", "underline white on blue",
    "underline white on red", "underline bright cyan on black",

    "dim white on black", "dim green on black", "dim red on black", "dim yellow on black",
    "dim cyan on black", "dim gray on black",

    "inverse red on white", "inverse white on black", "inverse black on white", "inverse blue on white",

    "strike red on black", "strike white on red", "strike gray on black",

    "blink red on black", "blink white on red", "blink yellow on black",

    "fast_blink red on black", "fast_blink white on red",

    "hidden white on black", "hidden black on black",

    "bold black on cyan", "bold black on green", "bold black on magenta", "bold red on yellow",
    "bold blue on white", "bold green on white", "bold magenta on white",

    "bold black on bright white", "bold black on bright yellow", "bold black on bright cyan",
    "bold black on bright green", "bold white on bright red", "bold white on bright blue",
    "bold white on bright magenta", "bold bright white on bright red", "bold bright white on bright blue",

    "italic white on gray", "underline green on black", "underline yellow on black",
    "dim blue on black", "dim magenta on black",
]

# ---------------------------------------------------------
# Custom errors
# ---------------------------------------------------------

class ColorNotFoundError(Exception):
    """Call this if the error has something to do with a color"""
    pass

class StyleNotFoundError(Exception):
    """Call this if the error has something to do with a style"""
    pass

# ---------------------------------------------------------
# TypedDict for options
# ---------------------------------------------------------

class ColorOptions(TypedDict, total=False):
    color: COLOR_NAMES | None
    style: STYLE_NAMES | None
    bg: COLOR_NAMES | None

# ---------------------------------------------------------
# Colorizing functions
# ---------------------------------------------------------

def colorize(text: Any,
             color: COLOR_NAMES | None = None,
             style: STYLE_NAMES | None = None,
             bg: COLOR_NAMES | None = None) -> str:
    """Easy colorize function with ANSI escape sequences."""
    color = color or "reset"
    style = style or "reset"
    bg = bg or "reset"

    if color not in COLOR_MAP:
        raise ColorNotFoundError(f"Color {color} is not supported.")
    if style not in STYLE_MAP:
        raise StyleNotFoundError(f"Style {style} is not supported.")
    if bg not in BG_COLOR_MAP:
        raise ColorNotFoundError(f"BG color {bg} is not supported.")

    fg_color = COLOR_MAP[color] if color != "reset" else ""
    bg_color = BG_COLOR_MAP[bg] if bg != "reset" else ""
    text_style = STYLE_MAP[style] if style != "reset" else ""
    return bg_color + fg_color + text_style + str(text) + clib.reset

def colortext(text: Any, as_: COMBINED_STYLES_LITERAL | str) -> str:
    """
    Simplified color function using combined style names.

    This function provides a cleaner, more intuitive API for colorizing text
    by accepting combined style strings like "bold red" or "italic cyan on blue"
    instead of separate color, style, and background parameters.

    Args:
        text: The text to colorize
        as_: Combined style string. Can be:
            - Style + color: "bold red", "italic cyan", "underline blue"
            - Style + color + background: "bold red on black", "italic white on blue"

    Returns:
        Colorized text with ANSI codes and automatic reset at the end

    Examples:
        >>> colortext("Error!", as_="bold red")
        '\\033[1m\\033[31mError!\\033[0m'

        >>> colortext("Success", as_="bold green on black")
        '\\033[1m\\033[32m\\033[40mSuccess\\033[0m'

        >>> colortext("Info", as_="italic bright cyan")
        '\\033[3m\\033[96mInfo\\033[0m'

        >>> colortext("Warning", as_="bold yellow on black")
        '\\033[1m\\033[33m\\033[40mWarning\\033[0m'

    Raises:
        StyleNotFoundError: If the combined style is not found in either
                           COMBINED_STYLES or COMBINED_STYLES_WITH_BG

    Note:
        The function checks COMBINED_STYLES_WITH_BG first (for "X on Y" patterns),
        then falls back to COMBINED_STYLES. This ensures proper precedence for
        background color specifications.
    """
    # Check COMBINED_STYLES_WITH_BG first (has precedence for "X on Y" patterns)

    if as_ in COMBINED_STYLES_WITH_BG:
        ansi_codes = COMBINED_STYLES_WITH_BG[as_]
        return ansi_codes + str(text) + clib.reset

    # Fall back to COMBINED_STYLES
    if as_ in COMBINED_STYLES:
        ansi_codes = COMBINED_STYLES[as_]
        return ansi_codes + str(text) + clib.reset

    # If not found in either, raise an error
    raise StyleNotFoundError(
        f"Combined style '{as_}' is not supported. "
        f"Use formats like 'bold red' or 'italic cyan on blue'."
    )

def cprint(text: Any,
           color: COLOR_NAMES | None = None,
           style: STYLE_NAMES | None = None,
           bg: COLOR_NAMES | None = None,
           as_: COMBINED_STYLES_LITERAL | str | None = None,
           **print_kwargs: Any) -> None:
    """
    Prints colorized text with support for both individual parameters and combined styles.

    This function supports two APIs:
    1. Legacy API: Use separate color, style, and bg parameters
    2. New API: Use the as_ parameter with combined style strings

    Args:
        text: Text to print
        color: Individual color name (legacy API)
        style: Individual style name (legacy API)
        bg: Individual background color (legacy API)
        as_: Combined style string (new API). Takes precedence over color/style/bg.
        **print_kwargs: Additional keyword arguments passed to print()

    Examples:
        # Old way (still works):
        >>> cprint("text", color="red", style="bold")

        # New way (recommended):
        >>> cprint("text", as_="bold red")
        >>> cprint("text", as_="bold red on blue")
        >>> cprint("Error!", as_="bold white on red")
        >>> cprint("Success!", as_="bold green on black")

        # With print kwargs:
        >>> cprint("text", as_="italic cyan", end="")
        >>> cprint("text", as_="bold yellow", sep=", ")

    Note:
        If as_ is provided, it takes precedence over color, style, and bg parameters.
        The as_ parameter provides a cleaner, more intuitive API.
    """
    # If as_ is provided, use the new colortext() function
    if as_ is not None:
        print(colortext(text, as_=as_), **print_kwargs)
    else:
        # Otherwise use the legacy colorize() for backward compatibility
        print(colorize(text, color=color, style=style, bg=bg), **print_kwargs)

def cinput(text: Any,
           as_: COMBINED_STYLES_LITERAL | str | None = None,
           **kwargs: ColorOptions) -> str:
    """
    Input with colorized prompt supporting both legacy and new APIs.

    This function displays a colorized prompt and returns the user's input.
    It supports two APIs for maximum flexibility.

    Args:
        text: Prompt text to display
        as_: Combined style string (new API). Takes precedence over kwargs.
        **kwargs: ColorOptions dict with 'color', 'style', and 'bg' keys (legacy API)

    Returns:
        User input as a string

    Examples:
        # Old way (still works):
        >>> name = cinput("Name: ", color="blue", style="bold")

        # New way (recommended):
        >>> name = cinput("Name: ", as_="bold blue")
        >>> age = cinput("Age: ", as_="italic cyan")
        >>> email = cinput("Email: ", as_="bold green on black")

    Note:
        If as_ is provided, it takes precedence over kwargs.
        The as_ parameter provides a cleaner, more intuitive API.
    """
    # If as_ is provided, use the new colortext() function
    if as_ is not None:
        return input(colortext(text, as_=as_))
    else:
        # Otherwise use the legacy colorize() with kwargs for backward compatibility
        return input(colorize(text, **kwargs))

if __name__ == "__main__":
    cprint("number colored text, passing numbers as argument")
    print("----")
    print(colortext(123, as_="bold red"))
    cprint(123, as_="bold red on black")
    cinput(123, as_="italic cyan on black")
    print("----")
    print("if you see this message, it has worked.")