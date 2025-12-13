"""
Tests for Logger Implementation (Iteration 5).

Tests cover:
- Basic Logger structure (instantiation, log methods)
- Logger factory (get_logger, caching)
- Context integration (automatic LogContext inclusion)
- Dev mode formatting (pretty output, colors, emojis)
- Error logging (PrismError handling)
- Child loggers (with_context)
"""


class TestLoggerBasicStructure:
    """Tests for basic Logger instantiation and methods."""

    def test_logger_can_be_instantiated_with_name(self):
        """Logger can be created with a name."""
        from prism.view.logger import Logger

        logger = Logger("test-logger")
        assert logger.name == "test-logger"

    def test_logger_has_info_method(self):
        """Logger has info() method."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert hasattr(logger, "info")
        assert callable(logger.info)

    def test_logger_has_error_method(self):
        """Logger has error() method."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert hasattr(logger, "error")
        assert callable(logger.error)

    def test_logger_has_warn_method(self):
        """Logger has warn() method."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert hasattr(logger, "warn")
        assert callable(logger.warn)

    def test_logger_has_debug_method(self):
        """Logger has debug() method."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert hasattr(logger, "debug")
        assert callable(logger.debug)

    def test_logger_has_critical_method(self):
        """Logger has critical() method."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert hasattr(logger, "critical")
        assert callable(logger.critical)

    def test_logger_info_logs_message(self, capsys):
        """Logger.info() outputs the message."""
        from prism.view.logger import Logger

        logger = Logger("test")
        logger.info("Hello, world!")

        captured = capsys.readouterr()
        assert "Hello, world!" in captured.out or "Hello, world!" in captured.err

    def test_logger_accepts_extra_kwargs(self, capsys):
        """Logger methods accept extra keyword arguments."""
        from prism.view.logger import Logger

        logger = Logger("test")
        logger.info("User action", user_id="user-123", action="login")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "User action" in output

    def test_logger_default_level_is_debug(self):
        """Logger default level is DEBUG (logs everything)."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert logger.level == "DEBUG"

    def test_logger_can_set_level(self):
        """Logger level can be set."""
        from prism.view.logger import Logger

        logger = Logger("test", level="WARNING")
        assert logger.level == "WARNING"

    def test_logger_respects_level_filtering(self, capsys):
        """Logger respects level filtering."""
        from prism.view.logger import Logger

        logger = Logger("test", level="WARNING")
        logger.debug("Debug message")  # Should be filtered
        logger.info("Info message")  # Should be filtered
        logger.warn("Warning message")  # Should appear

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "Debug message" not in output
        assert "Info message" not in output
        assert "Warning message" in output


class TestLoggerFactory:
    """Tests for get_logger() factory function."""

    def test_get_logger_returns_logger_instance(self):
        """get_logger() returns a Logger instance."""
        from prism.view.logger import Logger, get_logger

        logger = get_logger("my-service")
        assert isinstance(logger, Logger)

    def test_get_logger_caches_loggers(self):
        """get_logger() returns the same instance for the same name."""
        from prism.view.logger import get_logger

        logger1 = get_logger("cached-logger")
        logger2 = get_logger("cached-logger")
        assert logger1 is logger2

    def test_get_logger_different_names_different_instances(self):
        """get_logger() returns different instances for different names."""
        from prism.view.logger import get_logger

        logger1 = get_logger("logger-a")
        logger2 = get_logger("logger-b")
        assert logger1 is not logger2

    def test_get_logger_accepts_level(self):
        """get_logger() accepts level parameter."""
        from prism.view.logger import get_logger

        logger = get_logger("leveled-logger", level="ERROR")
        assert logger.level == "ERROR"


class TestContextIntegration:
    """Tests for automatic LogContext integration."""

    def test_logger_includes_service_context(self, capsys):
        """Logger automatically includes service context."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.clear()
        LogContext.set_service(name="payment-api", version="1.0.0")

        logger = Logger("test")
        logger.info("Processing payment")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "payment-api" in output or "service" in output.lower()

    def test_logger_includes_trace_id(self, capsys):
        """Logger includes trace_id from request context."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.clear()
        with LogContext.request(trace_id="trace-abc-123"):
            logger = Logger("test")
            logger.info("Request received")

            captured = capsys.readouterr()
            output = captured.out + captured.err
            assert "trace-abc-123" in output

    def test_logger_includes_user_id(self, capsys):
        """Logger includes user_id from user context."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.clear()
        with LogContext.user(user_id="user-456"):
            logger = Logger("test")
            logger.info("User action")

            captured = capsys.readouterr()
            output = captured.out + captured.err
            assert "user-456" in output

    def test_logger_includes_operation_context(self, capsys):
        """Logger includes operation context with duration."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.clear()
        with LogContext.operation(name="db_query", table="users"):
            logger = Logger("test")
            logger.info("Query executed")

            captured = capsys.readouterr()
            output = captured.out + captured.err
            assert "db_query" in output or "operation" in output.lower()

    def test_logger_merges_kwargs_with_context(self, capsys):
        """Logger merges extra kwargs with LogContext."""
        from prism.view import LogContext
        from prism.view.logger import Logger

        LogContext.clear()
        LogContext.set_service(name="api")

        logger = Logger("test")
        logger.info("Event", custom_field="custom_value")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "custom_value" in output


class TestDevModeFormatting:
    """Tests for dev mode (pretty) formatting."""

    def test_dev_mode_uses_pretty_formatting(self, capsys):
        """Dev mode uses human-readable formatting."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("Pretty message")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Should not be JSON (no leading brace)
        assert not output.strip().startswith("{")

    def test_dev_mode_includes_level_indicator(self, capsys):
        """Dev mode includes level indicator."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("Test message")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Should include INFO indicator
        assert "INFO" in output.upper() or "ℹ" in output

    def test_dev_mode_includes_timestamp(self, capsys):
        """Dev mode includes timestamp."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("Test message")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Should include time-like pattern (HH:MM or timestamp)
        assert ":" in output  # Time separator

    def test_dev_mode_includes_logger_name(self, capsys):
        """Dev mode includes logger name."""
        from prism.view.logger import Logger

        logger = Logger("my-service", mode="dev")
        logger.info("Test message")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "my-service" in output

    def test_dev_mode_formats_extra_fields(self, capsys):
        """Dev mode formats extra fields nicely."""
        from prism.view.logger import Logger

        logger = Logger("test", mode="dev")
        logger.info("Event", count=42, status="active")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "42" in output
        assert "active" in output

    def test_dev_mode_is_default(self):
        """Dev mode is the default mode."""
        from prism.view.logger import Logger

        logger = Logger("test")
        assert logger.mode == "dev"


class TestErrorLogging:
    """Tests for error logging with PrismError."""

    def test_logger_error_accepts_prism_error(self, capsys):
        """Logger.error() accepts PrismError instance."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test")

        class PaymentError(PrismError):
            code = (1001, "PAY", "PAYMENT_FAILED")

        error = PaymentError("Payment declined")
        logger.error("Payment failed", exc=error)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "Payment declined" in output or "PAYMENT_FAILED" in output

    def test_logger_error_includes_error_code(self, capsys):
        """Logger.error() includes error code."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test")

        class ConfigError(PrismError):
            code = (1, "CFG", "CONFIG_MISSING")

        error = ConfigError("Config file not found")
        logger.error("Configuration error", exc=error)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "CFG" in output or "CONFIG_MISSING" in output

    def test_logger_error_includes_suggestions(self, capsys):
        """Logger.error() includes suggestions from PrismError."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test")

        error = PrismError(
            "Connection failed",
            suggestions=["Check network connection", "Verify credentials"],
        )
        logger.error("Database error", exc=error)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "Check network" in output or "suggestion" in output.lower()

    def test_logger_error_includes_cause_chain(self, capsys):
        """Logger.error() includes cause chain."""
        from prism.view import PrismError
        from prism.view.logger import Logger

        logger = Logger("test")

        root = ValueError("Invalid port number")
        error = PrismError("Connection failed", cause=root)
        logger.error("Network error", exc=error)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "ValueError" in output or "Invalid port" in output

    def test_logger_error_accepts_standard_exception(self, capsys):
        """Logger.error() accepts standard Python exceptions."""
        from prism.view.logger import Logger

        logger = Logger("test")

        try:
            raise ValueError("Something went wrong")
        except ValueError as e:
            logger.error("An error occurred", exc=e)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "Something went wrong" in output or "ValueError" in output

    def test_logger_error_without_exception(self, capsys):
        """Logger.error() works without exception parameter."""
        from prism.view.logger import Logger

        logger = Logger("test")
        logger.error("An error message")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "An error message" in output


class TestChildLoggers:
    """Tests for child loggers with bound context."""

    def test_with_context_creates_child_logger(self):
        """with_context() creates a new logger instance."""
        from prism.view.logger import Logger

        parent = Logger("parent")
        child = parent.with_context(request_id="req-123")

        assert child is not parent
        assert isinstance(child, Logger)

    def test_child_logger_inherits_name(self):
        """Child logger inherits parent's name."""
        from prism.view.logger import Logger

        parent = Logger("my-service")
        child = parent.with_context(request_id="req-123")

        assert child.name == parent.name

    def test_child_logger_inherits_level(self):
        """Child logger inherits parent's level."""
        from prism.view.logger import Logger

        parent = Logger("test", level="WARNING")
        child = parent.with_context(request_id="req-123")

        assert child.level == parent.level

    def test_child_logger_includes_bound_context(self, capsys):
        """Child logger includes bound context in logs."""
        from prism.view.logger import Logger

        parent = Logger("test")
        child = parent.with_context(request_id="req-abc", user_id="user-xyz")
        child.info("Processing request")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "req-abc" in output
        assert "user-xyz" in output

    def test_child_logger_merges_context(self, capsys):
        """Child logger merges bound context with log kwargs."""
        from prism.view.logger import Logger

        parent = Logger("test")
        child = parent.with_context(request_id="req-123")
        child.info("Event", action="click")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "req-123" in output
        assert "click" in output

    def test_parent_logger_unchanged(self, capsys):
        """Parent logger is unchanged by child context."""
        from prism.view.logger import Logger

        parent = Logger("test")
        parent.with_context(request_id="child-only")  # Create child (not used directly)

        parent.info("Parent log")
        captured = capsys.readouterr()
        parent_output = captured.out + captured.err

        # Parent should not have child's context
        assert "child-only" not in parent_output

    def test_nested_child_loggers(self, capsys):
        """Child loggers can be nested."""
        from prism.view.logger import Logger

        root = Logger("test")
        child1 = root.with_context(level1="a")
        child2 = child1.with_context(level2="b")

        child2.info("Nested log")

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "level1" in output or "a" in output
        assert "level2" in output or "b" in output


class TestLogLevels:
    """Tests for log level constants and ordering."""

    def test_log_levels_exist(self):
        """Log level constants exist."""
        from prism.view.logger import LogLevel

        assert hasattr(LogLevel, "DEBUG")
        assert hasattr(LogLevel, "INFO")
        assert hasattr(LogLevel, "WARNING")
        assert hasattr(LogLevel, "ERROR")
        assert hasattr(LogLevel, "CRITICAL")

    def test_log_levels_are_ordered(self):
        """Log levels have correct ordering."""
        from prism.view.logger import LogLevel

        assert LogLevel.DEBUG < LogLevel.INFO
        assert LogLevel.INFO < LogLevel.WARNING
        assert LogLevel.WARNING < LogLevel.ERROR
        assert LogLevel.ERROR < LogLevel.CRITICAL
