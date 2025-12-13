"""
Tests for LogContext - context management for structured logging.

Tests cover:
- Service context (set_service, get_current)
- Request context (scoped, trace_id generation)
- User context (scoped, custom fields)
- Session context (session_id tracking)
- Transaction context (transaction_type, custom fields)
- Batch context (item_index, total_items)
- Operation context (duration tracking)
- Context nesting and merging
- Custom fields (add method)
"""

import asyncio
import time
import uuid
from datetime import datetime, timezone

import pytest


class TestServiceContext:
    """Tests for LogContext.set_service() and get_current()."""

    def test_set_service_stores_service_name(self):
        """LogContext.set_service() stores the service name."""
        from prism.view.context import LogContext

        LogContext.set_service(name="payment-service")
        ctx = LogContext.get_current()

        assert ctx["service"] == "payment-service"

    def test_set_service_stores_version(self):
        """LogContext.set_service() stores the service version."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api", version="1.2.3")
        ctx = LogContext.get_current()

        assert ctx["service"] == "api"
        assert ctx["version"] == "1.2.3"

    def test_set_service_stores_environment(self):
        """LogContext.set_service() stores the environment."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api", environment="production")
        ctx = LogContext.get_current()

        assert ctx["environment"] == "production"

    def test_set_service_accepts_custom_fields(self):
        """LogContext.set_service() accepts arbitrary custom fields."""
        from prism.view.context import LogContext

        LogContext.set_service(
            name="api",
            region="us-west-2",
            instance_id="i-1234567890abcdef0",
        )
        ctx = LogContext.get_current()

        assert ctx["service"] == "api"
        assert ctx["region"] == "us-west-2"
        assert ctx["instance_id"] == "i-1234567890abcdef0"

    def test_get_current_returns_empty_dict_when_no_context(self):
        """LogContext.get_current() returns empty dict when no context set."""
        from prism.view.context import LogContext

        LogContext.clear()
        ctx = LogContext.get_current()

        assert ctx == {}

    def test_set_service_overwrites_previous_service(self):
        """Calling set_service() again overwrites the previous service context."""
        from prism.view.context import LogContext

        LogContext.set_service(name="old-service")
        LogContext.set_service(name="new-service")
        ctx = LogContext.get_current()

        assert ctx["service"] == "new-service"

    def test_clear_removes_all_context(self):
        """LogContext.clear() removes all context."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api")
        LogContext.clear()
        ctx = LogContext.get_current()

        assert ctx == {}


class TestRequestContext:
    """Tests for LogContext.request() context manager."""

    def test_request_sets_trace_id(self):
        """LogContext.request() sets the trace_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="abc-123"):
            ctx = LogContext.get_current()
            assert ctx["trace_id"] == "abc-123"

    def test_request_auto_generates_trace_id(self):
        """LogContext.request() auto-generates trace_id if not provided."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request():
            ctx = LogContext.get_current()
            assert "trace_id" in ctx
            # Should be a valid UUID format
            uuid.UUID(ctx["trace_id"])

    def test_request_is_scoped(self):
        """Request context is removed when exiting the context manager."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="abc-123"):
            pass  # Context active here

        ctx = LogContext.get_current()
        assert "trace_id" not in ctx

    def test_request_merges_with_service_context(self):
        """Request context merges with existing service context."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api", version="1.0.0")
        with LogContext.request(trace_id="abc-123"):
            ctx = LogContext.get_current()
            assert ctx["service"] == "api"
            assert ctx["version"] == "1.0.0"
            assert ctx["trace_id"] == "abc-123"

    def test_request_accepts_custom_fields(self):
        """LogContext.request() accepts custom fields."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(
            trace_id="abc-123",
            method="POST",
            path="/api/users",
        ):
            ctx = LogContext.get_current()
            assert ctx["method"] == "POST"
            assert ctx["path"] == "/api/users"

    def test_request_sets_span_id(self):
        """LogContext.request() can set a span_id for distributed tracing."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="abc-123", span_id="span-456"):
            ctx = LogContext.get_current()
            assert ctx["span_id"] == "span-456"


class TestUserContext:
    """Tests for LogContext.user() context manager."""

    def test_user_sets_user_id(self):
        """LogContext.user() sets the user_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.user(user_id="user-123"):
            ctx = LogContext.get_current()
            assert ctx["user_id"] == "user-123"

    def test_user_is_scoped(self):
        """User context is removed when exiting the context manager."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.user(user_id="user-123"):
            pass

        ctx = LogContext.get_current()
        assert "user_id" not in ctx

    def test_user_merges_with_service_and_request(self):
        """User context merges with service and request contexts."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api")
        with LogContext.request(trace_id="trace-123"):
            with LogContext.user(user_id="user-456"):
                ctx = LogContext.get_current()
                assert ctx["service"] == "api"
                assert ctx["trace_id"] == "trace-123"
                assert ctx["user_id"] == "user-456"

    def test_user_accepts_custom_fields(self):
        """LogContext.user() accepts custom fields."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.user(
            user_id="user-123",
            email="user@example.com",
            role="admin",
        ):
            ctx = LogContext.get_current()
            assert ctx["email"] == "user@example.com"
            assert ctx["role"] == "admin"


class TestSessionContext:
    """Tests for LogContext.session() context manager."""

    def test_session_sets_session_id(self):
        """LogContext.session() sets the session_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.session(session_id="sess-abc"):
            ctx = LogContext.get_current()
            assert ctx["session_id"] == "sess-abc"

    def test_session_is_scoped(self):
        """Session context is removed when exiting the context manager."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.session(session_id="sess-abc"):
            pass

        ctx = LogContext.get_current()
        assert "session_id" not in ctx

    def test_session_accepts_custom_fields(self):
        """LogContext.session() accepts custom fields."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.session(
            session_id="sess-abc",
            device="mobile",
            ip_address="192.168.1.1",
        ):
            ctx = LogContext.get_current()
            assert ctx["device"] == "mobile"
            assert ctx["ip_address"] == "192.168.1.1"


class TestTransactionContext:
    """Tests for LogContext.transaction() context manager."""

    def test_transaction_sets_transaction_id(self):
        """LogContext.transaction() sets the transaction_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.transaction(transaction_id="txn-123"):
            ctx = LogContext.get_current()
            assert ctx["transaction_id"] == "txn-123"

    def test_transaction_sets_transaction_type(self):
        """LogContext.transaction() sets the transaction_type."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.transaction(
            transaction_id="txn-123",
            transaction_type="payment",
        ):
            ctx = LogContext.get_current()
            assert ctx["transaction_type"] == "payment"

    def test_transaction_is_scoped(self):
        """Transaction context is removed when exiting."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.transaction(transaction_id="txn-123"):
            pass

        ctx = LogContext.get_current()
        assert "transaction_id" not in ctx

    def test_transaction_accepts_custom_fields(self):
        """LogContext.transaction() accepts custom fields."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.transaction(
            transaction_id="txn-123",
            amount=99.99,
            currency="USD",
        ):
            ctx = LogContext.get_current()
            assert ctx["amount"] == 99.99
            assert ctx["currency"] == "USD"


class TestBatchContext:
    """Tests for LogContext.batch() context manager."""

    def test_batch_sets_batch_id(self):
        """LogContext.batch() sets the batch_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.batch(batch_id="batch-001"):
            ctx = LogContext.get_current()
            assert ctx["batch_id"] == "batch-001"

    def test_batch_tracks_item_index(self):
        """LogContext.batch() tracks item_index."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.batch(batch_id="batch-001", item_index=5):
            ctx = LogContext.get_current()
            assert ctx["item_index"] == 5

    def test_batch_tracks_total_items(self):
        """LogContext.batch() tracks total_items."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.batch(
            batch_id="batch-001",
            item_index=5,
            total_items=100,
        ):
            ctx = LogContext.get_current()
            assert ctx["total_items"] == 100

    def test_batch_is_scoped(self):
        """Batch context is removed when exiting."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.batch(batch_id="batch-001"):
            pass

        ctx = LogContext.get_current()
        assert "batch_id" not in ctx

    def test_batch_accepts_custom_fields(self):
        """LogContext.batch() accepts custom fields."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.batch(
            batch_id="batch-001",
            source="import-job",
            retry_count=2,
        ):
            ctx = LogContext.get_current()
            assert ctx["source"] == "import-job"
            assert ctx["retry_count"] == 2


class TestOperationContext:
    """Tests for LogContext.operation() context manager with duration tracking."""

    def test_operation_captures_operation_name(self):
        """LogContext.operation() captures the operation name."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.operation(name="fetch_user"):
            ctx = LogContext.get_current()
            assert ctx["operation"] == "fetch_user"

    def test_operation_captures_started_at(self):
        """LogContext.operation() captures started_at timestamp."""
        from prism.view.context import LogContext

        LogContext.clear()
        before = datetime.now(timezone.utc)
        with LogContext.operation(name="process"):
            ctx = LogContext.get_current()
            assert "started_at" in ctx
            # Parse the ISO timestamp
            started = datetime.fromisoformat(ctx["started_at"].replace("Z", "+00:00"))
            assert started >= before

    def test_operation_calculates_duration_ms_on_exit(self):
        """LogContext.operation() calculates duration_ms on exit."""
        from prism.view.context import LogContext

        LogContext.clear()

        class DurationCapture:
            def __init__(self):
                self.duration = None

        capture = DurationCapture()

        with LogContext.operation(name="slow_op") as op_ctx:
            time.sleep(0.05)  # 50ms
            capture.duration = op_ctx

        # Duration should be captured in the operation context
        assert capture.duration is not None
        assert "duration_ms" in capture.duration
        assert capture.duration["duration_ms"] >= 50

    def test_operation_duration_is_accurate(self):
        """Operation duration is accurate within reasonable tolerance."""
        from prism.view.context import LogContext

        LogContext.clear()

        with LogContext.operation(name="timed_op") as op_ctx:
            time.sleep(0.1)  # 100ms

        # Should be approximately 100ms (wider tolerance for CI environments)
        assert 50 <= op_ctx["duration_ms"] <= 500

    def test_operation_accepts_metadata(self):
        """LogContext.operation() accepts metadata."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.operation(
            name="db_query",
            table="users",
            query_type="SELECT",
        ):
            ctx = LogContext.get_current()
            assert ctx["table"] == "users"
            assert ctx["query_type"] == "SELECT"

    def test_operation_is_scoped(self):
        """Operation context is removed when exiting."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.operation(name="temp_op"):
            pass

        ctx = LogContext.get_current()
        assert "operation" not in ctx


class TestContextNesting:
    """Tests for context nesting and merging."""

    def test_contexts_nest_properly(self):
        """Contexts nest properly (service -> request -> user)."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api", version="1.0.0")

        with LogContext.request(trace_id="trace-123"):
            with LogContext.user(user_id="user-456"):
                ctx = LogContext.get_current()
                assert ctx["service"] == "api"
                assert ctx["version"] == "1.0.0"
                assert ctx["trace_id"] == "trace-123"
                assert ctx["user_id"] == "user-456"

    def test_get_current_merges_all_active_contexts(self):
        """get_current() merges all active contexts."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api")

        with LogContext.request(trace_id="trace-123"):
            with LogContext.user(user_id="user-456"):
                with LogContext.session(session_id="sess-789"):
                    ctx = LogContext.get_current()
                    assert len(ctx) >= 4
                    assert "service" in ctx
                    assert "trace_id" in ctx
                    assert "user_id" in ctx
                    assert "session_id" in ctx

    def test_inner_contexts_dont_leak_to_outer_scopes(self):
        """Inner contexts don't leak to outer scopes."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api")

        with LogContext.request(trace_id="trace-123"):
            with LogContext.user(user_id="user-456"):
                pass  # user context ends here

            ctx = LogContext.get_current()
            assert "user_id" not in ctx
            assert "trace_id" in ctx

        ctx = LogContext.get_current()
        assert "trace_id" not in ctx
        assert "service" in ctx

    def test_context_clears_on_scope_exit(self):
        """Context clears when exiting scope."""
        from prism.view.context import LogContext

        LogContext.clear()

        with LogContext.request(trace_id="trace-123"):
            assert "trace_id" in LogContext.get_current()

        assert "trace_id" not in LogContext.get_current()

    def test_deep_nesting_works_correctly(self):
        """Deep nesting (5+ levels) works correctly."""
        from prism.view.context import LogContext

        LogContext.set_service(name="api")

        with LogContext.request(trace_id="t1"):
            with LogContext.user(user_id="u1"):
                with LogContext.session(session_id="s1"):
                    with LogContext.transaction(transaction_id="tx1"):
                        with LogContext.operation(name="op1"):
                            ctx = LogContext.get_current()
                            assert ctx["service"] == "api"
                            assert ctx["trace_id"] == "t1"
                            assert ctx["user_id"] == "u1"
                            assert ctx["session_id"] == "s1"
                            assert ctx["transaction_id"] == "tx1"
                            assert ctx["operation"] == "op1"


class TestAsyncContextPropagation:
    """Tests for async context propagation."""

    @pytest.mark.asyncio
    async def test_context_propagates_across_await(self):
        """Context propagates across await boundaries."""
        from prism.view.context import LogContext

        LogContext.clear()

        async def inner():
            await asyncio.sleep(0.01)
            return LogContext.get_current()

        with LogContext.request(trace_id="async-trace"):
            ctx = await inner()
            assert ctx["trace_id"] == "async-trace"

    @pytest.mark.asyncio
    async def test_context_works_with_asyncio_gather(self):
        """Context works with asyncio.gather()."""
        from prism.view.context import LogContext

        LogContext.clear()

        async def task(n):
            await asyncio.sleep(0.01)
            ctx = LogContext.get_current()
            return ctx.get("trace_id")

        with LogContext.request(trace_id="gather-trace"):
            results = await asyncio.gather(task(1), task(2), task(3))
            assert all(r == "gather-trace" for r in results)

    @pytest.mark.asyncio
    async def test_context_works_with_create_task(self):
        """Context works with asyncio.create_task()."""
        from prism.view.context import LogContext

        LogContext.clear()
        results = []

        async def background_task():
            await asyncio.sleep(0.01)
            ctx = LogContext.get_current()
            results.append(ctx.get("trace_id"))

        with LogContext.request(trace_id="task-trace"):
            task = asyncio.create_task(background_task())
            await task

        assert results == ["task-trace"]

    @pytest.mark.asyncio
    async def test_async_contexts_are_isolated(self):
        """Different async tasks have isolated contexts when set separately."""
        from prism.view.context import LogContext

        LogContext.clear()
        results = []

        async def task_with_context(trace_id):
            with LogContext.request(trace_id=trace_id):
                await asyncio.sleep(0.01)
                ctx = LogContext.get_current()
                results.append(ctx.get("trace_id"))

        await asyncio.gather(
            task_with_context("trace-a"),
            task_with_context("trace-b"),
        )

        assert "trace-a" in results
        assert "trace-b" in results


class TestCustomFields:
    """Tests for LogContext.add() custom fields."""

    def test_add_adds_custom_fields(self):
        """LogContext.add() adds custom fields to current context."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="trace-123"):
            LogContext.add(custom_field="custom_value")
            ctx = LogContext.get_current()
            assert ctx["custom_field"] == "custom_value"

    def test_add_merges_with_existing(self):
        """LogContext.add() merges with existing context."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="trace-123"):
            LogContext.add(field1="value1")
            LogContext.add(field2="value2")
            ctx = LogContext.get_current()
            assert ctx["trace_id"] == "trace-123"
            assert ctx["field1"] == "value1"
            assert ctx["field2"] == "value2"

    def test_add_does_not_override_system_fields(self):
        """LogContext.add() does not override system fields like trace_id."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="original-trace"):
            # Attempting to override trace_id should not work
            LogContext.add(trace_id="hacked-trace")
            ctx = LogContext.get_current()
            # System field should be preserved
            assert ctx["trace_id"] == "original-trace"

    def test_add_is_scoped(self):
        """Custom fields added via add() are scoped to current context."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="trace-123"):
            LogContext.add(scoped_field="scoped_value")

        ctx = LogContext.get_current()
        assert "scoped_field" not in ctx

    def test_add_multiple_fields_at_once(self):
        """LogContext.add() can add multiple fields at once."""
        from prism.view.context import LogContext

        LogContext.clear()
        with LogContext.request(trace_id="trace-123"):
            LogContext.add(
                field1="value1",
                field2="value2",
                field3="value3",
            )
            ctx = LogContext.get_current()
            assert ctx["field1"] == "value1"
            assert ctx["field2"] == "value2"
            assert ctx["field3"] == "value3"
