import re
from typing import Optional, Any
from tinycolors.main import colorize, color, clib
from tinycolors.stringable import Stringable
from tinycolors.exists import exists


def indent(level: int) -> str:
    return '    ' * level


def is_quote(char: str) -> bool:
    return char in ('"', "'")


def is_bracket(char: str) -> bool:
    return char in ('{', '}', '[', ']', '(', ')')


def is_opening_bracket(char: str) -> bool:
    return char in ('{', '[', '(')


def is_closing_bracket(char: str) -> bool:
    return char in ('}', ']', ')')


def get_bracket_type(char: str) -> str:
    if char in ('{', '}'):
        return 'curly'
    elif char in ('[', ']'):
        return 'square'
    elif char in ('(', ')'):
        return 'paren'
    return ''


def get_bracket_colors():
    return [
        clib.yellow,
        clib.cyan,
        clib.magenta,
        clib.blue,
        clib.red,
    ]


def color_bracket(char: str, bracket_stack: list[tuple[str, int]]) -> str:
    colors = get_bracket_colors()
    bracket_type = get_bracket_type(char)

    type_depth = sum(1 for t, _ in bracket_stack if t == bracket_type)

    if is_closing_bracket(char):
        reverse_stack = bracket_stack[::-1]
        for idx, (t, _) in enumerate(reverse_stack):
            if t == bracket_type:
                # Calculate the depth of the *matching* opening bracket
                current_depth = len(reverse_stack) - idx
                bracket_color = colors[current_depth % len(colors)]
                return f"{bracket_color}{char}{clib.reset}"

    bracket_color = colors[type_depth % len(colors)]
    return f"{bracket_color}{char}{clib.reset}"


def open_quote(char: str) -> tuple[bool, str, str]:
    return True, char, char


def close_quote(substring: str) -> str:
    return colorize(substring, "green")


def append_char(substring: str, char: str) -> str:
    return substring + char


def color_syntax(text: str) -> str:
    def replacer(match: re.Match) -> str:
        word = match.group(0)
        return f"{color.italic.blue}{word}{clib.reset}"

    pattern = r"\b(True|False|None)\b"
    return re.sub(pattern, replacer, text)


def color_numbers(text: str) -> str:
    def replacer(match: re.Match) -> str:
        word = match.group(0)
        return f"{clib.yellow}{word}{clib.reset}"

    pattern = r"\b\d+(\.\d+)?\b"
    return re.sub(pattern, replacer, text)


def handle_escape(char: str, escaped: bool) -> tuple[str, bool]:
    if escaped:
        return char, False
    elif char == '\\':
        return char, True
    return char, False


def start_quote(char: str) -> tuple[bool, str, str]:
    return True, char, char


def maybe_close_quote(substring: str, char: str, quote_char: str, next_char: str) -> tuple[bool, str, Optional[str]]:
    if char == quote_char:
        if next_char == quote_char:
            return True, substring + char, quote_char
        else:
            return False, close_quote(substring + char), None
    return True, substring + char, quote_char


def append_result(result_parts: list[str], substring: str, in_quote: bool):
    if exists(substring):
        if in_quote:
            result_parts.append(substring)
        else:
            result_parts.append(substring)


def find_closed_quotes(element: str) -> tuple[set[int], set[int]]:
    """
    Identifies the starting and ending indices of balanced, non-escaped quotes
    in a string, handling escaped internal quotes like '\"'.
    """
    opening_positions = set()
    closing_positions = set()
    i = 0
    length = len(element)
    escaped = False

    while i < length:
        char = element[i]

        if escaped:
            escaped = False
            i += 1
            continue

        if char == '\\':
            escaped = True
            i += 1
            continue

        if is_quote(char):
            quote_char = char
            start_pos = i
            j = i + 1
            escaped_inner = False
            found_close = False

            while j < length:
                current_char = element[j]
                next_char = element[j + 1] if j + 1 < length else ""

                if escaped_inner:
                    escaped_inner = False
                elif current_char == '\\':
                    escaped_inner = True
                elif current_char == quote_char:
                    if next_char == quote_char:
                        # Handles potential triple quotes, allowing the inner loop to continue
                        j += 1
                    else:
                        opening_positions.add(start_pos)
                        closing_positions.add(j)
                        found_close = True
                        break
                j += 1

            if found_close:
                i = j

        i += 1

    return opening_positions, closing_positions


def prettify_string(element: str) -> str:
    """
    Highlights syntax, numbers, and quoted strings within a single string.
    Also handles bracket color matching when outside of quotes.
    """
    opening_quotes, closing_quotes = find_closed_quotes(element)
    result_parts: list[str] = []
    substring = ""
    plain_text = ""
    in_quote = False
    quote_char: Optional[str] = None
    bracket_stack: list[tuple[str, int]] = []
    i = 0
    length = len(element)

    while i < length:
        char = element[i]
        next_char = element[i + 1] if i + 1 < length else ""

        # Handle explicit escape sequences like '\n' or '\"'
        if char == '\\' and i + 1 < length:
            if in_quote:
                substring += char
                substring += next_char
            else:
                plain_text += char
                plain_text += next_char
            i += 2
            continue

        elif is_quote(char) and (i in opening_quotes or i in closing_quotes):
            if not in_quote and i in opening_quotes:
                if exists(plain_text):
                    result_parts.append(color_syntax(color_numbers(plain_text)))
                    plain_text = ""
                in_quote, quote_char, substring = start_quote(char)
            elif in_quote and char == quote_char and i in closing_quotes:
                # The quote character must be the expected closing quote
                in_quote, result_or_substring, quote_char = maybe_close_quote(substring, char, quote_char, next_char)
                if not in_quote:
                    # Closing quote found, append the colored string
                    result_parts.append(result_or_substring.replace('\\"', '"'))
                    substring = ""
                else:
                    # Still in quote (e.g. adjacent quotes like "" for triple quotes), continue building
                    substring = result_or_substring
            else:
                # Quote inside a quote, or mismatched closing quote
                if in_quote:
                    substring += char
                else:
                    plain_text += char

        elif is_bracket(char) and not in_quote:
            if exists(plain_text):
                result_parts.append(color_syntax(color_numbers(plain_text)))
                plain_text = ""

            colored_bracket = color_bracket(char, bracket_stack)
            result_parts.append(colored_bracket)

            if is_opening_bracket(char):
                bracket_type = get_bracket_type(char)
                bracket_stack.append((bracket_type, i))
            elif is_closing_bracket(char):
                bracket_type = get_bracket_type(char)
                # Pop the latest matching opening bracket from the stack
                for k in range(len(bracket_stack) - 1, -1, -1):
                    if bracket_stack[k][0] == bracket_type:
                        bracket_stack.pop(k)
                        break
        else:
            if in_quote:
                substring += char
            else:
                plain_text += char

        i += 1

    if exists(plain_text):
        result_parts.append(color_syntax(color_numbers(plain_text)))
    if exists(substring) and in_quote:
        # Final append for an unterminated string (shouldn't happen with find_closed_quotes, but for safety)
        result_parts.append(close_quote(substring).replace('\\"', '"'))

    return "".join(result_parts)


def escape_internal_quotes(s: str) -> str:
    """Escapes double quotes inside a string so it can be wrapped in double quotes."""
    return s.replace('"', '\\"')


def get_container_color_index(level: int) -> int:
    """Calculates the color index based on the nesting level for bracket coloring."""
    colors = get_bracket_colors()
    if level <= 1:
        return 0
    else:
        return (level - 1) % len(colors)


def prettify_simple(element: Any) -> str:
    """Highlights simple types (bool, None, int, float) with their respective colors."""
    s = str(element)
    if isinstance(element, (bool, type(None))):
        return color_syntax(s)  # Colors True, False, None
    elif isinstance(element, (int, float)):
        return color_numbers(s) # Colors numbers
    return s

def prettify_container(
    element: Any,
    open_char: str,
    close_char: str,
    level: int,
    is_key_value: bool = False,
) -> str:
    """
    Generic function to handle lists, tuples, and sets, controlling
    the bracket type and key/value formatting.
    """
    colors = get_bracket_colors()
    color_index = get_container_color_index(level)
    bracket_color = colors[color_index]

    colored_open = f"{bracket_color}{open_char}{clib.reset}"
    colored_close = f"{bracket_color}{close_char}{clib.reset}"

    nested_level = level + 1
    items = list(element)

    # Use compact, single-line format for small containers
    compact_limit = 3 if is_key_value else 10
    if len(element) <= compact_limit:
        parts = []
        if is_key_value:
            for k, v in element.items():
                # Key formatting
                if isinstance(k, str):
                    key_str = prettify(f'"{escape_internal_quotes(k)}"', nested_level)
                else:
                    key_str = prettify(k, nested_level)

                # Value formatting
                if isinstance(v, str):
                    value_str = prettify(f'"{escape_internal_quotes(v)}"', nested_level)
                else:
                    value_str = prettify(v, nested_level)

                parts.append(f"{key_str}: {value_str}")
        else:
            for item in items:
                if isinstance(item, str):
                    # Ensure strings are wrapped in quotes before being passed to prettify_string
                    item_str = prettify(f'"{escape_internal_quotes(item)}"', nested_level)
                else:
                    item_str = prettify(item, nested_level)
                parts.append(item_str)

        return colored_open + ', '.join(parts) + colored_close

    # Use expanded, multi-line format for large containers
    result = colored_open
    if is_key_value:
        items = list(element.items())

    for i, item in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''

        if is_key_value:
            key, value = item
            # Key formatting
            if isinstance(key, str):
                key_str = prettify(f'"{escape_internal_quotes(key)}"', nested_level)
            else:
                key_str = prettify(key, nested_level)

            # Value formatting
            if isinstance(value, str):
                value_str = prettify(f'"{escape_internal_quotes(value)}"', nested_level)
            else:
                value_str = prettify(value, nested_level)

            line = f"{key_str}: {value_str}{comma}"
        else:
            # Item formatting (for lists, tuples, sets)
            if isinstance(item, str):
                item_str = prettify(f'"{escape_internal_quotes(item)}"', nested_level)
            else:
                item_str = prettify(item, nested_level)
            line = f"{item_str}{comma}"

        result += f"\n{indent(nested_level)}{line}"

    result += f"\n{indent(level)}{colored_close}"
    return result


def prettify_list(element: list[Any], level: int = 0) -> str:
    """Recursively converts a list into a color-highlighted, formatted string."""
    return prettify_container(element, '[', ']', level, is_key_value=False)


def prettify_dict(element: dict[Any, Any], level: int = 0) -> str:
    """Recursively converts a dict into a color-highlighted, formatted string."""
    return prettify_container(element, '{', '}', level, is_key_value=True)


def prettify_tuple(element: tuple[Any, ...], level: int = 0) -> str:
    """NEW: Recursively converts a tuple into a color-highlighted, formatted string."""
    # Special handling for single-item tuples to ensure the trailing comma is present
    if len(element) == 1 and not isinstance(element[0], (list, dict, tuple, set)):
        item_str = prettify(element[0], level + 1)
        colors = get_bracket_colors()
        color_index = get_container_color_index(level)
        bracket_color = colors[color_index]
        return f"{bracket_color}({clib.reset}{item_str},{bracket_color}){clib.reset}"

    return prettify_container(element, '(', ')', level, is_key_value=False)


def prettify_set(element: set[Any], level: int = 0) -> str:
    """NEW: Recursively converts a set into a color-highlighted, formatted string."""
    return prettify_container(element, '{', '}', level, is_key_value=False)


def prettify(element: Stringable, level: int = 1) -> str:
    """
    The main entry point for prettifying an element, dispatching to the
    appropriate formatting function based on type.
    """
    if isinstance(element, str):
        result = prettify_string(element)
    elif isinstance(element, list):
        result = prettify_list(element, level)
    elif isinstance(element, dict):
        result = prettify_dict(element, level)
    elif isinstance(element, tuple):
        result = prettify_tuple(element, level)
    elif isinstance(element, set):
        result = prettify_set(element, level)
    elif isinstance(element, (int, float, bool, type(None))):
        # NEW: Handle simple types directly
        result = prettify_simple(element)
    else:
        # Fallback for other objects (e.g. custom classes, bytes)
        result = prettify_string(str(element))

    return result


def tprint(element: Stringable, level: int = 0) -> None:
    """Prints the prettified element to the console."""
    print(prettify(element, level))

def demo():
    """
    Demonstrates the features of the prettify module, including the new
    support for tuples and sets.
    """
    print(colorize("--- Prettify Module Showcase ---", color="green", style="bold"))

    # --- 1. Complex Nested Dictionary (Existing Demo) ---
    demo_data = {
        "user_id": 9001,
        "username": "ColorMaestro",
        "is_active": True,
        "profile": {
            "bio": "A demo for terminal readability.",
            "favorites": ["Python", "Colorizer", 100],
            "settings": {
                "theme": "dark_mode",
                "font_size": 14.5,
                "notifications": False
            }
        },
        "data_samples": [
            {
                "id": 1,
                "value": 123.45,
                "status": "VALID",
                "notes": "Escape seq: \\n and single quote: 'inner' are handled correctly.",
                "test_null": None,
                "complex_list": [
                    (1, 2, 3), # TUPLE nested here
                    "nested_string",
                    99,
                    False
                ]
            },
            {
                "id": 2,
                "value": -0.007,
                "status": "ERROR",
                "notes": 'Double quote: "inside" is also handled.',
                "metadata": {}
            },
        ],
        "list_of_11": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    }

    print(colorize("\n## Displaying a Nested Dictionary (`demo_data`):", color="cyan", style="bold"))
    tprint(demo_data)

    # --- 2. Long List Demonstration (triggers multi-line) ---
    long_list = ["apple", "banana", 1234567890, True, {"key": "value", "key2": 42}] * 3

    print(colorize("\n## Displaying a Long List (`long_list` - triggers expansion):", color="cyan", style="bold"))
    tprint(long_list)

    # --- 3. New Collection Types Demonstration (Tuples and Sets) ---
    new_collections = {
        "tuple_compact": (10, "ten", False),
        "tuple_single": ("one_item",),
        "tuple_long": tuple(range(12)),
        "set_compact": {1, "two", 3.0},
        "set_long": set(range(15)),
        "mixed_nesting": (
            {1: "A"},
            ["B", 2],
            {"C", 3},
            (4, 5)
        )
    }

    print(colorize("\n## Demonstration of New Types (Tuples and Sets):", color="cyan", style="bold"))
    tprint(new_collections)

    # --- 4. Standalone Simple Type Demonstration ---
    print(colorize("\n## Standalone Simple Type Demonstration:", color="cyan", style="bold"))
    print(f"Bool: {prettify(True)}")
    print(f"None: {prettify(None)}")
    print(f"Int: {prettify(404)}")
    print(f"Float: {prettify(3.14159)}")

    # --- 5. String Prettification Demonstration (standalone) ---
    test_string = 'Key is "name", value is None, number is 100.5, backslash is \\ and quote is \\" and boolean is True.'

    print(colorize("\n## Standalone String Prettification Demo:", color="cyan", style="bold"))
    print(colorize("Original:", color="white", style="bold"), test_string)
    print(colorize("Prettified:", color="white", style="bold"), prettify_string(test_string))

if __name__ == "__main__":
    demo()