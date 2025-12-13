# Release Notes - prism-view v1.0.0

**Release Date:** December 7, 2025

## Overview

prism-view is the observability component of [Project Prism](https://github.com/lukeudell/project-prism), providing structured logging, error handling, and beautiful terminal output for Python applications.

This is the first stable release, marking the completion of all 14 development iterations.

## Highlights

- **Dual-mode logging**: Pretty colored output for development, JSON for production
- **Rich error taxonomy**: 37+ built-in error codes with categories and severity levels
- **Context tracking**: Automatic propagation of trace IDs, user info, and request context
- **Secret scrubbing**: Automatic redaction of passwords, tokens, and PII
- **Beautiful output**: Vaporwave-themed colors, emojis, and ASCII art banner

## Features

### Error Handling
- `PrismError` base class with error codes, categories, and severity
- Automatic context capture (service, request, user, operation)
- Cause chain tracking with root cause extraction
- Recovery hints (retryable, max_retries, retry_delay)
- Documentation URL generation
- Debug information (dev-only)

### Logging
- `Logger` class with info/debug/warn/error/critical methods
- `get_logger(name)` factory with caching
- Dev mode: Pretty formatted with colors and emojis
- Prod mode: Single-line JSON output
- Automatic `LogContext` integration
- Child loggers with `with_context()`
- PrismError-aware formatting

### Context System
- `LogContext` with async-safe propagation (contextvars)
- Service, request, user, session, transaction, batch contexts
- Operation context with automatic duration tracking
- Custom fields via `LogContext.add()`

### Secret Scrubbing
- `Scrubber` class for automatic PII/secret redaction
- Key-based detection: password, secret, token, api_key, etc.
- Pattern-based detection: JWT, Bearer tokens, AWS keys, credit cards
- Extensible with custom patterns
- Logger integration (automatic scrubbing)

### Display Utilities
- `console_table()` for formatted tables
- Unicode-aware width calculation (CJK, emoji support)
- Box drawing styles: single, double, rounded, ascii
- `render_banner()` for ASCII art with vaporwave gradient

### Palette System
- TOML-based palette configuration
- Built-in palettes: vaporwave, monochrome, solarized-dark, high-contrast
- `colorize()` for ANSI 256 colors
- NO_COLOR/FORCE_COLOR environment variable support

### Exception Formatter
- `ExceptionFormatter` for beautiful exception rendering
- Dev mode: Colors, emojis, cause chain visualization
- Prod mode: JSON output for log aggregation
- `format_exception()` and `handle_exception()` utilities

### Integration
- `setup_logging()` for one-call initialization
- `PrismHandler` for stdlib logging integration
- `@operation` decorator for function tracking
- FastAPI middleware example
- Flask integration example

## Installation

```bash
pip install prism-view
```

## Quick Start

```python
from prism.view import get_logger, LogContext, PrismError

# Initialize logging
logger = get_logger("my-service")

# Set service context
LogContext.set_service(name="my-api", version="1.0.0", environment="prod")

# Log with context
with LogContext.request(trace_id="abc-123"):
    logger.info("Processing request", user_id="user-456")

# Custom errors
class PaymentError(PrismError):
    code = (1001, "PAY", "PAYMENT_FAILED")
    retryable = True
    max_retries = 3

raise PaymentError("Payment declined", suggestions=["Try another card"])
```

## Requirements

- Python 3.10+
- pydantic >= 2.0.0
- colorama >= 0.4.6
- pyyaml >= 6.0.0

## Test Coverage

- 465 tests passing
- ~92% code coverage
- Property-based tests with Hypothesis
- Tested on Python 3.10, 3.11, 3.12
- Tested on Ubuntu, Windows, macOS

## Breaking Changes

None - this is the first stable release.

## Known Issues

None at this time.

## Contributors

- Luke Udell ([@lukeudell](https://github.com/lukeudell))

## Links

- [GitHub Repository](https://github.com/lukeudell/prism-view)
- [Project Prism](https://github.com/lukeudell/project-prism)
- [Changelog](https://github.com/lukeudell/prism-view/blob/main/CHANGELOG.md)
- [Documentation](https://github.com/lukeudell/prism-view#readme)

## License

MIT License - see [LICENSE](LICENSE) for details.
