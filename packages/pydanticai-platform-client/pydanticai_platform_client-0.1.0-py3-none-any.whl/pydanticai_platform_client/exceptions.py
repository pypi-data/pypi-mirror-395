"""Exception classes for the Platform Client SDK."""


class PlatformError(Exception):
    """Base exception for platform errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(PlatformError):
    """Raised when API key is invalid or missing."""

    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, status_code=401)


class RateLimitError(PlatformError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class TokenLimitError(PlatformError):
    """Raised when monthly token limit is exceeded."""

    def __init__(
        self,
        message: str = "Monthly token limit exceeded",
        tokens_used: int | None = None,
        limit: int | None = None,
    ):
        super().__init__(message, status_code=429)
        self.tokens_used = tokens_used
        self.limit = limit


class AgentNotFoundError(PlatformError):
    """Raised when requested agent is not available."""

    def __init__(self, agent_name: str):
        super().__init__(f"Agent '{agent_name}' not found or not accessible", status_code=404)
        self.agent_name = agent_name


class ConversationNotFoundError(PlatformError):
    """Raised when conversation is not found."""

    def __init__(self, conversation_id: str):
        super().__init__(f"Conversation '{conversation_id}' not found", status_code=404)
        self.conversation_id = conversation_id
