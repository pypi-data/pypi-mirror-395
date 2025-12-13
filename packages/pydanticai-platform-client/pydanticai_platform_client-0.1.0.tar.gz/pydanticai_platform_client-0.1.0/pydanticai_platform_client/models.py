"""Response models for the Platform Client SDK."""

from dataclasses import dataclass, field


@dataclass
class ChatResponse:
    """Response from a chat request."""

    text: str
    conversation_id: str
    agent: str
    model: str


@dataclass
class AgentInfo:
    """Information about an available agent."""

    name: str
    description: str | None = None


@dataclass
class UsageStats:
    """Usage statistics for a tenant."""

    tenant_id: str
    period_days: int
    total_requests: int
    total_tokens: int
    estimated_cost_usd: float
    by_model: dict[str, int] = field(default_factory=dict)
    by_agent: dict[str, int] = field(default_factory=dict)


@dataclass
class ConversationSummary:
    """Summary of a conversation."""

    conversation_id: str
    created_at: str | None = None
    updated_at: str | None = None
    message_count: int = 0


@dataclass
class ConversationHistory:
    """Full conversation history."""

    conversation_id: str
    messages: list[dict]
