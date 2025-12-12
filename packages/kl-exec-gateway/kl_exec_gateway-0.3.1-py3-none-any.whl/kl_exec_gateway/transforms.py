# src/kl_exec_gateway/transforms.py

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransformResult:
    """
    Result of a text transformation.

    - output: transformed text
    - applied: whether transformation was applied
    - details: human-readable description of what changed
    """

    output: str
    applied: bool
    details: Optional[str] = None


class PIISanitizer:
    """
    Deterministic PII sanitization using regex patterns.

    Detects and masks:
    - Email addresses
    - Phone numbers (basic patterns)
    - Credit card numbers
    - SSN patterns (US format)
    """

    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )

    PHONE_PATTERN = re.compile(
        r"\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b"
    )

    CREDIT_CARD_PATTERN = re.compile(
        r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
    )

    SSN_PATTERN = re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b"
    )

    def __init__(self, mask_char: str = "*") -> None:
        self.mask_char = mask_char

    def sanitize(self, text: str) -> TransformResult:
        """
        Apply all sanitization rules to the text.

        Returns TransformResult with masked text and details.
        """
        if not text:
            return TransformResult(output="", applied=False)

        original = text
        changes = []

        # Mask emails
        email_count = len(self.EMAIL_PATTERN.findall(text))
        if email_count > 0:
            text = self.EMAIL_PATTERN.sub("[EMAIL]", text)
            changes.append(f"{email_count} email(s)")

        # Mask phone numbers
        phone_count = len(self.PHONE_PATTERN.findall(text))
        if phone_count > 0:
            text = self.PHONE_PATTERN.sub("[PHONE]", text)
            changes.append(f"{phone_count} phone number(s)")

        # Mask credit cards
        cc_count = len(self.CREDIT_CARD_PATTERN.findall(text))
        if cc_count > 0:
            text = self.CREDIT_CARD_PATTERN.sub("[CREDIT_CARD]", text)
            changes.append(f"{cc_count} credit card(s)")

        # Mask SSN
        ssn_count = len(self.SSN_PATTERN.findall(text))
        if ssn_count > 0:
            text = self.SSN_PATTERN.sub("[SSN]", text)
            changes.append(f"{ssn_count} SSN(s)")

        applied = text != original
        details = f"Sanitized: {', '.join(changes)}" if changes else None

        return TransformResult(
            output=text,
            applied=applied,
            details=details,
        )


class MarkdownFormatter:
    """
    Simple markdown formatting for LLM responses.

    - Ensures proper spacing around headers
    - Formats code blocks
    - Cleans up excessive newlines
    """

    def format(self, text: str) -> TransformResult:
        """
        Apply markdown formatting rules.
        """
        if not text:
            return TransformResult(output="", applied=False)

        original = text
        changes = []

        # Ensure blank line before headers
        lines = text.split("\n")
        formatted_lines = []
        for i, line in enumerate(lines):
            if line.startswith("#"):
                # Add blank line before header if not first line
                if i > 0 and formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append("")
                    changes.append("header spacing")
            formatted_lines.append(line)

        text = "\n".join(formatted_lines)

        # Remove excessive blank lines (more than 2 consecutive)
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
            if "excessive newlines" not in changes:
                changes.append("excessive newlines")

        # Trim leading/trailing whitespace
        text = text.strip()

        applied = text != original
        details = f"Formatted: {', '.join(changes)}" if changes else None

        return TransformResult(
            output=text,
            applied=applied,
            details=details,
        )


class LengthTruncator:
    """
    Truncate text to a maximum length while preserving word boundaries.
    """

    def __init__(self, max_chars: int, suffix: str = "...") -> None:
        self.max_chars = max_chars
        self.suffix = suffix

    def truncate(self, text: str) -> TransformResult:
        """
        Truncate text if it exceeds max_chars.
        """
        if not text or len(text) <= self.max_chars:
            return TransformResult(output=text, applied=False)

        # Truncate at word boundary
        truncated = text[: self.max_chars - len(self.suffix)]

        # Find last space to avoid cutting words
        last_space = truncated.rfind(" ")
        if last_space > 0:
            truncated = truncated[:last_space]

        truncated += self.suffix

        details = f"Truncated from {len(text)} to {len(truncated)} chars"

        return TransformResult(
            output=truncated,
            applied=True,
            details=details,
        )

