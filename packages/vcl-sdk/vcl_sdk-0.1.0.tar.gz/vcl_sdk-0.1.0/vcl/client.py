"""VCL Client - Drop-in replacement for OpenAI/Anthropic clients"""

import json
from typing import Any, Dict, Iterator, List, Optional, Union
import requests

from .exceptions import (
    AuthenticationError,
    RateLimitError,
    ServerError,
    ValidationError,
    VCLError,
)
from .receipts import Receipt, verify_receipt


class ChatCompletions:
    """OpenAI-compatible chat completions interface"""

    def __init__(self, client: "VCLClient"):
        self._client = client

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs,
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Create a chat completion (OpenAI-compatible).

        Args:
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            messages: List of message dicts with "role" and "content"
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Completion response dict or iterator for streaming
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }

        if stream:
            return self._stream_request(payload)
        else:
            return self._request(payload)

    def _request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a non-streaming request"""
        response = self._client._post("/v1/proxy/openai/chat/completions", payload)
        return response

    def _stream_request(
        self, payload: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Make a streaming request"""
        url = f"{self._client.base_url}/v1/proxy/openai/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._client.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=True,
            timeout=self._client.timeout,
        )

        self._client._handle_response_errors(response)

        # Store receipt ID from header
        receipt_id = response.headers.get("X-VCL-Receipt-ID")
        if receipt_id:
            self._client._last_receipt_id = receipt_id

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        continue


class Chat:
    """OpenAI-compatible chat interface"""

    def __init__(self, client: "VCLClient"):
        self.completions = ChatCompletions(client)


class Messages:
    """Anthropic-compatible messages interface"""

    def __init__(self, client: "VCLClient"):
        self._client = client

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        stream: bool = False,
        **kwargs,
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Create a message (Anthropic-compatible).

        Args:
            model: Model name (e.g., "claude-3-sonnet-20240229")
            messages: List of message dicts with "role" and "content"
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, system, etc.)

        Returns:
            Message response dict or iterator for streaming
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs,
        }

        if stream:
            return self._stream_request(payload)
        else:
            return self._request(payload)

    def _request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a non-streaming request"""
        response = self._client._post("/v1/proxy/anthropic/messages", payload)
        return response

    def _stream_request(
        self, payload: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Make a streaming request"""
        url = f"{self._client.base_url}/v1/proxy/anthropic/messages"
        headers = {
            "Authorization": f"Bearer {self._client.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=True,
            timeout=self._client.timeout,
        )

        self._client._handle_response_errors(response)

        # Store receipt ID from header
        receipt_id = response.headers.get("X-VCL-Receipt-ID")
        if receipt_id:
            self._client._last_receipt_id = receipt_id

        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        continue


class VCLClient:
    """
    VCL Client - Drop-in replacement for OpenAI/Anthropic clients.

    Provides OpenAI-compatible and Anthropic-compatible interfaces while
    generating cryptographically signed receipts for every request.

    Example:
        client = VCLClient(
            api_key="vcl_...",
            base_url="https://your-vcl-server.com"
        )

        # OpenAI-compatible
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )

        # Anthropic-compatible
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=1024
        )

        # Get receipt
        receipt = client.last_receipt
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8080",
        timeout: int = 120,
    ):
        """
        Initialize VCL client.

        Args:
            api_key: Your VCL API key (starts with "vcl_")
            base_url: VCL server URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._last_receipt_id: Optional[str] = None
        self._last_receipt: Optional[Receipt] = None

        # OpenAI-compatible interface
        self.chat = Chat(self)

        # Anthropic-compatible interface
        self.messages = Messages(self)

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _handle_response_errors(self, response: requests.Response):
        """Handle HTTP response errors"""
        if response.status_code == 401:
            raise AuthenticationError(
                "Invalid API key",
                status_code=401,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded",
                status_code=429,
            )
        elif response.status_code == 400:
            try:
                error = response.json()
            except:
                error = {}
            raise ValidationError(
                error.get("error", "Bad request"),
                status_code=400,
                response=error,
            )
        elif response.status_code >= 500:
            raise ServerError(
                f"Server error: {response.status_code}",
                status_code=response.status_code,
            )
        elif not response.ok:
            raise VCLError(
                f"Request failed: {response.status_code}",
                status_code=response.status_code,
            )

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request"""
        url = f"{self.base_url}{path}"

        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout,
        )

        self._handle_response_errors(response)

        # Store receipt ID from header
        receipt_id = response.headers.get("X-VCL-Receipt-ID")
        if receipt_id:
            self._last_receipt_id = receipt_id
            self._last_receipt = None  # Clear cached receipt

        return response.json()

    def _get(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a GET request"""
        url = f"{self.base_url}{path}"

        response = requests.get(
            url,
            params=params,
            headers=self._get_headers(),
            timeout=self.timeout,
        )

        self._handle_response_errors(response)
        return response.json()

    @property
    def last_receipt_id(self) -> Optional[str]:
        """Get the receipt ID from the last request"""
        return self._last_receipt_id

    @property
    def last_receipt(self) -> Optional[Receipt]:
        """
        Get the full receipt from the last request.

        Fetches the receipt from the server if not already cached.
        """
        if self._last_receipt_id is None:
            return None

        if self._last_receipt is None:
            self._last_receipt = self.get_receipt(self._last_receipt_id)

        return self._last_receipt

    def get_receipt(self, receipt_id: str) -> Receipt:
        """
        Get a receipt by ID.

        Args:
            receipt_id: The receipt ID

        Returns:
            Receipt object
        """
        data = self._get(f"/v1/receipts/{receipt_id}")
        return Receipt.from_dict(data)

    def list_receipts(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        List receipts.

        Args:
            limit: Maximum number of receipts to return
            offset: Offset for pagination

        Returns:
            Dict with "receipts" list and pagination info
        """
        return self._get("/v1/receipts", {"limit": limit, "offset": offset})

    def verify_receipt(self, receipt_id: str) -> Dict[str, Any]:
        """
        Verify a receipt.

        Args:
            receipt_id: The receipt ID to verify

        Returns:
            Verification result dict
        """
        return verify_receipt(self.base_url, receipt_id)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.

        Returns:
            Dict with total_receipts, total_compute_units, etc.
        """
        return self._get("/v1/stats")

    def health(self) -> Dict[str, Any]:
        """
        Get server health status.

        Returns:
            Health status dict
        """
        url = f"{self.base_url}/health"
        response = requests.get(url, timeout=self.timeout)
        return response.json()

    def create_api_key(self, name: str = "SDK Key") -> Dict[str, Any]:
        """
        Create a new API key.

        Args:
            name: Name for the new key

        Returns:
            Dict with new key details including the key itself
        """
        return self._post("/v1/auth/keys", {"name": name})

    def list_api_keys(self) -> Dict[str, Any]:
        """
        List API keys.

        Returns:
            Dict with "keys" list
        """
        return self._get("/v1/auth/keys")

    def delete_api_key(self, key_id: str) -> None:
        """
        Delete an API key.

        Args:
            key_id: The key ID to delete
        """
        url = f"{self.base_url}/v1/auth/keys/{key_id}"
        response = requests.delete(
            url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._handle_response_errors(response)
