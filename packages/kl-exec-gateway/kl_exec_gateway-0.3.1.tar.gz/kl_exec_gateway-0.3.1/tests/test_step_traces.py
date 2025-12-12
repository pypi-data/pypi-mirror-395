"""Tests for step-by-step trace persistence (Phase 2)."""

from pathlib import Path

import pytest

from kl_exec_gateway.chat_session import GatewayChatSession
from kl_exec_gateway.events import EventStore
from kl_exec_gateway.kernel_integration import build_gateway_kernel
from kl_exec_gateway.models import ChatMessage
from kl_exec_gateway.trace_store import TraceStore

# Import test helper
import sys
sys.path.insert(0, str(Path(__file__).parent))
from test_chat_session import DummyModelClient, _set_test_policy_engine


@pytest.fixture
def temp_trace_store_with_steps(tmp_path: Path) -> TraceStore:
    """Create a temporary trace store for step testing."""
    db_path = tmp_path / "test_step_traces.db"
    return TraceStore(db_path=db_path)


def test_step_traces_are_persisted(temp_trace_store_with_steps: TraceStore) -> None:
    """Test that each pipeline step creates a trace entry."""
    kernel = build_gateway_kernel()
    event_store = EventStore()
    model_client = DummyModelClient(response="Test response")
    
    _set_test_policy_engine(max_chars=100)
    
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=temp_trace_store_with_steps,
        enable_sanitization=True,
        enable_formatting=True,
    )
    
    # Send message
    reply, trace = session.send("Hello")
    
    # Verify step traces were persisted
    step_traces = temp_trace_store_with_steps.get_step_traces(trace.trace_id)
    
    # Should have 5 steps: llm, policy, sanitize, format, finalize
    assert len(step_traces) == 5
    
    # Verify step sequence
    step_ids = [st["step_id"] for st in step_traces]
    assert step_ids == [
        "llm_call",
        "policy_check",
        "sanitize_pii",
        "format_markdown",
        "finalize",
    ]
    
    # Verify step types
    step_types = [st["step_type"] for st in step_traces]
    assert step_types == [
        "llm",
        "policy",
        "transform",
        "transform",
        "finalize",
    ]
    
    # Verify sequence indices
    for idx, st in enumerate(step_traces):
        assert st["sequence_index"] == idx


def test_step_trace_contains_input_output(temp_trace_store_with_steps: TraceStore) -> None:
    """Test that step traces contain input and output snapshots."""
    import json
    
    kernel = build_gateway_kernel()
    event_store = EventStore()
    model_client = DummyModelClient(response="Test response")
    
    _set_test_policy_engine(max_chars=100)
    
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=temp_trace_store_with_steps,
    )
    
    # Send message
    reply, trace = session.send("Hello")
    
    # Get step traces
    step_traces = temp_trace_store_with_steps.get_step_traces(trace.trace_id)
    
    # Check LLM step
    llm_step = step_traces[0]
    llm_input = json.loads(llm_step["input_json"])
    llm_output = json.loads(llm_step["output_json"])
    
    assert llm_input["user_text"] == "Hello"
    assert llm_output["response"] == "Test response"
    
    # Check policy step
    policy_step = step_traces[1]
    policy_output = json.loads(policy_step["output_json"])
    
    assert policy_output["allowed"] is True
    assert policy_output["code"] == "OK"


def test_step_trace_shows_denied_policy(temp_trace_store_with_steps: TraceStore) -> None:
    """Test that denied policy is visible in step traces."""
    import json
    
    kernel = build_gateway_kernel()
    event_store = EventStore()
    
    # Create a very long response that will be denied
    long_response = "x" * 200
    model_client = DummyModelClient(response=long_response)
    
    _set_test_policy_engine(max_chars=100)
    
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=temp_trace_store_with_steps,
    )
    
    # Send message
    reply, trace = session.send("Hello")
    
    # Get step traces
    step_traces = temp_trace_store_with_steps.get_step_traces(trace.trace_id)
    
    # Check policy step
    policy_step = [st for st in step_traces if st["step_id"] == "policy_check"][0]
    policy_output = json.loads(policy_step["output_json"])
    
    assert policy_output["allowed"] is False
    assert policy_output["code"] == "DENY_LENGTH"
    assert "too long" in policy_output["reason"].lower()


def test_replay_from_step_traces(temp_trace_store_with_steps: TraceStore) -> None:
    """Test that step traces contain enough info for replay."""
    import json
    
    kernel = build_gateway_kernel()
    event_store = EventStore()
    model_client = DummyModelClient(response="Original response")
    
    _set_test_policy_engine(max_chars=100)
    
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=temp_trace_store_with_steps,
        enable_sanitization=True,
    )
    
    # Send message
    reply, trace = session.send("Hello")
    
    # Get step traces
    step_traces = temp_trace_store_with_steps.get_step_traces(trace.trace_id)
    
    # Verify we can reconstruct the flow from traces
    llm_step = step_traces[0]
    policy_step = step_traces[1]
    sanitize_step = step_traces[2]
    
    # Reconstruct: user input → LLM output
    llm_input = json.loads(llm_step["input_json"])
    llm_output = json.loads(llm_step["output_json"])
    assert llm_input["user_text"] == "Hello"
    assert llm_output["response"] == "Original response"
    
    # Reconstruct: LLM output → Policy decision
    policy_output = json.loads(policy_step["output_json"])
    assert policy_output["allowed"] is True
    
    # Reconstruct: Policy allowed → Sanitize applied (or not)
    sanitize_output = json.loads(sanitize_step["output_json"])
    # In this case, no PII to sanitize
    assert "applied" in sanitize_output
    
    # This demonstrates that the trace contains the complete execution path


def test_step_traces_without_trace_store() -> None:
    """Test that pipeline works without trace_store (backward compat)."""
    kernel = build_gateway_kernel()
    event_store = EventStore()
    model_client = DummyModelClient(response="Test")
    
    _set_test_policy_engine(max_chars=100)
    
    # No trace_store
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=None,  # Explicitly None
    )
    
    # Should still work
    reply, trace = session.send("Hello")
    
    assert reply == "Test"
    assert trace.trace_id is not None
    
    # EventStore should have the trace
    events = list(event_store.list_recent(limit=10))
    assert len(events) == 1

