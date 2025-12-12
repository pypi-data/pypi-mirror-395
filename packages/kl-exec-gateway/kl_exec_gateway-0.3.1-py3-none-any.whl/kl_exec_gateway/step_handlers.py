# src/kl_exec_gateway/step_handlers.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Tuple

from .kernel_integration import run_sanitization, run_markdown_formatting
from .models import PolicyDecision
from .pipeline_types import PipelineState, StepTrace
from .policy import evaluate_model_response

if TYPE_CHECKING:
    from .chat_session import ChatModelClient

logger = logging.getLogger(__name__)


def llm_step_handler(
    state: PipelineState,
    config: Dict[str, Any],
) -> Tuple[PipelineState, StepTrace]:
    """
    LLM call step handler.
    
    Expects config to contain:
    - model_client: ChatModelClient instance
    - history: list of ChatMessage
    """
    model_client = config["model_client"]  # ChatModelClient
    history = config["history"]
    
    # Call LLM
    response = model_client.complete(history)
    
    # Update state
    new_state = state.copy()
    new_state.model_output = response
    
    # Create trace
    step_trace = StepTrace(
        step_id="llm_call",
        step_type="llm",
        input_snapshot={
            "user_text": state.user_text,
            "history_length": len(history),
        },
        output_snapshot={
            "response": response,
            "response_length": len(response),
        },
        metadata={
            "model": getattr(model_client, "model", "unknown"),
        },
    )
    
    logger.debug(f"LLM step completed: {len(response)} chars")
    
    return new_state, step_trace


def policy_step_handler(
    state: PipelineState,
    config: Dict[str, Any],
) -> Tuple[PipelineState, StepTrace]:
    """
    Policy check step handler.
    
    Expects config to contain:
    - kernel: Kernel instance
    """
    kernel = config["kernel"]
    
    # Evaluate policy on model output
    text_to_check = state.model_output or state.user_text
    decision, kernel_trace = evaluate_model_response(kernel, text_to_check)
    
    # Update state
    new_state = state.copy()
    new_state.policy_decision = decision
    new_state.policy_allowed = decision.allowed
    
    # If denied, set final output
    if not decision.allowed:
        new_state.final_output = "Policy denied."
    
    # Create trace
    step_trace = StepTrace(
        step_id="policy_check",
        step_type="policy",
        input_snapshot={
            "text": text_to_check,
            "text_length": len(text_to_check),
        },
        output_snapshot={
            "allowed": decision.allowed,
            "code": decision.code,
            "reason": decision.reason,
        },
        metadata={
            "rule_id": decision.rule_id,
        },
    )
    
    logger.info(
        f"Policy step: allowed={decision.allowed}, code={decision.code}"
    )
    
    return new_state, step_trace


def sanitize_step_handler(
    state: PipelineState,
    config: Dict[str, Any],
) -> Tuple[PipelineState, StepTrace]:
    """
    PII sanitization step handler.
    
    Expects config to contain:
    - kernel: Kernel instance
    - enabled: bool (optional, default True)
    """
    kernel = config["kernel"]
    enabled = config.get("enabled", True)
    
    if not enabled or not state.policy_allowed:
        # Skip if disabled or policy denied
        new_state = state.copy()
        step_trace = StepTrace(
            step_id="sanitize_pii",
            step_type="transform",
            input_snapshot={},
            output_snapshot={"skipped": True},
            metadata={"enabled": enabled, "policy_allowed": state.policy_allowed},
        )
        return new_state, step_trace
    
    # Get text to sanitize
    source_text = state.model_output or state.user_text
    
    # Run sanitization
    result = run_sanitization(kernel, source_text)
    
    # Update state
    new_state = state.copy()
    new_state.sanitized_text = result.output
    
    # Create trace
    step_trace = StepTrace(
        step_id="sanitize_pii",
        step_type="transform",
        input_snapshot={
            "text": source_text,
            "text_length": len(source_text),
        },
        output_snapshot={
            "sanitized": result.output,
            "applied": result.applied,
            "details": result.details,
        },
        metadata={
            "transform": "pii_sanitizer",
        },
    )
    
    if result.applied:
        logger.info(f"Sanitization applied: {result.details}")
    
    return new_state, step_trace


def format_step_handler(
    state: PipelineState,
    config: Dict[str, Any],
) -> Tuple[PipelineState, StepTrace]:
    """
    Markdown formatting step handler.
    
    Expects config to contain:
    - kernel: Kernel instance
    - enabled: bool (optional, default True)
    """
    kernel = config["kernel"]
    enabled = config.get("enabled", True)
    
    if not enabled or not state.policy_allowed:
        # Skip if disabled or policy denied
        new_state = state.copy()
        step_trace = StepTrace(
            step_id="format_markdown",
            step_type="transform",
            input_snapshot={},
            output_snapshot={"skipped": True},
            metadata={"enabled": enabled, "policy_allowed": state.policy_allowed},
        )
        return new_state, step_trace
    
    # Get text to format (prioritize sanitized, then model output)
    source_text = state.sanitized_text or state.model_output or state.user_text
    
    # Run formatting
    result = run_markdown_formatting(kernel, source_text)
    
    # Update state
    new_state = state.copy()
    new_state.formatted_text = result.output
    
    # Set as final output if policy allowed
    if state.policy_allowed:
        new_state.final_output = result.output
    
    # Create trace
    step_trace = StepTrace(
        step_id="format_markdown",
        step_type="transform",
        input_snapshot={
            "text": source_text,
            "text_length": len(source_text),
        },
        output_snapshot={
            "formatted": result.output,
            "applied": result.applied,
            "details": result.details,
        },
        metadata={
            "transform": "markdown_formatter",
        },
    )
    
    if result.applied:
        logger.info(f"Formatting applied: {result.details}")
    
    return new_state, step_trace


def finalize_step_handler(
    state: PipelineState,
    config: Dict[str, Any],
) -> Tuple[PipelineState, StepTrace]:
    """
    Finalize output step handler.
    
    Determines final output based on pipeline state.
    """
    # Determine final output
    if state.final_output:
        output = state.final_output
    elif state.formatted_text:
        output = state.formatted_text
    elif state.sanitized_text:
        output = state.sanitized_text
    elif state.model_output:
        output = state.model_output
    else:
        output = state.user_text
    
    # Update state
    new_state = state.copy()
    new_state.final_output = output
    
    # Create trace
    step_trace = StepTrace(
        step_id="finalize",
        step_type="finalize",
        input_snapshot={
            "policy_allowed": state.policy_allowed,
            "has_formatted": state.formatted_text is not None,
            "has_sanitized": state.sanitized_text is not None,
            "has_model_output": state.model_output is not None,
        },
        output_snapshot={
            "final_output": output,
            "output_length": len(output),
        },
        metadata={},
    )
    
    logger.debug(f"Finalized output: {len(output)} chars")
    
    return new_state, step_trace

