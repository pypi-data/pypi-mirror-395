"""
Palette system for prism-view.

Provides color/emoji configuration with TOML loading and caching.

Features:
    - Load palettes from TOML files
    - ANSI 256 color support with colorize()
    - Emoji system with fallback support
    - Box drawing character sets
    - Built-in palettes: vaporwave, monochrome, solarized-dark, high-contrast
    - Respects NO_COLOR and FORCE_COLOR environment variables

Example:
    >>> from prism.view.palette import load_palette, colorize, get_emoji
    >>>
    >>> # Load a custom palette
    >>> palette = load_palette("my-palette.toml")
    >>>
    >>> # Colorize text
    >>> print(colorize("Error!", "error", palette=palette))
    >>>
    >>> # Get emoji
    >>> emoji = get_emoji("info", palette)
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Try to import tomllib (Python 3.11+) or fall back to tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[import-not-found]
    except ImportError:
        tomllib = None  # type: ignore[assignment]


# =============================================================================
# Palette Dataclass
# =============================================================================


@dataclass
class Palette:
    """
    Palette configuration for colors, emojis, and styles.

    Attributes:
        colors: Dictionary mapping color names to ANSI 256 color codes (0-255)
        emojis: Dictionary mapping emoji names to emoji strings
        styles: Dictionary mapping style names to style values

    Example:
        >>> palette = Palette(
        ...     colors={"primary": 39, "error": 196},
        ...     emojis={"info": "i", "error": "x"},
        ...     styles={"box": "single"},
        ... )
    """

    colors: Dict[str, int] = field(default_factory=dict)
    emojis: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=dict)


# =============================================================================
# Default Palettes
# =============================================================================


def _create_vaporwave_palette() -> Palette:
    """Create the default vaporwave palette (pink/cyan aesthetic)."""
    return Palette(
        colors={
            # Primary vaporwave colors
            "primary": 201,  # Hot pink
            "secondary": 51,  # Cyan
            "accent": 213,  # Light pink
            # Log levels
            "debug": 244,  # Gray
            "info": 39,  # Blue
            "warning": 214,  # Orange
            "error": 196,  # Red
            "critical": 201,  # Magenta/Pink
            # UI elements
            "muted": 240,  # Dark gray
            "success": 82,  # Green
            "header": 201,  # Pink for headers
            "border": 244,  # Gray for borders
        },
        emojis={
            "debug": "\U0001f50d",  # Magnifying glass
            "info": "\u2139\ufe0f",  # Information
            "warning": "\u26a0\ufe0f",  # Warning
            "error": "\u274c",  # Cross mark
            "critical": "\U0001f525",  # Fire
            "success": "\u2705",  # Check mark
            "rocket": "\U0001f680",  # Rocket
            "sparkles": "\u2728",  # Sparkles
            "eye": "\U0001f441\ufe0f",  # Eye (prism icon)
        },
        styles={
            "box": "rounded",
            "header_style": "bold",
        },
    )


def _create_monochrome_palette() -> Palette:
    """Create a monochrome/grayscale palette for prod environments."""
    return Palette(
        colors={
            "primary": 255,  # White
            "secondary": 250,  # Light gray
            "accent": 245,  # Medium gray
            "debug": 240,  # Dark gray
            "info": 252,  # Light gray
            "warning": 255,  # White (bold in context)
            "error": 255,  # White
            "critical": 255,  # White
            "muted": 238,  # Very dark gray
            "success": 252,  # Light gray
            "header": 255,  # White
            "border": 244,  # Gray
        },
        emojis={
            "debug": "[D]",
            "info": "[I]",
            "warning": "[W]",
            "error": "[E]",
            "critical": "[!]",
            "success": "[+]",
            "rocket": "[>]",
            "sparkles": "[*]",
            "eye": "[o]",
        },
        styles={
            "box": "ascii",
            "header_style": "plain",
        },
    )


def _create_solarized_dark_palette() -> Palette:
    """Create a solarized dark palette."""
    # Solarized base colors mapped to ANSI 256
    return Palette(
        colors={
            "primary": 37,  # Cyan
            "secondary": 136,  # Yellow
            "accent": 166,  # Orange
            "debug": 241,  # Base01
            "info": 37,  # Cyan
            "warning": 136,  # Yellow
            "error": 160,  # Red
            "critical": 125,  # Magenta
            "muted": 240,  # Base02
            "success": 64,  # Green
            "header": 37,  # Cyan
            "border": 240,  # Base02
        },
        emojis={
            "debug": "\U0001f50d",
            "info": "\u2139\ufe0f",
            "warning": "\u26a0\ufe0f",
            "error": "\u274c",
            "critical": "\U0001f525",
            "success": "\u2705",
            "rocket": "\U0001f680",
            "sparkles": "\u2728",
            "eye": "\U0001f441\ufe0f",
        },
        styles={
            "box": "single",
            "header_style": "bold",
        },
    )


def _create_high_contrast_palette() -> Palette:
    """Create a high contrast palette for accessibility."""
    return Palette(
        colors={
            "primary": 15,  # Bright white
            "secondary": 14,  # Bright cyan
            "accent": 11,  # Bright yellow
            "debug": 8,  # Dark gray
            "info": 14,  # Bright cyan
            "warning": 11,  # Bright yellow
            "error": 9,  # Bright red
            "critical": 13,  # Bright magenta
            "muted": 7,  # Light gray
            "success": 10,  # Bright green
            "header": 15,  # Bright white
            "border": 15,  # Bright white
        },
        emojis={
            "debug": "[DBG]",
            "info": "[INF]",
            "warning": "[WRN]",
            "error": "[ERR]",
            "critical": "[CRT]",
            "success": "[OK]",
            "rocket": "[>>>]",
            "sparkles": "[***]",
            "eye": "[EYE]",
        },
        styles={
            "box": "double",
            "header_style": "bold",
        },
    )


# Built-in palettes registry
_BUILT_IN_PALETTES: Dict[str, Palette] = {}


def _get_built_in_palettes() -> Dict[str, Palette]:
    """Get or initialize built-in palettes (lazy initialization)."""
    global _BUILT_IN_PALETTES
    if not _BUILT_IN_PALETTES:
        _BUILT_IN_PALETTES = {
            "vaporwave": _create_vaporwave_palette(),
            "monochrome": _create_monochrome_palette(),
            "solarized-dark": _create_solarized_dark_palette(),
            "high-contrast": _create_high_contrast_palette(),
        }
    return _BUILT_IN_PALETTES


# =============================================================================
# Palette Cache
# =============================================================================


# Cache for loaded palettes: path -> (mtime, Palette)
_palette_cache: Dict[str, tuple[float, Palette]] = {}


def _clear_palette_cache() -> None:
    """Clear the palette cache. Useful for testing."""
    global _palette_cache
    _palette_cache.clear()


# =============================================================================
# Palette Loading
# =============================================================================


def load_palette(path: str) -> Palette:
    """
    Load a palette from a TOML file.

    The palette is cached based on file modification time (mtime).
    If the file doesn't exist, returns the default vaporwave palette.

    Args:
        path: Path to the TOML palette file

    Returns:
        Loaded Palette instance

    Example:
        >>> palette = load_palette("my-palette.toml")
        >>> print(palette.colors["primary"])
    """
    global _palette_cache

    file_path = Path(path)

    # Check if file exists
    if not file_path.exists():
        return get_default_palette()

    # Get file mtime
    try:
        mtime = file_path.stat().st_mtime
    except OSError:
        return get_default_palette()

    # Check cache
    cache_key = str(file_path.resolve())
    if cache_key in _palette_cache:
        cached_mtime, cached_palette = _palette_cache[cache_key]
        if cached_mtime >= mtime:
            return cached_palette

    # Load from file
    palette = _load_palette_from_file(file_path)

    # Cache the result
    _palette_cache[cache_key] = (mtime, palette)

    return palette


def _load_palette_from_file(file_path: Path) -> Palette:
    """Load palette from a TOML file."""
    if tomllib is None:
        # No TOML parser available, return default
        return get_default_palette()

    try:
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return get_default_palette()

    # Parse sections with defaults
    default = get_default_palette()

    colors = data.get("colors", {})
    emojis = data.get("emojis", {})
    styles = data.get("styles", {})

    # Merge with defaults for missing values
    merged_colors = {**default.colors, **colors}
    merged_emojis = {**default.emojis, **emojis}
    merged_styles = {**default.styles, **styles}

    return Palette(
        colors=merged_colors,
        emojis=merged_emojis,
        styles=merged_styles,
    )


def get_default_palette() -> Palette:
    """
    Get the default palette (vaporwave).

    Returns:
        The default vaporwave Palette instance

    Example:
        >>> palette = get_default_palette()
        >>> print(palette.colors["primary"])  # 201 (hot pink)
    """
    return _get_built_in_palettes()["vaporwave"]


def get_palette(name: str) -> Palette:
    """
    Get a built-in palette by name.

    Available palettes:
        - "vaporwave": Pink/cyan aesthetic (default)
        - "monochrome": Grayscale for production
        - "solarized-dark": Solarized dark theme
        - "high-contrast": High contrast for accessibility

    Args:
        name: Name of the built-in palette

    Returns:
        The requested Palette instance

    Raises:
        KeyError: If palette name is not found

    Example:
        >>> palette = get_palette("monochrome")
        >>> print(palette.emojis["info"])  # "[I]"
    """
    palettes = _get_built_in_palettes()
    if name not in palettes:
        raise KeyError(f"Unknown palette: {name}. Available: {list(palettes.keys())}")
    return palettes[name]


# =============================================================================
# Color System
# =============================================================================


def should_use_color(stream: Any = None) -> bool:
    """
    Determine whether to use color output.

    Checks:
        1. NO_COLOR env var (if set, no colors)
        2. FORCE_COLOR env var (if set, force colors)
        3. Whether output is a TTY

    Args:
        stream: Output stream to check (default: sys.stderr)

    Returns:
        True if colors should be used, False otherwise

    Example:
        >>> if should_use_color():
        ...     print(colorize("Hello", 39))
        ... else:
        ...     print("Hello")
    """
    # NO_COLOR takes precedence (https://no-color.org/)
    if os.environ.get("NO_COLOR"):
        return False

    # FORCE_COLOR forces color output
    if os.environ.get("FORCE_COLOR"):
        return True

    # Check if stream is a TTY
    if stream is None:
        stream = sys.stderr

    if hasattr(stream, "isatty"):
        return stream.isatty()

    return False


def colorize(
    text: str,
    color: Optional[Union[int, str]] = None,
    palette: Optional[Palette] = None,
) -> str:
    """
    Apply ANSI 256 color to text.

    Args:
        text: Text to colorize
        color: ANSI 256 color code (0-255) or color name from palette
        palette: Palette to use for color name lookup

    Returns:
        Colorized text with ANSI escape codes, or plain text if colors disabled

    Example:
        >>> print(colorize("Error!", 196))  # Red text
        >>> print(colorize("Info", "info", palette=get_default_palette()))
    """
    # Check if colors should be used
    if os.environ.get("NO_COLOR"):
        return text

    # Handle None color
    if color is None:
        return text

    # Resolve color name to code
    color_code: Optional[int] = None

    if isinstance(color, int):
        color_code = color
    elif isinstance(color, str) and palette is not None:
        color_code = palette.colors.get(color)

    if color_code is None:
        return text

    # Validate color code range
    if not (0 <= color_code <= 255):
        return text

    # Apply ANSI 256 color
    return f"\033[38;5;{color_code}m{text}\033[0m"


# =============================================================================
# Emoji System
# =============================================================================


# Fallback emojis for when emoji display is disabled
_EMOJI_FALLBACKS: Dict[str, str] = {
    "debug": "[D]",
    "info": "[I]",
    "warning": "[W]",
    "error": "[E]",
    "critical": "[!]",
    "success": "[+]",
    "rocket": "[>]",
    "sparkles": "[*]",
    "eye": "[o]",
}


def get_emoji(
    name: str,
    palette: Optional[Palette] = None,
    use_emoji: bool = True,
) -> str:
    """
    Get an emoji by name.

    Args:
        name: Emoji name (e.g., "info", "error", "warning")
        palette: Palette to get emoji from (default: vaporwave)
        use_emoji: Whether to return actual emoji or fallback text

    Returns:
        Emoji string or fallback text

    Example:
        >>> get_emoji("info")  # Returns "i" or similar
        >>> get_emoji("error", use_emoji=False)  # Returns "[E]"
    """
    if palette is None:
        palette = get_default_palette()

    if not use_emoji:
        # Return ASCII fallback
        return _EMOJI_FALLBACKS.get(name, "")

    # Get from palette
    emoji = palette.emojis.get(name, "")

    # If not in palette, try fallback
    if not emoji:
        return _EMOJI_FALLBACKS.get(name, "")

    return emoji


# =============================================================================
# Box Drawing Styles
# =============================================================================


# Box drawing character sets
_BOX_CHARS: Dict[str, Dict[str, str]] = {
    "single": {
        "top_left": "\u250c",  # Box Drawings Light Down and Right
        "top_right": "\u2510",  # Box Drawings Light Down and Left
        "bottom_left": "\u2514",  # Box Drawings Light Up and Right
        "bottom_right": "\u2518",  # Box Drawings Light Up and Left
        "horizontal": "\u2500",  # Box Drawings Light Horizontal
        "vertical": "\u2502",  # Box Drawings Light Vertical
        "t_down": "\u252c",  # Box Drawings Light Down and Horizontal
        "t_up": "\u2534",  # Box Drawings Light Up and Horizontal
        "t_right": "\u251c",  # Box Drawings Light Vertical and Right
        "t_left": "\u2524",  # Box Drawings Light Vertical and Left
        "cross": "\u253c",  # Box Drawings Light Vertical and Horizontal
    },
    "double": {
        "top_left": "\u2554",  # Box Drawings Double Down and Right
        "top_right": "\u2557",  # Box Drawings Double Down and Left
        "bottom_left": "\u255a",  # Box Drawings Double Up and Right
        "bottom_right": "\u255d",  # Box Drawings Double Up and Left
        "horizontal": "\u2550",  # Box Drawings Double Horizontal
        "vertical": "\u2551",  # Box Drawings Double Vertical
        "t_down": "\u2566",  # Box Drawings Double Down and Horizontal
        "t_up": "\u2569",  # Box Drawings Double Up and Horizontal
        "t_right": "\u2560",  # Box Drawings Double Vertical and Right
        "t_left": "\u2563",  # Box Drawings Double Vertical and Left
        "cross": "\u256c",  # Box Drawings Double Vertical and Horizontal
    },
    "rounded": {
        "top_left": "\u256d",  # Box Drawings Light Arc Down and Right
        "top_right": "\u256e",  # Box Drawings Light Arc Down and Left
        "bottom_left": "\u2570",  # Box Drawings Light Arc Up and Right
        "bottom_right": "\u256f",  # Box Drawings Light Arc Up and Left
        "horizontal": "\u2500",  # Box Drawings Light Horizontal
        "vertical": "\u2502",  # Box Drawings Light Vertical
        "t_down": "\u252c",  # Box Drawings Light Down and Horizontal
        "t_up": "\u2534",  # Box Drawings Light Up and Horizontal
        "t_right": "\u251c",  # Box Drawings Light Vertical and Right
        "t_left": "\u2524",  # Box Drawings Light Vertical and Left
        "cross": "\u253c",  # Box Drawings Light Vertical and Horizontal
    },
    "ascii": {
        "top_left": "+",
        "top_right": "+",
        "bottom_left": "+",
        "bottom_right": "+",
        "horizontal": "-",
        "vertical": "|",
        "t_down": "+",
        "t_up": "+",
        "t_right": "+",
        "t_left": "+",
        "cross": "+",
    },
}


def get_box_chars(style: str = "single") -> Dict[str, str]:
    """
    Get box drawing characters for a given style.

    Available styles:
        - "single": Single-line box (default)
        - "double": Double-line box
        - "rounded": Rounded corners with single lines
        - "ascii": ASCII characters only

    Args:
        style: Box drawing style name

    Returns:
        Dictionary of box drawing characters

    Example:
        >>> chars = get_box_chars("rounded")
        >>> print(chars["top_left"])  # Prints rounded corner character
    """
    if style not in _BOX_CHARS:
        style = "single"

    return _BOX_CHARS[style].copy()
