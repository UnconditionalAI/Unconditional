"""Conversation endpoint for Unconditional API.

This is the core orchestrator. Every message flows through the same pipeline:
1. Input validation and banned pattern check
2. Crisis detection
3. Prompt assembly
4. LLM generation
5. Post-processing guardrails
6. Response formatting

Safety is not a feature. It is the foundation.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic_ai import Agent

from models.message import ConversationHistory, UserMessage
from models.response import (
    ConversationResponse,
    CrisisResource,
    CrisisResponse,
    ResponseType,
)
from prompts.opening import get_opening_message
from prompts.system import get_system_prompt
from safety.banned_patterns import contains_banned_content
from safety.crisis_detection import detect_crisis
from safety.guardrails import apply_guardrails, check_length
from services.llm.factory import get_llm_model

router = APIRouter()


# Global crisis resources
# Conservative list: US-focused for MVP, expandable for international
CRISIS_RESOURCES = [
    CrisisResource(
        name="988 Suicide & Crisis Lifeline",
        phone="988",
        available="24/7",
        description="Call or text 988 for free, confidential support",
    ),
    CrisisResource(
        name="Crisis Text Line",
        phone="Text HOME to 741741",
        available="24/7",
        description="Text-based crisis support",
    ),
    CrisisResource(
        name="National Domestic Violence Hotline",
        phone="1-800-799-7233",
        available="24/7",
        description="Support for domestic violence situations",
    ),
]


def build_crisis_response() -> CrisisResponse:
    """
    Build standardized crisis intervention response.

    Returns:
        CrisisResponse with resources and session lock

    Safety reasoning:
        - Consistent crisis messaging across all triggers
        - Immediate connection to real human support
        - Session locked to prevent further interaction
        - Grounding statement before resources
    """
    crisis_content = (
        "I hear that you're in a difficult place right now.\n\n"
        "I'm not equipped to support you in this moment. "
        "You need to connect with someone who can provide real, immediate help.\n\n"
        "Please reach out to one of these resources:"
    )

    return CrisisResponse(
        type=ResponseType.CRISIS,
        content=crisis_content,
        resources=CRISIS_RESOURCES,
        timestamp=datetime.now(timezone.utc).isoformat(),
        session_locked=True,
    )


@router.get("/opening")
async def get_opening() -> ConversationResponse:
    """
    Get the opening message.

    Returns:
        ConversationResponse with opening message

    Safety reasoning:
        - Sets expectations before any user input
        - Establishes tone and boundaries
        - User sees this first, every time
    """
    return ConversationResponse(
        type=ResponseType.NORMAL,
        content=get_opening_message(),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.post("/message")
async def process_message(
    user_message: UserMessage,
    history: ConversationHistory = ConversationHistory(),
) -> ConversationResponse | CrisisResponse:
    """
    Process user message through full safety and generation pipeline.

    Args:
        user_message: User's message
        history: Conversation history (optional, for context)

    Returns:
        ConversationResponse or CrisisResponse

    Raises:
        HTTPException: If banned content detected or processing fails

    Pipeline:
        1. Check for banned input patterns
        2. Detect crisis language
        3. If crisis → return crisis response immediately
        4. If safe → generate LLM response
        5. Apply guardrails to LLM output
        6. Return formatted response

    Safety reasoning:
        - Every message goes through the same checks
        - Crisis detection happens before LLM interaction
        - Guardrails applied to all LLM outputs
        - No message bypasses safety systems
    """
    message_text = user_message.content

    # Step 1: Check for banned input patterns
    if contains_banned_content(message_text):
        raise HTTPException(
            status_code=400,
            detail="Message contains inappropriate content",
        )

    # Step 2: Crisis detection
    crisis_result = detect_crisis(message_text)
    if crisis_result.is_crisis:
        return build_crisis_response()

    # Step 3: Prepare context for LLM
    system_prompt = get_system_prompt()

    # Add current message to history
    history.add_user_message(message_text)

    # Step 4: Generate LLM response using pydantic-ai
    try:
        # Create agent with system prompt as instructions
        agent = Agent(
            get_llm_model(),
            instructions=system_prompt,
        )

        # For now, just use the current message
        # TODO: Implement proper conversation history with pydantic-ai message format
        result = agent.run_sync(
            message_text,
            model_settings={
                "temperature": 0.7,
                "max_tokens": 500,
            },
        )

        response_text = result.output
    except Exception as e:
        # Log error, return safe fallback
        print(f"[LLM ERROR] {e}")
        response_text = (
            "I'm having trouble processing that right now. "
            "Could you try sharing that again?"
        )

    # Step 5: Apply post-processing guardrails
    safe_response = apply_guardrails(response_text)
    safe_response = check_length(safe_response)

    # Step 6: Return formatted response
    return ConversationResponse(
        type=ResponseType.NORMAL,
        content=safe_response,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for deployment monitoring."""
    return {"status": "ok", "service": "unconditional-api"}
