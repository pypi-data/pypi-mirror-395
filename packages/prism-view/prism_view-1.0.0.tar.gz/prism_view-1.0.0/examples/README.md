# prism-view Examples

This directory contains working examples demonstrating prism-view features.

## Examples

| Example | Description |
|---------|-------------|
| [01_basic_logging.py](01_basic_logging.py) | Getting started with logging, log levels, dev/prod modes |
| [02_custom_errors.py](02_custom_errors.py) | Creating custom error classes with codes, categories, and recovery hints |
| [03_context_tracking.py](03_context_tracking.py) | Using LogContext for request, user, session, and operation tracking |
| [04_secret_scrubbing.py](04_secret_scrubbing.py) | Automatic PII/secret redaction with Scrubber |
| [05_custom_palette.py](05_custom_palette.py) | Color themes, emojis, and box drawing characters |
| [06_error_recovery.py](06_error_recovery.py) | Retry logic, circuit breakers, and error cause chains |
| [07_batch_processing.py](07_batch_processing.py) | Batch context, chunked processing, and transaction tracking |

## Framework Integrations

| Example | Description |
|---------|-------------|
| [fastapi_middleware.py](fastapi_middleware.py) | FastAPI integration with middleware and error handlers |
| [flask_integration.py](flask_integration.py) | Flask integration with request hooks and error handlers |

## Running Examples

```bash
# Basic examples
python examples/01_basic_logging.py
python examples/02_custom_errors.py
python examples/03_context_tracking.py
python examples/04_secret_scrubbing.py
python examples/05_custom_palette.py
python examples/06_error_recovery.py
python examples/07_batch_processing.py

# Framework examples (requires framework installation)
pip install fastapi uvicorn
uvicorn examples.fastapi_middleware:app --reload

pip install flask
python examples/flask_integration.py
```

## Quick Start

```python
from prism.view import get_logger, setup_logging, PrismError

# Initialize prism-view
setup_logging(mode="dev")

# Create a logger
logger = get_logger("my-app")

# Log with context
logger.info("User logged in", user_id="user-123", ip="192.168.1.1")

# Create custom errors
class PaymentError(PrismError):
    code = (1001, "PAY", "PAYMENT_FAILED")
    retryable = True
    max_retries = 3

raise PaymentError("Payment declined", suggestions=["Try another card"])
```
