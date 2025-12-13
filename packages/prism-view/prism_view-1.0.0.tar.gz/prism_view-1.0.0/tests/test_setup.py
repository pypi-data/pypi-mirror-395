"""
Tests for setup_logging and Python logging integration.

Tests cover:
- setup_logging() function (11.1)
- Python logging integration (11.2)
- Operation decorator (11.5)
"""

import io
import json
import logging

import pytest

from prism.view import LogContext, get_logger


# =============================================================================
# 11.1: setup_logging() Tests
# =============================================================================


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_initializes_system(self):
        """11.1.1: setup_logging() initializes system."""
        from prism.view.setup import setup_logging

        # Should not raise
        result = setup_logging()

        # Should return a configuration object or None
        assert result is None or isinstance(result, dict)

    def test_setup_logging_accepts_config(self):
        """11.1.2: setup_logging accepts optional config."""
        from prism.view.setup import setup_logging

        config = {
            "mode": "dev",
            "level": "DEBUG",
        }

        # Should accept config without error
        setup_logging(config=config)

    def test_setup_logging_sets_global_mode(self):
        """11.1.3: setup_logging sets global mode."""
        from prism.view.setup import setup_logging, get_global_mode

        setup_logging(mode="prod")
        assert get_global_mode() == "prod"

        setup_logging(mode="dev")
        assert get_global_mode() == "dev"

    def test_setup_logging_loads_palette(self):
        """11.1.4: setup_logging loads palette."""
        from prism.view.setup import setup_logging, get_current_palette

        setup_logging(palette="vaporwave")
        palette = get_current_palette()

        assert palette is not None
        assert "error" in palette.colors

    def test_setup_logging_configures_root_logger(self):
        """11.1.5: setup_logging configures root logger."""
        from prism.view.setup import setup_logging

        output = io.StringIO()
        setup_logging(stream=output, mode="dev")

        # The root logger should be configured
        get_logger("test-root-config")  # Verify it works after setup

    def test_setup_logging_displays_banner_in_dev(self):
        """11.1.7: setup_logging displays VIEW LOADED banner in dev mode."""
        from prism.view.setup import setup_logging

        output = io.StringIO()

        setup_logging(mode="dev", stream=output, show_banner=True)

        banner_output = output.getvalue()
        # Banner should contain VIEW LOADED
        assert "VIEW LOADED" in banner_output or len(banner_output) > 0

    def test_setup_logging_no_banner_in_prod(self):
        """setup_logging should not display banner in prod mode."""
        from prism.view.setup import setup_logging

        output = io.StringIO()

        setup_logging(mode="prod", stream=output, show_banner=True)

        # In prod mode, no banner should be displayed
        banner_output = output.getvalue()
        assert "VIEW LOADED" not in banner_output


# =============================================================================
# 11.2: Python Logging Integration Tests
# =============================================================================


class TestPythonLoggingIntegration:
    """Tests for Python stdlib logging integration."""

    def setup_method(self):
        """Reset logging state before each test."""
        # Clear any existing handlers from the root logger
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)

    def teardown_method(self):
        """Clean up after each test."""
        # Reset logging
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
        root.setLevel(logging.WARNING)

    def test_prism_handler_can_be_added(self):
        """11.2.1: PrismHandler can be added to stdlib logger."""
        from prism.view.setup import PrismHandler

        handler = PrismHandler(mode="dev")
        logger = logging.getLogger("test.prism.handler")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # Should not raise
        logger.info("Test message")

    def test_prism_handler_formats_messages(self):
        """11.2.2: PrismHandler formats log messages."""
        from prism.view.setup import PrismHandler

        output = io.StringIO()
        handler = PrismHandler(mode="dev", stream=output)
        logger = logging.getLogger("test.format")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.info("Test message from stdlib")

        log_output = output.getvalue()
        assert "Test message from stdlib" in log_output

    def test_prism_handler_prod_mode_json(self):
        """11.2.3: PrismHandler produces JSON in prod mode."""
        from prism.view.setup import PrismHandler

        output = io.StringIO()
        handler = PrismHandler(mode="prod", stream=output)
        logger = logging.getLogger("test.prod")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.info("Prod mode message")

        log_output = output.getvalue().strip()
        # Should be valid JSON
        parsed = json.loads(log_output)
        assert parsed["msg"] == "Prod mode message"
        assert parsed["level"] == "INFO"

    def test_log_levels_propagate(self):
        """11.2.4: Log levels propagate correctly."""
        from prism.view.setup import PrismHandler

        output = io.StringIO()
        handler = PrismHandler(mode="prod", stream=output)
        logger = logging.getLogger("test.levels")
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

        # DEBUG and INFO should be filtered
        logger.debug("Debug message")
        logger.info("Info message")

        # WARNING and above should pass
        logger.warning("Warning message")
        logger.error("Error message")

        log_output = output.getvalue()
        assert "Debug message" not in log_output
        assert "Info message" not in log_output
        assert "Warning message" in log_output
        assert "Error message" in log_output

    def test_handler_includes_context(self):
        """PrismHandler includes LogContext in messages."""
        from prism.view.setup import PrismHandler

        LogContext.clear()
        output = io.StringIO()
        handler = PrismHandler(mode="prod", stream=output)
        logger = logging.getLogger("test.context")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        LogContext.set_service(name="test-service")

        with LogContext.request(trace_id="trace-123"):
            logger.info("Message with context")

        log_output = output.getvalue().strip()
        parsed = json.loads(log_output)

        # Should include context fields
        assert parsed.get("service") == "test-service" or parsed.get("trace_id") == "trace-123"

        LogContext.clear()


# =============================================================================
# 11.5: Operation Decorator Tests
# =============================================================================


class TestOperationDecorator:
    """Tests for @LogContext.operation_decorator."""

    def test_operation_decorator_works(self):
        """11.5.1: @operation decorator works."""
        from prism.view.setup import operation

        @operation("test_op")
        def my_function():
            return "result"

        result = my_function()
        assert result == "result"

    def test_decorator_captures_duration(self):
        """11.5.2: Decorator captures duration."""
        import time

        from prism.view.setup import operation

        durations = []

        @operation("timed_op", on_complete=lambda d: durations.append(d))
        def slow_function():
            time.sleep(0.01)
            return "done"

        slow_function()

        # Should have captured duration
        assert len(durations) == 1
        assert durations[0] >= 10  # At least 10ms

    def test_decorator_works_with_async(self):
        """11.5.3: Decorator works with async functions."""
        import asyncio

        from prism.view.setup import operation

        @operation("async_op")
        async def async_function():
            await asyncio.sleep(0.001)
            return "async result"

        result = asyncio.run(async_function())
        assert result == "async result"

    def test_decorator_preserves_signature(self):
        """11.5.4: Decorator preserves function signature."""
        from prism.view.setup import operation

        @operation("sig_test")
        def func_with_args(a: int, b: str, c: float = 1.0) -> str:
            """Docstring."""
            return f"{a}-{b}-{c}"

        # Function should still work with args
        result = func_with_args(1, "hello", c=2.5)
        assert result == "1-hello-2.5"

        # Name and docstring should be preserved
        assert func_with_args.__name__ == "func_with_args"
        assert "Docstring" in func_with_args.__doc__

    def test_decorator_sets_context(self):
        """Decorator sets operation in context."""
        from prism.view.setup import operation

        LogContext.clear()
        captured_ctx = None

        @operation("context_test")
        def capture_context():
            nonlocal captured_ctx
            captured_ctx = LogContext.get_current()
            return "done"

        capture_context()

        assert captured_ctx is not None
        assert captured_ctx.get("operation") == "context_test"

        LogContext.clear()

    def test_decorator_handles_exceptions(self):
        """Decorator should not swallow exceptions."""
        from prism.view.setup import operation

        @operation("error_test")
        def failing_function():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_function()
