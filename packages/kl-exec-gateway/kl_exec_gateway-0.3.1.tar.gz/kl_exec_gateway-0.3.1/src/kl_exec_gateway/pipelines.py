# src/kl_exec_gateway/pipelines.py

"""
Pre-defined pipeline configurations.

This module contains standard pipeline definitions that can be used
directly or serve as templates for custom pipelines.
"""

from __future__ import annotations

from .pipeline_types import Pipeline, PipelineStep
from .step_handlers import (
    finalize_step_handler,
    format_step_handler,
    llm_step_handler,
    policy_step_handler,
    sanitize_step_handler,
)


DEFAULT_CHAT_PIPELINE = Pipeline(
    pipeline_id="chat_default",
    version="0.3.0",
    description="Default chat pipeline (LLM → policy → sanitize → format → finalize)",
    steps=[
        PipelineStep(
            step_id="llm_call",
            step_type="llm",
            handler=llm_step_handler,
            config={},  # Will be filled at runtime
        ),
        PipelineStep(
            step_id="policy_check",
            step_type="policy",
            handler=policy_step_handler,
            config={},  # Will be filled at runtime
        ),
        PipelineStep(
            step_id="sanitize_pii",
            step_type="transform",
            handler=sanitize_step_handler,
            config={},  # Will be filled at runtime
            enabled=True,  # Can be disabled
        ),
        PipelineStep(
            step_id="format_markdown",
            step_type="transform",
            handler=format_step_handler,
            config={},  # Will be filled at runtime
            enabled=True,  # Can be disabled
        ),
        PipelineStep(
            step_id="finalize",
            step_type="finalize",
            handler=finalize_step_handler,
            config={},
        ),
    ],
)


MINIMAL_CHAT_PIPELINE = Pipeline(
    pipeline_id="chat_minimal",
    version="0.3.0",
    description="Minimal chat pipeline (LLM → policy → finalize)",
    steps=[
        PipelineStep(
            step_id="llm_call",
            step_type="llm",
            handler=llm_step_handler,
            config={},
        ),
        PipelineStep(
            step_id="policy_check",
            step_type="policy",
            handler=policy_step_handler,
            config={},
        ),
        PipelineStep(
            step_id="finalize",
            step_type="finalize",
            handler=finalize_step_handler,
            config={},
        ),
    ],
)


GDPR_CHAT_PIPELINE = Pipeline(
    pipeline_id="chat_gdpr",
    version="0.3.0",
    description="GDPR-compliant chat pipeline with mandatory PII sanitization",
    steps=[
        PipelineStep(
            step_id="llm_call",
            step_type="llm",
            handler=llm_step_handler,
            config={},
        ),
        PipelineStep(
            step_id="policy_check",
            step_type="policy",
            handler=policy_step_handler,
            config={},
        ),
        PipelineStep(
            step_id="sanitize_pii",
            step_type="transform",
            handler=sanitize_step_handler,
            config={},
            enabled=True,  # Always enabled for GDPR
        ),
        PipelineStep(
            step_id="format_markdown",
            step_type="transform",
            handler=format_step_handler,
            config={},
            enabled=True,
        ),
        PipelineStep(
            step_id="finalize",
            step_type="finalize",
            handler=finalize_step_handler,
            config={},
        ),
    ],
)


# Registry of built-in pipelines
BUILTIN_PIPELINES = [
    DEFAULT_CHAT_PIPELINE,
    MINIMAL_CHAT_PIPELINE,
    GDPR_CHAT_PIPELINE,
]

