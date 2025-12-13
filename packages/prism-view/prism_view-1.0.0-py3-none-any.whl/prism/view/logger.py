"""
Logger implementation for prism-view.

Provides dual-mode logging (dev vs prod) with automatic context integration.

Features:
    - Dev mode: Pretty, colorful, human-readable output
    - Prod mode: JSON output for production environments
    - Automatic LogContext integration
    - Child loggers with bound context
    - PrismError-aware error logging

Example:
    >>> from prism.view.logger import get_logger, Logger
    >>> from prism.view import LogContext
    >>>
    >>> # Get a logger
    >>> logger = get_logger("payment-service")
    >>>
    >>> # Log with context
    >>> LogContext.set_service(name="payment-api", version="1.0.0")
    >>> with LogContext.request(trace_id="abc-123"):
    ...     logger.info("Processing payment", amount=99.99)
    ...
    >>> # Create child logger with bound context
    >>> request_logger = logger.with_context(request_id="req-456")
    >>> request_logger.info("Handling request")
    >>>
    >>> # Prod mode outputs JSON
    >>> prod_logger = Logger("api", mode="prod")
    >>> prod_logger.info("Request received")  # {"ts": "...", "level": "INFO", ...}
"""

import json
import os
import sys
from datetime import datetime, timezone
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, Optional, TextIO

if TYPE_CHECKING:
    from prism.view.errors import PrismError
    from prism.view.palette import Palette


class LogLevel(IntEnum):
    """Log level enumeration with numeric ordering."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


# Level name to LogLevel mapping
_LEVEL_MAP: Dict[str, LogLevel] = {
    "DEBUG": LogLevel.DEBUG,
    "INFO": LogLevel.INFO,
    "WARNING": LogLevel.WARNING,
    "WARN": LogLevel.WARNING,
    "ERROR": LogLevel.ERROR,
    "CRITICAL": LogLevel.CRITICAL,
}

# Level to emoji mapping for dev mode
_LEVEL_EMOJI: Dict[LogLevel, str] = {
    LogLevel.DEBUG: "🔍",
    LogLevel.INFO: "ℹ️",
    LogLevel.WARNING: "⚠️",
    LogLevel.ERROR: "❌",
    LogLevel.CRITICAL: "🔥",
}

# Level to color code mapping (ANSI 256 colors)
_LEVEL_COLOR: Dict[LogLevel, str] = {
    LogLevel.DEBUG: "\033[38;5;244m",  # Gray
    LogLevel.INFO: "\033[38;5;39m",  # Blue
    LogLevel.WARNING: "\033[38;5;214m",  # Orange
    LogLevel.ERROR: "\033[38;5;196m",  # Red
    LogLevel.CRITICAL: "\033[38;5;201m",  # Magenta/Pink
}

_RESET = "\033[0m"


# Logger cache for get_logger()
_logger_cache: Dict[str, "Logger"] = {}


def get_default_mode() -> str:
    """
    Get the default logging mode from environment.

    Checks the PRISM_LOG_MODE environment variable. Supports:
    - "dev" or "development" -> "dev"
    - "prod" or "production" -> "prod"

    Returns:
        "dev" or "prod" (default: "dev")

    Example:
        >>> import os
        >>> os.environ["PRISM_LOG_MODE"] = "prod"
        >>> get_default_mode()
        'prod'
    """
    mode = os.environ.get("PRISM_LOG_MODE", "dev").lower()

    if mode in ("prod", "production"):
        return "prod"
    return "dev"


class Logger:
    """
    Prism logger with context integration and dual-mode output.

    Automatically includes LogContext fields in all log messages.
    Supports dev mode (pretty) and prod mode (JSON) formatting.

    Attributes:
        name: Logger name (typically service or module name)
        level: Minimum log level to output
        mode: Output mode ("dev" for pretty, "prod" for JSON)

    Example:
        >>> logger = Logger("my-service")
        >>> logger.info("User logged in", user_id="user-123")
        >>> logger.error("Payment failed", exc=PaymentError("Declined"))
    """

    def __init__(
        self,
        name: str,
        level: str = "DEBUG",
        mode: str = "dev",
        stream: Optional[TextIO] = None,
        _bound_context: Optional[Dict[str, Any]] = None,
        scrub: bool = True,
        palette: Optional["Palette"] = None,
    ):
        """
        Initialize a Logger.

        Args:
            name: Logger name (e.g., "payment-service")
            level: Minimum log level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
            mode: Output mode ("dev" or "prod")
            stream: Output stream (default: sys.stderr)
            _bound_context: Internal - context bound via with_context()
            scrub: Whether to scrub sensitive data (default: True)
            palette: Palette for colors and emojis (default: vaporwave)
        """
        self.name = name
        self.level = level.upper()
        self.mode = mode
        self._stream = stream or sys.stderr
        self._bound_context = _bound_context or {}
        self._level_value = _LEVEL_MAP.get(self.level, LogLevel.DEBUG)
        self._scrub = scrub
        self._palette = palette

    def _should_log(self, level: LogLevel) -> bool:
        """Check if the given level should be logged."""
        return level >= self._level_value

    def _get_palette(self) -> "Palette":
        """Get the palette, loading default if needed."""
        if self._palette is not None:
            return self._palette
        try:
            from prism.view.palette import get_default_palette

            return get_default_palette()
        except ImportError:
            # Return a minimal fallback if palette module not available
            return None  # type: ignore[return-value]

    def is_prod_mode(self) -> bool:
        """
        Check if the logger is in prod mode.

        Returns:
            True if mode is "prod", False otherwise.
        """
        return self.mode == "prod"

    def _get_context(self) -> Dict[str, Any]:
        """Get merged context from LogContext and bound context."""
        try:
            from prism.view.context import LogContext

            current = LogContext.get_current()
        except ImportError:
            current = {}

        # Merge: LogContext < bound context (bound takes precedence)
        result = {}
        result.update(current)
        result.update(self._bound_context)
        return result

    def _format_timestamp(self) -> str:
        """Format current timestamp for dev mode logging."""
        now = datetime.now(timezone.utc)
        return now.strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS.mmm

    def _format_timestamp_iso(self) -> str:
        """Format current timestamp in ISO 8601 format for prod mode."""
        now = datetime.now(timezone.utc)
        # ISO 8601 format with milliseconds and Z suffix
        return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"

    def _format_dev(
        self,
        level: LogLevel,
        message: str,
        context: Dict[str, Any],
        exc: Optional[BaseException] = None,
    ) -> str:
        """Format log message for dev mode (pretty output)."""
        parts = []

        # Get palette for colors and emojis
        palette = self._get_palette()

        # Timestamp
        timestamp = self._format_timestamp()
        parts.append(f"\033[38;5;240m{timestamp}\033[0m")

        # Level with emoji and color from palette
        level_key = level.name.lower()

        # Get emoji from palette or fallback
        if palette is not None:
            emoji = palette.emojis.get(level_key, _LEVEL_EMOJI.get(level, ""))
            color_code = palette.colors.get(level_key)
            if color_code is not None:
                color = f"\033[38;5;{color_code}m"
            else:
                color = _LEVEL_COLOR.get(level, "")
        else:
            emoji = _LEVEL_EMOJI.get(level, "")
            color = _LEVEL_COLOR.get(level, "")

        level_name = level.name
        parts.append(f"{color}{emoji} {level_name:8}{_RESET}")

        # Logger name
        parts.append(f"\033[38;5;245m[{self.name}]\033[0m")

        # Message
        parts.append(message)

        # Context fields - use info color from palette
        if context:
            context_parts = []
            if palette is not None:
                ctx_color_code = palette.colors.get("info", 39)
                ctx_color = f"\033[38;5;{ctx_color_code}m"
            else:
                ctx_color = "\033[38;5;39m"

            for key, value in context.items():
                context_parts.append(f"{ctx_color}{key}\033[0m={value}")
            if context_parts:
                parts.append(" | " + " ".join(context_parts))

        result = " ".join(parts)

        # Exception handling
        if exc is not None:
            result += "\n" + self._format_exception(exc)

        return result

    def _format_exception(self, exc: BaseException) -> str:
        """Format an exception for dev mode output."""
        lines = []

        # Check if it's a PrismError
        try:
            from prism.view.errors import PrismError

            if isinstance(exc, PrismError):
                return self._format_prism_error(exc)
        except ImportError:
            pass

        # Standard exception formatting
        exc_type = type(exc).__name__
        lines.append(f"  \033[38;5;196m{exc_type}\033[0m: {exc}")

        return "\n".join(lines)

    def _format_prism_error(self, exc: "PrismError") -> str:
        """Format a PrismError for dev mode output."""
        lines = []

        # Error header with code
        error_code = exc.get_error_code()
        exc_type = type(exc).__name__
        if error_code:
            lines.append(f"  \033[38;5;196m{exc_type}\033[0m [{error_code}]: {exc.message}")
        else:
            lines.append(f"  \033[38;5;196m{exc_type}\033[0m: {exc.message}")

        # Details
        if exc.details:
            lines.append("  \033[38;5;245mDetails:\033[0m")
            for key, value in exc.details.items():
                lines.append(f"    {key}: {value}")

        # Suggestions
        if exc.suggestions:
            lines.append("  \033[38;5;39mSuggestions:\033[0m")
            for suggestion in exc.suggestions:
                lines.append(f"    → {suggestion}")

        # Cause chain
        if exc.cause_chain:
            lines.append("  \033[38;5;245mCause chain:\033[0m")
            for i, cause in enumerate(exc.cause_chain):
                prefix = "    └─ " if i == len(exc.cause_chain) - 1 else "    ├─ "
                cause_code = cause.get("error_code", "")
                if cause_code:
                    lines.append(f"{prefix}{cause['type']} [{cause_code}]: {cause['message']}")
                else:
                    lines.append(f"{prefix}{cause['type']}: {cause['message']}")

        return "\n".join(lines)

    def _format_prod(
        self,
        level: LogLevel,
        message: str,
        context: Dict[str, Any],
        exc: Optional[BaseException] = None,
    ) -> str:
        """
        Format log message for prod mode (JSON output).

        Produces single-line JSON with standard fields:
        - ts: ISO 8601 timestamp
        - level: Log level name
        - logger: Logger name
        - msg: Log message
        - Additional context and extra fields

        Args:
            level: Log level
            message: Log message
            context: Context dictionary
            exc: Optional exception

        Returns:
            Single-line JSON string
        """
        record: Dict[str, Any] = {
            "ts": self._format_timestamp_iso(),
            "level": level.name,
            "logger": self.name,
            "msg": message,
        }

        # Flatten context into record
        # Extract common fields to top level
        for key, value in context.items():
            record[key] = value

        # Add exception if present
        if exc is not None:
            record["error"] = self._format_error_prod(exc)

        return json.dumps(record, ensure_ascii=False, default=str)

    def _format_error_prod(self, exc: BaseException) -> Dict[str, Any]:
        """
        Format an exception for prod mode JSON output.

        Args:
            exc: Exception to format

        Returns:
            Dictionary with error details (no debug info or stack trace)
        """
        error_dict: Dict[str, Any] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }

        # Check if it's a PrismError
        try:
            from prism.view.errors import PrismError

            if isinstance(exc, PrismError):
                # Use message attribute for PrismError
                error_dict["message"] = exc.message

                # Add error code
                error_code = exc.get_error_code()
                if error_code:
                    error_dict["error_code"] = error_code

                # Add details (scrubbed if enabled)
                if exc.details:
                    if self._scrub:
                        try:
                            from prism.view.scrubber import scrub as scrub_data

                            error_dict["details"] = scrub_data(exc.details)
                        except ImportError:
                            error_dict["details"] = exc.details
                    else:
                        error_dict["details"] = exc.details

                # Add suggestions
                if exc.suggestions:
                    error_dict["suggestions"] = exc.suggestions

                # Add cause chain (no debug info)
                if exc.cause_chain:
                    error_dict["cause_chain"] = exc.cause_chain

                # Add root cause
                if exc.root_cause:
                    error_dict["root_cause"] = exc.root_cause

                # Add recovery hints
                recovery = {
                    "retryable": exc.retryable,
                    "max_retries": exc.max_retries,
                    "retry_delay_seconds": exc.retry_delay_seconds,
                }
                error_dict["recovery"] = recovery

                # NO debug_info in prod mode
                # NO stack_trace in prod mode

        except ImportError:
            pass

        return error_dict

    def _log(
        self,
        level: LogLevel,
        message: str,
        exc: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> None:
        """Internal log method."""
        if not self._should_log(level):
            return

        # Merge context
        context = self._get_context()
        context.update(kwargs)

        # Scrub sensitive data if enabled
        if self._scrub:
            try:
                from prism.view.scrubber import scrub as scrub_data

                context = scrub_data(context)
            except ImportError:
                pass

        # Format based on mode
        if self.mode == "dev":
            output = self._format_dev(level, message, context, exc)
        else:
            output = self._format_prod(level, message, context, exc)

        # Write to stream
        print(output, file=self._stream)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        self._log(LogLevel.INFO, message, **kwargs)

    def warn(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        self._log(LogLevel.WARNING, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message (alias for warn)."""
        self._log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, exc: Optional[BaseException] = None, **kwargs: Any) -> None:
        """
        Log an error message.

        Args:
            message: Error message
            exc: Optional exception (PrismError or standard Exception)
            **kwargs: Additional context fields
        """
        self._log(LogLevel.ERROR, message, exc=exc, **kwargs)

    def critical(self, message: str, exc: Optional[BaseException] = None, **kwargs: Any) -> None:
        """
        Log a critical message.

        Args:
            message: Critical message
            exc: Optional exception
            **kwargs: Additional context fields
        """
        self._log(LogLevel.CRITICAL, message, exc=exc, **kwargs)

    def with_context(self, **kwargs: Any) -> "Logger":
        """
        Create a child logger with bound context.

        The child logger will include the bound context fields in all log messages,
        in addition to LogContext fields.

        Args:
            **kwargs: Context fields to bind to the child logger

        Returns:
            A new Logger instance with bound context

        Example:
            >>> logger = Logger("api")
            >>> request_logger = logger.with_context(request_id="req-123")
            >>> request_logger.info("Handling request")  # Includes request_id
        """
        # Merge parent's bound context with new context
        merged_context = {}
        merged_context.update(self._bound_context)
        merged_context.update(kwargs)

        return Logger(
            name=self.name,
            level=self.level,
            mode=self.mode,
            stream=self._stream,
            _bound_context=merged_context,
            scrub=self._scrub,
            palette=self._palette,
        )


def get_logger(
    name: str,
    level: str = "DEBUG",
    mode: str = "dev",
) -> Logger:
    """
    Get or create a logger with the given name.

    Loggers are cached by name, so calling get_logger with the same name
    returns the same Logger instance.

    Args:
        name: Logger name (e.g., "payment-service")
        level: Minimum log level (only used for first creation)
        mode: Output mode (only used for first creation)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger("my-service")
        >>> logger.info("Hello!")
    """
    if name not in _logger_cache:
        _logger_cache[name] = Logger(name=name, level=level, mode=mode)
    return _logger_cache[name]


def clear_logger_cache() -> None:
    """Clear the logger cache. Useful for testing."""
    _logger_cache.clear()
