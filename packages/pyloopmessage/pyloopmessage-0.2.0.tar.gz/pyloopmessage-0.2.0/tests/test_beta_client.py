"""Tests for the LoopMessage Beta client."""

import json

import pytest
from pytest_httpx import HTTPXMock

from pyloopmessage.beta import BetaLoopMessageClient, MessageEffect, MessageStatusEnum
from pyloopmessage.exceptions import (
    AuthenticationError,
    InvalidParameterError,
    MessageNotFoundError,
)
from pyloopmessage.beta.models import (
    MessageStatusResponse,
    OptInUrlResponse,
    SendMessageResponse,
)


class TestBetaLoopMessageClient:
    """Test BetaLoopMessageClient."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return BetaLoopMessageClient(api_key="test-api-key")

    def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.api_key == "test-api-key"
        assert client.base_url == "https://a.loopmessage.com/api/v1/"
        assert client.timeout == 30.0
        assert client.max_retries == 3

    def test_client_custom_params(self):
        """Test client with custom parameters."""
        client = BetaLoopMessageClient(
            api_key="test-api-key",
            base_url="https://custom.api.com/",
            timeout=60.0,
            max_retries=5,
        )
        assert client.base_url == "https://custom.api.com/"
        assert client.timeout == 60.0
        assert client.max_retries == 5

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with BetaLoopMessageClient("api-key") as client:
            assert client._client is not None

    @pytest.mark.asyncio
    async def test_send_message_success(self, httpx_mock: HTTPXMock, client):
        """Test successful message sending."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "contact": "+1234567890",
            "text": "Hello world",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        response = await client.send_message(
            contact="+1234567890",
            text="Hello world",
        )

        assert isinstance(response, SendMessageResponse)
        assert response.message_id == "test-message-id"
        assert response.success is True
        assert response.contact == "+1234567890"

    @pytest.mark.asyncio
    async def test_send_message_with_effect(self, httpx_mock: HTTPXMock, client):
        """Test sending message with effect."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "contact": "+1234567890",
            "text": "Hello world",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        await client.send_message(
            contact="+1234567890",
            text="Hello world",
            effect=MessageEffect.SLAM,
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["effect"] == "slam"

    @pytest.mark.asyncio
    async def test_send_message_with_subject(self, httpx_mock: HTTPXMock, client):
        """Test sending message with subject."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "contact": "+1234567890",
            "text": "Hello world",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        await client.send_message(
            contact="+1234567890",
            text="Hello world",
            subject="Important Message",
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["subject"] == "Important Message"

    @pytest.mark.asyncio
    async def test_send_message_with_attachments(self, httpx_mock: HTTPXMock, client):
        """Test sending message with attachments."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "contact": "+1234567890",
            "text": "Check this out",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        await client.send_message(
            contact="+1234567890",
            text="Check this out",
            attachments=["https://example.com/image.jpg"],
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["attachments"] == ["https://example.com/image.jpg"]

    @pytest.mark.asyncio
    async def test_send_message_missing_contact(self, client):
        """Test sending message without contact."""
        with pytest.raises(InvalidParameterError):
            await client.send_message(contact="", text="Hello")

    @pytest.mark.asyncio
    async def test_send_audio_message(self, httpx_mock: HTTPXMock, client):
        """Test sending audio message."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "contact": "+1234567890",
            "text": "Voice message",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        response = await client.send_audio_message(
            contact="+1234567890",
            text="Voice message",
            media_url="https://example.com/audio.mp3",
            sender_name="TestSender",
        )

        assert response.message_id == "test-message-id"

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["audio_message"] is True
        assert request_data["media_url"] == "https://example.com/audio.mp3"

    @pytest.mark.asyncio
    async def test_send_audio_message_to_group(self, httpx_mock: HTTPXMock, client):
        """Test sending audio message to group."""
        response_data = {
            "message_id": "test-message-id",
            "success": True,
            "text": "Voice message",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=response_data,
            status_code=200,
        )

        await client.send_audio_message(
            group="group-123",
            text="Voice message",
            media_url="https://example.com/audio.mp3",
            sender_name="TestSender",
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["group"] == "group-123"

    @pytest.mark.asyncio
    async def test_get_message_status(self, httpx_mock: HTTPXMock, client):
        """Test getting message status."""
        response_data = {
            "message_id": "test-message-id",
            "status": "delivered",
            "contact": "+1234567890",
            "text": "Hello world",
            "last_update": "2023-12-31T23:59:59.000Z",
        }

        httpx_mock.add_response(
            method="GET",
            url="https://a.loopmessage.com/v1/message/status/test-message-id/",
            json=response_data,
            status_code=200,
        )

        response = await client.get_message_status("test-message-id")

        assert isinstance(response, MessageStatusResponse)
        assert response.message_id == "test-message-id"
        assert response.status == MessageStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_generate_opt_in_url(self, httpx_mock: HTTPXMock, client):
        """Test generating opt-in URL."""
        response_data = {
            "id": "3718be9c-17bc-412e-9790-c4768ca5df3e",
            "imessage": "imessage://ahoy%40imsg.tel&body=Subscribe%20%5Bopt-in-code%5D",
            "sms": "sms:ahoy%40imsg.tel&body=Subscribe%20%5Bopt-in-code%5D",
            "url": "https://opt-in.imsg.link/opt-in/0Rig0/?id=3718be9c",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/opt-in/generate-url/",
            json=response_data,
            status_code=200,
        )

        response = await client.generate_opt_in_url(
            body="Subscribe [opt-in-code]",
            click_id="abc123",
            utm_campaign="summer_sale",
        )

        assert isinstance(response, OptInUrlResponse)
        assert response.id == "3718be9c-17bc-412e-9790-c4768ca5df3e"
        assert "imessage://" in response.imessage
        assert "sms:" in response.sms
        assert "https://" in response.url

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)
        assert request_data["body"] == "Subscribe [opt-in-code]"
        assert request_data["click_id"] == "abc123"
        assert request_data["utm_campaign"] == "summer_sale"

    @pytest.mark.asyncio
    async def test_generate_opt_in_url_missing_placeholder(self, client):
        """Test opt-in URL generation without placeholder."""
        with pytest.raises(InvalidParameterError):
            await client.generate_opt_in_url(body="Subscribe now!")

    @pytest.mark.asyncio
    async def test_error_handling_404(self, httpx_mock: HTTPXMock, client):
        """Test 404 error handling."""
        httpx_mock.add_response(
            method="GET",
            url="https://a.loopmessage.com/v1/message/status/nonexistent/",
            status_code=404,
        )

        with pytest.raises(MessageNotFoundError):
            await client.get_message_status("nonexistent")

    @pytest.mark.asyncio
    async def test_error_handling_api_error(self, httpx_mock: HTTPXMock, client):
        """Test API error response handling."""
        error_data = {
            "success": False,
            "code": 125,
            "message": "Authorization key is invalid or does not exist",
        }

        httpx_mock.add_response(
            method="POST",
            url="https://a.loopmessage.com/api/v1/message/send/",
            json=error_data,
            status_code=400,
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await client.send_message(
                contact="+1234567890",
                text="Hello",
            )

        assert exc_info.value.code == 125

    def test_parse_webhook(self, client):
        """Test webhook parsing."""
        webhook_data = {
            "webhook_id": "webhook-123",
            "event": "message_inbound",
            "message_id": "msg-123",
            "contact": "+1234567890",
            "text": "Hello",
            "api_version": "1.0",
        }

        event = client.parse_webhook(webhook_data)
        assert event.webhook_id == "webhook-123"
        assert event.event.value == "message_inbound"
        assert event.contact == "+1234567890"

    def test_parse_webhook_json_string(self, client):
        """Test webhook parsing from JSON string."""
        webhook_data = {
            "webhook_id": "webhook-123",
            "event": "message_inbound",
            "api_version": "1.0",
        }
        json_string = json.dumps(webhook_data)

        event = client.parse_webhook(json_string)
        assert event.webhook_id == "webhook-123"

    def test_parse_webhook_with_opt_in_parameters(self, client):
        """Test webhook parsing with opt-in custom parameters."""
        webhook_data = {
            "webhook_id": "webhook-123",
            "event": "opt-in",
            "contact": "+155566678958",
            "message_id": "2a12f7ed-da37-49fd-bbf9-e2965adfb01d",
            "text": "Hey guy, want to test end-to-end analytics a little?",
            "parameters": {
                "click_id": "asdasads1241412fdsf",
                "utm_medium": "google",
                "utm_campaign": "credit on card online",
            },
            "api_version": "1.0",
        }

        event = client.parse_webhook(webhook_data)
        assert event.event.value == "opt-in"
        assert event.parameters is not None
        assert event.parameters["click_id"] == "asdasads1241412fdsf"
        assert event.parameters["utm_campaign"] == "credit on card online"
