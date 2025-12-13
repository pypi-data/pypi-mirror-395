"""
Custom palette example for prism-view.

This example demonstrates:
- Loading custom palettes from TOML files
- Using built-in palettes (vaporwave, monochrome, solarized-dark, high-contrast)
- Creating palettes programmatically
- Colorizing text output
- Using emojis and box drawing characters

Usage:
    python examples/05_custom_palette.py
"""

from prism.view import (
    Palette,
    colorize,
    get_box_chars,
    get_emoji,
    get_palette,
    load_palette,
    should_use_color,
)


# =============================================================================
# Built-in Palettes
# =============================================================================

print("=== Built-in Palettes ===\n")

# Get built-in palettes by name
palettes = ["vaporwave", "monochrome", "solarized-dark", "high-contrast"]

for name in palettes:
    palette = get_palette(name)
    print(f"{name}:")
    print(f"  Colors: {list(palette.colors.keys())[:5]}...")
    print(f"  Emojis: {list(palette.emojis.keys())[:5]}...")
    print()


# =============================================================================
# Colorizing Text
# =============================================================================

print("=== Colorizing Text ===\n")

# Get the default vaporwave palette
palette = get_palette("vaporwave")

# Colorize text using color names from the palette
if should_use_color(None):
    print(colorize("This is the primary color", "primary", palette))
    print(colorize("This is the secondary color", "secondary", palette))
    print(colorize("This is an error message", "error", palette))
    print(colorize("This is a warning message", "warning", palette))
    print(colorize("This is a success message", "success", palette))
    print(colorize("This is info text", "info", palette))
else:
    print("Colors disabled (NO_COLOR is set or not a TTY)")
    print("  primary: Would show pink/magenta")
    print("  secondary: Would show cyan")
    print("  error: Would show red")
    print("  warning: Would show yellow")
    print("  success: Would show green")

print()


# =============================================================================
# Using Emojis
# =============================================================================

print("=== Using Emojis ===\n")

palette = get_palette("vaporwave")

# Get emojis from the palette
emoji_names = ["info", "warning", "error", "success", "debug", "trace"]

print("With emojis enabled:")
for name in emoji_names:
    emoji = get_emoji(name, palette, use_emoji=True)
    print(f"  {name}: {emoji}")

print("\nWith emojis disabled (ASCII fallback):")
for name in emoji_names:
    emoji = get_emoji(name, palette, use_emoji=False)
    print(f"  {name}: {emoji}")


# =============================================================================
# Box Drawing Characters
# =============================================================================

print("\n=== Box Drawing Characters ===\n")

styles = ["single", "double", "rounded", "ascii"]

for style in styles:
    chars = get_box_chars(style)
    print(f"{style} style:")
    print(f"  {chars['top_left']}{chars['horizontal']}{chars['horizontal']}{chars['horizontal']}{chars['top_right']}")
    print(f"  {chars['vertical']}   {chars['vertical']}")
    print(f"  {chars['bottom_left']}{chars['horizontal']}{chars['horizontal']}{chars['horizontal']}{chars['bottom_right']}")
    print()


# =============================================================================
# Creating Palettes Programmatically
# =============================================================================

print("=== Creating Palettes Programmatically ===\n")

# Create a custom palette
custom_palette = Palette(
    colors={
        "primary": 196,      # Bright red
        "secondary": 226,    # Yellow
        "error": 160,        # Dark red
        "warning": 208,      # Orange
        "success": 46,       # Bright green
        "info": 39,          # Light blue
        "muted": 240,        # Gray
    },
    emojis={
        "info": "i",
        "warning": "!",
        "error": "X",
        "success": "v",
        "debug": "?",
        "trace": ".",
    },
    styles={
        "box_style": "rounded",
    },
)

print("Custom palette created:")
print(f"  Colors: {custom_palette.colors}")
print(f"  Emojis: {custom_palette.emojis}")
print(f"  Styles: {custom_palette.styles}")


# =============================================================================
# Loading Palettes from TOML Files
# =============================================================================

print("\n=== Loading Palettes from TOML Files ===\n")

# Example TOML content (normally this would be in a file)
toml_example = '''
# Example palette.toml file:

[colors]
primary = 213      # Pink
secondary = 45     # Cyan
error = 196        # Red
warning = 220      # Yellow
success = 82       # Green
info = 75          # Light blue
muted = 242        # Gray

[emojis]
info = "ℹ️"
warning = "⚠️"
error = "❌"
success = "✅"
debug = "🔍"
trace = "📍"

[styles]
box_style = "rounded"
'''

print("Example palette.toml content:")
print(toml_example)

# Load from file (if exists)
# palette = load_palette("my_palette.toml")

# Falls back to default if file doesn't exist
palette = load_palette("nonexistent.toml")
print(f"Loaded palette (fallback to default): {palette.colors.get('primary', 'N/A')}")


# =============================================================================
# Logger with Custom Palette
# =============================================================================

print("\n=== Logger with Custom Palette ===\n")

from prism.view import get_logger, setup_logging

# Set up with a specific palette
setup_logging(mode="dev", palette="solarized-dark", show_banner=False)

logger = get_logger("palette-demo")

logger.info("Using solarized-dark palette")
logger.warning("Warnings use the warning color")
logger.error("Errors use the error color")

# Switch to monochrome for production-like output
setup_logging(mode="dev", palette="monochrome", show_banner=False)

logger2 = get_logger("monochrome-demo")
logger2.info("Monochrome palette - grayscale colors")
logger2.debug("Debug messages in muted gray")
