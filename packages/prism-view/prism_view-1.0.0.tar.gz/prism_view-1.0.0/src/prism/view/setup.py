"""
Setup and integration utilities for prism-view.

Provides easy initialization and integration with Python's stdlib logging.

Features:
    - setup_logging(): One-call initialization for prism-view
    - PrismHandler: logging.Handler for stdlib integration
    - @operation decorator: Track function execution with context

Example:
    >>> from prism.view.setup import setup_logging, operation
    >>>
    >>> # Initialize prism-view
    >>> setup_logging(mode="dev", show_banner=True)
    >>>
    >>> # Use operation decorator
    >>> @operation("process_payment")
    ... def process_payment(amount):
    ...     return f"Processed ${amount}"
"""

import asyncio
import functools
import json
import logging
import sys
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, TextIO, TypeVar, Union

from prism.view.context import LogContext
from prism.view.display import render_banner
from prism.view.palette import Palette, get_default_palette, get_palette

# =============================================================================
# Global State
# =============================================================================

_global_mode: str = "dev"
_global_palette: Optional[Palette] = None
_global_stream: TextIO = sys.stderr


def get_global_mode() -> str:
    """Get the global logging mode."""
    return _global_mode


def get_current_palette() -> Palette:
    """Get the current palette."""
    global _global_palette
    if _global_palette is None:
        _global_palette = get_default_palette()
    return _global_palette


# =============================================================================
# setup_logging
# =============================================================================


def setup_logging(
    mode: str = "dev",
    level: str = "DEBUG",
    palette: Optional[Union[str, Palette]] = None,
    stream: Optional[TextIO] = None,
    show_banner: bool = True,
    config: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Initialize prism-view logging system.

    This is the main entry point for configuring prism-view. It sets up
    the global mode, palette, and optionally displays the startup banner.

    Args:
        mode: Logging mode ("dev" for pretty output, "prod" for JSON)
        level: Default log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        palette: Palette name or Palette instance
        stream: Output stream (default: sys.stderr)
        show_banner: Whether to show the VIEW LOADED banner (dev mode only)
        config: Optional configuration dictionary (overrides other args)

    Returns:
        None, or configuration dict if requested

    Example:
        >>> # Simple dev mode setup
        >>> setup_logging()
        >>>
        >>> # Production setup
        >>> setup_logging(mode="prod", level="INFO")
        >>>
        >>> # Custom palette
        >>> setup_logging(palette="solarized-dark")
    """
    global _global_mode, _global_palette, _global_stream

    # Apply config overrides
    if config:
        mode = config.get("mode", mode)
        level = config.get("level", level)
        palette = config.get("palette", palette)
        show_banner = config.get("show_banner", show_banner)

    # Set global mode
    _global_mode = mode

    # Set global stream
    _global_stream = stream or sys.stderr

    # Load palette
    if palette is None:
        _global_palette = get_default_palette()
    elif isinstance(palette, str):
        _global_palette = get_palette(palette)
    else:
        _global_palette = palette

    # Show banner in dev mode
    if show_banner and mode == "dev":
        banner = render_banner(palette=_global_palette, use_color=True)
        print(banner, file=_global_stream)

    return None


# =============================================================================
# PrismHandler - stdlib logging integration
# =============================================================================


class PrismHandler(logging.Handler):
    """
    A logging.Handler that formats messages using prism-view.

    Integrates prism-view formatting with Python's stdlib logging system.
    In dev mode, produces pretty colored output. In prod mode, produces JSON.

    Example:
        >>> import logging
        >>> from prism.view.setup import PrismHandler
        >>>
        >>> handler = PrismHandler(mode="dev")
        >>> logger = logging.getLogger("my.module")
        >>> logger.addHandler(handler)
        >>> logger.setLevel(logging.DEBUG)
        >>>
        >>> logger.info("Hello from stdlib logging!")
    """

    # Map Python logging levels to prism-view level names
    _LEVEL_MAP = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL",
    }

    # Level emoji mapping for dev mode
    _LEVEL_EMOJI = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥",
    }

    # Level color codes (ANSI 256)
    _LEVEL_COLOR = {
        logging.DEBUG: 244,  # Gray
        logging.INFO: 39,  # Blue
        logging.WARNING: 214,  # Orange
        logging.ERROR: 196,  # Red
        logging.CRITICAL: 201,  # Magenta/Pink
    }

    def __init__(
        self,
        mode: str = "dev",
        stream: Optional[TextIO] = None,
        palette: Optional[Palette] = None,
    ):
        """
        Initialize the handler.

        Args:
            mode: Output mode ("dev" or "prod")
            stream: Output stream (default: sys.stderr)
            palette: Color palette for dev mode
        """
        super().__init__()
        self.mode = mode
        self._stream = stream or sys.stderr
        self._palette = palette or get_default_palette()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record.

        Args:
            record: The log record to emit
        """
        try:
            if self.mode == "prod":
                msg = self._format_prod(record)
            else:
                msg = self._format_dev(record)

            print(msg, file=self._stream)
        except Exception:
            self.handleError(record)

    def _format_timestamp(self) -> str:
        """Format current timestamp for dev mode."""
        now = datetime.now(timezone.utc)
        return now.strftime("%H:%M:%S.%f")[:-3]

    def _format_timestamp_iso(self) -> str:
        """Format current timestamp in ISO 8601."""
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"

    def _format_dev(self, record: logging.LogRecord) -> str:
        """Format log record for dev mode."""
        parts = []

        # Timestamp
        timestamp = self._format_timestamp()
        parts.append(f"\033[38;5;240m{timestamp}\033[0m")

        # Level with emoji and color
        level = record.levelno
        emoji = self._LEVEL_EMOJI.get(level, "")
        color = self._LEVEL_COLOR.get(level, 39)
        level_name = self._LEVEL_MAP.get(level, "INFO")
        parts.append(f"\033[38;5;{color}m{emoji} {level_name:8}\033[0m")

        # Logger name
        parts.append(f"\033[38;5;245m[{record.name}]\033[0m")

        # Message
        parts.append(record.getMessage())

        # Include context if available
        try:
            context = LogContext.get_current()
            if context:
                ctx_parts = []
                for key, value in context.items():
                    ctx_parts.append(f"\033[38;5;39m{key}\033[0m={value}")
                if ctx_parts:
                    parts.append(" | " + " ".join(ctx_parts))
        except Exception:
            pass

        return " ".join(parts)

    def _format_prod(self, record: logging.LogRecord) -> str:
        """Format log record for prod mode (JSON)."""
        output: Dict[str, Any] = {
            "ts": self._format_timestamp_iso(),
            "level": self._LEVEL_MAP.get(record.levelno, "INFO"),
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Include context if available
        try:
            context = LogContext.get_current()
            for key, value in context.items():
                output[key] = value
        except Exception:
            pass

        return json.dumps(output, ensure_ascii=False, default=str)


# =============================================================================
# Operation Decorator
# =============================================================================

F = TypeVar("F", bound=Callable[..., Any])


def operation(
    name: str,
    on_complete: Optional[Callable[[float], None]] = None,
) -> Callable[[F], F]:
    """
    Decorator to track function execution with context.

    Sets up an operation context for the decorated function, tracking
    the operation name and duration.

    Args:
        name: Name of the operation (for logging/tracing)
        on_complete: Optional callback called with duration_ms when complete

    Returns:
        Decorated function

    Example:
        >>> @operation("process_order")
        ... def process_order(order_id):
        ...     # LogContext.get_current() will include operation="process_order"
        ...     return f"Processed {order_id}"
        >>>
        >>> @operation("fetch_data", on_complete=lambda d: print(f"Took {d}ms"))
        ... async def fetch_data():
        ...     await some_async_call()
    """

    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):
            # Async function
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                try:
                    with LogContext.operation(name):
                        return await func(*args, **kwargs)
                finally:
                    duration_ms = (time.perf_counter() - start) * 1000
                    if on_complete:
                        on_complete(duration_ms)

            return async_wrapper  # type: ignore[return-value]
        else:
            # Sync function
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                try:
                    with LogContext.operation(name):
                        return func(*args, **kwargs)
                finally:
                    duration_ms = (time.perf_counter() - start) * 1000
                    if on_complete:
                        on_complete(duration_ms)

            return sync_wrapper  # type: ignore[return-value]

    return decorator
