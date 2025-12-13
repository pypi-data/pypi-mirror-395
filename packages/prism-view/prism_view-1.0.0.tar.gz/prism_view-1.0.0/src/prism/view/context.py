"""
LogContext implementation for prism-view.

Provides context management for service, request, user, session, transaction,
batch, and operation tracking. Uses contextvars for async-safe, thread-safe
context propagation.

Features:
    - Service context: Global service info (name, version, environment)
    - Request context: Per-request tracking (trace_id, span_id)
    - User context: User identification (user_id, email, role)
    - Session context: Session tracking (session_id)
    - Transaction context: Transaction tracking (transaction_id, type)
    - Batch context: Batch processing (batch_id, item_index, total_items)
    - Operation context: Timed operations with duration_ms
    - Context nesting and merging
    - Async-safe via contextvars

Example:
    >>> from prism.view.context import LogContext
    >>>
    >>> # Set service-level context (global)
    >>> LogContext.set_service(name="payment-api", version="1.0.0")
    >>>
    >>> # Request-level context (scoped)
    >>> with LogContext.request(trace_id="abc-123"):
    ...     with LogContext.user(user_id="user-456"):
    ...         ctx = LogContext.get_current()
    ...         print(ctx)  # Has service, trace_id, user_id
    ...
    >>> # Operation timing
    >>> with LogContext.operation(name="db_query") as op:
    ...     # do work
    ...     pass
    >>> print(op["duration_ms"])  # Time in milliseconds
"""

import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Dict, Generator, Optional


# Context variables for different context types
_service_context: ContextVar[Dict[str, Any]] = ContextVar("service_context", default={})
_request_context: ContextVar[Dict[str, Any]] = ContextVar("request_context", default={})
_user_context: ContextVar[Dict[str, Any]] = ContextVar("user_context", default={})
_session_context: ContextVar[Dict[str, Any]] = ContextVar("session_context", default={})
_transaction_context: ContextVar[Dict[str, Any]] = ContextVar("transaction_context", default={})
_batch_context: ContextVar[Dict[str, Any]] = ContextVar("batch_context", default={})
_operation_context: ContextVar[Dict[str, Any]] = ContextVar("operation_context", default={})
_custom_context: ContextVar[Dict[str, Any]] = ContextVar("custom_context", default={})

# System fields that cannot be overridden by add()
_SYSTEM_FIELDS = frozenset(
    {
        "service",
        "version",
        "environment",
        "trace_id",
        "span_id",
        "user_id",
        "session_id",
        "transaction_id",
        "transaction_type",
        "batch_id",
        "item_index",
        "total_items",
        "operation",
        "started_at",
        "duration_ms",
    }
)


class LogContext:
    """
    Context management for structured logging.

    Provides methods to set and retrieve context at various scopes:
    - Service: Global, set once at startup
    - Request: Per-request, scoped to context manager
    - User: Per-user, scoped to context manager
    - Session: Per-session, scoped to context manager
    - Transaction: Per-transaction, scoped to context manager
    - Batch: Per-batch item, scoped to context manager
    - Operation: Timed operations, scoped to context manager

    All context managers properly nest and merge their contexts.
    Uses contextvars for async-safe and thread-safe propagation.
    """

    @staticmethod
    def set_service(
        name: str,
        version: Optional[str] = None,
        environment: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Set service-level context (global).

        This is typically called once at application startup.

        Args:
            name: The service name (e.g., "payment-api")
            version: The service version (e.g., "1.0.0")
            environment: The environment (e.g., "production", "staging")
            **kwargs: Additional custom fields

        Example:
            >>> LogContext.set_service(
            ...     name="api",
            ...     version="1.0.0",
            ...     environment="production",
            ...     region="us-west-2",
            ... )
        """
        ctx: Dict[str, Any] = {"service": name}
        if version is not None:
            ctx["version"] = version
        if environment is not None:
            ctx["environment"] = environment
        ctx.update(kwargs)
        _service_context.set(ctx)

    @staticmethod
    def get_current() -> Dict[str, Any]:
        """
        Get the current merged context from all active scopes.

        Returns:
            Dictionary containing all context fields from all active scopes.
            Returns empty dict if no context is set.

        Example:
            >>> LogContext.set_service(name="api")
            >>> with LogContext.request(trace_id="abc"):
            ...     ctx = LogContext.get_current()
            ...     print(ctx)  # {'service': 'api', 'trace_id': 'abc'}
        """
        result: Dict[str, Any] = {}

        # Merge all contexts in order (later contexts can override earlier)
        result.update(_service_context.get())
        result.update(_request_context.get())
        result.update(_user_context.get())
        result.update(_session_context.get())
        result.update(_transaction_context.get())
        result.update(_batch_context.get())
        result.update(_operation_context.get())
        result.update(_custom_context.get())

        return result

    @staticmethod
    def clear() -> None:
        """
        Clear all context.

        This removes all context from all scopes. Useful for testing
        or when starting fresh.

        Example:
            >>> LogContext.set_service(name="api")
            >>> LogContext.clear()
            >>> LogContext.get_current()
            {}
        """
        _service_context.set({})
        _request_context.set({})
        _user_context.set({})
        _session_context.set({})
        _transaction_context.set({})
        _batch_context.set({})
        _operation_context.set({})
        _custom_context.set({})

    @staticmethod
    @contextmanager
    def request(
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Generator[None, None, None]:
        """
        Set request-level context (scoped).

        Creates a context manager that sets request context for the duration
        of the with block. Auto-generates trace_id if not provided.

        Args:
            trace_id: The trace ID for distributed tracing. Auto-generated if None.
            span_id: The span ID for distributed tracing.
            **kwargs: Additional custom fields (method, path, etc.)

        Yields:
            None

        Example:
            >>> with LogContext.request(trace_id="abc-123", method="POST"):
            ...     # trace_id and method available here
            ...     pass
            >>> # trace_id and method no longer available
        """
        ctx: Dict[str, Any] = {
            "trace_id": trace_id if trace_id is not None else str(uuid.uuid4()),
        }
        if span_id is not None:
            ctx["span_id"] = span_id
        ctx.update(kwargs)

        token = _request_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield
        finally:
            _custom_context.reset(custom_token)
            _request_context.reset(token)

    @staticmethod
    @contextmanager
    def user(user_id: str, **kwargs: Any) -> Generator[None, None, None]:
        """
        Set user-level context (scoped).

        Args:
            user_id: The user identifier
            **kwargs: Additional custom fields (email, role, etc.)

        Yields:
            None

        Example:
            >>> with LogContext.user(user_id="user-123", role="admin"):
            ...     # user_id and role available here
            ...     pass
        """
        ctx: Dict[str, Any] = {"user_id": user_id}
        ctx.update(kwargs)

        token = _user_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield
        finally:
            _custom_context.reset(custom_token)
            _user_context.reset(token)

    @staticmethod
    @contextmanager
    def session(session_id: str, **kwargs: Any) -> Generator[None, None, None]:
        """
        Set session-level context (scoped).

        Args:
            session_id: The session identifier
            **kwargs: Additional custom fields (device, ip_address, etc.)

        Yields:
            None

        Example:
            >>> with LogContext.session(session_id="sess-abc", device="mobile"):
            ...     # session_id and device available here
            ...     pass
        """
        ctx: Dict[str, Any] = {"session_id": session_id}
        ctx.update(kwargs)

        token = _session_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield
        finally:
            _custom_context.reset(custom_token)
            _session_context.reset(token)

    @staticmethod
    @contextmanager
    def transaction(
        transaction_id: str,
        transaction_type: Optional[str] = None,
        **kwargs: Any,
    ) -> Generator[None, None, None]:
        """
        Set transaction-level context (scoped).

        Args:
            transaction_id: The transaction identifier
            transaction_type: The type of transaction (e.g., "payment", "refund")
            **kwargs: Additional custom fields (amount, currency, etc.)

        Yields:
            None

        Example:
            >>> with LogContext.transaction(
            ...     transaction_id="txn-123",
            ...     transaction_type="payment",
            ...     amount=99.99,
            ... ):
            ...     # transaction context available here
            ...     pass
        """
        ctx: Dict[str, Any] = {"transaction_id": transaction_id}
        if transaction_type is not None:
            ctx["transaction_type"] = transaction_type
        ctx.update(kwargs)

        token = _transaction_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield
        finally:
            _custom_context.reset(custom_token)
            _transaction_context.reset(token)

    @staticmethod
    @contextmanager
    def batch(
        batch_id: str,
        item_index: Optional[int] = None,
        total_items: Optional[int] = None,
        **kwargs: Any,
    ) -> Generator[None, None, None]:
        """
        Set batch-level context (scoped).

        Useful for tracking progress through batch processing jobs.

        Args:
            batch_id: The batch identifier
            item_index: Current item index (0-based)
            total_items: Total number of items in the batch
            **kwargs: Additional custom fields (source, retry_count, etc.)

        Yields:
            None

        Example:
            >>> for i, item in enumerate(items):
            ...     with LogContext.batch(
            ...         batch_id="batch-001",
            ...         item_index=i,
            ...         total_items=len(items),
            ...     ):
            ...         # process item
            ...         pass
        """
        ctx: Dict[str, Any] = {"batch_id": batch_id}
        if item_index is not None:
            ctx["item_index"] = item_index
        if total_items is not None:
            ctx["total_items"] = total_items
        ctx.update(kwargs)

        token = _batch_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield
        finally:
            _custom_context.reset(custom_token)
            _batch_context.reset(token)

    @staticmethod
    @contextmanager
    def operation(name: str, **kwargs: Any) -> Generator[Dict[str, Any], None, None]:
        """
        Set operation-level context with automatic duration tracking.

        Tracks the operation name, start time, and calculates duration_ms
        when the context manager exits.

        Args:
            name: The operation name (e.g., "db_query", "api_call")
            **kwargs: Additional metadata (table, query_type, etc.)

        Yields:
            Dict containing operation context. After exit, includes duration_ms.

        Example:
            >>> with LogContext.operation(name="fetch_user", table="users") as op:
            ...     # do database query
            ...     result = db.query("SELECT * FROM users")
            >>> print(f"Query took {op['duration_ms']}ms")
        """
        start_time = time.perf_counter()
        started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        ctx: Dict[str, Any] = {
            "operation": name,
            "started_at": started_at,
        }
        ctx.update(kwargs)

        token = _operation_context.set(ctx)
        custom_token = _custom_context.set(_custom_context.get().copy())
        try:
            yield ctx
        finally:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            ctx["duration_ms"] = duration_ms
            _custom_context.reset(custom_token)
            _operation_context.reset(token)

    @staticmethod
    def add(**kwargs: Any) -> None:
        """
        Add custom fields to the current context.

        Fields added via add() are scoped to the current context and will
        be removed when the enclosing context manager exits.

        System fields (trace_id, user_id, etc.) cannot be overridden.

        Args:
            **kwargs: Custom key-value pairs to add

        Example:
            >>> with LogContext.request(trace_id="abc"):
            ...     LogContext.add(custom_field="value")
            ...     ctx = LogContext.get_current()
            ...     print(ctx["custom_field"])  # "value"
        """
        current = _custom_context.get().copy()

        # Filter out system fields
        for key, value in kwargs.items():
            if key not in _SYSTEM_FIELDS:
                current[key] = value

        _custom_context.set(current)
