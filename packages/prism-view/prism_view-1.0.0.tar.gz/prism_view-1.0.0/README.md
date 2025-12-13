# 👁️ Prism View

**Structured logging, error handling, and observability for Python applications.**

Part of [Project Prism](https://github.com/lukeudell/project-prism) - a cross-language platform engineering suite.

[![PyPI version](https://img.shields.io/pypi/v/prism-view.svg)](https://pypi.org/project/prism-view/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/lukeudell/prism-view/actions/workflows/test.yml/badge.svg)](https://github.com/lukeudell/prism-view/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is Prism View?

Prism View provides everything you need for production-ready logging and error handling:

- **Dual-mode logging** - Pretty terminal output (dev) vs structured JSON (prod)
- **Custom error taxonomy** - Define error codes, categories, and recovery hints
- **Context tracking** - Automatic trace IDs, user context, operation timing
- **Secret scrubbing** - Automatic PII/password redaction in logs
- **Framework integration** - Works with FastAPI, Flask, and standard library logging

---

## Installation

```bash
pip install prism-view
```

---

## Quick Start

### 1. Initialize Logging

```python
from prism.view import setup_logging, get_logger, LogContext

# Initialize (shows banner in dev mode)
setup_logging(mode="dev")

# Create a logger
logger = get_logger("my-app")

# Set service context (once at startup)
LogContext.set_service(name="my-app", version="1.0.0", environment="development")
```

### 2. Log with Context

```python
# Simple logging
logger.info("Server started", port=8080)
logger.warning("High memory usage", percent=85)
logger.error("Connection failed", host="db.example.com")

# With request context (trace_id auto-generated if not provided)
with LogContext.request(method="POST", path="/api/orders"):
    with LogContext.user(user_id="user-123"):
        logger.info("Processing order", order_id="ord-456")
        # Logs include: trace_id, user_id, method, path
```

### 3. Track Operation Duration

```python
with LogContext.operation("fetch_user_data"):
    # ... do work ...
    logger.info("Fetched user")  # Includes duration_ms automatically
```

---

## Custom Errors

Define errors with codes, categories, and recovery hints:

```python
from prism.view import PrismError, ErrorSeverity, ErrorCategory

class PaymentError(PrismError):
    """Payment processing failed."""
    code = (1001, "PAY", "PAYMENT_FAILED")
    category = ErrorCategory.EXTERNAL
    severity = ErrorSeverity.ERROR
    retryable = True
    max_retries = 3

# Raise with details and suggestions
raise PaymentError(
    "Card declined",
    details={"card_last4": "1234", "amount": 99.99},
    suggestions=["Try a different card", "Check card balance"]
)
```

Errors automatically capture:
- Current `LogContext` (trace_id, user_id, etc.)
- Stack location (file, line, function)
- Cause chain for nested exceptions
- Timestamp

---

## Dev vs Prod Mode

Set mode via environment variable or code:

```bash
export PRISM_LOG_MODE=prod  # or "dev"
```

```python
setup_logging(mode="prod")  # Explicit mode
```

**Dev mode** - Colorful, human-readable:
```
12:34:56.789 ℹ️ INFO    [my-app] Server started  | port=8080 trace_id=abc-123
```

**Prod mode** - Structured JSON for log aggregation:
```json
{"ts": "2025-01-15T12:34:56.789Z", "level": "INFO", "logger": "my-app", "msg": "Server started", "port": 8080, "trace_id": "abc-123"}
```

---

## Secret Scrubbing

Sensitive data is automatically redacted:

```python
from prism.view import scrub

data = {
    "username": "alice",
    "password": "secret123",  # Will be redacted
    "api_key": "sk_live_xxx",  # Will be redacted
    "config": {"db_password": "hunter2"}  # Nested - will be redacted
}

safe_data = scrub(data)
# {"username": "alice", "password": "[REDACTED]", "api_key": "[REDACTED]", ...}
```

The logger automatically scrubs all output. Built-in patterns detect:
- Passwords, secrets, tokens, API keys
- JWT tokens, Bearer tokens
- AWS access keys
- Credit card numbers

---

## Framework Integration

### FastAPI

```python
from fastapi import FastAPI, Request
from prism.view import setup_logging, get_logger, LogContext

app = FastAPI()
setup_logging(mode="dev")
logger = get_logger("api")

@app.middleware("http")
async def add_context(request: Request, call_next):
    with LogContext.request(method=request.method, path=request.url.path):
        return await call_next(request)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    logger.info("Fetching user", user_id=user_id)
    return {"user_id": user_id}
```

### Flask

```python
from flask import Flask, g
from prism.view import setup_logging, get_logger, LogContext

app = Flask(__name__)
setup_logging(mode="dev")
logger = get_logger("api")

@app.before_request
def before_request():
    g.ctx = LogContext.request(method=request.method, path=request.path)
    g.ctx.__enter__()

@app.teardown_request
def teardown_request(exc):
    if hasattr(g, 'ctx'):
        g.ctx.__exit__(None, None, None)
```

See [examples/](examples/) for complete integration examples.

---

## API Reference

### Logging

| Function | Description |
|----------|-------------|
| `setup_logging(mode, palette, show_banner)` | Initialize the logging system |
| `get_logger(name)` | Get a logger instance |
| `Logger.info/debug/warning/error/critical()` | Log at various levels |
| `Logger.with_context(**kwargs)` | Create child logger with bound context |

### Context

| Function | Description |
|----------|-------------|
| `LogContext.set_service(name, version, ...)` | Set global service context |
| `LogContext.request(trace_id, method, ...)` | Request-scoped context |
| `LogContext.user(user_id, ...)` | User-scoped context |
| `LogContext.operation(name)` | Operation with duration tracking |
| `LogContext.batch(batch_id, total_items)` | Batch processing context |
| `LogContext.get_current()` | Get merged current context |

### Errors

| Class/Function | Description |
|----------------|-------------|
| `PrismError` | Base exception with codes, context, recovery hints |
| `ErrorCategory` | Enum: CONFIGURATION, SECURITY, NETWORK, etc. |
| `ErrorSeverity` | Enum: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `format_exception(exc, mode)` | Format exception for display |

### Scrubbing

| Function | Description |
|----------|-------------|
| `scrub(data)` | Scrub sensitive data from dict |
| `Scrubber.add_key_pattern(key)` | Add custom sensitive key |
| `Scrubber.add_value_pattern(name, regex)` | Add custom value pattern |

---

## Examples

The [examples/](examples/) directory contains runnable examples:

- `01_basic_logging.py` - Getting started with logging
- `02_custom_errors.py` - Defining custom error classes
- `03_context_tracking.py` - Request, user, and operation context
- `04_secret_scrubbing.py` - PII/secret redaction
- `05_custom_palette.py` - Color themes and styling
- `06_error_recovery.py` - Retry logic and circuit breakers
- `07_batch_processing.py` - Batch context and chunked processing
- `fastapi_middleware.py` - FastAPI integration
- `flask_integration.py` - Flask integration

---

## Part of Project Prism

Prism View is part of [Project Prism](https://github.com/lukeudell/project-prism), a cross-language platform engineering suite:

```
┌─────────────────┐
│  prism-config   │  Settings & Secrets Foundation
└────────┬────────┘
         ↓
┌─────────────────┐
│   prism-view    │  Logging & Error Handling  ← You are here
└────────┬────────┘
         ↓
┌─────────────────┐
│  prism-guard    │  Auth & PQC Crypto
└────────┬────────┘
         ↓
┌─────────────────┐
│  prism-data     │  Persistence & Migrations
└────────┬────────┘
         ↓
┌─────────────────┐
│   prism-api     │  HTTP Standards & DTOs
└────────┬────────┘
         ↓
┌─────────────────┐
│  prism-boot     │  Service Lifecycle
└─────────────────┘
```

| Library | Description | Status |
|---------|-------------|--------|
| [prism-config](https://github.com/lukeudell/prism-config) | Typed configuration with secret resolution | Available |
| **prism-view** | Structured logging and error handling | **v1.0.0** |
| prism-guard | Authentication and PQC-ready crypto | Coming soon |
| prism-data | Database access and migrations | Coming soon |
| prism-api | HTTP envelopes and DTO standards | Coming soon |
| prism-boot | Application lifecycle management | Coming soon |

---

## Development

```bash
# Clone
git clone https://github.com/lukeudell/prism-view.git
cd prism-view

# Setup (creates venv, installs deps)
./setup-dev.sh      # Linux/Mac
.\setup-dev.ps1     # Windows

# Run tests
pytest

# Run with coverage
pytest --cov=src/prism/view --cov-report=term-missing
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Contributing

Contributions welcome! Please see the [Project Prism](https://github.com/lukeudell/project-prism) repository for contribution guidelines.

---

**Made with 💜 as part of [Project Prism](https://github.com/lukeudell/project-prism)**
