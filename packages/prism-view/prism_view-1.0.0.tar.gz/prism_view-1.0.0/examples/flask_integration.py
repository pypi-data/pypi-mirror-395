"""
Flask integration example for prism-view.

This example shows how to integrate prism-view with Flask for:
- Automatic request context (trace_id, user_id)
- Structured logging
- Exception formatting
- Trace ID propagation in responses

Usage:
    pip install flask
    python examples/flask_integration.py

Example requests:
    curl http://localhost:5000/
    curl http://localhost:5000/users/123
    curl http://localhost:5000/error
"""

import uuid
from functools import wraps
from typing import Optional

from prism.view import (
    ExceptionFormatter,
    LogContext,
    PrismError,
    get_logger,
    handle_exception,
)
from prism.view.setup import setup_logging

# Try to import Flask, provide helpful message if not installed
try:
    from flask import Flask, g, jsonify, request
except ImportError:
    print("Flask not installed. Run: pip install flask")
    raise


# =============================================================================
# Custom Error Classes
# =============================================================================


class NotFoundError(PrismError):
    """Resource not found."""

    code = (404, "HTTP", "NOT_FOUND")
    category = "HTTP"
    severity = "WARNING"


class ValidationError(PrismError):
    """Validation failed."""

    code = (400, "HTTP", "VALIDATION_ERROR")
    category = "HTTP"
    severity = "WARNING"


class InternalError(PrismError):
    """Internal server error."""

    code = (500, "HTTP", "INTERNAL_ERROR")
    category = "HTTP"
    severity = "ERROR"
    retryable = True
    max_retries = 3


# =============================================================================
# Initialize prism-view
# =============================================================================

setup_logging(mode="dev", show_banner=True)

# Set service context (once at startup)
LogContext.set_service(
    name="flask-example",
    version="1.0.0",
    environment="development",
)

# Create logger
logger = get_logger("flask-example")


# =============================================================================
# Flask App
# =============================================================================

app = Flask(__name__)


# =============================================================================
# Request Hooks (Context Management)
# =============================================================================


@app.before_request
def before_request():
    """
    Set up prism-view context before each request.

    This hook:
    1. Generates or extracts trace_id
    2. Stores context info in Flask's g object
    3. Sets up LogContext
    """
    # Generate or extract trace_id
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    g.trace_id = trace_id

    # Extract user_id from auth header if present
    user_id = request.headers.get("X-User-ID")
    g.user_id = user_id

    # Enter request context (stored in g for cleanup)
    g.request_context = LogContext.request(
        trace_id=trace_id,
        method=request.method,
        path=request.path,
    )
    g.request_context.__enter__()

    # Enter user context if available
    if user_id:
        g.user_context = LogContext.user(user_id=user_id)
        g.user_context.__enter__()
    else:
        g.user_context = None

    logger.info("Request started")


@app.after_request
def after_request(response):
    """
    Clean up context and add headers after each request.
    """
    # Add trace_id to response headers
    response.headers["X-Trace-ID"] = g.get("trace_id", "unknown")

    logger.info("Request completed", status=response.status_code)

    # Exit contexts
    if g.get("user_context"):
        g.user_context.__exit__(None, None, None)

    if g.get("request_context"):
        g.request_context.__exit__(None, None, None)

    return response


@app.teardown_request
def teardown_request(exception):
    """
    Clean up on request teardown (including errors).
    """
    if exception:
        logger.error("Request failed with exception", exc=exception)

    # Ensure contexts are cleaned up even on error
    if g.get("user_context"):
        try:
            g.user_context.__exit__(type(exception), exception, None)
        except Exception:
            pass

    if g.get("request_context"):
        try:
            g.request_context.__exit__(type(exception), exception, None)
        except Exception:
            pass


# =============================================================================
# Error Handlers
# =============================================================================


@app.errorhandler(PrismError)
def handle_prism_error(exc: PrismError):
    """
    Handle PrismError exceptions.

    Formats the error using prism-view and returns a JSON response.
    """
    logger.error("PrismError occurred", exc=exc)

    # Determine status code from error code
    status_code = 500
    if exc.code:
        error_num = exc.code[0]
        if 400 <= error_num < 600:
            status_code = error_num

    return (
        jsonify(
            {
                "error": {
                    "type": type(exc).__name__,
                    "message": exc.message,
                    "code": exc.get_error_code(),
                    "details": exc.details,
                    "suggestions": exc.suggestions,
                    "docs_url": exc.get_docs_url(),
                },
                "trace_id": g.get("trace_id"),
            }
        ),
        status_code,
    )


@app.errorhandler(Exception)
def handle_generic_error(exc: Exception):
    """Handle unexpected exceptions."""
    logger.error("Unexpected error", exc=exc)

    return (
        jsonify(
            {
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                "trace_id": g.get("trace_id"),
            }
        ),
        500,
    )


# =============================================================================
# Routes
# =============================================================================


@app.route("/")
def root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return jsonify(
        {
            "message": "Hello from Flask + prism-view!",
            "trace_id": g.get("trace_id"),
        }
    )


@app.route("/users/<user_id>")
def get_user(user_id: str):
    """Get user by ID."""
    logger.info("Fetching user", target_user_id=user_id)

    # Simulate user lookup
    if user_id == "not-found":
        raise NotFoundError(
            f"User {user_id} not found",
            details={"user_id": user_id},
            suggestions=["Check the user ID", "User may have been deleted"],
        )

    return jsonify(
        {
            "user_id": user_id,
            "name": f"User {user_id}",
            "trace_id": g.get("trace_id"),
        }
    )


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    data = request.get_json() or {}
    name = data.get("name", "")

    logger.info("Creating user", name=name)

    if not name:
        raise ValidationError(
            "Name is required",
            details={"field": "name"},
            suggestions=["Provide a non-empty name"],
        )

    return jsonify(
        {
            "user_id": str(uuid.uuid4()),
            "name": name,
            "trace_id": g.get("trace_id"),
        }
    )


@app.route("/error")
def trigger_error():
    """Endpoint that triggers an error (for testing)."""
    logger.warning("About to trigger intentional error")

    raise InternalError(
        "This is an intentional error for testing",
        details={"test": True},
        suggestions=["This is expected behavior", "No action needed"],
    )


@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


# =============================================================================
# Decorator for operation tracking
# =============================================================================


def track_operation(operation_name: str):
    """
    Decorator to track operation duration with prism-view.

    Example:
        @app.route("/slow")
        @track_operation("slow_operation")
        def slow_endpoint():
            time.sleep(1)
            return {"status": "done"}
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with LogContext.operation(operation_name):
                return f(*args, **kwargs)

        return wrapper

    return decorator


# =============================================================================
# Run with: python examples/flask_integration.py
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
