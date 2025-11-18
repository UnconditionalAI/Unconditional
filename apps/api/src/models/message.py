"""Message models for Unconditional API.

Defines the structure of incoming user messages and outgoing system responses.
"""

from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    """Incoming message from user."""

    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User's message content",
    )

    def __str__(self) -> str:
        return self.content


class ConversationHistory(BaseModel):
    """Full conversation context for stateless processing."""

    messages: list[dict[str, str]] = Field(
        default_factory=list,
        description="Array of {role: 'user'|'assistant', content: str}",
    )

    def add_user_message(self, content: str) -> None:
        """Add user message to history."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        """Add assistant message to history."""
        self.messages.append({"role": "assistant", "content": content})
