# src/kl_exec_gateway/orchestrator.py

"""
Gateway orchestrator - the central execution engine.

The orchestrator is intentionally "dumb" - it executes steps in sequence
and manages traces, but contains no business logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .pipeline_registry import PipelineRegistry
from .pipeline_types import PipelineState, StepTrace
from .trace_store import TraceStore


logger = logging.getLogger(__name__)


@dataclass
class GatewayRequest:
    """
    Request to the gateway orchestrator.
    
    Contains all information needed to execute a pipeline.
    """
    
    pipeline_id: str
    user_text: str
    correlation_id: Optional[str] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self) -> None:
        if self.context is None:
            self.context = {}


@dataclass
class GatewayResponse:
    """
    Response from the gateway orchestrator.
    
    Contains the final output and trace ID for auditing.
    """
    
    output: str
    trace_id: str
    step_count: int
    policy_allowed: bool
    step_traces: List[StepTrace] = None  # Phase 2.5: Include step traces for ChatSession
    final_state: Optional[PipelineState] = None  # Phase 2.5: Include final state


class GatewayOrchestrator:
    """
    Central orchestrator for gateway execution.
    
    Responsibilities:
    - Load pipeline from registry
    - Execute steps in sequence
    - Manage trace persistence
    - Return results
    
    Non-responsibilities (intentionally):
    - Business logic (that's in step handlers)
    - Policy decisions (that's in PolicyEngine)
    - Model calls (that's in model clients)
    """
    
    def __init__(
        self,
        registry: PipelineRegistry,
        trace_store: Optional[TraceStore] = None,
    ) -> None:
        """
        Initialize orchestrator.
        
        Args:
            registry: PipelineRegistry for pipeline lookup
            trace_store: Optional TraceStore for persistence
        """
        self.registry = registry
        self.trace_store = trace_store
        self.logger = logging.getLogger(__name__)
    
    def run(self, request: GatewayRequest) -> GatewayResponse:
        """
        Execute a pipeline for the given request.
        
        This is the main entry point for all gateway execution.
        
        Args:
            request: GatewayRequest with pipeline_id and user_text
            
        Returns:
            GatewayResponse with output and trace_id
        """
        # 1. Get pipeline
        pipeline = self.registry.get(request.pipeline_id)
        
        self.logger.info(
            f"Executing pipeline: {pipeline.pipeline_id} v{pipeline.version}"
        )
        
        # 2. Create initial state
        initial_state = PipelineState(
            user_text=request.user_text,
            context=request.context or {},
        )
        
        # 3. Execute pipeline
        final_state, step_traces = pipeline.execute(initial_state)
        
        # 4. Persist traces if trace_store available
        trace_id = "no-trace"  # Fallback if no trace_store
        
        if self.trace_store:
            trace_id = self._persist_traces(
                pipeline_id=pipeline.pipeline_id,
                correlation_id=request.correlation_id,
                user_text=request.user_text,
                final_state=final_state,
                step_traces=step_traces,
            )
        
        # 5. Return response
        output = final_state.final_output or final_state.user_text
        
        self.logger.info(
            f"Pipeline completed: {len(step_traces)} steps, "
            f"policy_allowed={final_state.policy_allowed}"
        )
        
        return GatewayResponse(
            output=output,
            trace_id=trace_id,
            step_count=len(step_traces),
            policy_allowed=final_state.policy_allowed,
            step_traces=step_traces,  # Phase 2.5: Pass step traces to caller
            final_state=final_state,  # Phase 2.5: Pass final state to caller
        )
    
    def _persist_traces(
        self,
        pipeline_id: str,
        correlation_id: Optional[str],
        user_text: str,
        final_state: PipelineState,
        step_traces: List[StepTrace],
    ) -> str:
        """
        Persist step traces to trace store.
        
        This is a temporary implementation that creates a minimal
        GatewayTrace for backward compatibility. In a future version,
        we might persist step traces directly without the wrapper.
        
        Returns:
            trace_id
        """
        from .models import ChatMessage, GatewayTrace, PolicyDecision
        from uuid import uuid4
        
        # Generate trace ID
        trace_id = str(uuid4())
        
        # Create minimal GatewayTrace for backward compatibility
        user_msg = ChatMessage(role="user", content=user_text)
        
        # Extract policy decision from step traces
        policy_decision = final_state.policy_decision or PolicyDecision(
            allowed=final_state.policy_allowed,
            code="OK" if final_state.policy_allowed else "DENY",
        )
        
        trace = GatewayTrace.new(
            user_message=user_msg,
            raw_model_response=final_state.model_output or "",
            effective_chat_response=final_state.final_output or "",
            policy_decision=policy_decision,
            kernel_policy_trace=None,
        )
        
        # Override trace_id to match what we're using
        trace.trace_id = trace_id
        
        # Save main trace
        self.trace_store.save_trace(trace)
        
        # Save step traces
        for idx, step_trace in enumerate(step_traces):
            self.trace_store.save_step_trace(trace_id, idx, step_trace)
        
        self.logger.debug(
            f"Persisted trace {trace_id} with {len(step_traces)} steps"
        )
        
        return trace_id

