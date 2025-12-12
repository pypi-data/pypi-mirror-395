"""
Tests for session-level governance (G(V) over conversation).

These tests validate that the session-level implementation follows KL Execution Theory:
- G(V) evaluates entire session behaviour, not just individual requests
- Shadow State (SS) captures session-wide metrics
- Governance is deterministic and non-executing
"""

import pytest
from kl_kernel_logic import Kernel

from kl_exec_gateway import (
    GatewayChatSession,
    EventStore,
    TraceStore,
)
from kl_exec_gateway.session_governance import (
    SessionPolicy,
    SessionGovernor,
    SessionPolicyViolation,
)
from kl_exec_gateway.models import GatewayTrace, ChatMessage, PolicyDecision


class MockModelClient:
    """Mock LLM client for testing."""
    
    def __init__(self, responses=None):
        self.responses = responses or ["Mock response"]
        self.call_count = 0
    
    def complete(self, messages):
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response


def test_session_governor_max_requests():
    """Test session governance denies requests after max_requests limit."""
    policy = SessionPolicy(max_requests=3)
    governor = SessionGovernor(policy)
    
    # First 3 requests should pass pre-check
    for i in range(3):
        decision = governor.evaluate_before_request()
        assert decision.allowed, f"Request {i+1} should be allowed"
        
        # Simulate a completed request
        mock_trace = GatewayTrace.new(
            user_message=ChatMessage(role="user", content=f"Request {i+1}"),
            raw_model_response="Mock response",
            effective_chat_response="Mock response",
            policy_decision=PolicyDecision(allowed=True, code="OK"),
            kernel_policy_trace=None,
        )
        governor.update_after_request(mock_trace)
    
    # 4th request should be denied
    decision = governor.evaluate_before_request()
    assert not decision.allowed
    assert decision.code == "SESSION_MAX_REQUESTS_EXCEEDED"


def test_session_governor_max_violations():
    """Test session governance denies after too many policy violations."""
    policy = SessionPolicy(max_policy_violations=2)
    governor = SessionGovernor(policy)
    
    # First violation - should pass
    mock_trace_1 = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="Request 1"),
        raw_model_response="Denied response",
        effective_chat_response="Policy denied.",
        policy_decision=PolicyDecision(allowed=False, code="DENY"),
        kernel_policy_trace=None,
    )
    governor.update_after_request(mock_trace_1)
    decision = governor.evaluate_after_request()
    assert decision.allowed, "First violation should not block session"
    
    # Second violation - now at limit (2 violations)
    # After this update, we have 2 denials which equals max_policy_violations
    mock_trace_2 = GatewayTrace.new(
        user_message=ChatMessage(role="user", content="Request 2"),
        raw_model_response="Denied response",
        effective_chat_response="Policy denied.",
        policy_decision=PolicyDecision(allowed=False, code="DENY"),
        kernel_policy_trace=None,
    )
    governor.update_after_request(mock_trace_2)
    
    # After 2 violations (at limit), next pre-check should deny
    decision = governor.evaluate_before_request()
    assert not decision.allowed
    assert decision.code == "SESSION_TOO_MANY_VIOLATIONS"


def test_session_governor_state_tracking():
    """Test that session governor correctly tracks state (Shadow State)."""
    policy = SessionPolicy(max_requests=100)
    governor = SessionGovernor(policy)
    
    # Simulate 3 requests
    for i in range(3):
        mock_trace = GatewayTrace.new(
            user_message=ChatMessage(role="user", content=f"Request {i+1}"),
            raw_model_response="Response",
            effective_chat_response="Response",
            policy_decision=PolicyDecision(allowed=True, code="OK"),
            kernel_policy_trace=None,
        )
        mock_trace.step_traces = [
            type('StepTrace', (), {
                'step_type': 'llm',
                'metadata': {'total_tokens': 100}
            })()
        ]
        governor.update_after_request(mock_trace)
    
    # Check Shadow State
    summary = governor.get_session_summary()
    assert summary["state"]["request_count"] == 3
    assert summary["state"]["llm_call_count"] == 3
    assert summary["state"]["total_tokens"] == 300
    assert summary["state"]["policy_denial_count"] == 0


def test_chat_session_with_session_governance():
    """Integration test: ChatSession with session governance."""
    kernel = Kernel()
    model = MockModelClient(responses=["Response 1", "Response 2", "Response 3"])
    event_store = EventStore()
    
    # Create session with max 2 requests
    policy = SessionPolicy(max_requests=2)
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model,
        event_store=event_store,
        session_policy=policy,
    )
    
    # First request - should succeed
    response1, trace1 = session.send("Hello")
    assert response1 is not None
    assert trace1 is not None
    
    # Second request - should succeed
    response2, trace2 = session.send("How are you?")
    assert response2 is not None
    assert trace2 is not None
    
    # Third request - should be denied by session governance
    with pytest.raises(SessionPolicyViolation) as exc_info:
        session.send("Third request")
    
    assert "SESSION_MAX_REQUESTS_EXCEEDED" in str(exc_info.value)


def test_trace_store_session_summary(tmp_path):
    """Test TraceStore.get_session_summary() for session-level Shadow State."""
    db_path = tmp_path / "test_session.db"
    trace_store = TraceStore(db_path=str(db_path))
    
    kernel = Kernel()
    model = MockModelClient(responses=["Response 1", "Response 2", "Response 3"])
    event_store = EventStore()
    
    session = GatewayChatSession(
        kernel=kernel,
        model_client=model,
        event_store=event_store,
        trace_store=trace_store,
    )
    
    # Send 3 requests
    session.send("Request 1")
    session.send("Request 2")
    session.send("Request 3")
    
    # Verify traces were stored
    stats = trace_store.get_stats()
    assert stats["total_traces"] == 3
    
    # Test session summary function exists and returns correct structure
    # Note: correlation_id not yet implemented in traces table
    # This test just verifies the API exists
    summary = trace_store.get_session_summary("test_session")
    assert "session_id" in summary
    assert "total_requests" in summary
    assert "policy_allowed" in summary
    assert "policy_denied" in summary
    assert "step_stats" in summary
    assert "governance_metrics" in summary


def test_session_governor_determinism():
    """Test that governance decisions are deterministic (same input -> same decision)."""
    policy = SessionPolicy(max_requests=5, max_policy_violations=2)
    
    # Create two governors with same policy
    governor1 = SessionGovernor(policy)
    governor2 = SessionGovernor(policy)
    
    # Apply same sequence of traces to both
    for i in range(3):
        mock_trace = GatewayTrace.new(
            user_message=ChatMessage(role="user", content=f"Request {i+1}"),
            raw_model_response="Response",
            effective_chat_response="Response",
            policy_decision=PolicyDecision(allowed=True, code="OK"),
            kernel_policy_trace=None,
        )
        
        governor1.update_after_request(mock_trace)
        governor2.update_after_request(mock_trace)
    
    # Both should produce identical decisions
    decision1 = governor1.evaluate_after_request()
    decision2 = governor2.evaluate_after_request()
    
    assert decision1.allowed == decision2.allowed
    assert decision1.code == decision2.code
    
    # Both should have identical state
    summary1 = governor1.get_session_summary()
    summary2 = governor2.get_session_summary()
    
    assert summary1["state"] == summary2["state"]

