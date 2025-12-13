"""
PrismError base class for prism-view.

Provides extensible base exception with:
- Message, details, and suggestions
- Error code, category, and severity (class-level, overridable)
- Timestamp
- Cause tracking with cause chain and root cause extraction
- Automatic LogContext capture
- Stack information capture (file, line, function, module)
- Recovery hints (retryable, max_retries, retry_delay_seconds)
- Debug information (dev mode only)
- Documentation URL generation
- Serialization via to_dict()

Example:
    >>> from prism.view.errors import PrismError, ErrorSeverity
    >>> from prism.view import LogContext
    >>>
    >>> class PaymentError(PrismError):
    ...     code = (1001, "PAY", "PAYMENT_FAILED")
    ...     category = "PAYMENT"
    ...     severity = ErrorSeverity.ERROR
    ...     retryable = True
    ...     max_retries = 3
    ...
    >>> LogContext.set_service(name="payment-api")
    >>> with LogContext.request(trace_id="abc-123"):
    ...     error = PaymentError("Payment declined", details={"card": "****1234"})
    ...     print(error.context)  # Includes service and request context
    ...     print(error.location)  # File, line, function info
"""

import inspect
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class PrismError(Exception):
    """
    Base exception for all Prism errors.

    This is the foundation for Prism's extensible error taxonomy.
    Users should subclass this to create their own domain-specific errors.

    Class Attributes (override in subclasses):
        code: Error code tuple (number, category, name) or None
        category: Error category string or None
        severity: Error severity string or None
        retryable: Whether the error is retryable (default False)
        max_retries: Maximum retry attempts (default 0)
        retry_delay_seconds: Delay between retries in seconds (default 0.0)
        docs_base_url: Base URL for error documentation

    Instance Attributes:
        message: Human-readable error message
        details: Additional context as key-value pairs
        suggestions: List of recovery suggestions
        cause: Original exception that caused this error
        timestamp: When the error was created (UTC)
        context: Captured LogContext at error creation time
        location: Stack information (file, line, function, module)
        cause_chain: List of cause information dicts
        root_cause: The root cause information dict
        debug_info: Debug-only information dict

    Example:
        >>> class DatabaseError(PrismError):
        ...     code = (200, "DB", "CONNECTION_FAILED")
        ...     category = "DATABASE"
        ...     severity = "ERROR"
        ...     retryable = True
        ...     max_retries = 3
        ...     retry_delay_seconds = 1.0
        ...
        >>> try:
        ...     connect_to_db()
        ... except ConnectionError as e:
        ...     raise DatabaseError(
        ...         "Failed to connect to database",
        ...         details={"host": "localhost", "port": 5432},
        ...         suggestions=["Check if database is running"],
        ...         cause=e,
        ...         debug_info={"connection_string": "..."},
        ...     )
    """

    # Class-level attributes (can be overridden in subclasses)
    code: Optional[Tuple[int, str, str]] = None
    category: Optional[str] = None
    severity: Optional[str] = None

    # Recovery hints (override in subclasses for retryable errors)
    retryable: bool = False
    max_retries: int = 0
    retry_delay_seconds: float = 0.0

    # Documentation URL base (override to customize)
    docs_base_url: str = "https://prism.dev/errors"

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None,
        cause: Optional[Exception] = None,
        capture_context: bool = True,
        capture_stack: bool = True,
        debug_info: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a PrismError.

        Args:
            message: Human-readable error message
            details: Additional context as key-value pairs
            suggestions: List of recovery suggestions for the user
            cause: Original exception that caused this error
            capture_context: Whether to capture LogContext (default True)
            capture_stack: Whether to capture stack location (default True)
            debug_info: Debug-only information (excluded in prod mode)
        """
        self.message = message
        self.details = details or {}
        self.suggestions = suggestions or []
        self.cause = cause
        self.timestamp = datetime.now(timezone.utc)
        self.debug_info = debug_info or {}

        # Capture LogContext if enabled
        if capture_context:
            self.context = self._capture_context()
        else:
            self.context = {}

        # Capture stack information if enabled
        if capture_stack:
            self.location = self._capture_location()
        else:
            self.location = {}

        # Build cause chain and extract root cause
        self.cause_chain = self._build_cause_chain()
        self.root_cause = self._extract_root_cause()

        # Call parent Exception with the message
        super().__init__(message)

    def _capture_context(self) -> Dict[str, Any]:
        """
        Capture the current LogContext.

        Returns:
            Dictionary containing current context fields.
        """
        try:
            from prism.view.context import LogContext

            return LogContext.get_current()
        except ImportError:
            return {}

    def _capture_location(self) -> Dict[str, Any]:
        """
        Capture the stack location where the error was created.

        Returns:
            Dictionary with file, line, function, and module information.
        """
        try:
            # Walk up the stack to find the first frame outside PrismError
            frame = inspect.currentframe()
            if frame is None:
                return {}

            caller_frame = frame
            # Walk up until we find a frame that's not in base.py (PrismError internals)
            while caller_frame is not None:
                caller_frame = caller_frame.f_back
                if caller_frame is None:
                    break
                # Check if we're outside the PrismError class methods
                filename = caller_frame.f_code.co_filename
                if not filename.endswith("base.py"):
                    break

            if caller_frame is None:
                return {}

            frame_info = inspect.getframeinfo(caller_frame)

            return {
                "file": frame_info.filename,
                "line": frame_info.lineno,
                "function": frame_info.function,
                "module": caller_frame.f_globals.get("__name__", "unknown"),
            }
        except Exception:
            return {}
        finally:
            # Clean up frame references to avoid reference cycles
            del frame

    def _build_cause_chain(self) -> List[Dict[str, Any]]:
        """
        Build a chain of cause information from the exception.

        Follows both explicit `cause` attributes (for PrismError) and
        standard `__cause__`/`__context__` attributes.

        Returns:
            List of dictionaries with cause information.
        """
        chain: List[Dict[str, Any]] = []

        current: Optional[BaseException] = self.cause
        seen: set = set()  # Prevent infinite loops

        while current is not None and id(current) not in seen:
            seen.add(id(current))

            cause_info: Dict[str, Any] = {
                "type": type(current).__name__,
                "message": str(current),
            }

            # Include error code if it's a PrismError
            if isinstance(current, PrismError):
                error_code = current.get_error_code()
                if error_code:
                    cause_info["error_code"] = error_code

            chain.append(cause_info)

            # Follow the cause chain - check PrismError.cause first
            next_cause: Optional[BaseException] = None
            if isinstance(current, PrismError) and current.cause is not None:
                next_cause = current.cause
            else:
                next_cause = getattr(current, "__cause__", None)
                if next_cause is None:
                    next_cause = getattr(current, "__context__", None)
            current = next_cause

        return chain

    def _extract_root_cause(self) -> Optional[Dict[str, Any]]:
        """
        Extract the root cause from the cause chain.

        Returns:
            Dictionary with root cause information, or None if no cause.
        """
        if not self.cause_chain:
            return None

        return self.cause_chain[-1]

    def __str__(self) -> str:
        """Return the error message."""
        return self.message

    def __repr__(self) -> str:
        """Return detailed representation."""
        class_name = self.__class__.__name__
        return f"{class_name}(message={self.message!r}, code={self.code})"

    def get_error_code(self) -> Optional[str]:
        """
        Get formatted error code string.

        Returns:
            Formatted error code like "E-CFG-001" or None if no code.
        """
        if not self.code:
            return None

        if not isinstance(self.code, tuple) or len(self.code) != 3:
            return str(self.code)

        number, category, _ = self.code

        # Get severity prefix (first letter, uppercase)
        if self.severity:
            prefix = self.severity[0].upper()
        else:
            prefix = "E"  # Default to Error

        return f"{prefix}-{category}-{number:03d}"

    def get_code_name(self) -> Optional[str]:
        """
        Get the error code name.

        Returns:
            Error code name like "CONFIG_FILE_NOT_FOUND" or None.
        """
        if not self.code:
            return None

        if isinstance(self.code, tuple) and len(self.code) >= 3:
            return self.code[2]

        return str(self.code)

    def get_docs_url(self) -> Optional[str]:
        """
        Get the documentation URL for this error.

        Returns:
            URL string for error documentation, or None if no code.
        """
        if not self.code:
            return None

        code_name = self.get_code_name()
        if not code_name:
            return None

        # Convert to URL-friendly format (lowercase, hyphens)
        url_slug = code_name.lower().replace("_", "-")
        return f"{self.docs_base_url}/{url_slug}"

    def to_dict(self, include_debug: bool = False) -> Dict[str, Any]:
        """
        Convert error to a dictionary for logging/serialization.

        Args:
            include_debug: Whether to include debug_info (default False for prod)

        Returns:
            Dictionary with all error details, suitable for JSON serialization.

        Example:
            >>> error = PrismError("Something failed", details={"key": "value"})
            >>> import json
            >>> print(json.dumps(error.to_dict(), indent=2))
        """
        result: Dict[str, Any] = {
            "message": self.message,
            "details": self.details,
            "suggestions": self.suggestions,
            "timestamp": self.timestamp.isoformat(),
            "exception_type": self.__class__.__name__,
        }

        # Add code info if present
        if self.code:
            result["code"] = self.get_code_name()
            result["error_code"] = self.get_error_code()

        # Add category if present
        if self.category:
            result["category"] = self.category

        # Add severity if present
        if self.severity:
            result["severity"] = self.severity

        # Add context if present (non-empty)
        if self.context:
            result["context"] = self.context

        # Add location if present (non-empty)
        if self.location:
            result["location"] = self.location

        # Add cause chain if present
        if self.cause_chain:
            result["cause_chain"] = self.cause_chain

        # Add root cause if present
        if self.root_cause:
            result["root_cause"] = self.root_cause

        # Add legacy cause info for backwards compatibility
        if self.cause:
            result["cause"] = {
                "type": type(self.cause).__name__,
                "message": str(self.cause),
            }

        # Add recovery hints
        result["recovery"] = {
            "retryable": self.retryable,
            "max_retries": self.max_retries,
            "retry_delay_seconds": self.retry_delay_seconds,
        }

        # Add documentation URL if available
        docs_url = self.get_docs_url()
        if docs_url:
            result["docs_url"] = docs_url

        # Add debug info only if requested (dev mode)
        if include_debug and self.debug_info:
            result["debug_info"] = self.debug_info

        return result

    def with_context(self, **kwargs: Any) -> "PrismError":
        """
        Add additional context to the error details.

        Args:
            **kwargs: Key-value pairs to add to details

        Returns:
            Self for chaining

        Example:
            >>> error = PrismError("Failed")
            >>> error.with_context(request_id="abc-123", user_id="user-456")
            >>> print(error.details)
            {'request_id': 'abc-123', 'user_id': 'user-456'}
        """
        self.details.update(kwargs)
        return self
