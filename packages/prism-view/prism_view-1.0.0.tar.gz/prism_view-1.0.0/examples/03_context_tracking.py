"""
Context tracking example for prism-view.

This example demonstrates:
- Setting service context (global)
- Request context with trace_id
- User context with user_id
- Session and transaction contexts
- Operation context with duration tracking
- Context nesting and merging

Usage:
    python examples/03_context_tracking.py
"""

import time

from prism.view import LogContext, get_logger, setup_logging

# Initialize
setup_logging(mode="dev", show_banner=False)
logger = get_logger("context-demo")


# =============================================================================
# Service Context (Global)
# =============================================================================

print("=== Service Context ===\n")

# Set service-level context (typically done once at startup)
LogContext.set_service(
    name="order-service",
    version="2.1.0",
    environment="development",
    region="us-west-2",
)

logger.info("Service started")
print(f"Current context: {LogContext.get_current()}\n")


# =============================================================================
# Request Context
# =============================================================================

print("=== Request Context ===\n")

with LogContext.request(trace_id="abc-123-def", method="POST", path="/orders"):
    logger.info("Request received")

    # Add custom fields to current context
    LogContext.add(ip_address="192.168.1.100")

    logger.info("Processing order", order_id="order-789")
    print(f"Context in request: {LogContext.get_current()}\n")

# Outside request - trace_id is gone
logger.info("Between requests")
print(f"Context after request: {LogContext.get_current()}\n")


# =============================================================================
# User Context
# =============================================================================

print("=== User Context ===\n")

with LogContext.request(trace_id="xyz-456"):
    with LogContext.user(user_id="user-123", email="alice@example.com", role="admin"):
        logger.info("User authenticated")
        print(f"Context with user: {LogContext.get_current()}\n")


# =============================================================================
# Session and Transaction Contexts
# =============================================================================

print("=== Session & Transaction Context ===\n")

with LogContext.request(trace_id="sess-demo"):
    with LogContext.session(session_id="sess-abc-123", device="mobile"):
        logger.info("Session active")

        with LogContext.transaction(
            transaction_id="txn-001",
            transaction_type="payment",
            amount=99.99,
            currency="USD",
        ):
            logger.info("Processing transaction")
            print(f"Full context: {LogContext.get_current()}\n")


# =============================================================================
# Batch Context
# =============================================================================

print("=== Batch Context ===\n")

items = ["item-1", "item-2", "item-3"]

with LogContext.request(trace_id="batch-demo"):
    for i, item in enumerate(items):
        with LogContext.batch(
            batch_id="batch-001",
            item_index=i,
            total_items=len(items),
        ):
            logger.info(f"Processing {item}")

    logger.info("Batch complete")


# =============================================================================
# Operation Context (with timing)
# =============================================================================

print("\n=== Operation Context (with timing) ===\n")

with LogContext.request(trace_id="op-demo"):
    with LogContext.operation("database_query", table="orders") as op:
        logger.info("Starting query")
        time.sleep(0.1)  # Simulate work
        logger.info("Query complete")

    # After context exits, duration_ms is available
    print(f"Operation took {op['duration_ms']:.2f}ms\n")

    with LogContext.operation("api_call", endpoint="https://api.example.com") as op:
        time.sleep(0.05)
    print(f"API call took {op['duration_ms']:.2f}ms\n")


# =============================================================================
# Context Capture in Errors
# =============================================================================

print("=== Context Capture in Errors ===\n")

from prism.view import PrismError

class OrderError(PrismError):
    code = (500, "ORD", "ORDER_FAILED")
    category = "ORDER"
    severity = "ERROR"

with LogContext.request(trace_id="error-demo"):
    with LogContext.user(user_id="user-456"):
        # Error automatically captures current context
        error = OrderError(
            "Failed to process order",
            details={"order_id": "ord-789"},
        )

        print("Error context:", error.context)
        print("Error location:", error.location)


# Clean up
LogContext.clear()
