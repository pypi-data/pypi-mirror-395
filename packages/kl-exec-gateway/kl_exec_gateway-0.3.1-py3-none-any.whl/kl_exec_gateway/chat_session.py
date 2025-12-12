# src/kl_exec_gateway/chat_session.py

from __future__ import annotations

import logging
from typing import Optional, Protocol, Tuple

from kl_kernel_logic import Kernel

from .events import EventStore
from .models import ChatMessage, GatewayTrace
from .orchestrator import GatewayOrchestrator, GatewayRequest
from .pipeline_registry import create_default_registry
from .pipeline_types import Pipeline
from .pipelines import DEFAULT_CHAT_PIPELINE
from .trace_store import TraceStore
from .session_governance import SessionPolicy, SessionGovernor, SessionPolicyViolation


class ChatModelClient(Protocol):
    """
    Protocol for the underlying chat model.

    You will implement this for OpenAI or other providers in a separate module.
    """

    def complete(self, messages: list[ChatMessage]) -> str:
        ...


class GatewayChatSession:
    """
    Chat session facade for the gateway orchestrator.
    
    This class provides a simple, stateful chat interface while
    delegating execution to the GatewayOrchestrator.
    
    Phase 2.5: ChatSession is now a convenience layer, not the orchestrator.
    """

    def __init__(
        self,
        kernel: Kernel,
        model_client: ChatModelClient,
        event_store: EventStore,
        trace_store: Optional[TraceStore] = None,
        enable_sanitization: bool = False,
        enable_formatting: bool = False,
        pipeline: Optional[Pipeline] = None,
        session_policy: Optional[SessionPolicy] = None,
    ) -> None:
        """
        Initialize chat session.
        
        Args:
            kernel: KL Kernel instance
            model_client: LLM client
            event_store: In-memory event store for insight panel
            trace_store: Optional persistent trace store
            enable_sanitization: Enable PII sanitization step
            enable_formatting: Enable markdown formatting step
            pipeline: Optional custom pipeline (default: DEFAULT_CHAT_PIPELINE)
            session_policy: Optional session-level governance policy (G(V) over entire conversation)
        """
        self.kernel = kernel
        self.model_client = model_client
        self.event_store = event_store
        self.trace_store = trace_store
        self.history: list[ChatMessage] = []
        self.logger = logging.getLogger(__name__)
        
        # Session-level governance (G(V) over entire conversation)
        self.session_governor = SessionGovernor(session_policy) if session_policy else None
        
        # Phase 2.5: Use pipeline from parameter or default
        self.pipeline = pipeline or self._create_pipeline(
            enable_sanitization=enable_sanitization,
            enable_formatting=enable_formatting,
        )
        
        # Phase 2.5: Create orchestrator with this pipeline
        from .pipeline_registry import PipelineRegistry
        
        registry = PipelineRegistry(pipelines=[self.pipeline])
        self.orchestrator = GatewayOrchestrator(
            registry=registry,
            trace_store=trace_store,
        )
    
    def _create_pipeline(
        self,
        enable_sanitization: bool,
        enable_formatting: bool,
    ) -> Pipeline:
        """
        Create a pipeline based on enabled features.
        
        This maintains backward compatibility with the old enable_* flags.
        """
        pipeline = Pipeline(
            pipeline_id="chat_session_default",
            version="0.3.0",
            description="ChatSession default pipeline",
            steps=[],
        )
        
        # Copy steps from DEFAULT_CHAT_PIPELINE
        from .pipelines import DEFAULT_CHAT_PIPELINE
        
        for step in DEFAULT_CHAT_PIPELINE.steps:
            # Clone step
            new_step = Pipeline(
                pipeline_id="",
                version="",
                description="",
                steps=[step],
            ).steps[0]
            
            # Apply enabled flags
            if step.step_id == "sanitize_pii":
                new_step.enabled = enable_sanitization
            elif step.step_id == "format_markdown":
                new_step.enabled = enable_formatting
            
            pipeline.steps.append(new_step)
        
        return pipeline

    def send(self, user_text: str) -> Tuple[str, GatewayTrace]:
        """
        Send a user message through the gateway.
        
        Phase 2.5: Now delegates to GatewayOrchestrator.
        Phase 3: Adds session-level governance (G(V) over conversation).
        External API remains unchanged.
        """
        # Session-level governance: Pre-check (G(V) before adding to V)
        if self.session_governor:
            pre_decision = self.session_governor.evaluate_before_request()
            if not pre_decision.allowed:
                self.logger.warning(f"Session governance denied request: {pre_decision.code}")
                raise SessionPolicyViolation(pre_decision)
        
        user_msg = ChatMessage(role="user", content=user_text)
        self.history.append(user_msg)

        self.logger.info("Processing user message via orchestrator")

        # Phase 2.5: Inject runtime config into pipeline steps
        for step in self.pipeline.steps:
            if step.step_id == "llm_call":
                step.config = {
                    "model_client": self.model_client,
                    "history": self.history,
                }
            elif step.step_id == "policy_check":
                step.config = {"kernel": self.kernel}
            elif step.step_id in ["sanitize_pii", "format_markdown"]:
                step.config = {"kernel": self.kernel}
        
        # Phase 2.5: Execute via orchestrator
        request = GatewayRequest(
            pipeline_id=self.pipeline.pipeline_id,
            user_text=user_text,
        )
        
        response = self.orchestrator.run(request)
        
        # Update history with response
        assistant_msg = ChatMessage(role="assistant", content=response.output)
        self.history.append(assistant_msg)

        # Extract data from step traces (Phase 2.5: from response directly)
        raw_model_response = response.output
        policy_code = "OK" if response.policy_allowed else "DENY"
        policy_reason = None
        policy_rule_id = None
        
        if response.step_traces:
            # Extract from step traces in response
            for st in response.step_traces:
                if st.step_id == "llm_call":
                    raw_model_response = st.output_snapshot.get("response", response.output)
                elif st.step_id == "policy_check":
                    policy_code = st.output_snapshot.get("code", policy_code)
                    policy_reason = st.output_snapshot.get("reason")
                    policy_rule_id = st.metadata.get("rule_id")
        
        # Build trace with real data
        from .models import PolicyDecision
        
        trace = GatewayTrace.new(
            user_message=user_msg,
            raw_model_response=raw_model_response,
            effective_chat_response=response.output,
            policy_decision=PolicyDecision(
                allowed=response.policy_allowed,
                code=policy_code,
                reason=policy_reason,
                rule_id=policy_rule_id,
            ),
            kernel_policy_trace=None,
        )
        
        # Use the orchestrator's trace_id for consistency
        trace.trace_id = response.trace_id
        
        # Attach step traces from orchestrator response
        trace.step_traces = response.step_traces

        # Add to in-memory event store
        self.event_store.add(trace)
        
        # Session-level governance: Post-update (update session Shadow State SS)
        if self.session_governor:
            self.session_governor.update_after_request(trace)
            
            # Optional: Post-check (could trigger warning or session termination)
            post_decision = self.session_governor.evaluate_after_request()
            if not post_decision.allowed:
                self.logger.warning(
                    f"Session governance warning: {post_decision.code}. "
                    "Next request will be denied."
                )

        return response.output, trace
