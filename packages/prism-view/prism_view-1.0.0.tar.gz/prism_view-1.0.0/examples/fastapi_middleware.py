"""
FastAPI middleware example for prism-view.

This example shows how to integrate prism-view with FastAPI for:
- Automatic request context (trace_id, user_id)
- Structured logging
- Exception formatting
- Trace ID propagation in responses

Usage:
    pip install fastapi uvicorn
    uvicorn examples.fastapi_middleware:app --reload

Example requests:
    curl http://localhost:8000/
    curl http://localhost:8000/users/123
    curl http://localhost:8000/error
"""

import uuid
from typing import Optional

from prism.view import (
    ExceptionFormatter,
    LogContext,
    PrismError,
    get_logger,
    handle_exception,
)
from prism.view.setup import setup_logging

# Try to import FastAPI, provide helpful message if not installed
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except ImportError:
    print("FastAPI not installed. Run: pip install fastapi uvicorn")
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
    name="fastapi-example",
    version="1.0.0",
    environment="development",
)

# Create logger
logger = get_logger("fastapi-example")


# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(
    title="FastAPI + prism-view Example",
    description="Demonstrates prism-view integration with FastAPI",
    version="1.0.0",
)


# =============================================================================
# Middleware
# =============================================================================


@app.middleware("http")
async def prism_context_middleware(request: Request, call_next):
    """
    Middleware to set up prism-view context for each request.

    This middleware:
    1. Generates or extracts trace_id
    2. Sets up request context
    3. Logs request start/end
    4. Adds trace_id to response headers
    """
    # Generate or extract trace_id
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())

    # Extract user_id from auth header if present (simplified example)
    user_id = _extract_user_id(request)

    # Set up request context
    with LogContext.request(trace_id=trace_id, method=request.method, path=str(request.url.path)):
        # Add user context if available
        if user_id:
            with LogContext.user(user_id=user_id):
                response = await _handle_request(request, call_next)
        else:
            response = await _handle_request(request, call_next)

        # Add trace_id to response headers
        response.headers["X-Trace-ID"] = trace_id

        return response


async def _handle_request(request: Request, call_next):
    """Handle the request with logging."""
    logger.info("Request started")

    try:
        response = await call_next(request)
        logger.info("Request completed", status=response.status_code)
        return response
    except Exception as e:
        logger.error("Request failed", exc=e)
        raise


def _extract_user_id(request: Request) -> Optional[str]:
    """
    Extract user ID from request.

    In a real application, this would decode a JWT token
    or check session data.
    """
    # Simplified: check for X-User-ID header
    return request.headers.get("X-User-ID")


# =============================================================================
# Exception Handlers
# =============================================================================


@app.exception_handler(PrismError)
async def prism_error_handler(request: Request, exc: PrismError):
    """
    Handle PrismError exceptions.

    Formats the error using prism-view and returns a JSON response.
    """
    logger.error("PrismError occurred", exc=exc)

    # Determine status code from error code
    status_code = 500
    if exc.code:
        error_num = exc.code[0]
        if 400 <= error_num < 500:
            status_code = error_num
        elif error_num >= 500:
            status_code = error_num

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": type(exc).__name__,
                "message": exc.message,
                "code": exc.get_error_code(),
                "details": exc.details,
                "suggestions": exc.suggestions,
                "docs_url": exc.get_docs_url(),
            },
            "trace_id": LogContext.get_current().get("trace_id"),
        },
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error("Unexpected error", exc=exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
            },
            "trace_id": LogContext.get_current().get("trace_id"),
        },
    )


# =============================================================================
# Routes
# =============================================================================


@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {
        "message": "Hello from FastAPI + prism-view!",
        "trace_id": LogContext.get_current().get("trace_id"),
    }


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID."""
    logger.info("Fetching user", target_user_id=user_id)

    # Simulate user lookup
    if user_id == "not-found":
        raise NotFoundError(
            f"User {user_id} not found",
            details={"user_id": user_id},
            suggestions=["Check the user ID", "User may have been deleted"],
        )

    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "trace_id": LogContext.get_current().get("trace_id"),
    }


@app.post("/users")
async def create_user(name: str = ""):
    """Create a new user."""
    logger.info("Creating user", name=name)

    if not name:
        raise ValidationError(
            "Name is required",
            details={"field": "name"},
            suggestions=["Provide a non-empty name"],
        )

    return {
        "user_id": str(uuid.uuid4()),
        "name": name,
        "trace_id": LogContext.get_current().get("trace_id"),
    }


@app.get("/error")
async def trigger_error():
    """Endpoint that triggers an error (for testing)."""
    logger.warning("About to trigger intentional error")

    raise InternalError(
        "This is an intentional error for testing",
        details={"test": True},
        suggestions=["This is expected behavior", "No action needed"],
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# =============================================================================
# Run with: uvicorn examples.fastapi_middleware:app --reload
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
