"""
Tests for PrismError base class.

Verifies the extensible error base class works correctly.
"""

import pytest
from datetime import datetime, timezone


class TestPrismErrorBasic:
    """Basic tests for PrismError instantiation."""

    def test_can_instantiate_with_message(self):
        """PrismError should accept a message."""
        from prism.view.errors import PrismError

        error = PrismError("Something went wrong")
        assert error.message == "Something went wrong"
        assert str(error) == "Something went wrong"

    def test_stores_details_dict(self):
        """PrismError should store details dictionary."""
        from prism.view.errors import PrismError

        error = PrismError("Validation failed", details={"field": "email", "value": "invalid"})
        assert error.details == {"field": "email", "value": "invalid"}

    def test_stores_suggestions_list(self):
        """PrismError should store suggestions list."""
        from prism.view.errors import PrismError

        error = PrismError("File not found", suggestions=["Check the path", "Verify file exists"])
        assert error.suggestions == ["Check the path", "Verify file exists"]

    def test_default_details_is_empty_dict(self):
        """Details should default to empty dict."""
        from prism.view.errors import PrismError

        error = PrismError("Error")
        assert error.details == {}

    def test_default_suggestions_is_empty_list(self):
        """Suggestions should default to empty list."""
        from prism.view.errors import PrismError

        error = PrismError("Error")
        assert error.suggestions == []

    def test_has_timestamp(self):
        """PrismError should have a timestamp."""
        from prism.view.errors import PrismError

        before = datetime.now(timezone.utc)
        error = PrismError("Error")
        after = datetime.now(timezone.utc)

        assert hasattr(error, "timestamp")
        assert isinstance(error.timestamp, datetime)
        assert before <= error.timestamp <= after

    def test_is_exception(self):
        """PrismError should be an Exception."""
        from prism.view.errors import PrismError

        error = PrismError("Error")
        assert isinstance(error, Exception)

    def test_can_be_raised(self):
        """PrismError should be raisable."""
        from prism.view.errors import PrismError

        with pytest.raises(PrismError) as exc_info:
            raise PrismError("Test error")

        assert exc_info.value.message == "Test error"


class TestPrismErrorClassAttributes:
    """Tests for PrismError class-level attributes."""

    def test_has_code_attribute(self):
        """PrismError should have code class attribute."""
        from prism.view.errors import PrismError

        assert hasattr(PrismError, "code")
        assert PrismError.code is None  # Default is None

    def test_has_category_attribute(self):
        """PrismError should have category class attribute."""
        from prism.view.errors import PrismError

        assert hasattr(PrismError, "category")
        assert PrismError.category is None  # Default is None

    def test_has_severity_attribute(self):
        """PrismError should have severity class attribute."""
        from prism.view.errors import PrismError

        assert hasattr(PrismError, "severity")
        assert PrismError.severity is None  # Default is None

    def test_subclass_can_override_code(self):
        """Subclass should be able to override code."""
        from prism.view.errors import PrismError

        class CustomError(PrismError):
            code = (100, "CUSTOM", "CUSTOM_ERROR")

        error = CustomError("Custom error")
        assert error.code == (100, "CUSTOM", "CUSTOM_ERROR")

    def test_subclass_can_override_category(self):
        """Subclass should be able to override category."""
        from prism.view.errors import PrismError

        class CustomError(PrismError):
            category = "CUSTOM"

        error = CustomError("Custom error")
        assert error.category == "CUSTOM"

    def test_subclass_can_override_severity(self):
        """Subclass should be able to override severity."""
        from prism.view.errors import PrismError, ErrorSeverity

        class CustomError(PrismError):
            severity = ErrorSeverity.WARNING

        error = CustomError("Custom error")
        assert error.severity == ErrorSeverity.WARNING


class TestPrismErrorToDict:
    """Tests for PrismError.to_dict() method."""

    def test_to_dict_returns_dict(self):
        """to_dict() should return a dictionary."""
        from prism.view.errors import PrismError

        error = PrismError("Test error")
        result = error.to_dict()

        assert isinstance(result, dict)

    def test_to_dict_includes_message(self):
        """to_dict() should include message."""
        from prism.view.errors import PrismError

        error = PrismError("Test error")
        result = error.to_dict()

        assert "message" in result
        assert result["message"] == "Test error"

    def test_to_dict_includes_details(self):
        """to_dict() should include details."""
        from prism.view.errors import PrismError

        error = PrismError("Error", details={"key": "value"})
        result = error.to_dict()

        assert "details" in result
        assert result["details"] == {"key": "value"}

    def test_to_dict_includes_suggestions(self):
        """to_dict() should include suggestions."""
        from prism.view.errors import PrismError

        error = PrismError("Error", suggestions=["Try this"])
        result = error.to_dict()

        assert "suggestions" in result
        assert result["suggestions"] == ["Try this"]

    def test_to_dict_includes_timestamp(self):
        """to_dict() should include timestamp as ISO string."""
        from prism.view.errors import PrismError

        error = PrismError("Error")
        result = error.to_dict()

        assert "timestamp" in result
        assert isinstance(result["timestamp"], str)
        # Should be parseable as ISO format
        datetime.fromisoformat(result["timestamp"].replace("Z", "+00:00"))

    def test_to_dict_includes_code(self):
        """to_dict() should include error code."""
        from prism.view.errors import PrismError

        class CustomError(PrismError):
            code = (100, "TEST", "TEST_ERROR")

        error = CustomError("Error")
        result = error.to_dict()

        assert "code" in result
        assert result["code"] == "TEST_ERROR"

    def test_to_dict_includes_error_code_formatted(self):
        """to_dict() should include formatted error_code."""
        from prism.view.errors import PrismError, ErrorSeverity

        class CustomError(PrismError):
            code = (100, "TEST", "TEST_ERROR")
            severity = ErrorSeverity.ERROR

        error = CustomError("Error")
        result = error.to_dict()

        assert "error_code" in result
        assert "TEST" in result["error_code"]
        assert "100" in result["error_code"]

    def test_to_dict_includes_category(self):
        """to_dict() should include category."""
        from prism.view.errors import PrismError

        class CustomError(PrismError):
            category = "CUSTOM"

        error = CustomError("Error")
        result = error.to_dict()

        assert "category" in result
        assert result["category"] == "CUSTOM"

    def test_to_dict_includes_severity(self):
        """to_dict() should include severity."""
        from prism.view.errors import PrismError, ErrorSeverity

        class CustomError(PrismError):
            severity = ErrorSeverity.ERROR

        error = CustomError("Error")
        result = error.to_dict()

        assert "severity" in result
        assert result["severity"] == "ERROR"

    def test_to_dict_includes_exception_type(self):
        """to_dict() should include exception_type."""
        from prism.view.errors import PrismError

        class CustomError(PrismError):
            pass

        error = CustomError("Error")
        result = error.to_dict()

        assert "exception_type" in result
        assert result["exception_type"] == "CustomError"


class TestPrismErrorCause:
    """Tests for PrismError cause handling."""

    def test_accepts_cause_parameter(self):
        """PrismError should accept cause parameter."""
        from prism.view.errors import PrismError

        original = ValueError("Original error")
        error = PrismError("Wrapped error", cause=original)

        assert error.cause is original

    def test_default_cause_is_none(self):
        """Cause should default to None."""
        from prism.view.errors import PrismError

        error = PrismError("Error")
        assert error.cause is None

    def test_cause_in_to_dict(self):
        """to_dict() should include cause info if present."""
        from prism.view.errors import PrismError

        original = ValueError("Original error")
        error = PrismError("Wrapped error", cause=original)
        result = error.to_dict()

        # Should have some indication of cause
        assert "cause" in result or "original_error" in result


class TestPrismErrorExtensibility:
    """Tests for PrismError extensibility."""

    def test_custom_error_with_all_attributes(self):
        """Custom error should support all attributes."""
        from prism.view.errors import PrismError, ErrorSeverity

        class PaymentError(PrismError):
            code = (1001, "PAY", "PAYMENT_FAILED")
            category = "PAYMENT"
            severity = ErrorSeverity.ERROR

        error = PaymentError(
            "Payment failed",
            details={"transaction_id": "tx-123"},
            suggestions=["Retry payment", "Use different card"],
        )

        assert error.message == "Payment failed"
        assert error.code == (1001, "PAY", "PAYMENT_FAILED")
        assert error.category == "PAYMENT"
        assert error.severity == ErrorSeverity.ERROR
        assert error.details == {"transaction_id": "tx-123"}
        assert error.suggestions == ["Retry payment", "Use different card"]

    def test_custom_error_serializes_correctly(self):
        """Custom error should serialize with to_dict()."""
        from prism.view.errors import PrismError, ErrorSeverity

        class PaymentError(PrismError):
            code = (1001, "PAY", "PAYMENT_FAILED")
            category = "PAYMENT"
            severity = ErrorSeverity.ERROR

        error = PaymentError("Payment failed", details={"transaction_id": "tx-123"})

        result = error.to_dict()

        assert result["message"] == "Payment failed"
        assert result["code"] == "PAYMENT_FAILED"
        assert result["category"] == "PAYMENT"
        assert result["severity"] == "ERROR"
        assert result["details"] == {"transaction_id": "tx-123"}
        assert result["exception_type"] == "PaymentError"
