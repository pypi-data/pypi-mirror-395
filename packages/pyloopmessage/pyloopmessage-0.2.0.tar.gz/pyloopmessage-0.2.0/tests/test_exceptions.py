"""Tests for exceptions."""


from pyloopmessage.exceptions import (
    AccountSuspendedError,
    AuthenticationError,
    DeliveryError,
    InsufficientCreditsError,
    InvalidParameterError,
    InvalidRecipientError,
    LoopMessageError,
    MessageNotFoundError,
    RateLimitError,
    SenderNameError,
)


class TestLoopMessageError:
    """Test base LoopMessageError."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = LoopMessageError("Test error")
        assert str(error) == "LoopMessage Error: Test error"
        assert error.message == "Test error"
        assert error.code is None

    def test_error_with_code(self):
        """Test error with error code."""
        error = LoopMessageError("Test error", 100)
        assert str(error) == "LoopMessage Error 100: Test error"
        assert error.code == 100


class TestSpecificExceptions:
    """Test specific exception types."""

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Invalid credentials", 125)
        assert isinstance(error, LoopMessageError)
        assert error.code == 125

    def test_invalid_recipient_error(self):
        """Test InvalidRecipientError."""
        error = InvalidRecipientError("Invalid phone number", 180)
        assert isinstance(error, LoopMessageError)
        assert error.code == 180

    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError("Too many requests", 330)
        assert isinstance(error, LoopMessageError)
        assert error.code == 330

    def test_insufficient_credits_error(self):
        """Test InsufficientCreditsError."""
        error = InsufficientCreditsError("No credits available", 400)
        assert isinstance(error, LoopMessageError)
        assert error.code == 400

    def test_sender_name_error(self):
        """Test SenderNameError."""
        error = SenderNameError("Invalid sender name", 220)
        assert isinstance(error, LoopMessageError)
        assert error.code == 220

    def test_message_not_found_error(self):
        """Test MessageNotFoundError."""
        error = MessageNotFoundError("Message not found", 404)
        assert isinstance(error, LoopMessageError)
        assert error.code == 404

    def test_invalid_parameter_error(self):
        """Test InvalidParameterError."""
        error = InvalidParameterError("Missing parameter", 120)
        assert isinstance(error, LoopMessageError)
        assert error.code == 120

    def test_account_suspended_error(self):
        """Test AccountSuspendedError."""
        error = AccountSuspendedError("Account suspended", 500)
        assert isinstance(error, LoopMessageError)
        assert error.code == 500

    def test_delivery_error(self):
        """Test DeliveryError."""
        error = DeliveryError("Delivery failed", 110)
        assert isinstance(error, LoopMessageError)
        assert error.code == 110
