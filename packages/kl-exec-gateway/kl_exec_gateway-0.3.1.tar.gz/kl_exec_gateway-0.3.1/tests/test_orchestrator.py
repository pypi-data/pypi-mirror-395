"""Tests for GatewayOrchestrator (Phase 2.5)."""

from pathlib import Path

import pytest

from kl_exec_gateway.events import EventStore
from kl_exec_gateway.kernel_integration import build_gateway_kernel
from kl_exec_gateway.orchestrator import GatewayOrchestrator, GatewayRequest
from kl_exec_gateway.pipeline_registry import PipelineRegistry
from kl_exec_gateway.pipelines import DEFAULT_CHAT_PIPELINE, MINIMAL_CHAT_PIPELINE
from kl_exec_gateway.trace_store import TraceStore

# Import test helpers
import sys
sys.path.insert(0, str(Path(__file__).parent))
from test_chat_session import DummyModelClient, _set_test_policy_engine


def test_orchestrator_executes_pipeline(tmp_path: Path) -> None:
    """Test that orchestrator executes a pipeline correctly."""
    kernel = build_gateway_kernel()
    trace_store = TraceStore(db_path=tmp_path / "test.db")
    model_client = DummyModelClient(response="Hello world")
    
    _set_test_policy_engine(max_chars=100)
    
    # Create registry with test pipeline
    registry = PipelineRegistry(pipelines=[DEFAULT_CHAT_PIPELINE])
    
    # Inject runtime config
    for step in DEFAULT_CHAT_PIPELINE.steps:
        if step.step_id == "llm_call":
            step.config = {
                "model_client": model_client,
                "history": [],
            }
        elif step.step_id in ["policy_check", "sanitize_pii", "format_markdown"]:
            step.config = {"kernel": kernel}
    
    # Create orchestrator
    orchestrator = GatewayOrchestrator(
        registry=registry,
        trace_store=trace_store,
    )
    
    # Execute
    request = GatewayRequest(
        pipeline_id="chat_default",
        user_text="Test message",
    )
    
    response = orchestrator.run(request)
    
    # Verify response
    assert response.output == "Hello world"
    assert response.policy_allowed is True
    # Note: sanitize and format steps are disabled by default, so only 3 steps execute
    assert response.step_count == 3
    assert response.trace_id is not None
    
    # Verify step traces were persisted
    step_traces = trace_store.get_step_traces(response.trace_id)
    assert len(step_traces) == 3


def test_orchestrator_with_minimal_pipeline(tmp_path: Path) -> None:
    """Test orchestrator with minimal pipeline (no transforms)."""
    kernel = build_gateway_kernel()
    trace_store = TraceStore(db_path=tmp_path / "test.db")
    model_client = DummyModelClient(response="Minimal response")
    
    _set_test_policy_engine(max_chars=100)
    
    # Create registry with minimal pipeline
    registry = PipelineRegistry(pipelines=[MINIMAL_CHAT_PIPELINE])
    
    # Inject runtime config
    for step in MINIMAL_CHAT_PIPELINE.steps:
        if step.step_id == "llm_call":
            step.config = {
                "model_client": model_client,
                "history": [],
            }
        elif step.step_id == "policy_check":
            step.config = {"kernel": kernel}
    
    orchestrator = GatewayOrchestrator(
        registry=registry,
        trace_store=trace_store,
    )
    
    request = GatewayRequest(
        pipeline_id="chat_minimal",
        user_text="Test",
    )
    
    response = orchestrator.run(request)
    
    # Should have only 3 steps: llm, policy, finalize
    assert response.step_count == 3
    
    step_traces = trace_store.get_step_traces(response.trace_id)
    assert len(step_traces) == 3
    
    step_ids = [st["step_id"] for st in step_traces]
    assert "llm_call" in step_ids
    assert "policy_check" in step_ids
    assert "finalize" in step_ids
    assert "sanitize_pii" not in step_ids


def test_orchestrator_without_trace_store() -> None:
    """Test that orchestrator works without trace_store."""
    kernel = build_gateway_kernel()
    model_client = DummyModelClient(response="No persistence")
    
    _set_test_policy_engine(max_chars=100)
    
    registry = PipelineRegistry(pipelines=[MINIMAL_CHAT_PIPELINE])
    
    for step in MINIMAL_CHAT_PIPELINE.steps:
        if step.step_id == "llm_call":
            step.config = {
                "model_client": model_client,
                "history": [],
            }
        elif step.step_id == "policy_check":
            step.config = {"kernel": kernel}
    
    # No trace_store
    orchestrator = GatewayOrchestrator(
        registry=registry,
        trace_store=None,
    )
    
    request = GatewayRequest(
        pipeline_id="chat_minimal",
        user_text="Test",
    )
    
    response = orchestrator.run(request)
    
    # Should still work
    assert response.output == "No persistence"
    assert response.trace_id == "no-trace"
    assert response.step_count == 3


def test_orchestrator_returns_step_traces_in_response() -> None:
    """Test that orchestrator includes step traces in response (Phase 2.5)."""
    kernel = build_gateway_kernel()
    model_client = DummyModelClient(response="Test")
    
    _set_test_policy_engine(max_chars=100)
    
    registry = PipelineRegistry(pipelines=[MINIMAL_CHAT_PIPELINE])
    
    for step in MINIMAL_CHAT_PIPELINE.steps:
        if step.step_id == "llm_call":
            step.config = {
                "model_client": model_client,
                "history": [],
            }
        elif step.step_id == "policy_check":
            step.config = {"kernel": kernel}
    
    orchestrator = GatewayOrchestrator(
        registry=registry,
        trace_store=None,
    )
    
    request = GatewayRequest(
        pipeline_id="chat_minimal",
        user_text="Test",
    )
    
    response = orchestrator.run(request)
    
    # Verify step_traces are included in response
    assert response.step_traces is not None
    assert len(response.step_traces) == 3
    
    # Verify we can access step data
    llm_step = response.step_traces[0]
    assert llm_step.step_id == "llm_call"
    assert llm_step.output_snapshot["response"] == "Test"

