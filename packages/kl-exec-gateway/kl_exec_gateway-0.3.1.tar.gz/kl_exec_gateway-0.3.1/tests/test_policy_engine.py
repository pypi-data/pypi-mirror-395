from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Protocol, Sequence


@dataclass
class PolicyResult:
    """
    Deterministic evaluation result of a text by the policy engine.

    - allowed: overall decision (true/false)
    - code: short machine readable code
    - reason: human readable explanation (optional)
    - rule_id: ID of the rule that decided (None for global allow)
    """
    allowed: bool
    code: str
    reason: Optional[str] = None
    rule_id: Optional[str] = None


class PolicyRule(Protocol):
    """
    Interface for a single policy rule.

    Evaluation must be deterministic:
    same input text -> same output.
    """

    rule_id: str

    def evaluate(self, text: str) -> PolicyResult:
        ...


@dataclass
class LengthLimitRule:
    rule_id: str
    max_chars: int

    def evaluate(self, text: str) -> PolicyResult:
        t = text or ""
        if len(t) > self.max_chars:
            return PolicyResult(
                allowed=False,
                code="DENY_LENGTH",
                reason=(
                    f"Response too long ({len(t)} characters, "
                    f"limit is {self.max_chars})."
                ),
                rule_id=self.rule_id,
            )
        return PolicyResult(
            allowed=True,
            code="OK",
            reason=None,
            rule_id=None,
        )


@dataclass
class ForbiddenPatternRule:
    rule_id: str
    patterns: Sequence[str]

    def evaluate(self, text: str) -> PolicyResult:
        t = text or ""
        for pattern in self.patterns:
            if pattern and pattern in t:
                return PolicyResult(
                    allowed=False,
                    code="DENY_PATTERN",
                    reason=f"Contains forbidden pattern: {pattern!r}",
                    rule_id=self.rule_id,
                )
        return PolicyResult(
            allowed=True,
            code="OK",
            reason=None,
            rule_id=None,
        )


class PolicyEngine:
    """
    Deterministic policy engine.

    - Rules are evaluated in the given order.
    - First deny decision wins (short circuit).
    - If all rules allow, a global "OK" is returned.
    """

    def __init__(self, rules: List[PolicyRule]) -> None:
        self._rules = list(rules)

    def evaluate(self, text: str) -> PolicyResult:
        for rule in self._rules:
            result = rule.evaluate(text)
            if not result.allowed:
                return result

        return PolicyResult(
            allowed=True,
            code="OK",
            reason=None,
            rule_id=None,
        )


# ---------------------------------------------------------------------------
# JSON based policy configuration
# ---------------------------------------------------------------------------

@dataclass
class PolicyConfig:
    """
    Configurable policy parameters loaded from policy.config.json.

    - max_chars: length limit for responses
    - forbidden_patterns: list of forbidden substrings
    """
    max_chars: int = 100
    forbidden_patterns: List[str] = field(default_factory=lambda: [
        "BEGIN PRIVATE KEY",
        "-----BEGIN RSA PRIVATE KEY-----",
        "-----BEGIN OPENSSH PRIVATE KEY-----",
    ])


DEFAULT_CONFIG_PATH = Path("policy.config.json")


def load_policy_config(path: str | Path = DEFAULT_CONFIG_PATH) -> PolicyConfig:
    """
    Load PolicyConfig from a JSON file.

    If the file is missing or invalid, defaults are used.
    """
    p = Path(path)
    if not p.exists():
        return PolicyConfig()

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return PolicyConfig()

    max_chars_raw = data.get("max_chars", 100)
    try:
        max_chars = int(max_chars_raw)
    except Exception:
        max_chars = 100

    patterns_raw = data.get("forbidden_patterns", None)
    if isinstance(patterns_raw, list):
        patterns = [str(x) for x in patterns_raw]
    else:
        patterns = PolicyConfig().forbidden_patterns

    return PolicyConfig(
        max_chars=max_chars,
        forbidden_patterns=patterns,
    )


def save_policy_config(config: PolicyConfig, path: str | Path = DEFAULT_CONFIG_PATH) -> None:
    """
    Persist the current PolicyConfig to a JSON file.
    """
    p = Path(path)
    payload = {
        "max_chars": config.max_chars,
        "forbidden_patterns": list(config.forbidden_patterns),
    }
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_default_policy_engine(config: PolicyConfig | None = None) -> PolicyEngine:
    """
    Build the default policy engine for the gateway.

    If a PolicyConfig is provided, it is used directly.
    Otherwise, policy.config.json is loaded if present.

    Rules:
    1) Length limit
    2) Simple pattern blocker
    """
    if config is None:
        config = load_policy_config()

    rules: List[PolicyRule] = [
        LengthLimitRule(rule_id="length_limit", max_chars=config.max_chars),
        ForbiddenPatternRule(
            rule_id="forbidden_patterns",
            patterns=tuple(config.forbidden_patterns),
        ),
    ]
    return PolicyEngine(rules=rules)
