from typing import List, Tuple

from kl_kernel_logic import Kernel

from kl_exec_gateway.chat_session import GatewayChatSession, ChatModelClient
from kl_exec_gateway.events import EventStore
from kl_exec_gateway.kernel_integration import build_gateway_kernel
import kl_exec_gateway.kernel_integration as kernel_integration
from kl_exec_gateway.models import ChatMessage, GatewayTrace
from kl_exec_gateway.policy_engine import (
    PolicyEngine,
    LengthLimitRule,
    ForbiddenPatternRule,
)


class DummyModelClient(ChatModelClient):
    """
    Minimal stub that always returns the same response.
    """

    def __init__(self, response: str) -> None:
        self._response = response

    def complete(self, messages: List[ChatMessage]) -> str:
        return self._response


def _set_test_policy_engine(max_chars: int) -> None:
    """
    Install a test-specific PolicyEngine into the kernel_integration module.

    This avoids depending on any real policy.config.json on disk.
    """
    engine = PolicyEngine(
        rules=[
            LengthLimitRule(rule_id="length_limit", max_chars=max_chars),
            ForbiddenPatternRule(
                rule_id="forbidden_patterns",
                patterns=("BLOCKME",),
            ),
        ]
    )
    kernel_integration._POLICY_ENGINE = engine  # type: ignore[attr-defined]


def _build_session_with_dummy(response: str, max_chars: int) -> Tuple[GatewayChatSession, EventStore]:
    """
    Build a session with a dummy LLM and a test-specific policy engine.
    """
    kernel: Kernel = build_gateway_kernel()
    store = EventStore()
    model_client = DummyModelClient(response=response)

    _set_test_policy_engine(max_chars=max_chars)

    session = GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=store,
    )
    return session, store


def test_chat_session_allows_short_response() -> None:
    session, store = _build_session_with_dummy("ok", max_chars=100)

    reply, trace = session.send("hello")

    # Chat side (left)
    assert reply == "ok"
    assert isinstance(trace, GatewayTrace)
    assert trace.policy_decision.allowed is True
    assert trace.effective_chat_response == "ok"

    # Insight side (right)
    events = list(store.list_recent(limit=10))
    assert len(events) == 1
    assert events[0].trace_id == trace.trace_id


def test_chat_session_denies_long_response() -> None:
    long_text = "x" * 200
    # For this test we enforce a small limit so the response is denied.
    session, store = _build_session_with_dummy(long_text, max_chars=100)

    reply, trace = session.send("hello")

    # Chat side: neutral message for the user
    assert reply == "Policy denied."
    assert trace.policy_decision.allowed is False
    assert trace.effective_chat_response == "Policy denied."

    # Insight side: full trace including raw response
    events = list(store.list_recent(limit=10))
    assert len(events) == 1
    ev = events[0]
    assert ev.trace_id == trace.trace_id
    assert ev.raw_model_response == long_text
    assert ev.policy_decision.allowed is False
