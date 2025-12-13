"""
Tests for exception formatter in prism-view.

Tests cover:
- Dev mode formatting (10.1)
- Prod mode formatting (10.2)
- Cause chain formatting (10.3)
- Stack trace formatting (10.4)
- Global exception handler (10.5)
"""

import json
import traceback

import pytest

from prism.view.errors import PrismError
from prism.view.formatter import ExceptionFormatter, format_exception, handle_exception


# =============================================================================
# Test Fixtures
# =============================================================================


class SampleError(PrismError):
    """Sample error class for testing."""

    code = (100, "TEST", "TEST_ERROR")
    category = "TEST"
    severity = "ERROR"


class RetryableError(PrismError):
    """Retryable error for testing recovery hints."""

    code = (101, "TEST", "RETRYABLE_ERROR")
    category = "TEST"
    severity = "ERROR"
    retryable = True
    max_retries = 3
    retry_delay_seconds = 1.5


class DatabaseError(PrismError):
    """Database error for testing cause chains."""

    code = (200, "DB", "CONNECTION_FAILED")
    category = "DATABASE"
    severity = "ERROR"


class NetworkError(PrismError):
    """Network error for testing cause chains."""

    code = (300, "NET", "TIMEOUT")
    category = "NETWORK"
    severity = "ERROR"


# =============================================================================
# 10.1: Dev Mode Formatter Tests
# =============================================================================


class TestDevModeFormatter:
    """Tests for dev mode exception formatting."""

    def test_formatter_renders_prism_error_beautifully(self):
        """Test that formatter renders PrismError with beautiful output."""
        error = SampleError("Something went wrong", details={"key": "value"})
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should have visual elements
        assert "SampleError" in result
        assert "Something went wrong" in result
        # Should have some visual formatting (colors, box chars, etc.)
        assert len(result) > 50  # Nontrivial output

    def test_formatter_includes_error_code(self):
        """Test that formatter includes error code in output."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should include the formatted error code
        assert "E-TEST-100" in result

    def test_formatter_includes_category_badge(self):
        """Test that formatter includes category badge."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should include category
        assert "TEST" in result

    def test_formatter_includes_suggestions(self):
        """Test that formatter includes suggestions."""
        error = SampleError(
            "Test message",
            suggestions=["Try this", "Or try that"],
        )
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should include suggestions
        assert "Try this" in result
        assert "Or try that" in result

    def test_formatter_includes_context(self):
        """Test that formatter includes context from error."""
        error = SampleError(
            "Test message", details={"user_id": "user-123", "request_id": "req-456"}
        )
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should include details
        assert "user_id" in result
        assert "user-123" in result

    def test_formatter_uses_colors_and_emojis(self):
        """Test that dev mode uses colors and emojis."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev", use_color=True)

        result = formatter.format(error)

        # Should include ANSI color codes when colors are enabled
        assert "\033[" in result or "❌" in result or "🔥" in result

    def test_formatter_respects_no_color(self, monkeypatch):
        """Test that NO_COLOR environment variable is respected."""
        monkeypatch.setenv("NO_COLOR", "1")
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should NOT include ANSI escape codes
        assert "\033[" not in result

    def test_formatter_dev_mode_is_human_readable(self):
        """Test that dev mode output is human-readable."""
        error = SampleError(
            "Something went wrong",
            details={"key": "value"},
            suggestions=["Try again"],
        )
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        # Output should be readable text, not JSON
        # Should have multiple lines
        assert "\n" in result
        # Should not be JSON
        try:
            json.loads(result)
            pytest.fail("Dev mode should not produce JSON")
        except json.JSONDecodeError:
            pass  # Expected

    def test_formatter_includes_recovery_hints(self):
        """Test that formatter includes recovery hints for retryable errors."""
        error = RetryableError("Operation failed")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should mention retryable or retry info
        assert "retry" in result.lower() or "retryable" in result.lower()

    def test_formatter_includes_docs_url(self):
        """Test that formatter includes documentation URL."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should include docs URL
        assert "prism.dev/errors" in result or "docs" in result.lower()


# =============================================================================
# 10.2: Prod Mode Formatter Tests
# =============================================================================


class TestProdModeFormatter:
    """Tests for prod mode exception formatting."""

    def test_prod_formatter_outputs_json(self):
        """Test that prod mode outputs valid JSON."""
        error = SampleError("Something went wrong")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_prod_json_includes_all_error_fields(self):
        """Test that JSON includes all relevant error fields."""
        error = SampleError(
            "Something went wrong",
            details={"key": "value"},
            suggestions=["Try this"],
        )
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should include standard fields
        assert parsed["type"] == "SampleError"
        assert parsed["message"] == "Something went wrong"
        assert parsed["error_code"] == "E-TEST-100"
        assert parsed["details"] == {"key": "value"}
        assert parsed["suggestions"] == ["Try this"]

    def test_prod_json_is_valid_and_parseable(self):
        """Test that JSON is valid and can be parsed."""
        error = SampleError(
            'Test with special chars: \n\t"quotes"',
            details={"unicode": "日本語", "nested": {"deep": True}},
        )
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)

        # Should parse without error
        parsed = json.loads(result)
        assert parsed["message"] == 'Test with special chars: \n\t"quotes"'
        assert parsed["details"]["unicode"] == "日本語"

    def test_prod_no_colors_or_emojis(self):
        """Test that prod mode has no colors or emojis."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)

        # Should NOT include ANSI escape codes
        assert "\033[" not in result
        # Parse as JSON - should not have emoji keys
        parsed = json.loads(result)
        for key in parsed.keys():
            # Keys should be plain alphanumeric/underscore
            assert key.isidentifier() or key.replace("_", "").isalnum()

    def test_prod_includes_timestamp(self):
        """Test that prod mode includes timestamp."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should include timestamp
        assert "timestamp" in parsed or "ts" in parsed

    def test_prod_includes_category(self):
        """Test that prod mode includes category."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should include category
        assert parsed.get("category") == "TEST"

    def test_prod_includes_recovery_info(self):
        """Test that prod mode includes recovery information."""
        error = RetryableError("Operation failed")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should include recovery info
        assert "recovery" in parsed
        assert parsed["recovery"]["retryable"] is True
        assert parsed["recovery"]["max_retries"] == 3

    def test_prod_no_stack_trace(self):
        """Test that prod mode does NOT include stack trace."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should NOT include stack trace
        assert "stack_trace" not in parsed
        assert "traceback" not in parsed

    def test_prod_no_debug_info(self):
        """Test that prod mode does NOT include debug info."""
        error = SampleError("Test message", debug_info={"secret": "value"})
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should NOT include debug info
        assert "debug_info" not in parsed
        assert "secret" not in str(parsed)


# =============================================================================
# 10.3: Cause Chain Formatting Tests
# =============================================================================


class TestCauseChainFormatting:
    """Tests for cause chain formatting."""

    def test_formatter_displays_cause_chain(self):
        """Test that formatter displays cause chain."""
        root = ValueError("Root problem")
        middle = NetworkError("Network failed", cause=root)
        error = DatabaseError("Database failed", cause=middle)
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        # Should show the chain
        assert "DatabaseError" in result
        assert "NetworkError" in result
        assert "ValueError" in result

    def test_cause_chain_is_indented(self):
        """Test that cause chain is indented for readability."""
        root = ValueError("Root problem")
        error = DatabaseError("Database failed", cause=root)
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)
        lines = result.split("\n")

        # Find cause-related lines and check for indentation
        cause_lines = [
            line
            for line in lines
            if "ValueError" in line or "Caused by" in line.lower() or "└" in line or "├" in line
        ]
        assert len(cause_lines) > 0
        # Cause should be indented (have leading spaces or tree chars)
        for line in cause_lines:
            if "ValueError" in line:
                assert line.startswith(" ") or "└" in line or "├" in line

    def test_root_cause_is_highlighted(self):
        """Test that root cause is highlighted or marked."""
        root = ValueError("Root problem")
        middle = NetworkError("Network failed", cause=root)
        error = DatabaseError("Database failed", cause=middle)
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        # Root cause should be identifiable (last in chain or marked)
        assert "Root problem" in result
        # Should have some indication it's the root
        assert "root" in result.lower() or "└" in result

    def test_cause_chain_includes_error_codes(self):
        """Test that cause chain includes error codes for PrismErrors."""
        root = NetworkError("Network failed")
        error = DatabaseError("Database failed", cause=root)
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        # Should include error codes for both
        assert "E-DB-200" in result
        assert "E-NET-300" in result

    def test_cause_chain_in_prod_mode(self):
        """Test that cause chain is included in prod mode JSON."""
        root = ValueError("Root problem")
        error = DatabaseError("Database failed", cause=root)
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should include cause_chain
        assert "cause_chain" in parsed
        assert len(parsed["cause_chain"]) > 0
        assert parsed["cause_chain"][0]["type"] == "ValueError"


# =============================================================================
# 10.4: Stack Trace Formatting Tests
# =============================================================================


class TestStackTraceFormatting:
    """Tests for stack trace formatting."""

    def test_formatter_includes_stack_trace_dev(self):
        """Test that dev mode includes stack trace."""
        try:
            raise SampleError("Test message")
        except SampleError as e:
            error = e
            # Capture traceback (unused, just for context)
            traceback.format_exc()

        formatter = ExceptionFormatter(mode="dev", include_stack=True)
        result = formatter.format(error)

        # Should include some stack info
        # Either location info or actual traceback
        assert "test_formatter" in result or "line" in result.lower() or "file" in result.lower()

    def test_stack_trace_shows_file_and_line(self):
        """Test that stack trace shows file and line info."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev", include_stack=True, use_color=False)

        result = formatter.format(error)

        # Should include location info from PrismError
        # Check for file or line indicators
        location_file = error.location.get("file", "")
        assert "line" in result.lower() or ".py" in result or location_file in result

    def test_stack_trace_not_in_prod(self):
        """Test that stack trace is NOT included in prod mode."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="prod", include_stack=True)  # Even with flag

        result = formatter.format(error)
        parsed = json.loads(result)

        # Should NOT include stack trace
        assert "stack_trace" not in parsed
        assert "traceback" not in parsed
        assert "location" not in parsed  # Location also hidden in prod

    def test_stack_trace_can_be_disabled(self):
        """Test that stack trace can be disabled in dev mode."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev", include_stack=False, use_color=False)

        result = formatter.format(error)

        # Should NOT include file/line info from stack
        # The error still has location, but formatter should not show it
        assert "Location" not in result

    def test_stack_trace_is_readable(self):
        """Test that stack trace is formatted readably."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev", include_stack=True, use_color=False)

        result = formatter.format(error)

        # Should be multi-line and readable
        if "Location" in result or "File" in result:
            # Stack info should be formatted nicely
            assert "\n" in result


# =============================================================================
# 10.5: Global Exception Handler Tests
# =============================================================================


class TestHandleException:
    """Tests for handle_exception utility function."""

    def test_handle_exception_formats_and_returns(self):
        """Test that handle_exception formats exception and returns string."""
        error = SampleError("Something went wrong")

        result = handle_exception(error)

        assert isinstance(result, str)
        assert "SampleError" in result
        assert "Something went wrong" in result

    def test_handle_exception_works_with_prism_error(self):
        """Test that handle_exception works with PrismError."""
        error = SampleError("Test message", suggestions=["Try this"])

        result = handle_exception(error)

        assert "SampleError" in result
        assert "Test message" in result
        assert "Try this" in result

    def test_handle_exception_works_with_standard_exceptions(self):
        """Test that handle_exception works with standard Python exceptions."""
        error = ValueError("Invalid value")

        result = handle_exception(error)

        assert "ValueError" in result
        assert "Invalid value" in result

    def test_handle_exception_returns_formatted_string(self):
        """Test that handle_exception returns a formatted string."""
        error = SampleError("Test")

        result = handle_exception(error)

        # Should return non-empty formatted string
        assert len(result) > 0
        assert isinstance(result, str)

    def test_handle_exception_respects_mode(self):
        """Test that handle_exception respects mode parameter."""
        error = SampleError("Test message")

        dev_result = handle_exception(error, mode="dev")
        prod_result = handle_exception(error, mode="prod")

        # Dev should be multi-line, prod should be JSON
        assert "\n" in dev_result or len(dev_result) > 50
        # Prod should be parseable JSON
        parsed = json.loads(prod_result)
        assert parsed["type"] == "SampleError"

    def test_handle_exception_with_traceback(self):
        """Test that handle_exception can include traceback."""
        try:
            raise SampleError("Test message")
        except SampleError as e:
            result = handle_exception(e, include_traceback=True, mode="dev")

        # Should include some traceback info
        assert "test_formatter" in result or "Traceback" in result or "File" in result


# =============================================================================
# 10.5: format_exception convenience function
# =============================================================================


class TestFormatException:
    """Tests for format_exception convenience function."""

    def test_format_exception_basic(self):
        """Test basic format_exception usage."""
        error = SampleError("Test message")

        result = format_exception(error)

        assert "SampleError" in result
        assert "Test message" in result

    def test_format_exception_dev_mode(self):
        """Test format_exception in dev mode."""
        error = SampleError("Test message")

        result = format_exception(error, mode="dev")

        # Should not be JSON
        try:
            json.loads(result)
            pytest.fail("Dev mode should not produce JSON")
        except json.JSONDecodeError:
            pass

    def test_format_exception_prod_mode(self):
        """Test format_exception in prod mode."""
        error = SampleError("Test message")

        result = format_exception(error, mode="prod")

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed["type"] == "SampleError"


# =============================================================================
# Edge Cases
# =============================================================================


class TestFormatterEdgeCases:
    """Edge case tests for formatter."""

    def test_formatter_handles_none_details(self):
        """Test that formatter handles None/empty details."""
        error = SampleError("Test message")
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        # Should not crash, should produce output
        assert "SampleError" in result

    def test_formatter_handles_unicode(self):
        """Test that formatter handles unicode in messages."""
        error = SampleError("日本語メッセージ", details={"emoji": "🔥"})
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        assert "日本語メッセージ" in result

    def test_formatter_handles_long_messages(self):
        """Test that formatter handles long messages."""
        long_message = "A" * 1000
        error = SampleError(long_message)
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        # Should truncate or handle gracefully
        assert "SampleError" in result

    def test_formatter_handles_nested_details(self):
        """Test that formatter handles nested details."""
        error = SampleError(
            "Test",
            details={
                "level1": {
                    "level2": {
                        "level3": "deep",
                    }
                }
            },
        )
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        assert parsed["details"]["level1"]["level2"]["level3"] == "deep"

    def test_formatter_handles_standard_exception(self):
        """Test that formatter handles standard exceptions."""
        error = ValueError("Not a PrismError")
        formatter = ExceptionFormatter(mode="dev", use_color=False)

        result = formatter.format(error)

        assert "ValueError" in result
        assert "Not a PrismError" in result

    def test_formatter_handles_exception_with_no_message(self):
        """Test that formatter handles exceptions with no message."""
        error = RuntimeError()
        formatter = ExceptionFormatter(mode="dev")

        result = formatter.format(error)

        assert "RuntimeError" in result

    def test_formatter_prod_handles_standard_exception(self):
        """Test that prod mode handles standard exceptions."""
        error = ValueError("Standard error")
        formatter = ExceptionFormatter(mode="prod")

        result = formatter.format(error)
        parsed = json.loads(result)

        assert parsed["type"] == "ValueError"
        assert parsed["message"] == "Standard error"
