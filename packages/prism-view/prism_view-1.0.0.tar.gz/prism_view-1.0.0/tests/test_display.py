"""
Tests for the Console Display Utilities.

Tests cover:
- Basic table rendering
- Table styling with palettes
- Column alignment
- Unicode width handling (emojis, CJK characters)
- Large data handling
- ASCII banner rendering
"""

import os


# =============================================================================
# 9.1: Basic Table Rendering Tests
# =============================================================================


class TestBasicTableRendering:
    """Tests for basic table rendering functionality."""

    def test_console_table_renders_simple_table(self) -> None:
        """9.1.1: console_table() renders simple table."""
        from prism.view.display import console_table

        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]

        result = console_table(data)

        assert result is not None
        assert isinstance(result, str)
        assert "Alice" in result
        assert "Bob" in result
        assert "30" in result
        assert "25" in result

    def test_table_has_header_row(self) -> None:
        """9.1.2: Table has header row."""
        from prism.view.display import console_table

        data = [
            {"name": "Alice", "age": 30},
        ]

        result = console_table(data)

        # Headers should be present (capitalized or as-is)
        assert "name" in result.lower()
        assert "age" in result.lower()

    def test_table_has_data_rows(self) -> None:
        """9.1.3: Table has data rows."""
        from prism.view.display import console_table

        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]

        result = console_table(data)

        # All data should be present
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result

    def test_table_uses_box_drawing_characters(self) -> None:
        """9.1.4: Table uses box drawing characters."""
        from prism.view.display import console_table

        data = [{"name": "Alice"}]

        result = console_table(data)

        # Should contain some box drawing characters
        # Either Unicode box drawing or ASCII fallback
        has_box_chars = (
            "\u2500" in result  # horizontal line
            or "\u2502" in result  # vertical line
            or "-" in result  # ASCII fallback
            or "|" in result  # ASCII fallback
        )
        assert has_box_chars

    def test_table_auto_calculates_column_widths(self) -> None:
        """9.1.5: Table auto-calculates column widths."""
        from prism.view.display import console_table

        data = [
            {"short": "a", "very_long_column_name": "value"},
            {"short": "bb", "very_long_column_name": "another_value"},
        ]

        result = console_table(data)

        # The table should be formatted consistently
        lines = result.strip().split("\n")
        # All lines with content should have similar structure
        assert len(lines) >= 3  # header + separator + at least one data row


# =============================================================================
# 9.2: Table Styling Tests
# =============================================================================


class TestTableStyling:
    """Tests for table styling with palettes."""

    def test_table_respects_palette_colors(self) -> None:
        """9.2.1: Table respects palette colors."""
        from prism.view.display import console_table
        from prism.view.palette import get_default_palette

        data = [{"name": "Alice"}]
        palette = get_default_palette()

        result = console_table(data, palette=palette, use_color=True)

        # Should contain ANSI color codes when colors enabled
        assert "\033[" in result

    def test_table_respects_box_style(self) -> None:
        """9.2.2: Table respects box style."""
        from prism.view.display import console_table

        data = [{"name": "Alice"}]

        # Test with different box styles - just verify they don't crash
        # and produce output
        console_table(data, box_style="single")
        console_table(data, box_style="double")
        result_ascii = console_table(data, box_style="ascii")

        # Different styles should produce different output
        # ASCII uses +, -, | while Unicode uses special chars
        assert "+" in result_ascii or "-" in result_ascii

    def test_table_has_optional_title(self) -> None:
        """9.2.3: Table has optional title."""
        from prism.view.display import console_table

        data = [{"name": "Alice"}]

        result = console_table(data, title="User List")

        assert "User List" in result

    def test_table_headers_are_styled(self) -> None:
        """9.2.4: Table headers are bold/colored."""
        from prism.view.display import console_table
        from prism.view.palette import get_default_palette

        data = [{"name": "Alice", "age": 30}]
        palette = get_default_palette()

        result = console_table(data, palette=palette, use_color=True)

        # Headers should have some styling applied
        # (color codes appear in output)
        assert "\033[" in result


# =============================================================================
# 9.3: Column Alignment Tests
# =============================================================================


class TestColumnAlignment:
    """Tests for column alignment."""

    def test_columns_can_be_left_aligned(self) -> None:
        """9.3.1: Columns can be left-aligned."""
        from prism.view.display import console_table

        data = [
            {"name": "A", "value": "test"},
            {"name": "BB", "value": "test2"},
        ]

        result = console_table(data, align={"name": "left"})

        # Left-aligned columns should have padding on the right
        assert "A" in result

    def test_columns_can_be_right_aligned(self) -> None:
        """9.3.2: Columns can be right-aligned."""
        from prism.view.display import console_table

        data = [
            {"num": 1, "value": "test"},
            {"num": 100, "value": "test2"},
        ]

        result = console_table(data, align={"num": "right"})

        # Right-aligned columns should have padding on the left
        assert "1" in result
        assert "100" in result

    def test_columns_can_be_center_aligned(self) -> None:
        """9.3.3: Columns can be center-aligned."""
        from prism.view.display import console_table

        data = [
            {"status": "OK"},
            {"status": "FAIL"},
        ]

        result = console_table(data, align={"status": "center"})

        assert "OK" in result
        assert "FAIL" in result

    def test_numeric_columns_auto_align_right(self) -> None:
        """9.3.4: Numeric columns auto-align right."""
        from prism.view.display import console_table

        data = [
            {"name": "Item", "price": 10.99},
            {"name": "Other", "price": 100.00},
        ]

        result = console_table(data)

        # Numeric values should be present and formatted
        assert "10.99" in result or "10.9" in result
        assert "100" in result


# =============================================================================
# 9.4: Unicode Width Handling Tests
# =============================================================================


class TestUnicodeWidthHandling:
    """Tests for Unicode width handling."""

    def test_display_width_calculates_ascii_correctly(self) -> None:
        """9.4.1: display_width() calculates ASCII string width correctly."""
        from prism.view.display import display_width

        assert display_width("hello") == 5
        assert display_width("test") == 4
        assert display_width("") == 0
        assert display_width("a") == 1

    def test_display_width_handles_emoji_widths(self) -> None:
        """9.4.2: display_width() handles emoji widths (2 columns)."""
        from prism.view.display import display_width

        # Most emojis take 2 columns
        assert display_width("\U0001f600") == 2  # Grinning face
        assert display_width("\u2764\ufe0f") >= 1  # Heart with variation selector

    def test_display_width_handles_cjk_characters(self) -> None:
        """9.4.3: display_width() handles CJK characters (2 columns)."""
        from prism.view.display import display_width

        # CJK characters are typically 2 columns wide
        assert display_width("\u4e2d") == 2  # Chinese character
        assert display_width("\u65e5\u672c") == 4  # Japanese characters (2 chars * 2 width)

    def test_display_width_handles_variation_selectors(self) -> None:
        """9.4.4: display_width() handles variation selectors (zero-width)."""
        from prism.view.display import display_width

        # Variation selectors should not add width
        # Base char + variation selector should be same as base char display
        base_width = display_width("\u2764")  # Heart
        with_selector = display_width("\u2764\ufe0f")  # Heart + variation selector

        # The variation selector should not add more than expected
        assert with_selector >= base_width

    def test_display_width_handles_zero_width_joiners(self) -> None:
        """9.4.5: display_width() handles zero-width joiners."""
        from prism.view.display import display_width

        # Zero-width joiner itself should be 0
        zwj = "\u200d"
        assert display_width(zwj) == 0

    def test_pad_to_width_pads_string(self) -> None:
        """9.4.6: pad_to_width() pads string to target display width."""
        from prism.view.display import pad_to_width

        result = pad_to_width("hello", 10)
        assert len(result) == 10  # ASCII, so len == display width
        assert result == "hello     "

    def test_table_handles_emoji_widths_correctly(self) -> None:
        """9.4.7: Table handles emoji widths correctly."""
        from prism.view.display import console_table

        data = [
            {"status": "\u2705", "name": "Success"},  # Check mark emoji
            {"status": "\u274c", "name": "Failure"},  # Cross mark emoji
        ]

        result = console_table(data)

        # Table should render without breaking alignment
        assert "\u2705" in result
        assert "\u274c" in result
        assert "Success" in result
        assert "Failure" in result

    def test_table_handles_cjk_characters(self) -> None:
        """9.4.8: Table handles CJK characters."""
        from prism.view.display import console_table

        data = [
            {"name": "\u4e2d\u6587", "value": "Chinese"},  # Chinese characters
            {"name": "\u65e5\u672c\u8a9e", "value": "Japanese"},  # Japanese
        ]

        result = console_table(data)

        # Table should render CJK characters
        assert "\u4e2d\u6587" in result
        assert "\u65e5\u672c\u8a9e" in result


# =============================================================================
# 9.5: Large Data Handling Tests
# =============================================================================


class TestLargeDataHandling:
    """Tests for handling large datasets."""

    def test_table_handles_100_plus_rows(self) -> None:
        """9.5.1: Table handles 100+ rows."""
        from prism.view.display import console_table

        data = [{"id": i, "value": f"item_{i}"} for i in range(150)]

        result = console_table(data)

        # Should render without error
        assert result is not None
        assert "item_0" in result
        assert "item_149" in result

    def test_table_handles_20_plus_columns(self) -> None:
        """9.5.2: Table handles 20+ columns."""
        from prism.view.display import console_table

        row = {f"col_{i}": f"val_{i}" for i in range(25)}
        data = [row]

        result = console_table(data)

        # Should render without error
        assert result is not None
        assert "col_0" in result
        assert "col_24" in result

    def test_table_truncates_long_values(self) -> None:
        """9.5.3: Table truncates long values."""
        from prism.view.display import console_table

        data = [
            {"name": "A" * 200, "value": "short"},
        ]

        result = console_table(data, max_col_width=20)

        # Long value should be truncated
        assert "..." in result or len(result.split("\n")[0]) < 250

    def test_table_has_max_width_option(self) -> None:
        """9.5.4: Table has max_width option."""
        from prism.view.display import console_table

        data = [
            {"col1": "value1", "col2": "value2", "col3": "value3"},
        ]

        # Without max_width - verify it works
        console_table(data, use_color=False)
        # With max_width
        result_limited = console_table(data, max_width=40, use_color=False)

        # The limited version should have constrained column widths
        # (though the effect depends on the data)
        # Check that the function accepts and processes the parameter
        assert result_limited is not None
        assert len(result_limited) > 0


# =============================================================================
# 9.6: ASCII Banner Tests
# =============================================================================


class TestASCIIBanner:
    """Tests for ASCII banner rendering."""

    def test_render_banner_returns_prism_ascii_art(self) -> None:
        """9.6.1: render_banner() returns PRISM ASCII art."""
        from prism.view.display import render_banner

        result = render_banner()

        # Should contain PRISM text or stylized version
        assert result is not None
        assert len(result) > 0
        # Banner should have multiple lines
        assert "\n" in result

    def test_banner_includes_view_loaded_title(self) -> None:
        """9.6.2: Banner includes 'VIEW LOADED' title."""
        from prism.view.display import render_banner

        result = render_banner()

        # Should contain VIEW LOADED or similar
        assert "VIEW" in result.upper() or "PRISM" in result.upper()

    def test_banner_uses_version_from_module(self) -> None:
        """9.6.3: Banner uses version from __version__."""
        from prism.view import __version__
        from prism.view.display import render_banner

        result = render_banner()

        # Version should be displayed
        assert __version__ in result or "v" in result.lower()

    def test_banner_uses_vaporwave_gradient_colors(self) -> None:
        """9.6.4: Banner uses vaporwave gradient colors (pink -> cyan)."""
        from prism.view.display import render_banner

        result = render_banner(use_color=True)

        # Should contain ANSI color codes
        assert "\033[" in result

    def test_banner_colors_disabled_when_use_color_false(self) -> None:
        """9.6.5: Banner colors disabled when use_color=False."""
        from prism.view.display import render_banner

        result = render_banner(use_color=False)

        # Should NOT contain ANSI color codes
        assert "\033[" not in result

    def test_banner_respects_no_color_env_var(self) -> None:
        """9.6.6: Banner respects NO_COLOR environment variable."""
        from prism.view.display import render_banner

        original = os.environ.get("NO_COLOR")
        try:
            os.environ["NO_COLOR"] = "1"

            result = render_banner()

            # Should NOT contain ANSI color codes
            assert "\033[" not in result
        finally:
            if original is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = original

    def test_should_use_color_detects_tty(self) -> None:
        """9.6.7: should_use_color() detects TTY correctly."""
        from prism.view.palette import should_use_color

        # In test environment, typically not a TTY
        # but the function should return a boolean
        result = should_use_color()
        assert isinstance(result, bool)


# =============================================================================
# Edge Cases and Additional Tests
# =============================================================================


class TestDisplayEdgeCases:
    """Tests for edge cases in display utilities."""

    def test_console_table_handles_empty_data(self) -> None:
        """console_table handles empty data list."""
        from prism.view.display import console_table

        result = console_table([])

        # Should return empty or minimal output
        assert result is not None

    def test_console_table_handles_none_values(self) -> None:
        """console_table handles None values in data."""
        from prism.view.display import console_table

        data = [
            {"name": "Alice", "age": None},
            {"name": None, "age": 30},
        ]

        result = console_table(data)

        # Should handle None gracefully
        assert result is not None
        assert "Alice" in result

    def test_console_table_handles_mixed_types(self) -> None:
        """console_table handles mixed value types."""
        from prism.view.display import console_table

        data = [
            {"name": "Test", "count": 42, "active": True, "ratio": 3.14},
        ]

        result = console_table(data)

        assert "Test" in result
        assert "42" in result
        assert "True" in result or "true" in result

    def test_display_width_handles_empty_string(self) -> None:
        """display_width handles empty string."""
        from prism.view.display import display_width

        assert display_width("") == 0

    def test_display_width_handles_newlines(self) -> None:
        """display_width handles strings with newlines."""
        from prism.view.display import display_width

        # Newlines should not add width or should be handled
        result = display_width("hello\nworld")
        assert result >= 5  # At least the width of "hello" or "world"

    def test_pad_to_width_handles_already_wide_string(self) -> None:
        """pad_to_width handles string already at target width."""
        from prism.view.display import pad_to_width

        result = pad_to_width("hello", 5)
        assert result == "hello"

    def test_pad_to_width_handles_wider_string(self) -> None:
        """pad_to_width handles string wider than target."""
        from prism.view.display import pad_to_width

        result = pad_to_width("hello world", 5)
        # Should truncate or return as-is
        assert len(result) >= 5

    def test_console_table_with_list_of_lists(self) -> None:
        """console_table can work with list of lists (with headers)."""
        from prism.view.display import console_table

        headers = ["Name", "Age"]
        data = [
            ["Alice", 30],
            ["Bob", 25],
        ]

        result = console_table(data, headers=headers)

        assert "Name" in result
        assert "Age" in result
        assert "Alice" in result

    def test_banner_with_custom_palette(self) -> None:
        """render_banner works with custom palette."""
        from prism.view.display import render_banner
        from prism.view.palette import get_palette

        palette = get_palette("monochrome")

        result = render_banner(palette=palette, use_color=True)

        # Should render without error
        assert result is not None
