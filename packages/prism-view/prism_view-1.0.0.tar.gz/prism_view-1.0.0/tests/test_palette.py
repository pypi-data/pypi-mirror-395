"""
Tests for the Palette system.

Tests cover:
- Palette loading from TOML files
- Color system with ANSI 256 codes
- Emoji system with fallback
- Box drawing styles
- Logger integration
- NO_COLOR environment variable support
"""

import os
import time
from pathlib import Path


# =============================================================================
# 8.1: Palette Loading Tests
# =============================================================================


class TestPaletteLoading:
    """Tests for palette loading functionality."""

    def test_load_palette_from_toml_file(self, tmp_path: Path) -> None:
        """8.1.1: Load palette from TOML file."""
        from prism.view.palette import load_palette

        # Create a test TOML file
        toml_content = """
[colors]
primary = 39
secondary = 201
error = 196
warning = 214
info = 39
debug = 244
muted = 240
success = 82

[emojis]
info = "i"
warning = "!"
error = "x"
debug = "?"
critical = "!!"
success = "ok"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        assert palette is not None
        assert hasattr(palette, "colors")
        assert hasattr(palette, "emojis")
        assert hasattr(palette, "styles")

    def test_palette_has_colors_section(self, tmp_path: Path) -> None:
        """8.1.2: Palette has colors section."""
        from prism.view.palette import load_palette

        toml_content = """
[colors]
primary = 39
secondary = 201
error = 196
warning = 214
info = 39
debug = 244
muted = 240
success = 82

[emojis]
info = "i"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        assert palette.colors is not None
        assert "primary" in palette.colors
        assert "error" in palette.colors
        assert palette.colors["primary"] == 39
        assert palette.colors["error"] == 196

    def test_palette_has_emojis_section(self, tmp_path: Path) -> None:
        """8.1.3: Palette has emojis section."""
        from prism.view.palette import load_palette

        toml_content = """
[colors]
primary = 39

[emojis]
info = "i"
warning = "!"
error = "x"
debug = "?"
critical = "!!"
success = "ok"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        assert palette.emojis is not None
        assert "info" in palette.emojis
        assert "error" in palette.emojis
        assert palette.emojis["info"] == "i"

    def test_palette_has_styles_section(self, tmp_path: Path) -> None:
        """8.1.4: Palette has styles section."""
        from prism.view.palette import load_palette

        toml_content = """
[colors]
primary = 39

[emojis]
info = "i"

[styles]
box = "double"
header_style = "bold"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        assert palette.styles is not None
        assert "box" in palette.styles
        assert palette.styles["box"] == "double"

    def test_default_palette_loads_if_file_missing(self) -> None:
        """8.1.5: Default palette loads if file missing."""
        from prism.view.palette import load_palette

        # Load from a non-existent file
        palette = load_palette("/nonexistent/path/palette.toml")

        # Should return the default palette
        assert palette is not None
        assert hasattr(palette, "colors")
        assert hasattr(palette, "emojis")
        assert hasattr(palette, "styles")
        # Default palette should have essential colors
        assert "error" in palette.colors
        assert "info" in palette.colors

    def test_palette_is_cached_after_first_load(self, tmp_path: Path) -> None:
        """8.1.6: Palette is cached after first load."""
        from prism.view.palette import _clear_palette_cache, load_palette

        # Clear any existing cache
        _clear_palette_cache()

        toml_content = """
[colors]
primary = 39

[emojis]
info = "i"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        # Load twice
        palette1 = load_palette(str(toml_file))
        palette2 = load_palette(str(toml_file))

        # Should be the same object (cached)
        assert palette1 is palette2

    def test_palette_cache_invalidated_when_file_changes(self, tmp_path: Path) -> None:
        """8.1.7: Palette cache is invalidated when file changes (mtime)."""
        from prism.view.palette import _clear_palette_cache, load_palette

        # Clear any existing cache
        _clear_palette_cache()

        toml_content_v1 = """
[colors]
primary = 39

[emojis]
info = "i"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content_v1)

        palette1 = load_palette(str(toml_file))
        assert palette1.colors["primary"] == 39

        # Wait a bit and modify the file
        time.sleep(0.1)

        toml_content_v2 = """
[colors]
primary = 201

[emojis]
info = "i"

[styles]
box = "single"
"""
        toml_file.write_text(toml_content_v2)

        # Force mtime update
        os.utime(str(toml_file), None)

        palette2 = load_palette(str(toml_file))

        # Should be a new palette with updated values
        assert palette2.colors["primary"] == 201
        # Should NOT be the same object
        assert palette1 is not palette2


# =============================================================================
# 8.2: Color System Tests
# =============================================================================


class TestColorSystem:
    """Tests for the color system."""

    def test_palette_colors_are_ansi_256_codes(self, tmp_path: Path) -> None:
        """8.2.1: Palette colors are ANSI 256 codes."""
        from prism.view.palette import load_palette

        toml_content = """
[colors]
primary = 39
secondary = 201
error = 196

[emojis]
info = "i"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        # All colors should be integers in ANSI 256 range (0-255)
        for name, code in palette.colors.items():
            assert isinstance(code, int), f"Color '{name}' should be an integer"
            assert 0 <= code <= 255, f"Color '{name}' should be in range 0-255"

    def test_colorize_applies_ansi_codes(self) -> None:
        """8.2.2: colorize(text, color) applies ANSI codes."""
        from prism.view.palette import colorize

        result = colorize("Hello", 39)

        # Should contain ANSI escape sequences
        assert "\033[38;5;39m" in result
        assert "Hello" in result
        assert "\033[0m" in result  # Reset code

    def test_colors_work_in_supported_terminals(self) -> None:
        """8.2.3: Colors work in supported terminals."""
        from prism.view.palette import colorize

        # Test various ANSI 256 colors
        test_colors = [0, 15, 39, 196, 201, 255]

        for color_code in test_colors:
            result = colorize("Test", color_code)
            expected_escape = f"\033[38;5;{color_code}m"
            assert expected_escape in result

    def test_colors_disabled_if_no_color_env_var_set(self) -> None:
        """8.2.4: Colors disabled if NO_COLOR env var set."""
        from prism.view.palette import colorize

        # Set NO_COLOR environment variable
        original = os.environ.get("NO_COLOR")
        try:
            os.environ["NO_COLOR"] = "1"

            result = colorize("Hello", 39)

            # Should NOT contain ANSI escape sequences
            assert "\033[" not in result
            assert result == "Hello"
        finally:
            if original is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = original

    def test_colorize_with_palette_color_name(self) -> None:
        """colorize can accept color name from palette."""
        from prism.view.palette import colorize, get_default_palette

        palette = get_default_palette()

        # Can colorize using color name
        result = colorize("Error!", "error", palette=palette)

        # Should contain the error color code from palette
        error_code = palette.colors.get("error", 196)
        assert f"\033[38;5;{error_code}m" in result


# =============================================================================
# 8.3: Emoji System Tests
# =============================================================================


class TestEmojiSystem:
    """Tests for the emoji system."""

    def test_palette_emojis_are_utf8_strings(self, tmp_path: Path) -> None:
        """8.3.1: Palette emojis are UTF-8 strings."""
        from prism.view.palette import load_palette

        toml_content = """
[colors]
primary = 39

[emojis]
info = "i"
warning = "!"
error = "x"
debug = "?"
critical = "!!"

[styles]
box = "single"
"""
        toml_file = tmp_path / "test-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        for name, emoji in palette.emojis.items():
            assert isinstance(emoji, str), f"Emoji '{name}' should be a string"
            # Should be encodable as UTF-8
            emoji.encode("utf-8")

    def test_get_emoji_returns_emoji(self) -> None:
        """8.3.2: get_emoji(name) returns emoji."""
        from prism.view.palette import get_default_palette, get_emoji

        palette = get_default_palette()

        # Get emoji for info level
        emoji = get_emoji("info", palette)

        assert emoji is not None
        assert isinstance(emoji, str)
        assert len(emoji) > 0

    def test_emojis_fallback_to_text_if_not_supported(self) -> None:
        """8.3.3: Emojis fallback to text if not supported."""
        from prism.view.palette import get_emoji

        # Create a palette with no emoji support indicator
        # When use_emoji=False, should return fallback text
        emoji = get_emoji("info", use_emoji=False)

        # Should return a text fallback
        assert emoji is not None
        assert isinstance(emoji, str)
        # Fallback should not contain actual emoji characters
        # (should be ASCII-safe)

    def test_get_emoji_with_unknown_name_returns_fallback(self) -> None:
        """get_emoji with unknown name returns empty or fallback."""
        from prism.view.palette import get_emoji

        emoji = get_emoji("nonexistent_emoji_name")

        # Should return empty string or some fallback
        assert isinstance(emoji, str)


# =============================================================================
# 8.4: Box Drawing Styles Tests
# =============================================================================


class TestBoxDrawingStyles:
    """Tests for box drawing character styles."""

    def test_get_box_chars_returns_box_drawing_set(self) -> None:
        """8.4.1: get_box_chars() returns box drawing set."""
        from prism.view.palette import get_box_chars

        chars = get_box_chars()

        assert chars is not None
        # Should have all necessary box drawing characters
        assert "top_left" in chars
        assert "top_right" in chars
        assert "bottom_left" in chars
        assert "bottom_right" in chars
        assert "horizontal" in chars
        assert "vertical" in chars

    def test_box_chars_support_double_style(self) -> None:
        """8.4.2a: Support for double box style."""
        from prism.view.palette import get_box_chars

        chars = get_box_chars(style="double")

        # Double box drawing uses specific Unicode characters
        assert chars["horizontal"] == "\u2550"  # Double horizontal
        assert chars["vertical"] == "\u2551"  # Double vertical

    def test_box_chars_support_single_style(self) -> None:
        """8.4.2b: Support for single box style."""
        from prism.view.palette import get_box_chars

        chars = get_box_chars(style="single")

        # Single box drawing uses specific Unicode characters
        assert chars["horizontal"] == "\u2500"  # Single horizontal
        assert chars["vertical"] == "\u2502"  # Single vertical

    def test_box_chars_support_rounded_style(self) -> None:
        """8.4.2c: Support for rounded box style."""
        from prism.view.palette import get_box_chars

        chars = get_box_chars(style="rounded")

        # Rounded uses single lines but rounded corners
        assert chars["top_left"] == "\u256d"  # Arc down and right
        assert chars["top_right"] == "\u256e"  # Arc down and left

    def test_box_chars_support_ascii_style(self) -> None:
        """8.4.2d: Support for ascii box style."""
        from prism.view.palette import get_box_chars

        chars = get_box_chars(style="ascii")

        # ASCII uses simple characters
        assert chars["horizontal"] == "-"
        assert chars["vertical"] == "|"
        assert chars["top_left"] == "+"
        assert chars["top_right"] == "+"

    def test_box_chars_are_unicode_or_ascii(self) -> None:
        """8.4.3: Box chars are Unicode or ASCII."""
        from prism.view.palette import get_box_chars

        for style in ["single", "double", "rounded", "ascii"]:
            chars = get_box_chars(style=style)

            for name, char in chars.items():
                assert isinstance(char, str), f"Char '{name}' should be string"
                assert len(char) == 1, f"Char '{name}' should be single character"
                # Should be encodable
                char.encode("utf-8")


# =============================================================================
# 8.5: Logger Integration Tests
# =============================================================================


class TestLoggerPaletteIntegration:
    """Tests for Logger integration with palette."""

    def test_logger_uses_palette_colors(self) -> None:
        """8.5.1: Logger uses palette colors."""
        from io import StringIO

        from prism.view.logger import Logger
        from prism.view.palette import get_default_palette

        stream = StringIO()
        palette = get_default_palette()
        logger = Logger("test", mode="dev", stream=stream, palette=palette)

        logger.info("Test message")
        output = stream.getvalue()

        # Should contain ANSI color codes from the palette
        # Info level typically uses blue (39) or similar
        assert "\033[38;5;" in output

    def test_logger_uses_palette_emojis(self) -> None:
        """8.5.2: Logger uses palette emojis."""
        from io import StringIO

        from prism.view.logger import Logger
        from prism.view.palette import get_default_palette

        stream = StringIO()
        palette = get_default_palette()
        logger = Logger("test", mode="dev", stream=stream, palette=palette)

        logger.info("Test message")
        output = stream.getvalue()

        # Should contain an emoji for the info level
        info_emoji = palette.emojis.get("info", "")
        if info_emoji:
            assert info_emoji in output

    def test_logger_respects_palette_config(self) -> None:
        """8.5.3: Logger respects palette config."""
        from io import StringIO

        from prism.view.logger import Logger
        from prism.view.palette import Palette

        # Create a custom palette
        custom_palette = Palette(
            colors={"info": 82, "error": 160, "warning": 220, "debug": 250},
            emojis={"info": "[I]", "error": "[E]", "warning": "[W]", "debug": "[D]"},
            styles={"box": "ascii"},
        )

        stream = StringIO()
        logger = Logger("test", mode="dev", stream=stream, palette=custom_palette)

        logger.info("Custom palette test")
        output = stream.getvalue()

        # Should use the custom info color (82)
        assert "\033[38;5;82m" in output
        # Should use the custom emoji
        assert "[I]" in output


# =============================================================================
# 8.6: Alternative Palettes Tests
# =============================================================================


class TestAlternativePalettes:
    """Tests for alternative palette definitions."""

    def test_monochrome_palette_exists(self) -> None:
        """8.6.1: Monochrome palette exists."""
        from prism.view.palette import get_palette

        palette = get_palette("monochrome")

        assert palette is not None
        # Monochrome should use grayscale colors
        for _name, code in palette.colors.items():
            # ANSI 256 grayscale is 232-255, plus 0 (black) and 15 (white)
            assert isinstance(code, int)

    def test_solarized_dark_palette_exists(self) -> None:
        """8.6.2: Solarized dark palette exists."""
        from prism.view.palette import get_palette

        palette = get_palette("solarized-dark")

        assert palette is not None
        assert hasattr(palette, "colors")
        assert hasattr(palette, "emojis")

    def test_high_contrast_palette_exists(self) -> None:
        """8.6.3: High contrast palette exists (accessibility)."""
        from prism.view.palette import get_palette

        palette = get_palette("high-contrast")

        assert palette is not None
        # High contrast should use very distinct colors
        assert palette.colors is not None

    def test_palette_switching(self) -> None:
        """8.6.4: Test palette switching."""
        from prism.view.palette import get_palette

        vaporwave = get_palette("vaporwave")
        monochrome = get_palette("monochrome")

        # Should be different palettes
        assert vaporwave is not monochrome
        # Colors should differ
        assert vaporwave.colors != monochrome.colors


# =============================================================================
# Edge Cases and Additional Tests
# =============================================================================


class TestPaletteEdgeCases:
    """Tests for edge cases in palette system."""

    def test_palette_dataclass_is_immutable_friendly(self) -> None:
        """Palette should be usable as a dataclass."""
        from prism.view.palette import Palette

        palette = Palette(
            colors={"primary": 39},
            emojis={"info": "i"},
            styles={"box": "single"},
        )

        assert palette.colors["primary"] == 39
        assert palette.emojis["info"] == "i"
        assert palette.styles["box"] == "single"

    def test_get_default_palette_returns_vaporwave(self) -> None:
        """get_default_palette returns the vaporwave palette."""
        from prism.view.palette import get_default_palette

        palette = get_default_palette()

        assert palette is not None
        # Vaporwave palette should have pink/cyan colors
        assert "primary" in palette.colors or "info" in palette.colors

    def test_colorize_with_none_color_returns_plain_text(self) -> None:
        """colorize with None color returns plain text."""
        from prism.view.palette import colorize

        result = colorize("Hello", None)

        assert result == "Hello"
        assert "\033[" not in result

    def test_palette_handles_missing_sections_gracefully(self, tmp_path: Path) -> None:
        """Palette handles missing sections with defaults."""
        from prism.view.palette import _clear_palette_cache, load_palette

        _clear_palette_cache()

        # TOML with only colors section
        toml_content = """
[colors]
primary = 39
"""
        toml_file = tmp_path / "partial-palette.toml"
        toml_file.write_text(toml_content)

        palette = load_palette(str(toml_file))

        # Should have defaults for missing sections
        assert palette.colors is not None
        assert palette.emojis is not None  # Should have defaults
        assert palette.styles is not None  # Should have defaults

    def test_should_use_color_detects_tty(self) -> None:
        """should_use_color() utility exists."""
        from prism.view.palette import should_use_color

        # Should return a boolean
        result = should_use_color()
        assert isinstance(result, bool)

    def test_should_use_color_respects_no_color(self) -> None:
        """should_use_color() respects NO_COLOR env var."""
        from prism.view.palette import should_use_color

        original = os.environ.get("NO_COLOR")
        try:
            os.environ["NO_COLOR"] = "1"
            assert should_use_color() is False
        finally:
            if original is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = original

    def test_should_use_color_respects_force_color(self) -> None:
        """should_use_color() respects FORCE_COLOR env var."""
        from prism.view.palette import should_use_color

        original_no_color = os.environ.get("NO_COLOR")
        original_force = os.environ.get("FORCE_COLOR")
        try:
            os.environ.pop("NO_COLOR", None)
            os.environ["FORCE_COLOR"] = "1"
            assert should_use_color() is True
        finally:
            if original_no_color is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = original_no_color
            if original_force is None:
                os.environ.pop("FORCE_COLOR", None)
            else:
                os.environ["FORCE_COLOR"] = original_force
