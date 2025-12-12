"""LoopMessage Beta API client."""

import asyncio
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from pydantic import ValidationError

from ..exceptions import (
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
from .enums import MessageEffect
from .models import (
    MessageStatusResponse,
    OptInUrlResponse,
    SendMessageResponse,
    WebhookEvent,
)


class BetaLoopMessageClient:
    """Async client for the LoopMessage Beta API."""

    BASE_URL = "https://a.loopmessage.com/api/v1/"
    # Status endpoint uses a different base path (no /api/ prefix)
    STATUS_BASE_URL = "https://a.loopmessage.com/v1/"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the LoopMessage Beta client.

        Args:
            api_key: Your API key (Authorization header)
            base_url: Custom base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries

        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "BetaLoopMessageClient":
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
                    "Authorization": self.api_key,
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
            elif code in [120, 140, 150, 570, 580, 590, 595, 600, 610, 620, 630, 640]:
                raise InvalidParameterError(message, code)
            elif code in [160, 170, 180, 190, 270, 280]:
                raise InvalidRecipientError(message, code)
            elif code in [210, 220, 230, 240, 540, 545, 550, 560]:
                raise SenderNameError(message, code)
            elif code in [400]:
                raise InsufficientCreditsError(message, code)
            elif code in [500, 510, 520, 530]:
                raise AccountSuspendedError(message, code)
            elif code in [1000, 1010, 1020, 1030, 1110, 1120, 1130, 1140]:
                raise DeliveryError(message, code)
            else:
                raise LoopMessageError(message, code)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        retries: int = 0,
        use_status_base: bool = False,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        client = await self._get_client()
        base = self.STATUS_BASE_URL if use_status_base else self.base_url
        url = urljoin(base, endpoint)

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
                    raise LoopMessageError(
                        f"HTTP {e.response.status_code}: Unhandled error"
                    )
                except Exception:
                    raise LoopMessageError(
                        f"HTTP {e.response.status_code}: {e.response.text}"
                    ) from e

        except httpx.RequestError as e:
            if retries < self.max_retries:
                await asyncio.sleep(2**retries)  # Exponential backoff
                return await self._make_request(
                    method, endpoint, data, retries + 1, use_status_base
                )
            raise LoopMessageError(f"Request failed: {str(e)}") from e

    async def send_message(
        self,
        contact: str,
        text: str,
        subject: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        effect: Optional[MessageEffect] = None,
        reply_to_id: Optional[str] = None,
    ) -> SendMessageResponse:
        """
        Send a message to a contact.

        Args:
            contact: Phone number, email, or Contact ID
            text: Message text (max 10000 characters)
            subject: Optional message subject (shown as bold title)
            attachments: List of attachment URLs (max 3, HTTPS only, max 256 chars each)
            effect: Message effect (slam, loud, gentle, etc.)
            reply_to_id: Message ID to reply to (from webhook)

        Returns:
            SendMessageResponse: Response with message ID and details
        """
        if not contact:
            raise InvalidParameterError("Contact must be specified")

        data: Dict[str, Any] = {
            "contact": contact,
            "text": text,
        }

        if subject:
            data["subject"] = subject
        if attachments:
            data["attachments"] = attachments
        if effect:
            data["effect"] = effect.value
        if reply_to_id:
            data["reply_to_id"] = reply_to_id

        response_data = await self._make_request("POST", "message/send/", data)
        return SendMessageResponse(**response_data)

    async def send_audio_message(
        self,
        contact: Optional[str] = None,
        group: Optional[str] = None,
        text: str = "",
        media_url: str = "",
        sender_name: str = "",
        passthrough: Optional[str] = None,
        status_callback: Optional[str] = None,
        status_callback_header: Optional[str] = None,
    ) -> SendMessageResponse:
        """
        Send an audio message.

        Args:
            contact: Phone number or email (for individual messages)
            group: Group ID (for group messages)
            text: Message text
            media_url: URL of the audio file (HTTPS, max 256 chars)
                       Supported formats: mp3, wav, m4a, caf, aac
            sender_name: Your dedicated sender name
            passthrough: Metadata to store with the message (max 1000 chars)
            status_callback: URL for status updates (max 256 chars)
            status_callback_header: Authorization header for callbacks (max 256 chars)

        Returns:
            SendMessageResponse: Response with message ID and details
        """
        if not contact and not group:
            raise InvalidParameterError("Either contact or group must be specified")

        data: Dict[str, Any] = {
            "text": text,
            "media_url": media_url,
            "sender_name": sender_name,
            "audio_message": True,
        }

        if contact:
            data["recipient"] = contact
        if group:
            data["group"] = group
        if passthrough:
            data["passthrough"] = passthrough
        if status_callback:
            data["status_callback"] = status_callback
        if status_callback_header:
            data["status_callback_header"] = status_callback_header

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
        # Beta API uses /v1/message/status/{id}/ without 'api' prefix
        response_data = await self._make_request(
            "GET", f"message/status/{message_id}/", use_status_base=True
        )
        return MessageStatusResponse(**response_data)

    async def generate_opt_in_url(
        self,
        body: str = "[opt-in-code]",
        **custom_parameters: Any,
    ) -> OptInUrlResponse:
        """
        Generate an opt-in URL for user subscription.

        Args:
            body: Custom message body. Must contain [opt-in-code] placeholder
                  which will be replaced with a unique code.
            **custom_parameters: Any additional parameters (click_id, utm_campaign, etc.)
                                 These will be returned in the webhook when user opts in.

        Returns:
            OptInUrlResponse: Contains iMessage, SMS, and smart link URLs

        Example:
            response = await client.generate_opt_in_url(
                body="Subscribe to updates! [opt-in-code]",
                click_id="abc123",
                utm_campaign="summer_sale"
            )
        """
        if "[opt-in-code]" not in body:
            raise InvalidParameterError("body must contain [opt-in-code] placeholder")

        data: Dict[str, Any] = {"body": body}
        data.update(custom_parameters)

        response_data = await self._make_request("POST", "opt-in/generate-url/", data)
        return OptInUrlResponse(**response_data)

    def parse_webhook(self, webhook_data: Union[Dict[str, Any], str]) -> WebhookEvent:
        """
        Parse webhook data into a WebhookEvent model.

        Args:
            webhook_data: Raw webhook data (dict or JSON string)

        Returns:
            WebhookEvent: Parsed webhook event

        Raises:
            LoopMessageError: If webhook data is invalid
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
