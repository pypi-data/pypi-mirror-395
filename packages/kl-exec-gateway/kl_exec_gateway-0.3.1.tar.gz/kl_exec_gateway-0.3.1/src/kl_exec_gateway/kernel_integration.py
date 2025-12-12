from __future__ import annotations

from typing import Optional, Tuple

from kl_kernel_logic import (
    Kernel,
    PsiDefinition,
    PsiConstraints,
    ExecutionTrace,
)

from .models import PolicyDecision
from .policy_engine import PolicyEngine, PolicyResult, build_default_policy_engine
from .transforms import PIISanitizer, MarkdownFormatter, TransformResult


def build_gateway_kernel() -> Kernel:
    """
    Create a Kernel instance for the gateway.

    The Kernel is used for deterministic operations like transformations.
    
    Documented PSIs (for future kernel integration):
    - gateway.policy.evaluate: Policy evaluation over LLM responses
    - gateway.transform.sanitize: PII sanitization (emails, phones, etc.)
    - gateway.transform.format_markdown: Markdown formatting and cleanup
    """
    kernel = Kernel()
    return kernel


def build_policy_psi() -> PsiDefinition:
    """
    Documents the policy interface to the Kernel.

    The actual policy logic resides in the Gateway, not in the Kernel.
    """
    return PsiDefinition(
        psi_type="gateway.policy.evaluate",
        domain="gateway",
        effect="pure",
        description=(
            "Gateway-local policy over LLM responses. "
            "Implemented outside the kernel; Psi only documents intent."
        ),
        constraints=PsiConstraints(
            scope="llm_output",
            format="plain text",
        ),
    )


# Singleton-like instances for the process
_POLICY_ENGINE: Optional[PolicyEngine] = None
_PII_SANITIZER: Optional[PIISanitizer] = None
_MARKDOWN_FORMATTER: Optional[MarkdownFormatter] = None


def _get_policy_engine() -> PolicyEngine:
    global _POLICY_ENGINE
    if _POLICY_ENGINE is None:
        _POLICY_ENGINE = build_default_policy_engine()
    return _POLICY_ENGINE


def _get_pii_sanitizer() -> PIISanitizer:
    global _PII_SANITIZER
    if _PII_SANITIZER is None:
        _PII_SANITIZER = PIISanitizer()
    return _PII_SANITIZER


def _get_markdown_formatter() -> MarkdownFormatter:
    global _MARKDOWN_FORMATTER
    if _MARKDOWN_FORMATTER is None:
        _MARKDOWN_FORMATTER = MarkdownFormatter()
    return _MARKDOWN_FORMATTER


def run_policy_kernel(
    kernel: Kernel,  # intentionally present, currently unused
    model_response: str,
) -> Tuple[PolicyDecision, Optional[ExecutionTrace]]:
    """
    Policy entry point for the gateway.

    - Policy is evaluated entirely locally in the gateway via PolicyEngine.
    - Kernel is *not* used for policy (no dilution of the core).
    - ExecutionTrace is reserved for future kernel-based steps.
    """

    engine = _get_policy_engine()
    result: PolicyResult = engine.evaluate(model_response)

    decision = PolicyDecision(
        allowed=result.allowed,
        reason=result.reason,
        code=result.code,
        rule_id=result.rule_id,
    )

    trace: Optional[ExecutionTrace] = None
    return decision, trace


def run_sanitization(kernel: Kernel, text: str) -> TransformResult:
    """
    Run PII sanitization transformation.

    PSI: gateway.transform.sanitize
    Deterministic: same input -> same output
    """
    sanitizer = _get_pii_sanitizer()
    return sanitizer.sanitize(text)


def run_markdown_formatting(kernel: Kernel, text: str) -> TransformResult:
    """
    Run markdown formatting transformation.

    PSI: gateway.transform.format_markdown
    Deterministic: same input -> same output
    """
    formatter = _get_markdown_formatter()
    return formatter.format(text)
