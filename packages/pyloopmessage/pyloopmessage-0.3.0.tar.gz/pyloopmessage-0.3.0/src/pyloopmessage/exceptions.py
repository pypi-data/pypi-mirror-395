"""Exceptions for the LoopMessage API."""

from typing import Union


class LoopMessageError(Exception):
    """Base exception for LoopMessage API errors."""

    def __init__(self, message: str, code: Union[int, None] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        if self.code:
            return f"LoopMessage Error {self.code}: {self.message}"
        return f"LoopMessage Error: {self.message}"


class AuthenticationError(LoopMessageError):
    """Raised when authentication fails."""

    pass


class InvalidRecipientError(LoopMessageError):
    """Raised when recipient is invalid."""

    pass


class RateLimitError(LoopMessageError):
    """Raised when rate limit is exceeded."""

    pass


class InsufficientCreditsError(LoopMessageError):
    """Raised when insufficient credits/requests are available."""

    pass


class SenderNameError(LoopMessageError):
    """Raised when sender name is invalid or not activated."""

    pass


class MessageNotFoundError(LoopMessageError):
    """Raised when message ID is not found."""

    pass


class InvalidParameterError(LoopMessageError):
    """Raised when request parameters are invalid."""

    pass


class AccountSuspendedError(LoopMessageError):
    """Raised when account is suspended or blocked."""

    pass


class DeliveryError(LoopMessageError):
    """Raised when message delivery fails."""

    pass
