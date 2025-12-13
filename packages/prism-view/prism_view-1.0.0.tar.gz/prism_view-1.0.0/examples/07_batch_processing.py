"""
Batch processing example for prism-view.

This example demonstrates:
- Batch context for tracking multi-item operations
- Progress logging within batches
- Error handling in batch operations
- Aggregating results and statistics
- Transaction context for related operations

Usage:
    python examples/07_batch_processing.py
"""

import random
import time
from dataclasses import dataclass
from typing import List, Optional

from prism.view import (
    ErrorCategory,
    ErrorSeverity,
    LogContext,
    PrismError,
    get_logger,
    setup_logging,
)

setup_logging(mode="dev", show_banner=False)
logger = get_logger("batch-processor")


# =============================================================================
# Custom Errors for Batch Processing
# =============================================================================


class BatchError(PrismError):
    """Base error for batch processing."""

    code = (6001, "BATCH", "BATCH_ERROR")
    category = ErrorCategory.PROCESSING
    severity = ErrorSeverity.ERROR


class ItemProcessingError(BatchError):
    """Error processing a single item in a batch."""

    code = (6002, "BATCH", "ITEM_ERROR")
    severity = ErrorSeverity.WARNING
    retryable = True
    max_retries = 2


class BatchValidationError(BatchError):
    """Batch validation failed."""

    code = (6003, "BATCH", "VALIDATION_ERROR")
    severity = ErrorSeverity.WARNING
    retryable = False


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class Order:
    """Sample order for processing."""

    id: str
    customer_id: str
    amount: float
    items: List[str]


@dataclass
class ProcessingResult:
    """Result of processing a single item."""

    order_id: str
    success: bool
    error: Optional[str] = None
    duration_ms: Optional[float] = None


# =============================================================================
# Basic Batch Processing
# =============================================================================

print("=== Basic Batch Processing ===\n")


def process_order(order: Order) -> ProcessingResult:
    """Process a single order."""
    start = time.time()

    # Simulate processing with random failures
    if random.random() < 0.2:
        raise ItemProcessingError(
            f"Failed to process order {order.id}",
            details={"order_id": order.id, "amount": order.amount},
            suggestions=["Retry the operation", "Check order data"],
        )

    # Simulate processing time
    time.sleep(random.uniform(0.05, 0.15))

    duration = (time.time() - start) * 1000
    return ProcessingResult(order_id=order.id, success=True, duration_ms=duration)


def process_batch(orders: List[Order], batch_id: str) -> dict:
    """Process a batch of orders with context tracking."""
    results = []
    errors = []

    # Use batch context for the entire operation
    with LogContext.batch(batch_id=batch_id, total_items=len(orders)):
        logger.info("Starting batch processing", order_count=len(orders))

        for i, order in enumerate(orders):
            # Track progress within the batch
            with LogContext.operation(f"process_order_{order.id}"):
                try:
                    logger.debug(
                        f"Processing item {i + 1}/{len(orders)}",
                        order_id=order.id,
                        customer=order.customer_id,
                    )

                    result = process_order(order)
                    results.append(result)

                    logger.info(
                        "Order processed",
                        order_id=order.id,
                        duration_ms=f"{result.duration_ms:.2f}",
                    )

                except ItemProcessingError as e:
                    errors.append({"order_id": order.id, "error": str(e)})
                    results.append(
                        ProcessingResult(
                            order_id=order.id, success=False, error=str(e)
                        )
                    )
                    logger.warning("Order processing failed", order_id=order.id, error=str(e))

        # Log batch summary
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        logger.info(
            "Batch processing complete",
            total=len(orders),
            successful=successful,
            failed=failed,
            success_rate=f"{successful / len(orders) * 100:.1f}%",
        )

    return {
        "batch_id": batch_id,
        "total": len(orders),
        "successful": successful,
        "failed": failed,
        "results": results,
        "errors": errors,
    }


# Create sample orders
orders = [
    Order(id=f"ORD-{i:04d}", customer_id=f"CUST-{i % 10:03d}", amount=random.uniform(10, 500), items=["item1", "item2"])
    for i in range(10)
]

# Process the batch
summary = process_batch(orders, batch_id="BATCH-001")
print(f"\nBatch Summary: {summary['successful']}/{summary['total']} successful\n")


# =============================================================================
# Nested Batch Processing (Chunked)
# =============================================================================

print("=== Chunked Batch Processing ===\n")


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split list into chunks."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def process_large_batch(orders: List[Order], batch_id: str, chunk_size: int = 5) -> dict:
    """Process a large batch in chunks."""
    chunks = chunk_list(orders, chunk_size)
    all_results = []
    all_errors = []

    with LogContext.batch(batch_id=batch_id, total_items=len(orders)):
        logger.info(
            "Starting chunked batch processing",
            total_orders=len(orders),
            chunks=len(chunks),
            chunk_size=chunk_size,
        )

        for chunk_idx, chunk in enumerate(chunks):
            chunk_id = f"{batch_id}-CHUNK-{chunk_idx + 1:03d}"

            # Nested batch context for the chunk
            with LogContext.batch(batch_id=chunk_id, total_items=len(chunk)):
                logger.info(
                    f"Processing chunk {chunk_idx + 1}/{len(chunks)}",
                    chunk_id=chunk_id,
                    items=len(chunk),
                )

                for order in chunk:
                    try:
                        result = process_order(order)
                        all_results.append(result)
                    except ItemProcessingError as e:
                        all_errors.append({"order_id": order.id, "chunk": chunk_id, "error": str(e)})
                        all_results.append(ProcessingResult(order_id=order.id, success=False, error=str(e)))

                chunk_success = sum(1 for r in all_results[-len(chunk) :] if r.success)
                logger.info(
                    f"Chunk complete",
                    chunk_id=chunk_id,
                    successful=chunk_success,
                    failed=len(chunk) - chunk_success,
                )

        successful = sum(1 for r in all_results if r.success)
        logger.info(
            "Large batch complete",
            total=len(orders),
            successful=successful,
            failed=len(orders) - successful,
        )

    return {
        "batch_id": batch_id,
        "total": len(orders),
        "successful": successful,
        "chunks_processed": len(chunks),
        "errors": all_errors,
    }


# Process a larger batch in chunks
large_orders = [
    Order(id=f"ORD-{i:04d}", customer_id=f"CUST-{i % 20:03d}", amount=random.uniform(10, 1000), items=["item1"])
    for i in range(25)
]

result = process_large_batch(large_orders, batch_id="LARGE-BATCH-001", chunk_size=5)
print(f"\nLarge Batch: {result['successful']}/{result['total']} in {result['chunks_processed']} chunks\n")


# =============================================================================
# Transaction Context
# =============================================================================

print("=== Transaction Context ===\n")


def transfer_funds(from_account: str, to_account: str, amount: float, transaction_id: str):
    """Simulate a fund transfer with transaction context."""
    with LogContext.transaction(transaction_id=transaction_id):
        logger.info(
            "Starting fund transfer",
            from_account=from_account,
            to_account=to_account,
            amount=amount,
        )

        # Step 1: Validate accounts
        with LogContext.operation("validate_accounts"):
            logger.debug("Validating accounts")
            time.sleep(0.05)  # Simulate validation

        # Step 2: Debit source account
        with LogContext.operation("debit_source"):
            logger.debug("Debiting source account", account=from_account, amount=amount)
            time.sleep(0.05)  # Simulate debit

            if random.random() < 0.1:
                raise BatchError(
                    "Insufficient funds",
                    details={"account": from_account, "requested": amount},
                )

        # Step 3: Credit destination account
        with LogContext.operation("credit_destination"):
            logger.debug("Crediting destination account", account=to_account, amount=amount)
            time.sleep(0.05)  # Simulate credit

        # Step 4: Record transaction
        with LogContext.operation("record_transaction"):
            logger.debug("Recording transaction")
            time.sleep(0.02)

        logger.info(
            "Fund transfer complete",
            transaction_id=transaction_id,
            from_account=from_account,
            to_account=to_account,
            amount=amount,
        )

        return {"transaction_id": transaction_id, "status": "completed"}


# Execute some transfers
transfers = [
    ("ACC-001", "ACC-002", 100.00),
    ("ACC-003", "ACC-004", 250.50),
    ("ACC-002", "ACC-005", 75.25),
]

for i, (from_acc, to_acc, amount) in enumerate(transfers):
    txn_id = f"TXN-{i + 1:06d}"
    try:
        result = transfer_funds(from_acc, to_acc, amount, txn_id)
        print(f"Transfer {txn_id}: {result['status']}")
    except BatchError as e:
        print(f"Transfer {txn_id}: FAILED - {e.message}")


# =============================================================================
# Batch with Session Context
# =============================================================================

print("\n=== Batch with Session Context ===\n")


def process_user_uploads(user_id: str, session_id: str, files: List[str]):
    """Process file uploads within a user session."""
    # Set up user and session context
    with LogContext.user(user_id=user_id):
        with LogContext.session(session_id=session_id):
            batch_id = f"UPLOAD-{session_id[:8]}"

            with LogContext.batch(batch_id=batch_id, total_items=len(files)):
                logger.info("Starting file upload batch", file_count=len(files))

                results = []
                for filename in files:
                    with LogContext.operation(f"upload_{filename}"):
                        logger.debug("Processing file", filename=filename)
                        time.sleep(0.05)  # Simulate upload

                        # Random failure
                        if random.random() < 0.15:
                            logger.warning("File upload failed", filename=filename)
                            results.append({"file": filename, "status": "failed"})
                        else:
                            logger.info("File uploaded", filename=filename)
                            results.append({"file": filename, "status": "success"})

                successful = sum(1 for r in results if r["status"] == "success")
                logger.info(
                    "Upload batch complete",
                    total=len(files),
                    successful=successful,
                    failed=len(files) - successful,
                )

                return results


# Simulate user upload session
files = ["document.pdf", "image.png", "data.csv", "report.xlsx", "notes.txt"]
results = process_user_uploads(
    user_id="USER-12345",
    session_id="SESSION-abc123def456",
    files=files,
)

successful = sum(1 for r in results if r["status"] == "success")
print(f"\nUpload Results: {successful}/{len(files)} files uploaded successfully")
