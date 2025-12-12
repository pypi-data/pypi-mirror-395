"""Pydantic models for the LoopMessage API."""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator

from .enums import (
    AlertType,
    DeliveryType,
    MessageStatusEnum,
    MessageType,
    ReactionType,
)


class GroupInfo(BaseModel):
    """Information about an iMessage group."""

    group_id: str
    name: Optional[str] = None
    participants: List[str]


class LanguageInfo(BaseModel):
    """Language information for messages."""

    code: str = Field(..., description="ISO 639-1 language code")
    name: str = Field(..., description="Language name")
    script: Optional[str] = Field(None, description="Script type (e.g., Hans, Hant)")


class SpeechMetadata(BaseModel):
    """Metadata for speech recognition."""

    speaking_rate: Optional[float] = None
    average_pause_duration: Optional[float] = None
    speech_start_timestamp: Optional[float] = None
    speech_duration: Optional[float] = None
    jitter: Optional[float] = None
    shimmer: Optional[float] = None
    pitch: Optional[float] = None
    voicing: Optional[float] = None


class SpeechInfo(BaseModel):
    """Speech recognition information."""

    text: str
    language: LanguageInfo
    metadata: Optional[SpeechMetadata] = None


class SendMessageResponse(BaseModel):
    """Response from sending a message."""

    message_id: str
    success: bool
    recipient: Optional[str] = None
    group: Optional[GroupInfo] = None
    text: str


class MessageStatusResponse(BaseModel):
    """Response from checking message status."""

    message_id: str
    status: MessageStatusEnum
    recipient: Optional[str] = None
    text: str
    sandbox: bool = False
    error_code: Optional[int] = None
    sender_name: Optional[str] = None
    passthrough: Optional[str] = None
    last_update: datetime


class WebhookEvent(BaseModel):
    """Webhook event from LoopMessage."""

    message_id: Optional[str] = None
    webhook_id: str
    alert_type: AlertType
    success: Optional[bool] = None
    recipient: Optional[str] = None
    text: Optional[str] = None
    subject: Optional[str] = None
    attachments: Optional[List[str]] = None
    message_type: Optional[MessageType] = None
    delivery_type: Optional[DeliveryType] = None
    reaction: Optional[ReactionType] = None
    thread_id: Optional[str] = None
    sandbox: Optional[bool] = None
    sender_name: Optional[str] = None
    error_code: Optional[int] = None
    passthrough: Optional[str] = None
    language: Optional[LanguageInfo] = None
    group: Optional[GroupInfo] = None
    speech: Optional[SpeechInfo] = None
    api_version: str = "1.0"

    @field_validator("recipient", mode="before")
    @classmethod
    def normalize_recipient(cls, v: Any) -> Optional[str]:
        """Normalize phone numbers and emails."""
        if isinstance(v, str):
            if "@" in v:
                return v.lower()
            else:
                # Remove spaces, dashes, parentheses from phone numbers
                return "".join(c for c in v if c.isdigit() or c == "+")
        return None if v is None else str(v)


class MessageStatus(BaseModel):
    """Simple message status model."""

    message_id: str
    status: MessageStatusEnum
    error_code: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response from the API."""

    success: bool = False
    code: int
    message: Optional[str] = None


class WebhookResponse(BaseModel):
    """Response to send back to webhook."""

    typing: Optional[int] = Field(None, ge=1, le=60, description="Typing indicator duration in seconds")
    read: Optional[bool] = Field(None, description="Mark message as read")

    @field_validator("typing")
    @classmethod
    def validate_typing(cls, v: Optional[int]) -> Optional[int]:
        """Validate typing indicator duration."""
        if v is not None and (v < 1 or v > 60):
            raise ValueError("Typing indicator must be between 1 and 60 seconds")
        return v
