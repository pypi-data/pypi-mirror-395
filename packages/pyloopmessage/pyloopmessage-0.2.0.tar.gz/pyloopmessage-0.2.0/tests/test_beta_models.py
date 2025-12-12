"""Tests for beta pydantic models."""

from datetime import datetime

import pytest

from pyloopmessage.beta import (
    EventType,
    MessageStatusEnum,
    MessageType,
    ReactionType,
)
from pyloopmessage.beta.models import (
    LanguageInfo,
    MessageStatusResponse,
    OptInUrlResponse,
    SendMessageResponse,
    SpeechInfo,
    SpeechMetadata,
    WebhookEvent,
)


class TestLanguageInfo:
    """Test LanguageInfo model."""

    def test_language_info_creation(self):
        """Test basic LanguageInfo creation."""
        lang = LanguageInfo(code="en", name="English")
        assert lang.code == "en"
        assert lang.name == "English"
        assert lang.script is None

    def test_language_info_with_script(self):
        """Test LanguageInfo with script."""
        lang = LanguageInfo(code="zh", name="Chinese", script="Hans")
        assert lang.script == "Hans"


class TestSpeechMetadata:
    """Test SpeechMetadata model."""

    def test_speech_metadata_creation(self):
        """Test SpeechMetadata creation."""
        metadata = SpeechMetadata(
            speaking_rate=150.0,
            average_pause_duration=0.5,
            speech_duration=10.0,
        )
        assert metadata.speaking_rate == 150.0
        assert metadata.average_pause_duration == 0.5
        assert metadata.speech_duration == 10.0

    def test_speech_metadata_all_optional(self):
        """Test SpeechMetadata with all fields optional."""
        metadata = SpeechMetadata()
        assert metadata.speaking_rate is None
        assert metadata.pitch is None


class TestSpeechInfo:
    """Test SpeechInfo model."""

    def test_speech_info_creation(self):
        """Test SpeechInfo creation."""
        speech = SpeechInfo(
            text="Hello world",
            language=LanguageInfo(code="en", name="English"),
        )
        assert speech.text == "Hello world"
        assert speech.language.code == "en"
        assert speech.metadata is None


class TestSendMessageResponse:
    """Test SendMessageResponse model."""

    def test_send_message_response(self):
        """Test SendMessageResponse creation."""
        response = SendMessageResponse(
            message_id="test-message-id",
            success=True,
            contact="+1234567890",
            text="Hello world",
        )
        assert response.message_id == "test-message-id"
        assert response.success is True
        assert response.contact == "+1234567890"

    def test_send_message_response_without_contact(self):
        """Test SendMessageResponse without contact."""
        response = SendMessageResponse(
            message_id="test-message-id",
            success=True,
            text="Hello world",
        )
        assert response.contact is None


class TestMessageStatusResponse:
    """Test MessageStatusResponse model."""

    def test_message_status_response(self):
        """Test MessageStatusResponse creation."""
        response = MessageStatusResponse(
            message_id="test-id",
            status=MessageStatusEnum.DELIVERED,
            contact="+1234567890",
            text="Test message",
            last_update=datetime.now(),
        )
        assert response.status == MessageStatusEnum.DELIVERED
        assert response.error_code is None

    def test_message_status_response_with_error(self):
        """Test MessageStatusResponse with error code."""
        response = MessageStatusResponse(
            message_id="test-id",
            status=MessageStatusEnum.FAILED,
            contact="+1234567890",
            text="Test message",
            error_code=1020,
            last_update=datetime.now(),
        )
        assert response.status == MessageStatusEnum.FAILED
        assert response.error_code == 1020


class TestWebhookEvent:
    """Test WebhookEvent model."""

    def test_webhook_event_message_inbound(self):
        """Test WebhookEvent for inbound message."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_INBOUND,
            message_id="msg-id",
            contact="+1234567890",
            text="Hello",
            message_type=MessageType.TEXT,
        )
        assert event.event == EventType.MESSAGE_INBOUND
        assert event.message_type == MessageType.TEXT

    def test_webhook_event_contact_normalization_phone(self):
        """Test contact normalization for phone numbers."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_INBOUND,
            contact="+1 (234) 567-8900",
        )
        assert event.contact == "+12345678900"

    def test_webhook_event_contact_normalization_email(self):
        """Test contact normalization for emails."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_INBOUND,
            contact="TEST@EXAMPLE.COM",
        )
        assert event.contact == "test@example.com"

    def test_webhook_event_opt_in(self):
        """Test WebhookEvent for opt-in event."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.OPT_IN,
            contact="+1234567890",
            text="Subscribe",
            parameters={
                "click_id": "abc123",
                "utm_campaign": "test",
            },
        )
        assert event.event == EventType.OPT_IN
        assert event.parameters is not None
        assert event.parameters["click_id"] == "abc123"

    def test_webhook_event_reaction(self):
        """Test WebhookEvent for reaction."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_REACTION,
            contact="+1234567890",
            reaction=ReactionType.LOVE,
            message_type=MessageType.REACTION,
        )
        assert event.event == EventType.MESSAGE_REACTION
        assert event.reaction == ReactionType.LOVE

    def test_webhook_event_with_language(self):
        """Test WebhookEvent with language info."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_INBOUND,
            contact="+1234567890",
            text="Bonjour",
            language=LanguageInfo(code="fr", name="French"),
        )
        assert event.language is not None
        assert event.language.code == "fr"

    def test_webhook_event_with_speech(self):
        """Test WebhookEvent with speech transcription."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_INBOUND,
            contact="+1234567890",
            message_type=MessageType.AUDIO,
            speech=SpeechInfo(
                text="Hello from voice message",
                language=LanguageInfo(code="en", name="English"),
            ),
        )
        assert event.speech is not None
        assert event.speech.text == "Hello from voice message"

    def test_webhook_event_message_failed(self):
        """Test WebhookEvent for failed message."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            event=EventType.MESSAGE_FAILED,
            message_id="msg-id",
            contact="+1234567890",
            error_code=1020,
        )
        assert event.event == EventType.MESSAGE_FAILED
        assert event.error_code == 1020


class TestOptInUrlResponse:
    """Test OptInUrlResponse model."""

    def test_opt_in_url_response(self):
        """Test OptInUrlResponse creation."""
        response = OptInUrlResponse(
            id="3718be9c-17bc-412e-9790-c4768ca5df3e",
            imessage="imessage://ahoy%40imsg.tel&body=Subscribe%20%5Bopt-in-code%5D",
            sms="sms:ahoy%40imsg.tel&body=Subscribe%20%5Bopt-in-code%5D",
            url="https://opt-in.imsg.link/opt-in/0Rig0/?id=3718be9c",
        )
        assert response.id == "3718be9c-17bc-412e-9790-c4768ca5df3e"
        assert "imessage://" in response.imessage
        assert "sms:" in response.sms
        assert "https://" in response.url
