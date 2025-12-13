"""
Tests for Logger Implementation - Prod Mode (Iteration 6).

Tests cover:
- Prod mode detection (env var, config)
- JSON formatting (structure, validity)
- Timestamp formatting (ISO 8601, UTC)
- Error formatting in prod mode
- Mode switching
"""

import json
import os
from datetime import datetime, timezone
from unittest.mock import patch


class TestProdModeDetection:
    """Tests for prod mode detection (6.1)."""

    def test_logger_default_mode_is_dev(self):
        """Logger default mode is dev."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert logger.mode == "dev"

    def test_logger_can_set_prod_mode(self):
        """Logger can be set to prod mode."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        assert logger.mode == "prod"

    def test_get_logger_accepts_mode_parameter(self):
        """get_logger() accepts mode parameter."""
        from prism.view.logger import get_logger

        logger = get_logger("prod-test-logger", mode="prod")
        assert logger.mode == "prod"

    def test_logger_mode_from_environment_variable(self):
        """Logger respects PRISM_LOG_MODE environment variable."""
        from prism.view.logger import get_default_mode

        with patch.dict(os.environ, {"PRISM_LOG_MODE": "prod"}):
            mode = get_default_mode()
            assert mode == "prod"

    def test_logger_mode_env_var_dev(self):
        """PRISM_LOG_MODE=dev sets dev mode."""
        from prism.view.logger import get_default_mode

        with patch.dict(os.environ, {"PRISM_LOG_MODE": "dev"}):
            mode = get_default_mode()
            assert mode == "dev"

    def test_logger_mode_env_var_case_insensitive(self):
        """PRISM_LOG_MODE is case-insensitive."""
        from prism.view.logger import get_default_mode

        with patch.dict(os.environ, {"PRISM_LOG_MODE": "PROD"}):
            mode = get_default_mode()
            assert mode == "prod"

    def test_logger_mode_env_var_production_alias(self):
        """PRISM_LOG_MODE=production is alias for prod."""
        from prism.view.logger import get_default_mode

        with patch.dict(os.environ, {"PRISM_LOG_MODE": "production"}):
            mode = get_default_mode()
            assert mode == "prod"

    def test_logger_mode_defaults_to_dev_when_not_set(self):
        """Default mode is dev when env var not set."""
        from prism.view.logger import get_default_mode

        with patch.dict(os.environ, {}, clear=True):
            # Remove PRISM_LOG_MODE if it exists
            os.environ.pop("PRISM_LOG_MODE", None)
            mode = get_default_mode()
            assert mode == "dev"

    def test_is_prod_mode_utility(self):
        """is_prod_mode() returns True when mode is prod."""
        from prism.view.logger import Logger

        dev_logger = Logger("test", mode="dev")
        prod_logger = Logger("test", mode="prod")

        assert dev_logger.is_prod_mode() is False
        assert prod_logger.is_prod_mode() is True


class TestJSONFormatting:
    """Tests for JSON formatting in prod mode (6.2)."""

    def test_prod_mode_outputs_json(self, capsys):
        """Prod mode outputs JSON."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        output = captured.err.strip()

        # Should be valid JSON
        parsed = json.loads(output)
        assert isinstance(parsed, dict)

    def test_json_has_timestamp_field(self, capsys):
        """JSON output has 'ts' timestamp field."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "ts" in parsed

    def test_json_has_level_field(self, capsys):
        """JSON output has 'level' field."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "level" in parsed
        assert parsed["level"] == "INFO"

    def test_json_has_message_field(self, capsys):
        """JSON output has 'msg' message field."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "msg" in parsed
        assert parsed["msg"] == "Test message"

    def test_json_has_logger_name(self, capsys):
        """JSON output has 'logger' name field."""
        from prism.view.logger import Logger

        logger = Logger("my-service", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "logger" in parsed
        assert parsed["logger"] == "my-service"

    def test_json_includes_context(self, capsys):
        """JSON output includes context fields."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.set_service(name="api", version="1.0.0")

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        # Context should be included
        assert "context" in parsed or "service" in parsed
        # Service name should be present somewhere
        output = captured.err
        assert "api" in output

    def test_json_includes_extra_fields(self, capsys):
        """JSON output includes extra fields from kwargs."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message", user_id="user-123", action="login")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert parsed.get("user_id") == "user-123"
        assert parsed.get("action") == "login"

    def test_json_includes_trace_id(self, capsys):
        """JSON output includes trace_id from context."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        with LogContext.request(trace_id="trace-abc-123"):
            logger = Logger("test", mode="prod")
            logger.info("Test message")

            captured = capsys.readouterr()
            parsed = json.loads(captured.err.strip())

            assert "trace_id" in parsed or "trace-abc-123" in captured.err

    def test_json_is_single_line(self, capsys):
        """JSON output is single line (no pretty printing)."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message", field1="value1", field2="value2")

        captured = capsys.readouterr()
        output = captured.err.strip()

        # Should be exactly one line
        assert output.count("\n") == 0

    def test_json_is_valid_parseable(self, capsys):
        """JSON output is always valid and parseable."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        # Log various types of messages
        logger.info("Simple message")
        logger.warn("Warning with data", count=42, active=True, ratio=3.14)
        logger.error("Error message")
        logger.debug("Debug message")

        captured = capsys.readouterr()
        lines = captured.err.strip().split("\n")

        for line in lines:
            if line:  # Skip empty lines
                parsed = json.loads(line)
                assert isinstance(parsed, dict)

    def test_json_level_values_are_correct(self, capsys):
        """JSON level field has correct values for each log level."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        test_cases = [
            ("debug", "DEBUG"),
            ("info", "INFO"),
            ("warn", "WARNING"),
            ("error", "ERROR"),
            ("critical", "CRITICAL"),
        ]

        for method_name, _expected_level in test_cases:
            method = getattr(logger, method_name)
            method(f"{method_name} message")

        captured = capsys.readouterr()
        lines = [line for line in captured.err.strip().split("\n") if line]

        for i, (_, expected_level) in enumerate(test_cases):
            parsed = json.loads(lines[i])
            assert parsed["level"] == expected_level


class TestTimestampFormatting:
    """Tests for timestamp formatting in prod mode (6.3)."""

    def test_timestamp_is_iso8601_format(self, capsys):
        """Timestamp is in ISO 8601 format."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        ts = parsed["ts"]
        # ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ
        assert "T" in ts
        assert ts.endswith("Z")

    def test_timestamp_includes_milliseconds(self, capsys):
        """Timestamp includes milliseconds."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        ts = parsed["ts"]
        # Should have decimal point for milliseconds
        assert "." in ts

    def test_timestamp_is_utc(self, capsys):
        """Timestamp is in UTC (ends with Z)."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        ts = parsed["ts"]
        assert ts.endswith("Z")

    def test_timestamp_is_parseable(self, capsys):
        """Timestamp can be parsed as datetime."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        ts = parsed["ts"]
        # Remove Z suffix and parse
        ts_clean = ts.rstrip("Z")
        dt = datetime.fromisoformat(ts_clean)
        assert dt is not None

    def test_timestamp_is_recent(self, capsys):
        """Timestamp is recent (within last second)."""
        from prism.view.logger import Logger

        before = datetime.now(timezone.utc)

        logger = Logger("test", mode="prod")
        logger.info("Test message")

        after = datetime.now(timezone.utc)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        ts = parsed["ts"]
        ts_clean = ts.rstrip("Z")
        dt = datetime.fromisoformat(ts_clean).replace(tzinfo=timezone.utc)

        # Account for millisecond truncation - allow 1 second tolerance
        from datetime import timedelta

        assert before - timedelta(seconds=1) <= dt <= after + timedelta(seconds=1)


class TestErrorFormattingProd:
    """Tests for error formatting in prod mode (6.4)."""

    def test_prod_error_includes_error_object(self, capsys):
        """Prod mode includes error object in JSON."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        error = PrismError("Test error")
        logger.error("An error occurred", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "error" in parsed

    def test_prod_error_includes_error_type(self, capsys):
        """Prod error object includes error type."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        class CustomError(PrismError):
            pass

        error = CustomError("Test error")
        logger.error("An error occurred", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert parsed["error"]["type"] == "CustomError"

    def test_prod_error_includes_error_message(self, capsys):
        """Prod error object includes error message."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        error = PrismError("Detailed error message")
        logger.error("An error occurred", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert parsed["error"]["message"] == "Detailed error message"

    def test_prod_error_includes_error_code(self, capsys):
        """Prod error object includes error code."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        class ConfigError(PrismError):
            code = (1, "CFG", "CONFIG_MISSING")

        error = ConfigError("Config file not found")
        logger.error("Configuration error", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "error_code" in parsed["error"]
        assert parsed["error"]["error_code"] == "E-CFG-001"

    def test_prod_error_includes_details(self, capsys):
        """Prod error object includes details."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        error = PrismError(
            "Validation failed",
            details={"field": "email", "reason": "invalid format"},
        )
        logger.error("Validation error", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "details" in parsed["error"]
        assert parsed["error"]["details"]["field"] == "email"

    def test_prod_error_includes_cause_chain(self, capsys):
        """Prod error object includes cause chain."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        root_cause = ValueError("Invalid port number")
        error = PrismError("Connection failed", cause=root_cause)
        logger.error("Network error", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "cause_chain" in parsed["error"]
        assert len(parsed["error"]["cause_chain"]) > 0

    def test_prod_error_no_stack_trace(self, capsys):
        """Prod mode does NOT include stack trace in error."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        error = PrismError("Test error")
        logger.error("An error occurred", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        # Stack trace should not be in the error object
        assert "stack_trace" not in parsed.get("error", {})
        assert "traceback" not in parsed.get("error", {})

    def test_prod_error_no_debug_info(self, capsys):
        """Prod mode does NOT include debug_info."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        error = PrismError("Test error", debug_info={"secret": "data"})
        logger.error("An error occurred", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        # Debug info should not be in the error object
        assert "debug_info" not in parsed.get("error", {})

    def test_prod_error_includes_recovery_hints(self, capsys):
        """Prod error object includes recovery hints."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        class RetryableError(PrismError):
            retryable = True
            max_retries = 3
            retry_delay_seconds = 1.5

        error = RetryableError("Temporary failure")
        logger.error("Service error", exc=error)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "recovery" in parsed["error"]
        assert parsed["error"]["recovery"]["retryable"] is True
        assert parsed["error"]["recovery"]["max_retries"] == 3

    def test_prod_standard_exception_formatting(self, capsys):
        """Prod mode handles standard Python exceptions."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")

        try:
            raise ValueError("Something went wrong")
        except ValueError as e:
            logger.error("An error occurred", exc=e)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "error" in parsed
        assert parsed["error"]["type"] == "ValueError"
        assert parsed["error"]["message"] == "Something went wrong"


class TestModeSwitching:
    """Tests for mode switching (6.5)."""

    def test_logger_mode_can_change(self):
        """Logger mode can be changed after creation."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        assert logger.mode == "dev"

        logger.mode = "prod"
        assert logger.mode == "prod"

    def test_logger_output_changes_with_mode(self, capsys):
        """Logger output format changes with mode."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("Dev message")

        dev_output = capsys.readouterr().err

        logger.mode = "prod"
        logger.info("Prod message")

        prod_output = capsys.readouterr().err

        # Dev mode should NOT be JSON
        assert not dev_output.strip().startswith("{")

        # Prod mode should be JSON
        assert prod_output.strip().startswith("{")

    def test_child_logger_inherits_mode(self):
        """Child logger inherits parent's mode."""
        from prism.view.logger import Logger

        parent = Logger("parent", mode="prod")
        child = parent.with_context(request_id="req-123")

        assert child.mode == parent.mode

    def test_child_logger_mode_independent_after_creation(self):
        """Child logger mode is independent after creation."""
        from prism.view.logger import Logger

        parent = Logger("parent", mode="prod")
        child = parent.with_context(request_id="req-123")

        parent.mode = "dev"

        # Child should still be prod (independent)
        assert child.mode == "prod"

    def test_get_logger_mode_only_applied_on_first_call(self):
        """get_logger() mode parameter only applies on first call."""
        from prism.view.logger import get_logger

        logger1 = get_logger("mode-test-logger", mode="prod")
        logger2 = get_logger("mode-test-logger", mode="dev")

        # Both should return same instance with original mode
        assert logger1 is logger2
        assert logger1.mode == "prod"


class TestJSONSpecialCases:
    """Tests for JSON handling of special cases."""

    def test_json_handles_unicode(self, capsys):
        """JSON handles unicode characters correctly."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        # Use valid unicode characters: Chinese, accented letters
        logger.info("Unicode: 中文 éèê")

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert "Unicode" in parsed["msg"]
        assert "中文" in parsed["msg"]

    def test_json_handles_special_characters(self, capsys):
        """JSON properly escapes special characters."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info('Message with "quotes" and \\ backslash')

        captured = capsys.readouterr()
        # Should be valid JSON despite special characters
        parsed = json.loads(captured.err.strip())
        assert "quotes" in parsed["msg"]

    def test_json_handles_newlines_in_message(self, capsys):
        """JSON properly escapes newlines in message."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Line 1\nLine 2\nLine 3")

        captured = capsys.readouterr()
        output = captured.err.strip()

        # Output should still be single line JSON
        assert output.count("\n") == 0

        parsed = json.loads(output)
        assert "Line 1" in parsed["msg"]

    def test_json_handles_none_values(self, capsys):
        """JSON handles None values in extra fields."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info("Test message", optional_field=None)

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert parsed.get("optional_field") is None

    def test_json_handles_nested_dicts(self, capsys):
        """JSON handles nested dictionaries in extra fields."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="prod")
        logger.info(
            "Test message",
            metadata={"nested": {"deep": "value"}, "list": [1, 2, 3]},
        )

        captured = capsys.readouterr()
        parsed = json.loads(captured.err.strip())

        assert parsed["metadata"]["nested"]["deep"] == "value"
        assert parsed["metadata"]["list"] == [1, 2, 3]
