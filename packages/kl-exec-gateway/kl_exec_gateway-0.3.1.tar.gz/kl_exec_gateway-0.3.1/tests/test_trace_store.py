"""Tests for SQLite trace persistence."""

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from kl_exec_gateway.models import ChatMessage, GatewayTrace, PolicyDecision
from kl_exec_gateway.trace_store import TraceStore


@pytest.fixture
def temp_trace_store(tmp_path: Path) -> TraceStore:
    """Create a temporary trace store for testing."""
    db_path = tmp_path / "test_traces.db"
    return TraceStore(db_path=db_path)


def test_trace_store_init(tmp_path: Path) -> None:
    """Test that trace store initializes correctly."""
    db_path = tmp_path / "test.db"
    store = TraceStore(db_path=db_path)

    assert db_path.exists()
    stats = store.get_stats()
    assert stats["total_traces"] == 0


def test_save_and_retrieve_trace(temp_trace_store: TraceStore) -> None:
    """Test saving and retrieving a trace."""
    trace = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="Hello"),
        raw_model_response="Hi there!",
        effective_chat_response="Hi there!",
        policy_decision=PolicyDecision(allowed=True, code="OK"),
    )

    temp_trace_store.save_trace(trace)

    retrieved = temp_trace_store.get_trace(trace.trace_id)

    assert retrieved is not None
    assert retrieved["trace_id"] == trace.trace_id
    assert retrieved["user_message"] == "Hello"
    assert retrieved["raw_model_response"] == "Hi there!"
    assert retrieved["policy_allowed"] == 1


def test_query_denied_traces(temp_trace_store: TraceStore) -> None:
    """Test querying denied traces."""
    # Save allowed trace
    allowed_trace = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="OK message"),
        raw_model_response="OK",
        effective_chat_response="OK",
        policy_decision=PolicyDecision(allowed=True, code="OK"),
    )
    temp_trace_store.save_trace(allowed_trace)

    # Save denied trace
    denied_trace = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="Bad message"),
        raw_model_response="x" * 1000,
        effective_chat_response="Policy denied.",
        policy_decision=PolicyDecision(
            allowed=False, code="DENY_LENGTH", reason="Too long"
        ),
    )
    temp_trace_store.save_trace(denied_trace)

    # Query denied traces
    denied = temp_trace_store.query_denied_traces(limit=10)

    assert len(denied) == 1
    assert denied[0]["trace_id"] == denied_trace.trace_id
    assert denied[0]["policy_code"] == "DENY_LENGTH"


def test_query_by_policy_code(temp_trace_store: TraceStore) -> None:
    """Test querying traces by policy code."""
    # Save traces with different codes
    for i, code in enumerate(["OK", "DENY_LENGTH", "DENY_PATTERN", "OK"]):
        trace = GatewayTrace.new(
            user_message=ChatMessage(role="user", content=f"Message {i}"),
            raw_model_response=f"Response {i}",
            effective_chat_response=f"Response {i}",
            policy_decision=PolicyDecision(
                allowed=(code == "OK"), code=code, reason=f"Reason {i}"
            ),
        )
        temp_trace_store.save_trace(trace)

    # Query for DENY_LENGTH
    deny_length = temp_trace_store.query_by_policy_code("DENY_LENGTH", limit=10)
    assert len(deny_length) == 1
    assert deny_length[0]["policy_code"] == "DENY_LENGTH"

    # Query for OK
    ok_traces = temp_trace_store.query_by_policy_code("OK", limit=10)
    assert len(ok_traces) == 2


def test_get_stats(temp_trace_store: TraceStore) -> None:
    """Test getting statistics from trace store."""
    # Save some traces
    for i in range(5):
        allowed = i % 2 == 0
        trace = GatewayTrace.new(
            user_message=ChatMessage(role="user", content=f"Message {i}"),
            raw_model_response=f"Response {i}",
            effective_chat_response=f"Response {i}",
            policy_decision=PolicyDecision(
                allowed=allowed, code="OK" if allowed else "DENY_LENGTH"
            ),
        )
        temp_trace_store.save_trace(trace)

    stats = temp_trace_store.get_stats()

    assert stats["total_traces"] == 5
    assert stats["allowed"] == 3  # 0, 2, 4
    assert stats["denied"] == 2  # 1, 3


def test_save_trace_with_transform_details(temp_trace_store: TraceStore) -> None:
    """Test saving trace with transformation details."""
    trace = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="Test"),
        raw_model_response="Response with email@example.com",
        effective_chat_response="Response with [EMAIL]",
        policy_decision=PolicyDecision(allowed=True, code="OK"),
    )

    transform_details = "Sanitization: 1 email(s); Formatting: header spacing"
    temp_trace_store.save_trace(trace, transform_details=transform_details)

    retrieved = temp_trace_store.get_trace(trace.trace_id)

    assert retrieved is not None
    assert retrieved["transform_details"] == transform_details


def test_trace_not_found(temp_trace_store: TraceStore) -> None:
    """Test retrieving non-existent trace."""
    result = temp_trace_store.get_trace("non-existent-id")
    assert result is None

