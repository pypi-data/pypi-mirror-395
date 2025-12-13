"""
Exception formatter for prism-view.

Renders PrismError instances as beautiful, actionable output.

Features:
    - Dev mode: Colorful, human-readable exception formatting
    - Prod mode: JSON output for production logging
    - Cause chain visualization with tree structure
    - Stack trace formatting (dev mode only)
    - Recovery hints and documentation URLs

Example:
    >>> from prism.view.formatter import ExceptionFormatter, handle_exception
    >>> from prism.view.errors import PrismError
    >>>
    >>> class MyError(PrismError):
    ...     code = (100, "APP", "MY_ERROR")
    ...
    >>> error = MyError("Something went wrong", suggestions=["Try again"])
    >>> formatter = ExceptionFormatter(mode="dev")
    >>> print(formatter.format(error))
    >>>
    >>> # Or use the convenience function
    >>> print(handle_exception(error))
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from prism.view.palette import Palette, get_box_chars, get_default_palette


# =============================================================================
# Exception Formatter
# =============================================================================


class ExceptionFormatter:
    """
    Formats exceptions for display in dev or prod mode.

    Dev mode produces beautiful, colorful, human-readable output with:
    - Error type and code
    - Message and details
    - Suggestions
    - Cause chain with tree visualization
    - Stack trace (optional)
    - Recovery hints
    - Documentation URL

    Prod mode produces JSON output with:
    - All error fields
    - No colors or emojis
    - No stack trace or debug info

    Attributes:
        mode: Output mode ("dev" or "prod")
        use_color: Whether to use ANSI colors (dev mode only)
        include_stack: Whether to include stack trace (dev mode only)
        palette: Color palette for styling

    Example:
        >>> formatter = ExceptionFormatter(mode="dev")
        >>> error = PrismError("Something failed")
        >>> print(formatter.format(error))
    """

    def __init__(
        self,
        mode: str = "dev",
        use_color: Optional[bool] = None,
        include_stack: bool = True,
        palette: Optional[Palette] = None,
    ):
        """
        Initialize the formatter.

        Args:
            mode: Output mode ("dev" or "prod")
            use_color: Whether to use colors (auto-detect if None)
            include_stack: Whether to include stack trace (dev mode only)
            palette: Color palette for styling
        """
        self.mode = mode
        self.include_stack = include_stack
        self._palette = palette

        # Determine color usage
        if os.environ.get("NO_COLOR"):
            self.use_color = False
        elif use_color is not None:
            self.use_color = use_color
        else:
            self.use_color = mode == "dev"

    def _get_palette(self) -> Palette:
        """Get the palette, loading default if needed."""
        if self._palette is not None:
            return self._palette
        return get_default_palette()

    def format(self, exc: BaseException) -> str:
        """
        Format an exception.

        Args:
            exc: Exception to format

        Returns:
            Formatted string (dev mode) or JSON string (prod mode)
        """
        if self.mode == "prod":
            return self._format_prod(exc)
        return self._format_dev(exc)

    # =========================================================================
    # Dev Mode Formatting
    # =========================================================================

    def _format_dev(self, exc: BaseException) -> str:
        """Format exception for dev mode (pretty output)."""
        lines: List[str] = []
        palette = self._get_palette()
        box = get_box_chars("rounded")

        # Check if it's a PrismError
        is_prism_error = self._is_prism_error(exc)

        # Header with error type and code
        lines.extend(self._format_header(exc, palette, box))

        # Message
        lines.extend(self._format_message(exc, palette))

        # Details (PrismError only)
        if is_prism_error:
            lines.extend(self._format_details(exc, palette))

        # Suggestions (PrismError only)
        if is_prism_error:
            lines.extend(self._format_suggestions(exc, palette))

        # Cause chain (PrismError only)
        if is_prism_error:
            lines.extend(self._format_cause_chain(exc, palette, box))

        # Location/Stack trace (PrismError only, if enabled)
        if is_prism_error and self.include_stack:
            lines.extend(self._format_location(exc, palette))

        # Recovery hints (PrismError only)
        if is_prism_error:
            lines.extend(self._format_recovery(exc, palette))

        # Documentation URL (PrismError only)
        if is_prism_error:
            lines.extend(self._format_docs_url(exc, palette))

        return "\n".join(lines)

    def _is_prism_error(self, exc: BaseException) -> bool:
        """Check if exception is a PrismError."""
        try:
            from prism.view.errors import PrismError

            return isinstance(exc, PrismError)
        except ImportError:
            return False

    def _colorize(self, text: str, color_name: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_color:
            return text
        palette = self._get_palette()
        color_code = palette.colors.get(color_name)
        if color_code is not None:
            return f"\033[38;5;{color_code}m{text}\033[0m"
        return text

    def _format_header(
        self, exc: BaseException, palette: Palette, box: Dict[str, str]
    ) -> List[str]:
        """Format the error header."""
        lines: List[str] = []
        exc_type = type(exc).__name__

        # Get error code if PrismError
        error_code = ""
        category = ""
        if self._is_prism_error(exc):
            error_code = exc.get_error_code() or ""  # type: ignore[union-attr]
            category = getattr(exc, "category", "") or ""

        # Build header line
        if self.use_color:
            # Use error color from palette
            error_color = palette.colors.get("error", 196)
            emoji = palette.emojis.get("error", "❌")

            header_parts = [f"\033[38;5;{error_color}m{emoji} {exc_type}\033[0m"]

            if error_code:
                # Error code in brackets
                code_color = palette.colors.get("warning", 214)
                header_parts.append(f"\033[38;5;{code_color}m[{error_code}]\033[0m")

            if category:
                # Category badge
                cat_color = palette.colors.get("secondary", 51)
                header_parts.append(f"\033[38;5;{cat_color}m({category})\033[0m")

            lines.append(" ".join(header_parts))
        else:
            header_parts = [exc_type]
            if error_code:
                header_parts.append(f"[{error_code}]")
            if category:
                header_parts.append(f"({category})")
            lines.append(" ".join(header_parts))

        # Separator line
        sep_char = box["horizontal"] if self.use_color else "-"
        lines.append(sep_char * 50)

        return lines

    def _format_message(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format the error message."""
        lines: List[str] = []

        # Get message
        if self._is_prism_error(exc):
            message = exc.message  # type: ignore[union-attr]
        else:
            message = str(exc) or "(no message)"

        lines.append("")
        lines.append(f"  {message}")
        lines.append("")

        return lines

    def _format_details(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format error details."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        details = getattr(exc, "details", {})
        if not details:
            return lines

        label = self._colorize("Details:", "info")
        lines.append(f"  {label}")

        for key, value in details.items():
            key_str = self._colorize(key, "secondary")
            lines.append(f"    {key_str}: {value}")

        lines.append("")
        return lines

    def _format_suggestions(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format suggestions."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        suggestions = getattr(exc, "suggestions", [])
        if not suggestions:
            return lines

        label = self._colorize("Suggestions:", "info")
        lines.append(f"  {label}")

        emoji = palette.emojis.get("arrow_right", "→") if self.use_color else "→"
        for suggestion in suggestions:
            lines.append(f"    {emoji} {suggestion}")

        lines.append("")
        return lines

    def _format_cause_chain(
        self, exc: BaseException, palette: Palette, box: Dict[str, str]
    ) -> List[str]:
        """Format cause chain with tree visualization."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        cause_chain = getattr(exc, "cause_chain", [])
        if not cause_chain:
            return lines

        label = self._colorize("Caused by:", "warning")
        lines.append(f"  {label}")

        for i, cause in enumerate(cause_chain):
            is_last = i == len(cause_chain) - 1
            prefix = "  └─ " if is_last else "  ├─ "

            cause_type = cause.get("type", "Unknown")
            cause_msg = cause.get("message", "")
            cause_code = cause.get("error_code", "")

            if self.use_color:
                type_str = self._colorize(cause_type, "error")
            else:
                type_str = cause_type

            if cause_code:
                lines.append(f"{prefix}{type_str} [{cause_code}]: {cause_msg}")
            else:
                lines.append(f"{prefix}{type_str}: {cause_msg}")

            # Mark root cause
            if is_last:
                root_label = self._colorize("(root cause)", "secondary")
                lines[-1] += f" {root_label}"

        lines.append("")
        return lines

    def _format_location(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format location/stack information."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        location = getattr(exc, "location", {})
        if not location:
            return lines

        label = self._colorize("Location:", "info")
        lines.append(f"  {label}")

        file_path = location.get("file", "unknown")
        line_num = location.get("line", "?")
        function = location.get("function", "unknown")

        lines.append(f"    File: {file_path}")
        lines.append(f"    Line: {line_num}")
        lines.append(f"    Function: {function}")

        lines.append("")
        return lines

    def _format_recovery(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format recovery hints."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        retryable = getattr(exc, "retryable", False)
        max_retries = getattr(exc, "max_retries", 0)
        retry_delay = getattr(exc, "retry_delay_seconds", 0.0)

        if not retryable:
            return lines

        label = self._colorize("Recovery:", "info")
        lines.append(f"  {label}")

        lines.append(f"    Retryable: {retryable}")
        if max_retries:
            lines.append(f"    Max retries: {max_retries}")
        if retry_delay:
            lines.append(f"    Retry delay: {retry_delay}s")

        lines.append("")
        return lines

    def _format_docs_url(self, exc: BaseException, palette: Palette) -> List[str]:
        """Format documentation URL."""
        lines: List[str] = []

        if not self._is_prism_error(exc):
            return lines

        docs_url = exc.get_docs_url() if hasattr(exc, "get_docs_url") else None  # type: ignore[union-attr]
        if not docs_url:
            return lines

        label = self._colorize("Documentation:", "info")
        url = self._colorize(docs_url, "secondary")
        lines.append(f"  {label} {url}")
        lines.append("")

        return lines

    # =========================================================================
    # Prod Mode Formatting
    # =========================================================================

    def _format_prod(self, exc: BaseException) -> str:
        """Format exception for prod mode (JSON output)."""
        record: Dict[str, Any] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._is_prism_error(exc):
            # Use PrismError's message attribute
            record["message"] = exc.message  # type: ignore[union-attr]

            # Error code
            error_code = exc.get_error_code()  # type: ignore[union-attr]
            if error_code:
                record["error_code"] = error_code

            # Category
            category = getattr(exc, "category", None)
            if category:
                record["category"] = category

            # Severity
            severity = getattr(exc, "severity", None)
            if severity:
                record["severity"] = severity

            # Details
            details = getattr(exc, "details", {})
            if details:
                record["details"] = details

            # Suggestions
            suggestions = getattr(exc, "suggestions", [])
            if suggestions:
                record["suggestions"] = suggestions

            # Cause chain
            cause_chain = getattr(exc, "cause_chain", [])
            if cause_chain:
                record["cause_chain"] = cause_chain

            # Root cause
            root_cause = getattr(exc, "root_cause", None)
            if root_cause:
                record["root_cause"] = root_cause

            # Recovery hints
            record["recovery"] = {
                "retryable": getattr(exc, "retryable", False),
                "max_retries": getattr(exc, "max_retries", 0),
                "retry_delay_seconds": getattr(exc, "retry_delay_seconds", 0.0),
            }

            # NO debug_info in prod
            # NO location/stack trace in prod

        return json.dumps(record, ensure_ascii=False, default=str)


# =============================================================================
# Convenience Functions
# =============================================================================


def format_exception(
    exc: BaseException,
    mode: str = "dev",
    use_color: Optional[bool] = None,
    include_stack: bool = True,
) -> str:
    """
    Format an exception for display.

    This is a convenience wrapper around ExceptionFormatter.

    Args:
        exc: Exception to format
        mode: Output mode ("dev" or "prod")
        use_color: Whether to use colors (auto-detect if None)
        include_stack: Whether to include stack trace (dev mode only)

    Returns:
        Formatted string

    Example:
        >>> from prism.view.formatter import format_exception
        >>> try:
        ...     raise ValueError("Something went wrong")
        ... except Exception as e:
        ...     print(format_exception(e))
    """
    formatter = ExceptionFormatter(
        mode=mode,
        use_color=use_color,
        include_stack=include_stack,
    )
    return formatter.format(exc)


def handle_exception(
    exc: BaseException,
    mode: str = "dev",
    use_color: Optional[bool] = None,
    include_traceback: bool = False,
) -> str:
    """
    Handle an exception by formatting it for display.

    This is a utility function for use in exception handlers.
    It formats the exception and returns the formatted string.

    Args:
        exc: Exception to handle
        mode: Output mode ("dev" or "prod")
        use_color: Whether to use colors
        include_traceback: Whether to include full traceback

    Returns:
        Formatted exception string

    Example:
        >>> from prism.view.formatter import handle_exception
        >>> try:
        ...     raise ValueError("Something went wrong")
        ... except Exception as e:
        ...     print(handle_exception(e))
    """
    formatter = ExceptionFormatter(
        mode=mode,
        use_color=use_color,
        include_stack=include_traceback,
    )
    return formatter.format(exc)
