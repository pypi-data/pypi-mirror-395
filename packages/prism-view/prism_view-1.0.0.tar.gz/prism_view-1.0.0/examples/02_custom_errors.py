"""
Custom error classes example for prism-view.

This example demonstrates:
- Creating custom error classes with PrismError
- Using error codes, categories, and severity
- Adding suggestions and details
- Recovery hints (retryable errors)
- Documentation URLs

Usage:
    python examples/02_custom_errors.py
"""

from prism.view import PrismError, ErrorSeverity, format_exception


# =============================================================================
# Define Custom Error Classes
# =============================================================================


class PaymentError(PrismError):
    """Base class for payment-related errors."""

    category = "PAYMENT"


class PaymentDeclinedError(PaymentError):
    """Payment was declined by the payment processor."""

    code = (1001, "PAY", "PAYMENT_DECLINED")
    severity = "ERROR"
    retryable = True
    max_retries = 3
    retry_delay_seconds = 2.0


class InsufficientFundsError(PaymentError):
    """Account has insufficient funds for the transaction."""

    code = (1002, "PAY", "INSUFFICIENT_FUNDS")
    severity = "WARNING"
    retryable = False


class PaymentGatewayError(PaymentError):
    """Payment gateway is unavailable."""

    code = (1003, "PAY", "GATEWAY_ERROR")
    severity = "ERROR"
    retryable = True
    max_retries = 5
    retry_delay_seconds = 5.0


class ValidationError(PrismError):
    """Input validation failed."""

    code = (400, "VAL", "VALIDATION_FAILED")
    category = "VALIDATION"
    severity = "WARNING"


# =============================================================================
# Use the Custom Errors
# =============================================================================

print("=== Creating and formatting errors ===\n")

# Create a payment declined error
error = PaymentDeclinedError(
    "Payment was declined",
    details={
        "card_last_four": "4242",
        "decline_code": "card_declined",
        "amount": 99.99,
    },
    suggestions=[
        "Try a different payment method",
        "Contact your bank for more information",
        "Verify the card details are correct",
    ],
)

# Format and print the error (dev mode)
print(format_exception(error, mode="dev"))

print("\n" + "=" * 60 + "\n")

# Create a chained error (with cause)
try:
    raise ConnectionError("Could not connect to payment gateway")
except ConnectionError as e:
    gateway_error = PaymentGatewayError(
        "Payment gateway unavailable",
        cause=e,
        details={"gateway": "stripe", "region": "us-west"},
        suggestions=["Try again in a few minutes", "Check service status page"],
    )
    print(format_exception(gateway_error, mode="dev"))

print("\n" + "=" * 60 + "\n")

# Show error as dict (for JSON serialization)
validation_error = ValidationError(
    "Invalid email address",
    details={"field": "email", "value": "not-an-email"},
    suggestions=["Enter a valid email address like user@example.com"],
)

print("=== Error as dictionary (for JSON) ===\n")
import json
print(json.dumps(validation_error.to_dict(), indent=2))

print("\n=== Prod mode (single-line JSON) ===\n")
print(format_exception(validation_error, mode="prod"))
