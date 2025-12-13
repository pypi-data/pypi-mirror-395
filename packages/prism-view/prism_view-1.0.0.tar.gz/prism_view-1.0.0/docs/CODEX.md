# 👁️ Prism View - CODEX

> Design decisions, architecture notes, and implementation rationale.

---

## Overview

Prism View provides structured logging, error handling, and observability for Prism applications. This document captures the key design decisions and their rationale.

---

## Design Principles

### 1. Dual-Mode Output

**Decision:** Support both pretty (dev) and JSON (prod) output modes.

**Rationale:**
- Developers need readable, colorful output during development
- Production systems need structured JSON for log aggregation (ELK, Datadog, etc.)
- Mode should be auto-detected based on environment or explicitly configured

### 2. Extensible Error Taxonomy

**Decision:** Provide base classes that users extend, not a fixed set of exceptions.

**Rationale:**
- Different domains have different error categories (e-commerce vs healthcare vs fintech)
- Users should define their own error codes and categories
- Built-in codes are optional convenience, not requirements
- Error codes use tuple format: `(number, category, name)` for flexibility

### 3. Context Propagation via contextvars

**Decision:** Use Python's `contextvars` for context propagation.

**Rationale:**
- Async-safe: Works correctly with asyncio
- Thread-safe: Works with traditional threaded code
- Zero configuration: No need for explicit passing of context
- Standard library: No external dependencies

### 4. Automatic Context Capture

**Decision:** Errors automatically capture context when raised.

**Rationale:**
- Reduces boilerplate in error handling
- Ensures consistent context in all errors
- Can be disabled when not needed (performance-critical paths)

### 5. Recovery Hints

**Decision:** Errors can include recovery hints (retryable, max_retries, delay).

**Rationale:**
- Enables automatic retry logic in calling code
- Self-documenting: Error tells you how to handle it
- Class-level defaults with instance overrides

---

## Architecture Decisions

### ADR-001: Why contextvars over ThreadLocal?

**Context:** Need to propagate context (trace IDs, user info) through call stacks.

**Decision:** Use `contextvars` module.

**Consequences:**
- Works with both sync and async code
- Properly handles asyncio task spawning
- Slight learning curve for developers unfamiliar with contextvars

### ADR-002: Why tuple-based error codes?

**Context:** Error codes need to be unique, categorized, and human-readable.

**Decision:** Use tuples: `(number, category, name)`

**Example:** `(1001, "PAY", "PAYMENT_FAILED")`

**Consequences:**
- Formatted as `E-PAY-1001` in logs
- Category grouping for filtering
- Name for human readability
- Number for uniqueness

### ADR-003: Why not use logging.Logger directly?

**Context:** Python has built-in logging, why wrap it?

**Decision:** Wrap logging to add Prism-specific features.

**Consequences:**
- Automatic context injection
- Dual-mode output (dev vs prod)
- Integration with PrismError
- Still compatible with standard logging ecosystem

---

## Module Organization

```
src/prism/view/
├── __init__.py          # Public API
├── logger.py            # Logger class and factory
├── handler.py           # Output handlers (dev/prod)
├── context.py           # LogContext with contextvars
├── errors/
│   ├── base.py          # PrismError base class
│   ├── categories.py    # ErrorCategory constants
│   ├── severity.py      # ErrorSeverity constants
│   └── standard_codes.py # Optional built-in codes
├── formatter.py         # Exception formatting
├── scrubber.py          # Secret redaction
├── display.py           # Console tables and banner
└── palette.py           # Color/emoji configuration
```

---

## Performance Considerations

### Context Access: O(1)
- contextvars lookup is constant time
- Cached per-task in asyncio

### Stack Capture: On-Demand
- Only captured on error creation
- Can be disabled with `capture_stack=False`
- Full traces only in dev mode

### Cause Chain: Lazy Build
- Built once on error creation
- Cached in error instance

---

## Future Considerations

1. **OpenTelemetry Integration** - Export traces to OTEL-compatible backends
2. **Async Context Managers** - Better support for async operations
3. **Sampling** - Log sampling for high-volume production systems
4. **Metrics Integration** - Export metrics alongside logs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12 | Initial release - project setup |

---

**Last Updated:** 2025-12-06
