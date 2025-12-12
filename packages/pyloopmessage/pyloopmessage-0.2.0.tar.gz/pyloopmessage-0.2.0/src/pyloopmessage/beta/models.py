"""Pydantic models for the LoopMessage Beta API."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from .enums import (
    EventType,
    MessageStatusEnum,
    MessageType,
    ReactionType,
)


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
    """Response from sending a message in Beta API."""

    message_id: str
    success: bool
    contact: Optional[str] = None
    text: str


class MessageStatusResponse(BaseModel):
    """Response from checking message status in Beta API."""

    message_id: str
    status: MessageStatusEnum
    contact: Optional[str] = None
    text: str
    error_code: Optional[int] = None
    last_update: datetime


class WebhookEvent(BaseModel):
    """Webhook event from LoopMessage Beta API."""

    message_id: Optional[str] = None
    webhook_id: str
    event: EventType = Field(..., description="Event type")
    contact: Optional[str] = None
    text: Optional[str] = None
    subject: Optional[str] = None
    attachments: Optional[List[str]] = None
    message_type: Optional[MessageType] = None
    reaction: Optional[ReactionType] = None
    thread_id: Optional[str] = None
    error_code: Optional[int] = None
    language: Optional[LanguageInfo] = None
    speech: Optional[SpeechInfo] = None
    parameters: Optional[Dict[str, Any]] = Field(
        None, description="Custom parameters from opt-in request"
    )
    api_version: str = "1.0"

    @field_validator("contact", mode="before")
    @classmethod
    def normalize_contact(cls, v: Any) -> Optional[str]:
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


class OptInUrlResponse(BaseModel):
    """Response from generating an opt-in URL."""

    id: str = Field(..., description="Unique identifier for this opt-in request")
    imessage: str = Field(..., description="iMessage URL scheme for iOS 13+")
    sms: str = Field(..., description="SMS URL scheme for iOS 12 and below")
    url: str = Field(..., description="Smart link URL that detects device")
