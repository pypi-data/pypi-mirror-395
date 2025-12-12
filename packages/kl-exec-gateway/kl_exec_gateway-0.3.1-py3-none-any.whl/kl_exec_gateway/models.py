from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from kl_kernel_logic import ExecutionTrace


Role = Literal["user", "assistant", "system"]


@dataclass
class ChatMessage:
    role: Role
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PolicyDecision:
    allowed: bool
    reason: Optional[str] = None
    code: Optional[str] = None  # e.g. "OK", "DENY_LENGTH", "DENY_PATTERN"
    rule_id: Optional[str] = None  # ID of the rule that decided


@dataclass
class GatewayTrace:
    trace_id: str
    user_message: ChatMessage
    raw_model_response: str
    effective_chat_response: str
    policy_decision: PolicyDecision
    kernel_policy_trace: Optional[ExecutionTrace] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    step_traces: list = field(default_factory=list)  # List of StepTrace objects

    @staticmethod
    def new(
        user_message: ChatMessage,
        raw_model_response: str,
        effective_chat_response: str,
        policy_decision: PolicyDecision,
        kernel_policy_trace: Optional[ExecutionTrace] = None,
    ) -> "GatewayTrace":
        return GatewayTrace(
            trace_id=str(uuid4()),
            user_message=user_message,
            raw_model_response=raw_model_response,
            effective_chat_response=effective_chat_response,
            policy_decision=policy_decision,
            kernel_policy_trace=kernel_policy_trace,
        )
