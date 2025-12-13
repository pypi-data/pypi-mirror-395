# PydanticAI Platform Client

A lightweight Python client for the PydanticAI Multi-Agent Platform API.

## Installation

```bash
pip install pydanticai-platform-client
```

Or install from source:

```bash
pip install -e sdk/
```

## Quick Start

```python
from pydanticai_platform_client import PlatformClient

async def main():
    async with PlatformClient(
        base_url="https://your-platform.fly.dev",
        api_key="pk_your_tenant_key",
    ) as client:
        # Chat with the default agent
        response = await client.chat("What's the weather like?")
        print(response.text)

        # Use a specific agent
        response = await client.chat(
            "Analyze this data: [1, 2, 3, 4, 5]",
            agent="analyst",
        )
        print(response.text)

        # Continue a conversation
        response = await client.chat(
            "Tell me more",
            conversation_id=response.conversation_id,
        )
```

## Streaming Responses

```python
async with PlatformClient(base_url, api_key) as client:
    async for chunk in client.chat_stream("Write a poem about Python"):
        print(chunk, end="", flush=True)
    print()  # newline at the end
```

## Available Methods

| Method | Description |
|--------|-------------|
| `chat(prompt, agent?, conversation_id?)` | Send a message, get complete response |
| `chat_stream(prompt, agent?, conversation_id?)` | Stream response chunks |
| `list_agents()` | List available agents |
| `get_usage(days=30)` | Get usage statistics |
| `list_conversations(limit=20)` | List recent conversations |
| `get_conversation(id)` | Get full conversation history |
| `clear_conversation(id)` | Delete a conversation |

## Error Handling

```python
from pydanticai_platform_client import (
    PlatformClient,
    AuthenticationError,
    RateLimitError,
    TokenLimitError,
    AgentNotFoundError,
)

async with PlatformClient(base_url, api_key) as client:
    try:
        response = await client.chat("Hello")
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError as e:
        print(f"Rate limited, retry after {e.retry_after}s")
    except TokenLimitError as e:
        print(f"Token limit exceeded: {e.tokens_used}/{e.limit}")
    except AgentNotFoundError as e:
        print(f"Agent not found: {e.agent_name}")
```

## Response Models

### ChatResponse
```python
@dataclass
class ChatResponse:
    text: str              # The agent's response
    conversation_id: str   # ID for continuing the conversation
    agent: str             # Agent that handled the request
    model: str             # Model used
```

### UsageStats
```python
@dataclass
class UsageStats:
    tenant_id: str
    period_days: int
    total_requests: int
    total_tokens: int
    estimated_cost_usd: float
    by_model: dict[str, int]
    by_agent: dict[str, int]
```

## License

MIT
