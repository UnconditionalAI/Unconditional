"""Response models for Unconditional API.

Defines the structure of all API responses including normal conversation
responses and crisis intervention responses.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ResponseType(str, Enum):
    """Type of response being returned."""

    NORMAL = "normal"
    CRISIS = "crisis"


class CrisisResource(BaseModel):
    """Crisis support resource information."""

    name: str
    phone: str
    available: str
    description: Optional[str] = None


class ConversationResponse(BaseModel):
    """Standard conversation response."""

    type: ResponseType = ResponseType.NORMAL
    content: str = Field(..., description="Assistant's response text")
    timestamp: str = Field(..., description="ISO 8601 timestamp")


class CrisisResponse(BaseModel):
    """Crisis intervention response with resources."""

    type: ResponseType = ResponseType.CRISIS
    content: str = Field(..., description="Crisis support message")
    resources: list[CrisisResource] = Field(
        ..., description="Crisis hotlines and resources"
    )
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    session_locked: bool = Field(
        default=True, description="Whether the session is locked"
    )
