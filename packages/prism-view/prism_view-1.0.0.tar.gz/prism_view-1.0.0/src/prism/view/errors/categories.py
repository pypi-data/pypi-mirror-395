"""
ErrorCategory constants for prism-view.

Provides standard error categories for classification.
Users can define their own categories by creating similar string constants.

Example:
    >>> from prism.view.errors import ErrorCategory
    >>> print(ErrorCategory.DATABASE)
    'DATABASE'

    # Custom categories
    >>> class MyCategories:
    ...     PAYMENT = "PAYMENT"
    ...     INVENTORY = "INVENTORY"
"""


class ErrorCategory:
    """
    Standard error categories for Prism applications.

    These categories help classify errors for filtering and monitoring.
    All values are strings for easy serialization and comparison.

    Categories:
        CONFIGURATION: Config file, environment, settings errors
        SECURITY: Authentication, authorization, encryption errors
        DATABASE: Connection, query, transaction errors
        NETWORK: HTTP, timeout, connection errors
        VALIDATION: Input validation, schema, type errors
        FILESYSTEM: File, directory, permission errors
        RUNTIME: Unexpected errors, internal failures
        EXTERNAL: Third-party service, API errors
    """

    CONFIGURATION = "CONFIGURATION"
    SECURITY = "SECURITY"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    VALIDATION = "VALIDATION"
    FILESYSTEM = "FILESYSTEM"
    RUNTIME = "RUNTIME"
    EXTERNAL = "EXTERNAL"
