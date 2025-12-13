"""
Basic logging example for prism-view.

This example demonstrates:
- Creating a logger with get_logger()
- Logging at different levels (debug, info, warn, error, critical)
- Dev mode vs prod mode output
- Adding context to log messages

Usage:
    python examples/01_basic_logging.py
"""

from prism.view import get_logger, setup_logging

# Initialize prism-view (shows the VIEW LOADED banner)
setup_logging(mode="dev", show_banner=True)

# Get a logger
logger = get_logger("my-app")

# Basic logging at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warn("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

print("\n--- Logging with context ---\n")

# Logging with additional context
logger.info("User logged in", user_id="user-123", ip_address="192.168.1.1")
logger.info("Payment processed", amount=99.99, currency="USD", order_id="order-456")

print("\n--- Child logger with bound context ---\n")

# Create a child logger with bound context
request_logger = logger.with_context(request_id="req-abc", session_id="sess-xyz")
request_logger.info("Handling request")
request_logger.info("Request completed", status=200)

print("\n--- Prod mode logging (JSON output) ---\n")

# Switch to prod mode for JSON output
prod_logger = get_logger("my-app-prod")
prod_logger.mode = "prod"

prod_logger.info("User logged in", user_id="user-123")
prod_logger.error("Payment failed", error_code="E-PAY-001")
