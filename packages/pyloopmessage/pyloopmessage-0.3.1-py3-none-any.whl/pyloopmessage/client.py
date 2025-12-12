"""LoopMessage API client."""

import asyncio
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from pydantic import ValidationError

from .enums import MessageEffect, ReactionType, ServiceType
from .exceptions import (
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
from .models import (
    MessageStatusResponse,
    SendMessageResponse,
    WebhookEvent,
)


class LoopMessageClient:
    """Async client for the LoopMessage API."""

    BASE_URL = "https://server.loopmessage.com/api/v1/"

    def __init__(
        self,
        authorization_key: str,
        secret_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the LoopMessage client.

        Args:
            authorization_key: Your authorization key
            secret_key: Your API secret key
            base_url: Custom base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.authorization_key = authorization_key
        self.secret_key = secret_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries

        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "LoopMessageClient":
        """Async context manager entry."""
        await self._get_client()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": self.authorization_key,
                    "Loop-Secret-Key": self.secret_key,
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _handle_error_response(self, response_data: Dict[str, Any]) -> None:
        """Handle API error responses."""
        if not response_data.get("success", True):
            code = response_data.get("code", 0)
            message = response_data.get("message", "Unknown error")

            # Map error codes to specific exceptions
            if code in [110, 125]:
                raise AuthenticationError(message, code)
            elif code in [130]:
                raise AuthenticationError(message, code)
            elif code in [120, 140, 150]:
                raise InvalidParameterError(message, code)
            elif code in [160, 170, 180, 190]:
                raise InvalidRecipientError(message, code)
            elif code in [210, 220, 230, 240, 545]:
                raise SenderNameError(message, code)
            elif code in [330]:
                raise RateLimitError(message, code)
            elif code in [400]:
                raise InsufficientCreditsError(message, code)
            elif code in [500, 510, 530]:
                raise AccountSuspendedError(message, code)
            elif code in [100, 110, 120, 130, 140, 150]:
                raise DeliveryError(message, code)
            else:
                raise LoopMessageError(message, code)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        retries: int = 0,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        client = await self._get_client()
        url = urljoin(self.base_url, endpoint)

        try:
            if method.upper() == "GET":
                response = await client.get(url)
            elif method.upper() == "POST":
                response = await client.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Try to parse JSON response first
            try:
                response_data: Dict[str, Any] = response.json()
                # Handle API errors in JSON response (even if HTTP status is 4xx)
                if "success" in response_data and not response_data["success"]:
                    self._handle_error_response(response_data)

                # If we get here and status is bad, raise HTTP error
                response.raise_for_status()
                return response_data
            except ValueError:
                # No JSON response, just check HTTP status
                response.raise_for_status()
                return {}

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise MessageNotFoundError("Message not found", 404) from e
            elif e.response.status_code == 402:
                raise InsufficientCreditsError("Insufficient credits", 402) from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed", 401) from e
            else:
                try:
                    error_data = e.response.json()
                    self._handle_error_response(error_data)
                    # This should never be reached as _handle_error_response always raises
                    raise LoopMessageError(f"HTTP {e.response.status_code}: Unhandled error")
                except Exception:
                    raise LoopMessageError(f"HTTP {e.response.status_code}: {e.response.text}") from e

        except httpx.RequestError as e:
            if retries < self.max_retries:
                await asyncio.sleep(2**retries)  # Exponential backoff
                return await self._make_request(method, endpoint, data, retries + 1)
            raise LoopMessageError(f"Request failed: {str(e)}") from e

    async def send_message(
        self,
        recipient: Optional[str] = None,
        group: Optional[str] = None,
        text: str = "",
        sender_name: str = "",
        attachments: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        passthrough: Optional[str] = None,
        status_callback: Optional[str] = None,
        status_callback_header: Optional[str] = None,
        reply_to_id: Optional[str] = None,
        subject: Optional[str] = None,
        effect: Optional[MessageEffect] = None,
        service: Optional[ServiceType] = None,
    ) -> SendMessageResponse:
        """
        Send a message to a recipient or group.

        Args:
            recipient: Phone number or email (for individual messages)
            group: Group ID (for group messages)
            text: Message text
            sender_name: Your dedicated sender name
            attachments: List of attachment URLs (max 3)
            timeout: Request timeout in seconds (min 5)
            passthrough: Metadata to store with the message
            status_callback: URL for status updates
            status_callback_header: Authorization header for callbacks
            reply_to_id: Message ID to reply to
            subject: Message subject
            effect: Message effect
            service: Service type (imessage or sms)

        Returns:
            SendMessageResponse: Response with message ID and details
        """
        if not recipient and not group:
            raise InvalidParameterError("Either recipient or group must be specified")

        if recipient and group:
            raise InvalidParameterError("Cannot specify both recipient and group")

        data: Dict[str, Any] = {
            "text": text,
            "sender_name": sender_name,
        }

        if recipient:
            data["recipient"] = recipient
        if group:
            data["group"] = group
        if attachments:
            data["attachments"] = attachments
        if timeout:
            data["timeout"] = timeout
        if passthrough:
            data["passthrough"] = passthrough
        if status_callback:
            data["status_callback"] = status_callback
        if status_callback_header:
            data["status_callback_header"] = status_callback_header
        if reply_to_id:
            data["reply_to_id"] = reply_to_id
        if subject:
            data["subject"] = subject
        if effect:
            data["effect"] = effect.value
        if service:
            data["service"] = service.value

        response_data = await self._make_request("POST", "message/send/", data)
        return SendMessageResponse(**response_data)

    async def send_audio_message(
        self,
        recipient: Optional[str] = None,
        group: Optional[str] = None,
        text: str = "",
        media_url: str = "",
        sender_name: str = "",
        status_callback: Optional[str] = None,
        status_callback_header: Optional[str] = None,
        passthrough: Optional[str] = None,
    ) -> SendMessageResponse:
        """
        Send an audio message.

        Args:
            recipient: Phone number or email (for individual messages)
            group: Group ID (for group messages)
            text: Message text
            media_url: URL of the audio file
            sender_name: Your dedicated sender name
            status_callback: URL for status updates
            status_callback_header: Authorization header for callbacks
            passthrough: Metadata to store with the message

        Returns:
            SendMessageResponse: Response with message ID and details
        """
        if not recipient and not group:
            raise InvalidParameterError("Either recipient or group must be specified")

        data: Dict[str, Any] = {
            "text": text,
            "media_url": media_url,
            "sender_name": sender_name,
            "audio_message": True,
        }

        if recipient:
            data["recipient"] = recipient
        if group:
            data["group"] = group
        if status_callback:
            data["status_callback"] = status_callback
        if status_callback_header:
            data["status_callback_header"] = status_callback_header
        if passthrough:
            data["passthrough"] = passthrough

        response_data = await self._make_request("POST", "message/send/", data)
        return SendMessageResponse(**response_data)

    async def send_reaction(
        self,
        recipient: Optional[str] = None,
        group: Optional[str] = None,
        text: str = "",
        message_id: str = "",
        reaction: ReactionType = ReactionType.LIKE,
        sender_name: str = "",
        status_callback: Optional[str] = None,
        status_callback_header: Optional[str] = None,
        passthrough: Optional[str] = None,
    ) -> SendMessageResponse:
        """
        Send a reaction to a message.

        Args:
            recipient: Phone number or email (for individual messages)
            group: Group ID (for group messages)
            text: Message text
            message_id: ID of the message to react to
            reaction: Reaction type
            sender_name: Your dedicated sender name
            status_callback: URL for status updates
            status_callback_header: Authorization header for callbacks
            passthrough: Metadata to store with the message

        Returns:
            SendMessageResponse: Response with message ID and details
        """
        if not recipient and not group:
            raise InvalidParameterError("Either recipient or group must be specified")

        data: Dict[str, Any] = {
            "text": text,
            "message_id": message_id,
            "reaction": reaction.value,
            "sender_name": sender_name,
        }

        if recipient:
            data["recipient"] = recipient
        if group:
            data["group"] = group
        if status_callback:
            data["status_callback"] = status_callback
        if status_callback_header:
            data["status_callback_header"] = status_callback_header
        if passthrough:
            data["passthrough"] = passthrough

        response_data = await self._make_request("POST", "message/send/", data)
        return SendMessageResponse(**response_data)

    async def get_message_status(self, message_id: str) -> MessageStatusResponse:
        """
        Get the status of a message.

        Args:
            message_id: The message ID to check

        Returns:
            MessageStatusResponse: Current status of the message
        """
        response_data = await self._make_request("GET", f"message/status/{message_id}/")
        return MessageStatusResponse(**response_data)

    def parse_webhook(self, webhook_data: Union[Dict[str, Any], str]) -> WebhookEvent:
        """
        Parse webhook data into a WebhookEvent model.

        Args:
            webhook_data: Raw webhook data (dict or JSON string)

        Returns:
            WebhookEvent: Parsed webhook event

        Raises:
            ValidationError: If webhook data is invalid
        """
        parsed_data: Dict[str, Any]
        if isinstance(webhook_data, str):
            import json

            parsed_data = json.loads(webhook_data)
        else:
            parsed_data = webhook_data

        try:
            return WebhookEvent(**parsed_data)
        except ValidationError as e:
            raise LoopMessageError(f"Invalid webhook data: {e}") from e

    @staticmethod
    def create_webhook_response(
        typing_duration: Optional[int] = None, mark_as_read: bool = False
    ) -> Dict[str, Any]:
        """
        Create a webhook response.

        Args:
            typing_duration: Show typing indicator for this many seconds (1-60)
            mark_as_read: Mark the message as read

        Returns:
            Dict containing the webhook response
        """
        response = {}
        if typing_duration is not None:
            if not 1 <= typing_duration <= 60:
                raise ValueError("Typing duration must be between 1 and 60 seconds")
            response["typing"] = typing_duration
        if mark_as_read:
            response["read"] = True
        return response
