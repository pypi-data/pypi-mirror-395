from typing import List, Optional
import httpx

from .types import Message, ChatResponse, ChatChoice, Usage


class CaistroError(Exception):
    """Exception raised for Caistro API errors."""

    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"[{status}] {message}")


class Caistro:
    """Official Caistro API client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.caistrolabs.com",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def chat(
        self,
        messages: List[Message],
        model: str = "Nous-20B",
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> ChatResponse:
        """Send a chat completion request."""
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = self._client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
        )

        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            raise CaistroError(
                response.status_code,
                error_data.get("message", "API request failed"),
            )

        data = response.json()
        return ChatResponse(
            id=data["id"],
            object=data["object"],
            model=data["model"],
            choices=[
                ChatChoice(
                    index=c["index"],
                    message=Message(
                        role=c["message"]["role"],
                        content=c["message"]["content"],
                    ),
                    finish_reason=c["finish_reason"],
                )
                for c in data["choices"]
            ],
            usage=Usage(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"],
            ),
        )

    def list_models(self) -> dict:
        """List available models."""
        response = self._client.get(f"{self.base_url}/v1/models")

        if response.status_code != 200:
            raise CaistroError(response.status_code, "Failed to list models")

        return response.json()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class AsyncCaistro:
    """Async Caistro API client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.caistrolabs.com",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def chat(
        self,
        messages: List[Message],
        model: str = "Nous-20B",
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> ChatResponse:
        """Send a chat completion request."""
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = await self._client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
        )

        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            raise CaistroError(
                response.status_code,
                error_data.get("message", "API request failed"),
            )

        data = response.json()
        return ChatResponse(
            id=data["id"],
            object=data["object"],
            model=data["model"],
            choices=[
                ChatChoice(
                    index=c["index"],
                    message=Message(
                        role=c["message"]["role"],
                        content=c["message"]["content"],
                    ),
                    finish_reason=c["finish_reason"],
                )
                for c in data["choices"]
            ],
            usage=Usage(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"],
            ),
        )

    async def list_models(self) -> dict:
        """List available models."""
        response = await self._client.get(f"{self.base_url}/v1/models")

        if response.status_code != 200:
            raise CaistroError(response.status_code, "Failed to list models")

        return response.json()

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
