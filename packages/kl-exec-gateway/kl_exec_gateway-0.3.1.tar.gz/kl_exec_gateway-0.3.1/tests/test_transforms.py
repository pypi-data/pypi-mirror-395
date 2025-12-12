"""Tests for transformation modules (PII sanitization, markdown formatting)."""

from kl_exec_gateway.transforms import (
    PIISanitizer,
    MarkdownFormatter,
    LengthTruncator,
    TransformResult,
)


def test_pii_sanitizer_emails() -> None:
    """Test that email addresses are correctly masked."""
    sanitizer = PIISanitizer()

    text = "Contact me at john@example.com or support@company.org"
    result = sanitizer.sanitize(text)

    assert result.applied is True
    assert "[EMAIL]" in result.output
    assert "john@example.com" not in result.output
    assert "support@company.org" not in result.output
    assert "2 email(s)" in result.details


def test_pii_sanitizer_phone_numbers() -> None:
    """Test that phone numbers are correctly masked."""
    sanitizer = PIISanitizer()

    text = "Call me at 555-123-4567 or (555) 987-6543"
    result = sanitizer.sanitize(text)

    assert result.applied is True
    assert "[PHONE]" in result.output
    assert "555-123-4567" not in result.output
    assert "phone number(s)" in result.details


def test_pii_sanitizer_credit_cards() -> None:
    """Test that credit card numbers are correctly masked."""
    sanitizer = PIISanitizer()

    text = "Card number: 4532-1234-5678-9010"
    result = sanitizer.sanitize(text)

    assert result.applied is True
    assert "[CREDIT_CARD]" in result.output
    assert "4532-1234-5678-9010" not in result.output


def test_pii_sanitizer_ssn() -> None:
    """Test that SSN numbers are correctly masked."""
    sanitizer = PIISanitizer()

    text = "My SSN is 123-45-6789"
    result = sanitizer.sanitize(text)

    assert result.applied is True
    assert "[SSN]" in result.output
    assert "123-45-6789" not in result.output


def test_pii_sanitizer_no_pii() -> None:
    """Test that text without PII is not modified."""
    sanitizer = PIISanitizer()

    text = "This is just normal text without any PII"
    result = sanitizer.sanitize(text)

    assert result.applied is False
    assert result.output == text
    assert result.details is None


def test_pii_sanitizer_multiple_types() -> None:
    """Test sanitizing multiple PII types at once."""
    sanitizer = PIISanitizer()

    text = "Email: test@example.com, Phone: 555-123-4567, Card: 4532-1234-5678-9010"
    result = sanitizer.sanitize(text)

    assert result.applied is True
    assert "[EMAIL]" in result.output
    assert "[PHONE]" in result.output
    assert "[CREDIT_CARD]" in result.output


def test_markdown_formatter_headers() -> None:
    """Test markdown header spacing."""
    formatter = MarkdownFormatter()

    text = "Some text\n# Header\nMore text"
    result = formatter.format(text)

    assert result.applied is True
    # Should add blank line before header
    assert "\n\n# Header" in result.output


def test_markdown_formatter_excessive_newlines() -> None:
    """Test removal of excessive blank lines."""
    formatter = MarkdownFormatter()

    text = "Line 1\n\n\n\nLine 2"
    result = formatter.format(text)

    assert result.applied is True
    # Should reduce to max 2 newlines
    assert "\n\n\n\n" not in result.output
    assert result.output == "Line 1\n\nLine 2"


def test_markdown_formatter_no_changes_needed() -> None:
    """Test when formatting is not needed."""
    formatter = MarkdownFormatter()

    text = "# Header\n\nSome text"
    result = formatter.format(text)

    # Might still apply due to trimming, but content should be similar
    assert result.output.strip() == text.strip()


def test_length_truncator_long_text() -> None:
    """Test truncation of long text."""
    truncator = LengthTruncator(max_chars=50)

    text = "This is a very long text that should be truncated because it exceeds the limit"
    result = truncator.truncate(text)

    assert result.applied is True
    assert len(result.output) <= 50
    assert result.output.endswith("...")
    assert "Truncated from" in result.details


def test_length_truncator_short_text() -> None:
    """Test that short text is not truncated."""
    truncator = LengthTruncator(max_chars=100)

    text = "Short text"
    result = truncator.truncate(text)

    assert result.applied is False
    assert result.output == text


def test_length_truncator_word_boundary() -> None:
    """Test that truncation respects word boundaries."""
    truncator = LengthTruncator(max_chars=30)

    text = "This is a sentence with multiple words"
    result = truncator.truncate(text)

    assert result.applied is True
    # Should not cut in the middle of a word
    assert not result.output[:-3].endswith(" w")  # -3 for "..."

