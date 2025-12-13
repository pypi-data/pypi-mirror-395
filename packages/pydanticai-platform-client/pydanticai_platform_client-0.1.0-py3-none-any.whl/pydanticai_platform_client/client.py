"""Platform Client for calling the PydanticAI Multi-Agent API."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from .exceptions import (
    AgentNotFoundError,
    AuthenticationError,
    PlatformError,
    RateLimitError,
    TokenLimitError,
)
from .models import (
    AgentInfo,
    ChatResponse,
    ConversationHistory,
    ConversationSummary,
    UsageStats,
)


class PlatformClient:
    """Async client for the PydanticAI Multi-Agent Platform.

    Example:
        ```python
        from pydanticai_platform_client import PlatformClient

        async with PlatformClient("https://api.example.com", "pk_abc123") as client:
            response = await client.chat("Hello!", agent="research")
            print(response.text)

            # Continue the conversation
            response = await client.chat(
                "Tell me more",
                conversation_id=response.conversation_id,
            )
        ```
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        """Initialize the platform client.

        Args:
            base_url: Base URL of the platform API (e.g., "https://api.example.com").
            api_key: Tenant API key for authentication.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for transient failures.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> PlatformClient:
        """Enter async context manager."""
        await self._ensure_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context manager."""
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=f"{self.base_url}/api/v1/platform",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses."""
        if response.status_code == 401:
            raise AuthenticationError()

        if response.status_code == 429:
            try:
                detail = response.json().get("detail", {})
                if isinstance(detail, dict) and "tokens_used" in detail:
                    raise TokenLimitError(
                        tokens_used=detail.get("tokens_used"),
                        limit=detail.get("limit"),
                    )
            except (json.JSONDecodeError, AttributeError):
                pass
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(retry_after=int(retry_after) if retry_after else None)

        if response.status_code in (403, 404):
            try:
                detail = response.json().get("detail", "")
                if "Agent" in detail:
                    # Extract agent name from error message
                    raise AgentNotFoundError(detail.split("'")[1] if "'" in detail else "unknown")
            except (json.JSONDecodeError, IndexError):
                pass

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except json.JSONDecodeError:
                detail = response.text
            raise PlatformError(str(detail), status_code=response.status_code)

    async def chat(
        self,
        prompt: str,
        *,
        agent: str | None = None,
        conversation_id: str | None = None,
    ) -> ChatResponse:
        """Send a message and get a complete response.

        Args:
            prompt: The message to send.
            agent: Agent to use (uses tenant default if not specified).
            conversation_id: Continue an existing conversation.

        Returns:
            ChatResponse with the agent's reply.

        Raises:
            AuthenticationError: If API key is invalid.
            RateLimitError: If rate limit is exceeded.
            TokenLimitError: If monthly token limit is exceeded.
            AgentNotFoundError: If requested agent is not available.
        """
        client = await self._ensure_client()

        payload: dict[str, Any] = {"prompt": prompt}
        if agent:
            payload["agent"] = agent
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = await client.post("/chat", json=payload)
        self._handle_error(response)

        data = response.json()
        return ChatResponse(
            text=data["response"],
            conversation_id=data["conversation_id"],
            agent=data["agent"],
            model=data["model"],
        )

    async def chat_stream(
        self,
        prompt: str,
        *,
        agent: str | None = None,
        conversation_id: str | None = None,
    ) -> AsyncIterator[str]:
        """Send a message and stream the response.

        Args:
            prompt: The message to send.
            agent: Agent to use (uses tenant default if not specified).
            conversation_id: Continue an existing conversation.

        Yields:
            Chunks of the response text as they arrive.

        Raises:
            AuthenticationError: If API key is invalid.
            RateLimitError: If rate limit is exceeded.
            TokenLimitError: If monthly token limit is exceeded.
            AgentNotFoundError: If requested agent is not available.
        """
        client = await self._ensure_client()

        payload: dict[str, Any] = {"prompt": prompt}
        if agent:
            payload["agent"] = agent
        if conversation_id:
            payload["conversation_id"] = conversation_id

        async with client.stream("POST", "/chat/stream", json=payload) as response:
            if response.status_code >= 400:
                await response.aread()
                self._handle_error(response)

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if data.get("done"):
                        return
                    if chunk := data.get("chunk"):
                        yield chunk

    async def list_agents(self) -> list[AgentInfo]:
        """List agents available to this tenant.

        Returns:
            List of available agents.
        """
        client = await self._ensure_client()
        response = await client.get("/agents")
        self._handle_error(response)

        return [
            AgentInfo(name=a["name"], description=a.get("description")) for a in response.json()
        ]

    async def get_usage(self, days: int = 30) -> UsageStats:
        """Get usage statistics for this tenant.

        Args:
            days: Number of days to include (default 30).

        Returns:
            Usage statistics including tokens, requests, and costs.
        """
        client = await self._ensure_client()
        response = await client.get("/usage", params={"days": days})
        self._handle_error(response)

        data = response.json()
        return UsageStats(
            tenant_id=data["tenant_id"],
            period_days=data["period_days"],
            total_requests=data["total_requests"],
            total_tokens=data["total_tokens"],
            estimated_cost_usd=data["estimated_cost_usd"],
            by_model=data.get("by_model", {}),
            by_agent=data.get("by_agent", {}),
        )

    async def list_conversations(self, limit: int = 20) -> list[ConversationSummary]:
        """List recent conversations.

        Args:
            limit: Maximum number of conversations to return.

        Returns:
            List of conversation summaries.
        """
        client = await self._ensure_client()
        response = await client.get("/conversations", params={"limit": limit})
        self._handle_error(response)

        return [
            ConversationSummary(
                conversation_id=c["conversation_id"],
                created_at=c.get("created_at"),
                updated_at=c.get("updated_at"),
                message_count=c.get("message_count", 0),
            )
            for c in response.json()
        ]

    async def get_conversation(self, conversation_id: str) -> ConversationHistory:
        """Get the full history of a conversation.

        Args:
            conversation_id: The conversation to retrieve.

        Returns:
            Full conversation history with all messages.
        """
        client = await self._ensure_client()
        response = await client.get(f"/conversations/{conversation_id}")
        self._handle_error(response)

        data = response.json()
        return ConversationHistory(
            conversation_id=data["conversation_id"],
            messages=data["messages"],
        )

    async def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation's history.

        Args:
            conversation_id: The conversation to clear.

        Returns:
            True if conversation was cleared, False if not found.
        """
        client = await self._ensure_client()
        response = await client.delete(f"/conversations/{conversation_id}")
        self._handle_error(response)

        return response.json().get("status") == "cleared"
