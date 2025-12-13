"""
ErrorSeverity constants for prism-view.

Provides standard severity levels compatible with logging systems.

Example:
    >>> from prism.view.errors import ErrorSeverity
    >>> print(ErrorSeverity.ERROR)
    'ERROR'
"""


class ErrorSeverity:
    """
    Standard severity levels for Prism errors.

    These levels align with standard logging levels for easy integration
    with logging systems. All values are strings for serialization.

    Levels (in order of increasing severity):
        DEBUG: Diagnostic information for debugging
        INFO: Informational messages, normal operation
        WARNING: Warning conditions, recoverable issues
        ERROR: Error conditions, operation failed
        CRITICAL: Critical conditions, system may be unstable
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
