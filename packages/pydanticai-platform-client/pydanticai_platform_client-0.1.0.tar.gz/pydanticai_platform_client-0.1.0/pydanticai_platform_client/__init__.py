"""PydanticAI Platform Client SDK.

A lightweight client for the PydanticAI Multi-Agent Platform API.

Example:
    ```python
    from pydanticai_platform_client import PlatformClient

    async with PlatformClient("https://api.example.com", "pk_abc123") as client:
        # Chat with an agent
        response = await client.chat("Hello!", agent="research")
        print(response.text)

        # Stream a response
        async for chunk in client.chat_stream("Tell me more"):
            print(chunk, end="")

        # Check usage
        usage = await client.get_usage()
        print(f"Tokens used: {usage.total_tokens}")
    ```
"""

from .client import PlatformClient
from .exceptions import (
    AgentNotFoundError,
    AuthenticationError,
    ConversationNotFoundError,
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

__version__ = "0.1.0"

__all__ = [
    # Client
    "PlatformClient",
    # Models
    "ChatResponse",
    "AgentInfo",
    "UsageStats",
    "ConversationSummary",
    "ConversationHistory",
    # Exceptions
    "PlatformError",
    "AuthenticationError",
    "RateLimitError",
    "TokenLimitError",
    "AgentNotFoundError",
    "ConversationNotFoundError",
]
