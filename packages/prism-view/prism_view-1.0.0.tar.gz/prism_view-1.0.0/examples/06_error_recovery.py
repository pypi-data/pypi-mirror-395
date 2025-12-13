"""
Error recovery example for prism-view.

This example demonstrates:
- Retryable errors with max_retries and retry_delay
- Error cause chains
- Recovery hints and suggestions
- Using error metadata for retry logic
- Implementing retry decorators

Usage:
    python examples/06_error_recovery.py
"""

import random
import time
from functools import wraps
from typing import Callable, TypeVar

from prism.view import (
    ErrorCategory,
    ErrorSeverity,
    PrismError,
    get_logger,
    setup_logging,
)

setup_logging(mode="dev", show_banner=False)
logger = get_logger("error-recovery")


# =============================================================================
# Retryable Error Classes
# =============================================================================


class NetworkError(PrismError):
    """Network connectivity error."""

    code = (5001, "NET", "NETWORK_ERROR")
    category = ErrorCategory.NETWORK
    severity = ErrorSeverity.ERROR
    retryable = True
    max_retries = 3
    retry_delay = 1.0  # seconds


class RateLimitError(PrismError):
    """API rate limit exceeded."""

    code = (429, "API", "RATE_LIMITED")
    category = ErrorCategory.EXTERNAL
    severity = ErrorSeverity.WARNING
    retryable = True
    max_retries = 5
    retry_delay = 2.0  # Longer delay for rate limits


class DatabaseError(PrismError):
    """Database connection error."""

    code = (5002, "DB", "DATABASE_ERROR")
    category = ErrorCategory.DATA
    severity = ErrorSeverity.ERROR
    retryable = True
    max_retries = 3
    retry_delay = 0.5


class ValidationError(PrismError):
    """Validation error - not retryable."""

    code = (4001, "VAL", "VALIDATION_FAILED")
    category = ErrorCategory.VALIDATION
    severity = ErrorSeverity.WARNING
    retryable = False  # No point retrying validation errors


# =============================================================================
# Basic Retry Logic
# =============================================================================

print("=== Basic Retry Logic ===\n")


def fetch_data_with_retry():
    """Fetch data with manual retry logic."""
    error = NetworkError(
        "Connection timeout",
        details={"host": "api.example.com", "timeout": 30},
        suggestions=["Check network connectivity", "Verify firewall rules"],
    )

    for attempt in range(1, error.max_retries + 1):
        try:
            logger.info(f"Attempt {attempt}/{error.max_retries}")

            # Simulate random failures
            if random.random() < 0.7:
                raise error

            logger.info("Success!")
            return {"data": "fetched"}

        except NetworkError as e:
            logger.warning(
                f"Attempt {attempt} failed",
                error=str(e),
                retryable=e.retryable,
                attempts_remaining=e.max_retries - attempt,
            )

            if attempt < e.max_retries:
                logger.info(f"Retrying in {e.retry_delay}s...")
                time.sleep(e.retry_delay)
            else:
                logger.error("All retries exhausted")
                raise


try:
    result = fetch_data_with_retry()
    print(f"Result: {result}\n")
except NetworkError:
    print("Failed after all retries\n")


# =============================================================================
# Retry Decorator
# =============================================================================

print("=== Retry Decorator ===\n")

T = TypeVar("T")


def with_retry(
    exceptions: tuple = (PrismError,),
    max_retries: int = None,
    delay: float = None,
    backoff: float = 2.0,
):
    """
    Decorator that retries a function on failure.

    Args:
        exceptions: Tuple of exception types to catch and retry
        max_retries: Override max_retries from exception (if None, uses exception's value)
        delay: Override retry_delay from exception (if None, uses exception's value)
        backoff: Multiplier for exponential backoff (default 2.0)

    Example:
        @with_retry(exceptions=(NetworkError, DatabaseError))
        def fetch_user(user_id):
            return api.get_user(user_id)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay

            # Default max_retries if not specified
            retries = max_retries or 3

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    # Get retry settings from exception if available
                    if hasattr(e, "retryable") and not e.retryable:
                        logger.warning(
                            "Error is not retryable, failing immediately",
                            error=type(e).__name__,
                        )
                        raise

                    exc_max_retries = getattr(e, "max_retries", retries)
                    exc_delay = getattr(e, "retry_delay", 1.0)

                    # Use exception's settings if not overridden
                    actual_retries = max_retries or exc_max_retries
                    actual_delay = current_delay or exc_delay

                    if attempt < actual_retries:
                        logger.warning(
                            f"Retry {attempt}/{actual_retries}",
                            error=str(e),
                            next_delay=actual_delay,
                        )
                        time.sleep(actual_delay)
                        current_delay = (current_delay or exc_delay) * backoff
                    else:
                        logger.error(
                            "All retries exhausted",
                            error=str(e),
                            total_attempts=attempt,
                        )

            raise last_exception

        return wrapper

    return decorator


# Example usage of the retry decorator
@with_retry(exceptions=(NetworkError, RateLimitError))
def call_external_api():
    """Simulated API call that might fail."""
    if random.random() < 0.6:
        raise NetworkError("Connection refused")
    return {"status": "ok"}


try:
    result = call_external_api()
    print(f"API Result: {result}\n")
except PrismError as e:
    print(f"API call failed: {e.message}\n")


# =============================================================================
# Error Cause Chains
# =============================================================================

print("=== Error Cause Chains ===\n")


def low_level_operation():
    """Simulate a low-level failure."""
    raise ConnectionError("TCP connection reset by peer")


def database_query():
    """Simulate a database operation that fails due to network issues."""
    try:
        low_level_operation()
    except ConnectionError as e:
        raise DatabaseError(
            "Failed to execute query",
            details={"query": "SELECT * FROM users", "database": "main"},
            cause=e,
        )


def get_user(user_id: str):
    """Get user from database."""
    try:
        database_query()
    except DatabaseError as e:
        raise NetworkError(
            f"Could not fetch user {user_id}",
            details={"user_id": user_id, "operation": "get_user"},
            suggestions=[
                "Check database connectivity",
                "Verify network configuration",
                "Check if database is running",
            ],
            cause=e,
        )


try:
    get_user("user-123")
except NetworkError as e:
    print("Error occurred with cause chain:")
    print(f"  Error: {e.message}")
    print(f"  Details: {e.details}")
    print(f"  Cause: {e.cause}")

    # Get root cause
    root = e.get_root_cause()
    print(f"  Root cause: {root}")

    # Get full cause chain
    chain = e.get_cause_chain()
    print(f"  Cause chain ({len(chain)} levels):")
    for i, cause in enumerate(chain):
        print(f"    {i + 1}. {type(cause).__name__}: {cause}")

    # Check recovery options
    print(f"\n  Retryable: {e.retryable}")
    print(f"  Max retries: {e.max_retries}")
    print(f"  Retry delay: {e.retry_delay}s")
    print(f"  Suggestions: {e.suggestions}")


# =============================================================================
# Recovery Hints in Formatted Output
# =============================================================================

print("\n=== Recovery Hints in Formatted Output ===\n")

from prism.view import format_exception

error = RateLimitError(
    "API rate limit exceeded",
    details={
        "limit": 100,
        "current": 150,
        "reset_at": "2024-01-15T10:30:00Z",
    },
    suggestions=[
        "Wait for rate limit to reset",
        "Reduce request frequency",
        "Consider upgrading API tier",
    ],
)

# Format for dev mode (shows recovery hints prominently)
print("Dev mode output:")
print(format_exception(error, mode="dev"))

# Format for prod mode (includes recovery in JSON)
print("\nProd mode output (JSON):")
print(format_exception(error, mode="prod"))


# =============================================================================
# Implementing Circuit Breaker Pattern
# =============================================================================

print("\n=== Circuit Breaker Pattern ===\n")


class CircuitBreaker:
    """
    Simple circuit breaker implementation using PrismError.

    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Circuit tripped, requests fail fast
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                logger.info("Circuit half-open, testing...")
                self.state = "HALF_OPEN"
            else:
                raise NetworkError(
                    "Circuit breaker is OPEN",
                    details={
                        "failures": self.failures,
                        "reset_in": self.reset_timeout
                        - (time.time() - self.last_failure_time),
                    },
                    suggestions=["Wait for circuit to reset", "Check service health"],
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call."""
        if self.state == "HALF_OPEN":
            logger.info("Circuit closed - service recovered")
        self.failures = 0
        self.state = "CLOSED"

    def _on_failure(self):
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(
                "Circuit opened",
                failures=self.failures,
                threshold=self.failure_threshold,
            )


# Example usage
breaker = CircuitBreaker(failure_threshold=2, reset_timeout=5.0)


def unreliable_service():
    """Simulate an unreliable service."""
    if random.random() < 0.8:
        raise NetworkError("Service unavailable")
    return "success"


for i in range(5):
    try:
        result = breaker.call(unreliable_service)
        print(f"Call {i + 1}: {result}")
    except NetworkError as e:
        print(f"Call {i + 1}: Failed - {e.message}")
        if "Circuit breaker" in e.message:
            print(f"  (failing fast due to circuit breaker)")
    time.sleep(0.5)
