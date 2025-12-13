"""
👁️ Prism View

Structured logging, error handling, and observability for Prism applications.

Features:
    - Dual-mode logging: Pretty (dev) vs JSON (prod)
    - Extensible error taxonomy with built-in codes + user-defined
    - Rich context capture: WHO, WHAT, WHERE, WHEN, WHY, HOW
    - Correlation & tracking: trace, session, transaction, batch IDs
    - Exception formatting with actionable messages and recovery hints
    - Secret scrubbing for automatic PII/secret redaction
    - Beautiful terminal output with colors, emojis, and tables
    - Performance tracking with operation duration metrics
    - ASCII banner display with version info

Example:
    >>> from prism.view import PrismError, ErrorSeverity
    >>>
    >>> class PaymentError(PrismError):
    ...     code = (1001, "PAY", "PAYMENT_FAILED")
    ...     severity = ErrorSeverity.ERROR
    ...
    >>> raise PaymentError("Payment declined", suggestions=["Try another card"])
"""

__version__ = "1.0.0"
__icon__ = "👁️"
__requires__ = ["prism-config"]  # Dependencies on other Prism libraries

# Error taxonomy (Iteration 2)
from .errors import (
    ErrorCategory,
    ErrorSeverity,
    PrismError,
    StandardErrorCode,
)

# Context system (Iteration 3)
from .context import LogContext

# Logging (Iteration 5 + 6)
from .logger import Logger, LogLevel, get_default_mode, get_logger

# Secret scrubbing (Iteration 7)
from .scrubber import Scrubber, default_scrubber, scrub

# Palette system (Iteration 8)
from .palette import (
    Palette,
    colorize,
    get_box_chars,
    get_default_palette,
    get_emoji,
    get_palette,
    load_palette,
    should_use_color,
)

# Display utilities (Iteration 9)
from .display import (
    console_table,
    display_width,
    pad_to_width,
    render_banner,
    truncate_to_width,
)

# Exception formatter (Iteration 10)
from .formatter import ExceptionFormatter, format_exception, handle_exception

# Setup and integration (Iteration 11)
from .setup import (
    PrismHandler,
    get_current_palette,
    get_global_mode,
    operation,
    setup_logging,
)

__all__ = [
    # Metadata
    "__version__",
    "__icon__",
    "__requires__",
    # Errors (Iteration 2)
    "PrismError",
    "ErrorCategory",
    "ErrorSeverity",
    "StandardErrorCode",
    # Context (Iteration 3)
    "LogContext",
    # Logging (Iteration 5 + 6)
    "get_logger",
    "get_default_mode",
    "Logger",
    "LogLevel",
    # Scrubbing (Iteration 7)
    "Scrubber",
    "scrub",
    "default_scrubber",
    # Palette (Iteration 8)
    "Palette",
    "load_palette",
    "get_palette",
    "get_default_palette",
    "colorize",
    "get_emoji",
    "get_box_chars",
    "should_use_color",
    # Display (Iteration 9)
    "console_table",
    "render_banner",
    "display_width",
    "pad_to_width",
    "truncate_to_width",
    # Formatter (Iteration 10)
    "ExceptionFormatter",
    "format_exception",
    "handle_exception",
    # Setup (Iteration 11)
    "setup_logging",
    "PrismHandler",
    "operation",
    "get_global_mode",
    "get_current_palette",
]
