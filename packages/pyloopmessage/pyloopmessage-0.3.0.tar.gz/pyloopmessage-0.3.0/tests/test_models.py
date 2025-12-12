"""Tests for pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from pyloopmessage.enums import AlertType, DeliveryType, MessageStatusEnum
from pyloopmessage.models import (
    GroupInfo,
    LanguageInfo,
    MessageStatusResponse,
    SendMessageResponse,
    WebhookEvent,
    WebhookResponse,
)


class TestGroupInfo:
    """Test GroupInfo model."""

    def test_group_info_creation(self):
        """Test basic GroupInfo creation."""
        group = GroupInfo(
            group_id="test-group-id",
            name="Test Group",
            participants=["+1234567890", "test@example.com"]
        )
        assert group.group_id == "test-group-id"
        assert group.name == "Test Group"
        assert len(group.participants) == 2

    def test_group_info_without_name(self):
        """Test GroupInfo without optional name."""
        group = GroupInfo(
            group_id="test-group-id",
            participants=["+1234567890"]
        )
        assert group.name is None


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


class TestSendMessageResponse:
    """Test SendMessageResponse model."""

    def test_send_message_response_individual(self):
        """Test SendMessageResponse for individual message."""
        response = SendMessageResponse(
            message_id="test-message-id",
            success=True,
            recipient="+1234567890",
            text="Hello world"
        )
        assert response.message_id == "test-message-id"
        assert response.success is True
        assert response.recipient == "+1234567890"
        assert response.group is None

    def test_send_message_response_group(self):
        """Test SendMessageResponse for group message."""
        group_info = GroupInfo(
            group_id="group-id",
            participants=["+1234567890", "+0987654321"]
        )
        response = SendMessageResponse(
            message_id="test-message-id",
            success=True,
            group=group_info,
            text="Hello group"
        )
        assert response.group is not None
        assert response.recipient is None


class TestMessageStatusResponse:
    """Test MessageStatusResponse model."""

    def test_message_status_response(self):
        """Test MessageStatusResponse creation."""
        response = MessageStatusResponse(
            message_id="test-id",
            status=MessageStatusEnum.SENT,
            recipient="+1234567890",
            text="Test message",
            sandbox=False,
            last_update=datetime.now()
        )
        assert response.status == MessageStatusEnum.SENT
        assert response.sandbox is False


class TestWebhookEvent:
    """Test WebhookEvent model."""

    def test_webhook_event_message_inbound(self):
        """Test WebhookEvent for inbound message."""
        event = WebhookEvent(
            webhook_id="webhook-id",
            alert_type=AlertType.MESSAGE_INBOUND,
            message_id="msg-id",
            recipient="+1234567890",
            text="Hello",
            delivery_type=DeliveryType.IMESSAGE
        )
        assert event.alert_type == AlertType.MESSAGE_INBOUND
        assert event.delivery_type == DeliveryType.IMESSAGE

    def test_webhook_event_recipient_normalization(self):
        """Test recipient normalization in WebhookEvent."""
        # Test phone number normalization
        event = WebhookEvent(
            webhook_id="webhook-id",
            alert_type=AlertType.MESSAGE_INBOUND,
            recipient="+1 (234) 567-8900"
        )
        assert event.recipient == "+12345678900"

        # Test email normalization
        event = WebhookEvent(
            webhook_id="webhook-id",
            alert_type=AlertType.MESSAGE_INBOUND,
            recipient="TEST@EXAMPLE.COM"
        )
        assert event.recipient == "test@example.com"


class TestWebhookResponse:
    """Test WebhookResponse model."""

    def test_webhook_response_typing(self):
        """Test WebhookResponse with typing indicator."""
        response = WebhookResponse(typing=30)
        assert response.typing == 30
        assert response.read is None

    def test_webhook_response_read(self):
        """Test WebhookResponse with read status."""
        response = WebhookResponse(read=True)
        assert response.read is True
        assert response.typing is None

    def test_webhook_response_invalid_typing(self):
        """Test WebhookResponse with invalid typing duration."""
        with pytest.raises(ValidationError):
            WebhookResponse(typing=0)  # Too low

        with pytest.raises(ValidationError):
            WebhookResponse(typing=61)  # Too high
