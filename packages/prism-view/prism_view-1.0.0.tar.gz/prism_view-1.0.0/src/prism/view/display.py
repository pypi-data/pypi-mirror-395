"""
Display utilities for prism-view.

Provides console tables, ASCII banner rendering, and Unicode width handling.

Features:
    - console_table(): Render data as formatted tables
    - render_banner(): Display PRISM ASCII art banner
    - display_width(): Calculate display width of Unicode strings
    - pad_to_width(): Pad strings to target display width

Example:
    >>> from prism.view.display import console_table, render_banner
    >>>
    >>> # Render a table
    >>> data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    >>> print(console_table(data, title="Users"))
    >>>
    >>> # Display banner
    >>> print(render_banner())
"""

import os
import unicodedata
from typing import Any, Dict, List, Optional, Union

from prism.view.palette import Palette, get_box_chars, get_default_palette, should_use_color


# =============================================================================
# Unicode Width Handling
# =============================================================================


def display_width(text: str) -> int:
    """
    Calculate the display width of a Unicode string.

    Takes into account:
    - ASCII characters (width 1)
    - Wide characters like CJK (width 2)
    - Emojis (width 2)
    - Zero-width characters (width 0)
    - Variation selectors (width 0)

    Args:
        text: The string to measure

    Returns:
        The display width in terminal columns

    Example:
        >>> display_width("hello")
        5
        >>> display_width("\u4e2d\u6587")  # Chinese characters
        4
    """
    if not text:
        return 0

    width = 0
    i = 0
    chars = list(text)

    while i < len(chars):
        char = chars[i]

        # Handle newlines - count width of longest line
        if char == "\n":
            i += 1
            continue

        # Get Unicode category
        category = unicodedata.category(char)

        # Zero-width characters
        if category in ("Mn", "Me", "Cf"):  # Mark, Nonspacing / Enclosing / Format
            i += 1
            continue

        # Variation selectors (U+FE00 to U+FE0F)
        if "\ufe00" <= char <= "\ufe0f":
            i += 1
            continue

        # Zero-width joiner/non-joiner
        if char in ("\u200d", "\u200c"):
            i += 1
            continue

        # Check East Asian Width
        ea_width = unicodedata.east_asian_width(char)

        if ea_width in ("F", "W"):  # Fullwidth or Wide
            width += 2
        elif ea_width == "A":  # Ambiguous - treat as wide in East Asian context
            # For terminal compatibility, treat as 1
            width += 1
        else:
            width += 1

        i += 1

    return width


def pad_to_width(text: str, target_width: int, align: str = "left") -> str:
    """
    Pad a string to a target display width.

    Args:
        text: The string to pad
        target_width: The target display width
        align: Alignment ("left", "right", "center")

    Returns:
        The padded string

    Example:
        >>> pad_to_width("hello", 10)
        'hello     '
        >>> pad_to_width("hi", 10, align="right")
        '        hi'
    """
    current_width = display_width(text)

    if current_width >= target_width:
        return text

    padding_needed = target_width - current_width

    if align == "right":
        return " " * padding_needed + text
    elif align == "center":
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return " " * left_pad + text + " " * right_pad
    else:  # left
        return text + " " * padding_needed


def truncate_to_width(text: str, max_width: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum display width.

    Args:
        text: The string to truncate
        max_width: The maximum display width
        suffix: Suffix to append when truncating

    Returns:
        The truncated string with suffix if needed
    """
    if display_width(text) <= max_width:
        return text

    suffix_width = display_width(suffix)
    target_width = max_width - suffix_width

    if target_width <= 0:
        return suffix[:max_width]

    result = []
    current_width = 0

    for char in text:
        char_width = display_width(char)
        if current_width + char_width > target_width:
            break
        result.append(char)
        current_width += char_width

    return "".join(result) + suffix


# =============================================================================
# Table Rendering
# =============================================================================


def console_table(
    data: Union[List[Dict[str, Any]], List[List[Any]]],
    headers: Optional[List[str]] = None,
    title: Optional[str] = None,
    palette: Optional[Palette] = None,
    use_color: bool = True,
    box_style: str = "rounded",
    align: Optional[Dict[str, str]] = None,
    max_col_width: Optional[int] = None,
    max_width: Optional[int] = None,
) -> str:
    """
    Render data as a formatted console table.

    Args:
        data: List of dicts or list of lists
        headers: Column headers (auto-detected from dict keys if not provided)
        title: Optional table title
        palette: Color palette to use
        use_color: Whether to use ANSI colors
        box_style: Box drawing style ("single", "double", "rounded", "ascii")
        align: Dict mapping column names to alignment ("left", "right", "center")
        max_col_width: Maximum width for any column
        max_width: Maximum total table width

    Returns:
        Formatted table as a string

    Example:
        >>> data = [{"name": "Alice", "age": 30}]
        >>> print(console_table(data, title="Users"))
    """
    if not data:
        return ""

    # Check NO_COLOR
    if os.environ.get("NO_COLOR"):
        use_color = False

    # Get palette
    if palette is None:
        palette = get_default_palette()

    # Get box characters
    box = get_box_chars(box_style)

    # Extract headers and normalize data
    if isinstance(data[0], dict):
        if headers is None:
            headers = list(data[0].keys())
        rows = [[str(row.get(h, "")) for h in headers] for row in data]
    else:
        if headers is None:
            headers = [f"col_{i}" for i in range(len(data[0]))]
        rows = [[str(cell) for cell in row] for row in data]

    # Handle None values
    rows = [[cell if cell != "None" else "" for cell in row] for row in rows]

    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_w = display_width(header)
        for row in rows:
            if i < len(row):
                max_w = max(max_w, display_width(row[i]))
        if max_col_width:
            max_w = min(max_w, max_col_width)
        col_widths.append(max_w)

    # Apply max_width constraint if needed
    if max_width:
        total_width = sum(col_widths) + len(col_widths) * 3 + 1  # borders and padding
        if total_width > max_width:
            # Reduce column widths proportionally
            reduction = total_width - max_width
            for i in range(len(col_widths)):
                if col_widths[i] > 5:
                    reduce_by = min(col_widths[i] - 5, reduction // len(col_widths) + 1)
                    col_widths[i] -= reduce_by
                    reduction -= reduce_by

    # Truncate data if needed
    if max_col_width:
        rows = [[truncate_to_width(cell, max_col_width) for cell in row] for row in rows]

    # Determine alignment
    if align is None:
        align = {}

    # Auto-detect numeric columns for right alignment
    for i, header in enumerate(headers):
        if header not in align:
            # Check if all values in this column are numeric
            is_numeric = True
            for row in rows:
                if i < len(row) and row[i]:
                    try:
                        float(row[i].replace(",", ""))
                    except ValueError:
                        is_numeric = False
                        break
            if is_numeric and rows:
                align[header] = "right"

    # Build table
    lines = []

    # Color helpers
    def colorize(text: str, color_name: str) -> str:
        if not use_color:
            return text
        color_code = palette.colors.get(color_name)
        if color_code is not None:
            return f"\033[38;5;{color_code}m{text}\033[0m"
        return text

    def border(char: str) -> str:
        return colorize(char, "border")

    # Top border
    top_line = border(box["top_left"])
    for i, width in enumerate(col_widths):
        top_line += border(box["horizontal"] * (width + 2))
        if i < len(col_widths) - 1:
            top_line += border(box["t_down"])
    top_line += border(box["top_right"])

    # Title
    if title:
        title_width = sum(col_widths) + len(col_widths) * 3 - 1
        title_line = border(box["vertical"]) + " "
        title_text = colorize(title.center(title_width), "header")
        title_line += title_text + " " + border(box["vertical"])

        # Title top border
        title_top = border(box["top_left"])
        title_top += border(box["horizontal"] * (title_width + 2))
        title_top += border(box["top_right"])
        lines.append(title_top)
        lines.append(title_line)

        # Title separator
        sep_line = border(box["t_right"])
        for i, width in enumerate(col_widths):
            sep_line += border(box["horizontal"] * (width + 2))
            if i < len(col_widths) - 1:
                sep_line += border(box["t_down"])
        sep_line += border(box["t_left"])
        lines.append(sep_line)
    else:
        lines.append(top_line)

    # Header row
    header_line = border(box["vertical"])
    for header, width in zip(headers, col_widths, strict=False):
        cell_align = align.get(header, "left")
        padded = pad_to_width(header, width, cell_align)
        header_line += " " + colorize(padded, "header") + " " + border(box["vertical"])
    lines.append(header_line)

    # Header separator
    sep_line = border(box["t_right"])
    for i, width in enumerate(col_widths):
        sep_line += border(box["horizontal"] * (width + 2))
        if i < len(col_widths) - 1:
            sep_line += border(box["cross"])
    sep_line += border(box["t_left"])
    lines.append(sep_line)

    # Data rows
    for row in rows:
        data_line = border(box["vertical"])
        for idx, (cell, width) in enumerate(zip(row, col_widths, strict=False)):
            header = headers[idx] if idx < len(headers) else f"col_{idx}"
            cell_align = align.get(header, "left")
            padded = pad_to_width(cell, width, cell_align)
            data_line += " " + padded + " " + border(box["vertical"])
        lines.append(data_line)

    # Bottom border
    bottom_line = border(box["bottom_left"])
    for i, width in enumerate(col_widths):
        bottom_line += border(box["horizontal"] * (width + 2))
        if i < len(col_widths) - 1:
            bottom_line += border(box["t_up"])
    bottom_line += border(box["bottom_right"])
    lines.append(bottom_line)

    return "\n".join(lines)


# =============================================================================
# ASCII Banner
# =============================================================================


# PRISM ASCII Art
PRISM_ASCII_ART = r"""
    ____  ____  _________  ___
   / __ \/ __ \/  _/ ___/ /  |/  /
  / /_/ / /_/ // / \__ \ / /|_/ /
 / ____/ _, _// / ___/ // /  / /
/_/   /_/ |_/___//____//_/  /_/
"""

PRISM_ASCII_ART_SMALL = r"""
 ___ ___ ___ ___ __  __
| _ \ _ \_ _/ __|  \/  |
|  _/   /| |\__ \ |\/| |
|_| |_|_\___|___/_|  |_|
"""


def render_banner(
    palette: Optional[Palette] = None,
    use_color: Optional[bool] = None,
    show_version: bool = True,
) -> str:
    """
    Render the PRISM VIEW LOADED banner.

    Args:
        palette: Color palette to use
        use_color: Whether to use colors (auto-detect if None)
        show_version: Whether to show version number

    Returns:
        Formatted banner string

    Example:
        >>> print(render_banner())
    """
    # Check NO_COLOR
    if os.environ.get("NO_COLOR"):
        use_color = False
    elif use_color is None:
        use_color = should_use_color()

    # Get palette
    if palette is None:
        palette = get_default_palette()

    # Get version
    try:
        from prism.view import __version__

        version = __version__
    except ImportError:
        version = "0.1.0"

    # Build banner
    lines = []

    # ASCII art lines
    art_lines = PRISM_ASCII_ART_SMALL.strip().split("\n")

    # Vaporwave gradient colors (pink to cyan)
    gradient_colors = [201, 200, 199, 164, 128, 93, 57, 51]  # Pink to cyan

    if use_color:
        for i, line in enumerate(art_lines):
            color_idx = i % len(gradient_colors)
            color = gradient_colors[color_idx]
            lines.append(f"\033[38;5;{color}m{line}\033[0m")
    else:
        lines.extend(art_lines)

    # VIEW LOADED subtitle
    subtitle = "  VIEW LOADED"
    if show_version:
        subtitle += f" (v{version})"

    if use_color:
        # Use secondary color for subtitle
        color = palette.colors.get("secondary", 51)
        lines.append(f"\033[38;5;{color}m{subtitle}\033[0m")
    else:
        lines.append(subtitle)

    # Add sparkle line
    sparkle = "  " + palette.emojis.get("sparkles", "*") * 3 if use_color else "  ***"
    lines.append(sparkle)

    return "\n".join(lines)
