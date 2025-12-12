"""Tests for utility functions."""


from pyloopmessage.utils import (
    is_phone_number,
    normalize_email,
    normalize_phone_number,
    truncate_text,
    validate_attachment_url,
    validate_callback_header,
    validate_callback_url,
    validate_passthrough,
    validate_sender_name,
)


class TestNormalizePhoneNumber:
    """Test phone number normalization."""

    def test_normalize_with_plus(self):
        """Test normalization with + prefix."""
        assert normalize_phone_number("+1234567890") == "+1234567890"

    def test_normalize_without_plus(self):
        """Test normalization without + prefix."""
        assert normalize_phone_number("1234567890") == "+1234567890"

    def test_normalize_with_formatting(self):
        """Test normalization with various formatting."""
        assert normalize_phone_number("+1 (234) 567-8900") == "+12345678900"
        assert normalize_phone_number("1 234 567 8900") == "+12345678900"
        assert normalize_phone_number("1-234-567-8900") == "+12345678900"


class TestNormalizeEmail:
    """Test email normalization."""

    def test_normalize_email_case(self):
        """Test email case normalization."""
        assert normalize_email("Test@Example.Com") == "test@example.com"

    def test_normalize_email_whitespace(self):
        """Test email whitespace normalization."""
        assert normalize_email("  test@example.com  ") == "test@example.com"


class TestIsPhoneNumber:
    """Test phone number detection."""

    def test_is_phone_number_true(self):
        """Test phone number detection returns True."""
        assert is_phone_number("+1234567890") is True
        assert is_phone_number("1234567890") is True

    def test_is_phone_number_false(self):
        """Test phone number detection returns False for emails."""
        assert is_phone_number("test@example.com") is False


class TestValidateAttachmentUrl:
    """Test attachment URL validation."""

    def test_valid_url(self):
        """Test valid HTTPS URL."""
        assert validate_attachment_url("https://example.com/image.jpg") is True

    def test_invalid_protocol(self):
        """Test invalid protocol."""
        assert validate_attachment_url("http://example.com/image.jpg") is False

    def test_too_long_url(self):
        """Test URL that's too long."""
        long_url = "https://example.com/" + "a" * 250
        assert validate_attachment_url(long_url) is False


class TestValidateSenderName:
    """Test sender name validation."""

    def test_valid_sender_name(self):
        """Test valid sender name."""
        assert validate_sender_name("MyCompany") is True
        assert validate_sender_name("Support Team") is True

    def test_invalid_phone_number_sender_name(self):
        """Test sender name that looks like a phone number."""
        assert validate_sender_name("+1234567890") is False
        assert validate_sender_name("1234567890") is False
        assert validate_sender_name("(123) 456-7890") is False

    def test_empty_sender_name(self):
        """Test empty sender name."""
        assert validate_sender_name("") is False
        assert validate_sender_name("   ") is False


class TestTruncateText:
    """Test text truncation."""

    def test_no_truncation_needed(self):
        """Test text that doesn't need truncation."""
        text = "Hello world"
        assert truncate_text(text) == "Hello world"

    def test_truncation_needed(self):
        """Test text that needs truncation."""
        text = "a" * 20000
        truncated = truncate_text(text)
        assert len(truncated) == 10000
        assert truncated == "a" * 10000

    def test_custom_max_length(self):
        """Test truncation with custom max length."""
        text = "Hello world"
        assert truncate_text(text, 5) == "Hello"


class TestValidatePassthrough:
    """Test passthrough validation."""

    def test_valid_passthrough(self):
        """Test valid passthrough values."""
        assert validate_passthrough(None) is True
        assert validate_passthrough("metadata") is True
        assert validate_passthrough("a" * 1000) is True

    def test_invalid_passthrough(self):
        """Test invalid passthrough (too long)."""
        assert validate_passthrough("a" * 1001) is False


class TestValidateCallbackUrl:
    """Test callback URL validation."""

    def test_valid_callback_url(self):
        """Test valid callback URLs."""
        assert validate_callback_url(None) is True
        assert validate_callback_url("https://example.com/webhook") is True

    def test_invalid_callback_url_protocol(self):
        """Test invalid callback URL protocol."""
        assert validate_callback_url("http://example.com/webhook") is False

    def test_invalid_callback_url_too_long(self):
        """Test callback URL that's too long."""
        long_url = "https://example.com/" + "a" * 250
        assert validate_callback_url(long_url) is False


class TestValidateCallbackHeader:
    """Test callback header validation."""

    def test_valid_callback_header(self):
        """Test valid callback headers."""
        assert validate_callback_header(None) is True
        assert validate_callback_header("Bearer token123") is True
        assert validate_callback_header("a" * 256) is True

    def test_invalid_callback_header(self):
        """Test invalid callback header (too long)."""
        assert validate_callback_header("a" * 257) is False
