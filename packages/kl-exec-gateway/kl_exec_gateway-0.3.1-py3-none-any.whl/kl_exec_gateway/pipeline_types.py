# src/kl_exec_gateway/pipeline_types.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Tuple


@dataclass
class PipelineState:
    """
    Immutable-like state that flows through the pipeline.
    
    Each step receives state, produces new state + trace.
    """
    
    # User input
    user_text: str
    
    # LLM output
    model_output: Optional[str] = None
    
    # Policy decision
    policy_decision: Optional[Any] = None
    policy_allowed: bool = True
    
    # Transform outputs
    sanitized_text: Optional[str] = None
    formatted_text: Optional[str] = None
    
    # Final output
    final_output: Optional[str] = None
    
    # Generic context bag for extensions
    context: Dict[str, Any] = field(default_factory=dict)
    
    def copy(self) -> PipelineState:
        """Create a shallow copy for immutable-style updates."""
        return PipelineState(
            user_text=self.user_text,
            model_output=self.model_output,
            policy_decision=self.policy_decision,
            policy_allowed=self.policy_allowed,
            sanitized_text=self.sanitized_text,
            formatted_text=self.formatted_text,
            final_output=self.final_output,
            context=dict(self.context),
        )


@dataclass
class StepTrace:
    """
    Trace entry for a single pipeline step.
    
    Captures input, output, and metadata for replay and audit.
    """
    
    step_id: str
    step_type: str
    input_snapshot: Dict[str, Any]
    output_snapshot: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for storage."""
        return {
            "step_id": self.step_id,
            "step_type": self.step_type,
            "input_snapshot": self.input_snapshot,
            "output_snapshot": self.output_snapshot,
            "metadata": self.metadata,
        }


# Type alias for step handler functions
StepHandler = Callable[[PipelineState, Dict[str, Any]], Tuple[PipelineState, StepTrace]]


@dataclass
class PipelineStep:
    """
    Definition of a single pipeline step.
    
    Contains step metadata and the handler function.
    """
    
    step_id: str
    step_type: str
    handler: StepHandler
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    
    def execute(self, state: PipelineState) -> Tuple[PipelineState, Optional[StepTrace]]:
        """
        Execute this step if enabled.
        
        Returns (new_state, step_trace) or (state, None) if disabled.
        """
        if not self.enabled:
            return state, None
        
        return self.handler(state, self.config)


@dataclass
class Pipeline:
    """
    Complete pipeline definition.
    
    A sequence of steps to execute.
    """
    
    pipeline_id: str
    version: str
    description: str
    steps: list[PipelineStep]
    
    def execute(self, initial_state: PipelineState) -> Tuple[PipelineState, list[StepTrace]]:
        """
        Execute all steps in sequence.
        
        Returns final state and list of step traces.
        """
        state = initial_state
        traces = []
        
        for step in self.steps:
            new_state, step_trace = step.execute(state)
            state = new_state
            
            if step_trace is not None:
                traces.append(step_trace)
        
        return state, traces

