"""Utility functions for the LoopMessage API."""

import re
from typing import Optional


def normalize_phone_number(phone: str) -> str:
    """
    Normalize a phone number to E164 format.

    Args:
        phone: Raw phone number

    Returns:
        Normalized phone number in E164 format
    """
    # Remove all non-digit characters except +
    digits_only = re.sub(r"[^\d+]", "", phone)

    # Ensure it starts with +
    if not digits_only.startswith("+"):
        digits_only = "+" + digits_only

    return digits_only


def normalize_email(email: str) -> str:
    """
    Normalize an email address.

    Args:
        email: Raw email address

    Returns:
        Normalized email address (lowercase)
    """
    return email.lower().strip()


def is_phone_number(contact: str) -> bool:
    """
    Check if a contact string is a phone number.

    Args:
        contact: Contact string

    Returns:
        True if it's a phone number, False if it's an email
    """
    return "@" not in contact


def validate_attachment_url(url: str) -> bool:
    """
    Validate an attachment URL.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url.startswith("https://"):
        return False
    if len(url) > 256:
        return False
    return True


def validate_sender_name(sender_name: str) -> bool:
    """
    Validate a sender name.

    Args:
        sender_name: Sender name to validate

    Returns:
        True if valid, False otherwise
    """
    # Don't allow phone numbers as sender names
    if re.match(r"^\+?[\d\s\-\(\)]+$", sender_name):
        return False
    return len(sender_name.strip()) > 0


def truncate_text(text: str, max_length: int = 10000) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum allowed length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length]


def validate_passthrough(passthrough: Optional[str]) -> bool:
    """
    Validate passthrough metadata.

    Args:
        passthrough: Passthrough string to validate

    Returns:
        True if valid, False otherwise
    """
    if passthrough is None:
        return True
    return len(passthrough) <= 1000


def validate_callback_url(url: Optional[str]) -> bool:
    """
    Validate a callback URL.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if url is None:
        return True
    if not url.startswith("https://"):
        return False
    return len(url) <= 256


def validate_callback_header(header: Optional[str]) -> bool:
    """
    Validate a callback header.

    Args:
        header: Header to validate

    Returns:
        True if valid, False otherwise
    """
    if header is None:
        return True
    return len(header) <= 256
