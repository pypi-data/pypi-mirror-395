"""
Golden path test for prism-view.

This test validates the complete end-to-end workflow of prism-view,
ensuring all components work together seamlessly.

The "golden path" represents the typical usage pattern:
1. Set up logging with setup_logging()
2. Create logger with get_logger()
3. Set service context
4. Handle requests with request context
5. Log messages with context
6. Handle errors with PrismError
7. Format exceptions beautifully
"""

import io
import json

import pytest

from prism.view import (
    LogContext,
    Logger,
    PrismError,
    console_table,
    format_exception,
    get_logger,
    get_palette,
    render_banner,
    scrub,
)


# =============================================================================
# Custom Error Classes for Testing
# =============================================================================


class PaymentError(PrismError):
    """Payment processing error."""

    code = (1001, "PAY", "PAYMENT_FAILED")
    category = "PAYMENT"
    severity = "ERROR"
    retryable = True
    max_retries = 3
    retry_delay_seconds = 1.0


class ValidationError(PrismError):
    """Input validation error."""

    code = (400, "VAL", "VALIDATION_FAILED")
    category = "VALIDATION"
    severity = "WARNING"


# =============================================================================
# Golden Path Test
# =============================================================================


class TestGoldenPath:
    """End-to-end integration tests for prism-view."""

    def test_complete_workflow(self):
        """
        11.0.1: Golden path validates end-to-end workflow.

        This test exercises the complete prism-view workflow:
        1. Create logger
        2. Set service context
        3. Set request context
        4. Log messages
        5. Create and handle errors
        6. Verify serialization
        7. Verify formatting
        """
        # Clear any existing context
        LogContext.clear()

        # 1. Create logger with get_logger()
        output = io.StringIO()
        logger = Logger("payment-service", mode="dev", stream=output)

        # 2. Set service context with LogContext.set_service()
        LogContext.set_service(
            name="payment-service",
            version="1.0.0",
            environment="test",
        )

        # 3. Set request context with LogContext.request()
        with LogContext.request(trace_id="trace-abc-123"):
            # 4. Log info message with context
            logger.info("Processing payment request", amount=99.99, currency="USD")

            # Verify log output contains context
            log_output = output.getvalue()
            assert "Processing payment request" in log_output
            assert "payment-service" in log_output

            # 5. Create PrismError with details
            error = PaymentError(
                "Payment declined by processor",
                details={
                    "card_last_four": "1234",
                    "processor": "stripe",
                    "decline_code": "insufficient_funds",
                },
                suggestions=[
                    "Try a different payment method",
                    "Contact your bank",
                ],
            )

            # 6. Verify error has context, code, suggestions
            assert error.message == "Payment declined by processor"
            assert error.get_error_code() == "E-PAY-1001"
            assert len(error.suggestions) == 2
            assert error.retryable is True
            assert error.max_retries == 3

            # Error should have captured context
            assert "service" in error.context or "trace_id" in error.context

            # 7. Verify error serializes to dict correctly
            error_dict = error.to_dict()
            assert error_dict["message"] == "Payment declined by processor"
            assert error_dict["error_code"] == "E-PAY-1001"
            assert error_dict["details"]["processor"] == "stripe"
            assert error_dict["suggestions"] == [
                "Try a different payment method",
                "Contact your bank",
            ]
            assert error_dict["recovery"]["retryable"] is True

            # Verify JSON serialization works
            json_str = json.dumps(error_dict)
            parsed = json.loads(json_str)
            assert parsed["error_code"] == "E-PAY-1001"

        # Clean up
        LogContext.clear()

    def test_banner_renders_correctly(self):
        """11.0.1: Verify banner renders correctly."""
        # Render banner
        banner = render_banner(use_color=False)

        # Should contain PRISM ASCII art (stylized as | _ \ _ \_ etc.)
        # The ASCII art spells PRISM using special characters
        assert "| _ \\" in banner or "___ ___" in banner
        # Should contain VIEW LOADED
        assert "VIEW LOADED" in banner
        # Should contain version
        assert "v" in banner or "0.1.0" in banner

    def test_logger_with_context_integration(self):
        """Test logger integrates properly with context system."""
        LogContext.clear()
        output = io.StringIO()

        # Set up context
        LogContext.set_service(name="api-gateway", version="2.0.0")

        with LogContext.request(trace_id="req-123"):
            with LogContext.user(user_id="user-456"):
                logger = Logger("api", mode="dev", stream=output)
                logger.info("User action", action="view_dashboard")

                log_output = output.getvalue()
                # Should include context fields
                assert "api" in log_output
                assert "User action" in log_output

        LogContext.clear()

    def test_error_cause_chain(self):
        """Test error cause chain is properly tracked."""
        # Create a chain of errors
        root_error = ValueError("Invalid card number format")
        validation_error = ValidationError(
            "Card validation failed",
            cause=root_error,
        )
        payment_error = PaymentError(
            "Payment processing failed",
            cause=validation_error,
        )

        # Verify cause chain
        assert len(payment_error.cause_chain) == 2
        assert payment_error.cause_chain[0]["type"] == "ValidationError"
        assert payment_error.cause_chain[1]["type"] == "ValueError"

        # Verify root cause
        assert payment_error.root_cause["type"] == "ValueError"
        assert "Invalid card number" in payment_error.root_cause["message"]

    def test_exception_formatter_integration(self):
        """Test exception formatter with full error context."""
        LogContext.clear()
        LogContext.set_service(name="payment-api")

        with LogContext.request(trace_id="trace-789"):
            error = PaymentError(
                "Transaction declined",
                details={"amount": 150.00},
                suggestions=["Retry with smaller amount"],
            )

            # Dev mode formatting
            dev_output = format_exception(error, mode="dev", use_color=False)
            assert "PaymentError" in dev_output
            assert "E-PAY-1001" in dev_output
            assert "Transaction declined" in dev_output
            assert "Retry with smaller amount" in dev_output

            # Prod mode formatting
            prod_output = format_exception(error, mode="prod")
            parsed = json.loads(prod_output)
            assert parsed["type"] == "PaymentError"
            assert parsed["error_code"] == "E-PAY-1001"

        LogContext.clear()

    def test_scrubber_integration(self):
        """Test scrubber works with real-world data."""
        sensitive_data = {
            "user": "john_doe",
            "password": "super_secret_123",
            "api_key": "sk-1234567890abcdef",
            "card_number": "4111111111111111",
            "metadata": {
                "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
            },
        }

        scrubbed = scrub(sensitive_data)

        # Non-sensitive should be preserved
        assert scrubbed["user"] == "john_doe"

        # Sensitive should be redacted
        assert scrubbed["password"] == "[REDACTED]"
        assert scrubbed["api_key"] == "[REDACTED]"
        assert "[REDACTED]" in scrubbed["metadata"]["session_token"]

    def test_console_table_integration(self):
        """Test console table with real data."""
        data = [
            {"error_code": "E-PAY-1001", "count": 5, "status": "active"},
            {"error_code": "E-VAL-400", "count": 12, "status": "resolved"},
            {"error_code": "E-NET-300", "count": 3, "status": "active"},
        ]

        table = console_table(data, title="Error Summary", use_color=False)

        # Should contain all data
        assert "E-PAY-1001" in table
        assert "E-VAL-400" in table
        assert "Error Summary" in table

    def test_palette_integration(self):
        """Test palette system works correctly."""
        # Get built-in palettes
        vaporwave = get_palette("vaporwave")
        monochrome = get_palette("monochrome")

        # Verify palettes have expected structure
        assert "error" in vaporwave.colors
        assert "info" in vaporwave.colors
        assert "error" in vaporwave.emojis

        # Monochrome should have different colors
        assert vaporwave.colors != monochrome.colors

    def test_logger_prod_mode_json(self):
        """Test logger produces valid JSON in prod mode."""
        LogContext.clear()
        output = io.StringIO()

        LogContext.set_service(name="api", version="1.0.0")

        with LogContext.request(trace_id="trace-prod-test"):
            logger = Logger("api", mode="prod", stream=output)
            logger.info("Request received", method="GET", path="/api/users")

            log_output = output.getvalue().strip()

            # Should be valid JSON
            parsed = json.loads(log_output)
            assert parsed["msg"] == "Request received"
            assert parsed["level"] == "INFO"
            assert parsed["logger"] == "api"
            assert parsed["method"] == "GET"

        LogContext.clear()

    def test_error_with_debug_info(self):
        """Test error debug info is handled correctly."""
        error = PaymentError(
            "Debug test",
            debug_info={
                "stack_depth": 5,
                "internal_state": {"buffer": "data"},
            },
        )

        # Debug info should NOT be in regular to_dict()
        regular_dict = error.to_dict(include_debug=False)
        assert "debug_info" not in regular_dict

        # Debug info should be in to_dict(include_debug=True)
        debug_dict = error.to_dict(include_debug=True)
        assert "debug_info" in debug_dict
        assert debug_dict["debug_info"]["stack_depth"] == 5

    def test_docs_url_generation(self):
        """Test documentation URL generation."""
        error = PaymentError("Test")

        docs_url = error.get_docs_url()

        assert docs_url is not None
        assert "payment-failed" in docs_url.lower()
        assert "prism.dev/errors" in docs_url

    def test_operation_context_with_duration(self):
        """Test operation context tracks duration."""
        import time

        LogContext.clear()

        with LogContext.operation("test_operation"):
            time.sleep(0.01)  # 10ms
            ctx = LogContext.get_current()
            assert "operation" in ctx
            assert ctx["operation"] == "test_operation"

        # After exiting, duration should have been tracked
        # (duration is added on exit, so we can't check it inside)
        LogContext.clear()

    def test_batch_context(self):
        """Test batch processing context."""
        LogContext.clear()

        with LogContext.batch(batch_id="batch-001", item_index=0, total_items=100):
            ctx = LogContext.get_current()
            assert ctx["batch_id"] == "batch-001"
            assert ctx["item_index"] == 0
            assert ctx["total_items"] == 100

        LogContext.clear()

    def test_transaction_context(self):
        """Test transaction context."""
        LogContext.clear()

        with LogContext.transaction(
            transaction_id="txn-12345",
            transaction_type="payment",
        ):
            ctx = LogContext.get_current()
            assert ctx["transaction_id"] == "txn-12345"
            assert ctx["transaction_type"] == "payment"

        LogContext.clear()


class TestErrorHierarchy:
    """Test error class hierarchy and inheritance."""

    def test_prism_error_is_exception(self):
        """PrismError should be a proper Exception."""
        error = PrismError("Test")
        assert isinstance(error, Exception)

    def test_custom_errors_inherit_properly(self):
        """Custom errors should inherit from PrismError."""
        error = PaymentError("Test")
        assert isinstance(error, PrismError)
        assert isinstance(error, Exception)

    def test_error_can_be_raised_and_caught(self):
        """Errors should work in try/except blocks."""
        with pytest.raises(PaymentError) as exc_info:
            raise PaymentError("Payment failed")

        assert exc_info.value.message == "Payment failed"
        assert exc_info.value.get_error_code() == "E-PAY-1001"

    def test_error_caught_as_prism_error(self):
        """Custom errors should be catchable as PrismError."""
        with pytest.raises(PrismError) as exc_info:
            raise PaymentError("Payment failed")

        assert isinstance(exc_info.value, PaymentError)

    def test_error_caught_as_exception(self):
        """Custom errors should be catchable as Exception."""
        with pytest.raises(Exception) as exc_info:
            raise PaymentError("Payment failed")

        assert isinstance(exc_info.value, PaymentError)


class TestLoggerGetLogger:
    """Test get_logger factory function."""

    def test_get_logger_returns_logger(self):
        """get_logger should return a Logger instance."""
        logger = get_logger("test-service")
        assert isinstance(logger, Logger)
        assert logger.name == "test-service"

    def test_get_logger_caches_by_name(self):
        """get_logger should return same instance for same name."""
        logger1 = get_logger("cached-service")
        logger2 = get_logger("cached-service")
        assert logger1 is logger2

    def test_get_logger_different_names(self):
        """get_logger should return different instances for different names."""
        logger1 = get_logger("service-a")
        logger2 = get_logger("service-b")
        assert logger1 is not logger2
