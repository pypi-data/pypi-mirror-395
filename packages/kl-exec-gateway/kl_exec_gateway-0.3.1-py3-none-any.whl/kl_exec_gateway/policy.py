# src/kl_exec_gateway/policy.py

from __future__ import annotations

from typing import Tuple

from kl_kernel_logic import Kernel, ExecutionTrace

from .kernel_integration import run_policy_kernel
from .models import PolicyDecision


def evaluate_model_response(
    kernel: Kernel,
    model_response: str,
) -> Tuple[PolicyDecision, ExecutionTrace | None]:
    """
    Main policy entrypoint used by the gateway.

    Wraps the Kernel-based policy evaluation to keep a stable
    interface for the higher layers.
    """
    decision, trace = run_policy_kernel(kernel=kernel, model_response=model_response)
    return decision, trace
