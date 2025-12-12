"""Tests for the LoopMessage client."""

import json

import pytest
from pytest_httpx import HTTPXMock

from pyloopmessage.client import LoopMessageClient
from pyloopmessage.enums import (
    MessageEffect,
    MessageStatusEnum,
    ReactionType,
)
from pyloopmessage.exceptions import (
    AuthenticationError,
    InvalidParameterError,
    MessageNotFoundError,
)
from pyloopmessage.models import MessageStatusResponse, SendMessageResponse


class TestLoopMessageClient:
    """Test LoopMessageClient."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return LoopMessageClient(
            authorization_key="test-auth-key",
            secret_key="test-secret-key"
        )

    def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.authorization_key == "test-auth-key"
        assert client.secret_key == "test-secret-key"
        assert client.base_url == "https://server.loopmessage.com/api/v1/"
        assert client.timeout == 30.0
        assert client.max_retries == 3

    def test_client_custom_params(self):
        """Test client with custom parameters."""
        client = LoopMessageClient(
            authorization_key="test-auth",
            secret_key="test-secret",
            base_url="https://custom.api.com/",
            timeout=60.0,
            max_retries=5
        )
        assert client.base_url == "https://custom.api.com/"
        assert client.timeout == 60.0
        assert client.max_retries == 5

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with LoopMessageClient("auth", "secret") as client:
            assert client._client is not None

    @pytest.mark.asyncio
    async def test_send_message_success(self, httpx_mock: HTTPXMock, client):
        """Test successful message sending."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "recipient": "+1234567890",
            "text": "Hello world"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200
        )

        response = await client.send_message(
            recipient="+1234567890",
            text="Hello world",
            sender_name="TestSender"
        )

        assert isinstance(response, SendMessageResponse)
        assert response.message_id == "test-message-id"
        assert response.success is True
        assert response.recipient == "+1234567890"

    @pytest.mark.asyncio
    async def test_send_message_with_effect(self, httpx_mock: HTTPXMock, client):
        """Test sending message with effect."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "recipient": "+1234567890",
            "text": "Hello world"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200
        )

        await client.send_message(
            recipient="+1234567890",
            text="Hello world",
            sender_name="TestSender",
            effect=MessageEffect.SLAM
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["effect"] == "slam"

    @pytest.mark.asyncio
    async def test_send_group_message(self, httpx_mock: HTTPXMock, client):
        """Test sending message to group."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "group": {
                "group_id": "group-123",
                "participants": ["+1234567890", "+0987654321"]
            },
            "text": "Hello group"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200
        )

        response = await client.send_message(
            group="group-123",
            text="Hello group",
            sender_name="TestSender"
        )

        assert response.group is not None
        assert response.group.group_id == "group-123"

    @pytest.mark.asyncio
    async def test_send_message_invalid_params(self, client):
        """Test sending message with invalid parameters."""
        # Test missing recipient and group
        with pytest.raises(InvalidParameterError):
            await client.send_message(text="Hello", sender_name="Test")

        # Test both recipient and group specified
        with pytest.raises(InvalidParameterError):
            await client.send_message(
                recipient="+1234567890",
                group="group-123",
                text="Hello",
                sender_name="Test"
            )

    @pytest.mark.asyncio
    async def test_send_audio_message(self, httpx_mock: HTTPXMock, client):
        """Test sending audio message."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "recipient": "+1234567890",
            "text": "Voice message"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200
        )

        response = await client.send_audio_message(
            recipient="+1234567890",
            text="Voice message",
            media_url="https://example.com/audio.mp3",
            sender_name="TestSender"
        )

        assert response.message_id == "test-message-id"

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["audio_message"] is True
        assert request_data["media_url"] == "https://example.com/audio.mp3"

    @pytest.mark.asyncio
    async def test_send_reaction(self, httpx_mock: HTTPXMock, client):
        """Test sending reaction."""
        response_data = {
            "message_id": "reaction-message-id",
            "success": True,
            "recipient": "+1234567890",
            "text": "reaction"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200
        )

        response = await client.send_reaction(
            recipient="+1234567890",
            text="reaction",
            message_id="original-message-id",
            reaction=ReactionType.LOVE,
            sender_name="TestSender"
        )

        assert response.message_id == "reaction-message-id"

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["reaction"] == "love"
        assert request_data["message_id"] == "original-message-id"

    @pytest.mark.asyncio
    async def test_get_message_status(self, httpx_mock: HTTPXMock, client):
        """Test getting message status."""
        response_data = {
            "message_id": "test-message-id",
            "status": "sent",
            "recipient": "+1234567890",
            "text": "Hello world",
            "sandbox": False,
            "sender_name": "TestSender",
            "last_update": "2023-12-31T23:59:59.000Z"
        }

        httpx_mock.add_response(
            method="GET",
            url="https://server.loopmessage.com/api/v1/message/status/test-message-id/",
            json=response_data,
            status_code=200
        )

        response = await client.get_message_status("test-message-id")

        assert isinstance(response, MessageStatusResponse)
        assert response.message_id == "test-message-id"
        assert response.status == MessageStatusEnum.SENT

    @pytest.mark.asyncio
    async def test_error_handling_404(self, httpx_mock: HTTPXMock, client):
        """Test 404 error handling."""
        httpx_mock.add_response(
            method="GET",
            url="https://server.loopmessage.com/api/v1/message/status/nonexistent/",
            status_code=404
        )

        with pytest.raises(MessageNotFoundError):
            await client.get_message_status("nonexistent")

    @pytest.mark.asyncio
    async def test_error_handling_api_error(self, httpx_mock: HTTPXMock, client):
        """Test API error response handling."""
        error_data = {
            "success": False,
            "code": 125,
            "message": "Invalid authorization key"
        }

        httpx_mock.add_response(
            method="POST",
            url="https://server.loopmessage.com/api/v1/message/send/",
            json=error_data,
            status_code=400
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await client.send_message(
                recipient="+1234567890",
                text="Hello",
                sender_name="Test"
            )

        assert exc_info.value.code == 125

    def test_parse_webhook(self, client):
        """Test webhook parsing."""
        webhook_data = {
            "webhook_id": "webhook-123",
            "alert_type": "message_inbound",
            "message_id": "msg-123",
            "recipient": "+1234567890",
            "text": "Hello",
            "api_version": "1.0"
        }

        event = client.parse_webhook(webhook_data)
        assert event.webhook_id == "webhook-123"
        assert event.alert_type.value == "message_inbound"

    def test_parse_webhook_json_string(self, client):
        """Test webhook parsing from JSON string."""
        webhook_data = {
            "webhook_id": "webhook-123",
            "alert_type": "message_inbound",
            "api_version": "1.0"
        }
        json_string = json.dumps(webhook_data)

        event = client.parse_webhook(json_string)
        assert event.webhook_id == "webhook-123"

    def test_create_webhook_response(self):
        """Test creating webhook responses."""
        # Test typing only
        response = LoopMessageClient.create_webhook_response(typing_duration=30)
        assert response == {"typing": 30}

        # Test read only
        response = LoopMessageClient.create_webhook_response(mark_as_read=True)
        assert response == {"read": True}

        # Test both
        response = LoopMessageClient.create_webhook_response(
            typing_duration=15, mark_as_read=True
        )
        assert response == {"typing": 15, "read": True}

        # Test invalid typing duration
        with pytest.raises(ValueError):
            LoopMessageClient.create_webhook_response(typing_duration=0)

        with pytest.raises(ValueError):
            LoopMessageClient.create_webhook_response(typing_duration=61)
