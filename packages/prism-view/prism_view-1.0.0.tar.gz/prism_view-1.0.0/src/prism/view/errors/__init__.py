"""
Error classes for prism-view.

Provides extensible error taxonomy with built-in codes and user-defined errors.

Example:
    >>> from prism.view.errors import PrismError, ErrorCategory, ErrorSeverity
    >>>
    >>> class MyError(PrismError):
    ...     code = (100, "APP", "MY_ERROR")
    ...     category = ErrorCategory.RUNTIME
    ...     severity = ErrorSeverity.ERROR
    ...
    >>> raise MyError("Something went wrong")
"""

from .base import PrismError
from .categories import ErrorCategory
from .severity import ErrorSeverity
from .standard_codes import StandardErrorCode

__all__ = [
    "PrismError",
    "ErrorCategory",
    "ErrorSeverity",
    "StandardErrorCode",
]
