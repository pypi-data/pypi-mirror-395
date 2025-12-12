# src/kl_exec_gateway/cli.py

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from kl_kernel_logic import Kernel

from .chat_session import GatewayChatSession
from .config_loader import load_config, GatewayConfig
from .events import EventStore
from .kernel_integration import build_gateway_kernel
from .logging_config import setup_logging
from .providers import OpenAIChatClient
from .trace_store import TraceStore


def build_session(
    model: str = "gpt-4.1-mini", 
    config_path: Optional[Path] = None,
    api_key: Optional[str] = None
) -> GatewayChatSession:
    """
    Build a fully wired GatewayChatSession with configuration:
    - Kernel (KL Kernel Logic) with registered PSIs
    - EventStore (for Insight logging)
    - Optional TraceStore (persistent SQLite)
    - OpenAI model client (raw HTTP)
    - Configurable pipeline (sanitization, formatting)
    """

    # Load configuration
    config = load_config(config_path or Path("pipeline.config.json"))

    # Setup logging
    if config.logging.enabled:
        setup_logging(
            log_dir=config.logging.log_dir,
            max_bytes=config.logging.max_bytes,
            backup_count=config.logging.backup_count,
            log_level=config.logging.level,
        )

    # Use provided api_key or fall back to environment variable
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Use --key argument or set environment variable.", file=sys.stderr)
        sys.exit(1)

    kernel: Kernel = build_gateway_kernel()
    event_store = EventStore()
    model_client = OpenAIChatClient(model=model, api_key=api_key)

    # Optional trace persistence
    trace_store = None
    if config.trace_persistence.enabled:
        trace_store = TraceStore(db_path=config.trace_persistence.db_path)

    # Check which transforms are enabled
    enable_sanitization = config.is_step_enabled("sanitize")
    enable_formatting = config.is_step_enabled("format")

    return GatewayChatSession(
        kernel=kernel,
        model_client=model_client,
        event_store=event_store,
        trace_store=trace_store,
        enable_sanitization=enable_sanitization,
        enable_formatting=enable_formatting,
    )


def main() -> None:
    """
    Terminal-based guarded chat session.

    This is the MVP frontend:
    user input → LLM → Kernel Policy → optional transforms → decisions + trace → printed output.

    Set config via CLI args:
        kl-gateway --config configs/production.config.json
    """
    import argparse

    parser = argparse.ArgumentParser(description="KL Exec Gateway CLI")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("pipeline.config.json"),
        help="Path to configuration file",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="OpenAI API key (alternative to OPENAI_API_KEY env variable)"
    )
    args = parser.parse_args()

    print("[kl-exec-gateway] Guarded chat session started.")
    print(f"[kl-exec-gateway] Loading config from: {args.config}")
    if args.key:
        print("[kl-exec-gateway] Using API key from --key argument")
    print("Type 'exit' to quit.\n")

    session = build_session(config_path=args.config, api_key=args.key)

    while True:
        try:
            user_text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[kl-exec-gateway] Session terminated.")
            break

        if not user_text:
            continue

        if user_text.lower() in {"exit", "quit"}:
            print("[kl-exec-gateway] Session terminated.")
            break

        try:
            reply, trace = session.send(user_text)
        except Exception as exc:
            print(f"[error] Unexpected exception: {exc}", file=sys.stderr)
            continue

        print(f"ai> {reply}")

        if not trace.policy_decision.allowed:
            print(
                f"[policy] denied "
                f"(code={trace.policy_decision.code}, "
                f"reason={trace.policy_decision.reason or 'n/a'})"
            )


if __name__ == "__main__":
    main()
