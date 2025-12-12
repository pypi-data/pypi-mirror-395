"""
Session-level Governance (G(V) over entire conversation).

Implements governance over the entire session behaviour V, not just individual steps.
This is the session-level realization of G(V) from KL Execution Theory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List
import logging

from .models import PolicyDecision, GatewayTrace

logger = logging.getLogger(__name__)


@dataclass
class SessionPolicy:
    """
    Policy constraints at session level (G(V) configuration).
    
    These limits apply to the ENTIRE conversation, not individual requests.
    """
    max_requests: Optional[int] = None
    max_llm_calls: Optional[int] = None
    max_policy_violations: int = 3
    max_cost_usd: Optional[float] = None
    max_total_tokens: Optional[int] = None
    
    # Future extensions
    forbidden_topic_switches: List[str] = field(default_factory=list)
    require_gdpr_acknowledgment: bool = False


@dataclass
class SessionState:
    """
    Current state of session-level counters.
    
    This is part of Shadow State (SS) at session level.
    """
    request_count: int = 0
    llm_call_count: int = 0
    policy_violation_count: int = 0
    policy_denial_count: int = 0
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    
    def to_dict(self):
        return {
            "request_count": self.request_count,
            "llm_call_count": self.llm_call_count,
            "policy_violation_count": self.policy_violation_count,
            "policy_denial_count": self.policy_denial_count,
            "total_cost_usd": self.total_cost_usd,
            "total_tokens": self.total_tokens,
        }


class SessionGovernor:
    """
    Session-level governance function G(V).
    
    Evaluates session-wide behaviour against SessionPolicy.
    This implements the G(V) element from KL Execution Theory at session level.
    
    Key properties (from Theory):
    - Non-executing: Only observes and evaluates, does not modify V
    - Behaviour-derived: Decisions based only on observable session history
    - Deterministic: Same session history -> same governance decision
    - Domain-neutral: Evaluates structure (counts, limits), not content semantics
    """
    
    def __init__(self, policy: SessionPolicy):
        self.policy = policy
        self.state = SessionState()
        self.logger = logging.getLogger(f"{__name__}.SessionGovernor")
    
    def evaluate_before_request(self) -> PolicyDecision:
        """
        Evaluate if session can accept another request (pre-check).
        
        Returns:
            PolicyDecision: allowed=False if session limits already exceeded
        """
        # Check request count limit
        if self.policy.max_requests is not None:
            if self.state.request_count >= self.policy.max_requests:
                return PolicyDecision(
                    allowed=False,
                    code="SESSION_MAX_REQUESTS_EXCEEDED",
                    reason=f"Session has reached max requests ({self.policy.max_requests})"
                )
        
        # Check policy violation limit
        if self.state.policy_denial_count >= self.policy.max_policy_violations:
            return PolicyDecision(
                allowed=False,
                code="SESSION_TOO_MANY_VIOLATIONS",
                reason=f"Session has {self.state.policy_denial_count} policy violations (max: {self.policy.max_policy_violations})"
            )
        
        # Check cost limit
        if self.policy.max_cost_usd is not None:
            if self.state.total_cost_usd >= self.policy.max_cost_usd:
                return PolicyDecision(
                    allowed=False,
                    code="SESSION_MAX_COST_EXCEEDED",
                    reason=f"Session cost ${self.state.total_cost_usd:.2f} exceeds limit ${self.policy.max_cost_usd:.2f}"
                )
        
        return PolicyDecision(allowed=True, code="SESSION_OK", reason="Session governance passed")
    
    def update_after_request(self, trace: GatewayTrace) -> None:
        """
        Update session state after a request completes.
        
        This builds the session-level Shadow State (SS).
        
        Args:
            trace: The completed request trace
        """
        # Update request counter
        self.state.request_count += 1
        
        # Count LLM calls from step traces
        if hasattr(trace, 'step_traces') and trace.step_traces:
            llm_steps = [st for st in trace.step_traces if st.step_type == "llm"]
            self.state.llm_call_count += len(llm_steps)
            
            # Extract token counts from metadata (if available)
            for step in llm_steps:
                if "total_tokens" in step.metadata:
                    self.state.total_tokens += step.metadata["total_tokens"]
        
        # Track policy decisions
        if not trace.policy_decision.allowed:
            self.state.policy_denial_count += 1
        
        self.logger.debug(
            f"Session state updated: {self.state.request_count} requests, "
            f"{self.state.llm_call_count} LLM calls, "
            f"{self.state.policy_denial_count} denials"
        )
    
    def evaluate_after_request(self) -> PolicyDecision:
        """
        Evaluate session state after request (post-check).
        
        This can trigger session termination if soft limits are exceeded.
        
        Returns:
            PolicyDecision: Session-level governance decision
        """
        # Same checks as before, but now with updated counters
        return self.evaluate_before_request()
    
    def get_session_summary(self) -> dict:
        """
        Get current session state for audit/debugging.
        
        Returns session-level Shadow State (SS).
        """
        return {
            "policy": {
                "max_requests": self.policy.max_requests,
                "max_llm_calls": self.policy.max_llm_calls,
                "max_policy_violations": self.policy.max_policy_violations,
                "max_cost_usd": self.policy.max_cost_usd,
            },
            "state": self.state.to_dict(),
            "limits_reached": {
                "requests": self.policy.max_requests is not None and self.state.request_count >= self.policy.max_requests,
                "violations": self.state.policy_denial_count >= self.policy.max_policy_violations,
                "cost": self.policy.max_cost_usd is not None and self.state.total_cost_usd >= self.policy.max_cost_usd,
            }
        }


class SessionPolicyViolation(Exception):
    """Raised when session-level governance denies a request."""
    
    def __init__(self, decision: PolicyDecision):
        self.decision = decision
        super().__init__(f"Session policy violation: {decision.code} - {decision.reason}")

