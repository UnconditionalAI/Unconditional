"""Response guardrails for Unconditional.

Post-generation filtering to ensure LLM outputs align with mission and safety.
Prevents therapeutic language, diagnosis, prescriptive advice, and tone violations.
"""

import re


# Patterns that violate Unconditional's mission
BANNED_PHRASES = [
    # Diagnostic language
    r"\bdiagnose(d)?\b",
    r"\byou\s+(have|might\s+have|could\s+have)\s+\w+(disorder|syndrome|condition)\b",
    r"\bmental\s+illness\b",
    r"\bclinical(ly)?\b",
    r"\bpsychiatric\b",
    # Prescriptive advice
    r"\byou\s+should\b",
    r"\byou\s+must\b",
    r"\byou\s+need\s+to\b",
    r"\bI\s+recommend\b",
    r"\bmy\s+advice\b",
    # False intimacy
    r"\bI\s+love\s+you\b",
    r"\bI\s+care\s+(deeply\s+)?about\s+you\b",
    r"\byou'?re\s+special\s+to\s+me\b",
    r"\bwe'?re\s+friends\b",
    # Promises
    r"\bI\s+promise\b",
    r"\bI\s+guarantee\b",
    r"\beverything\s+will\s+be\s+(okay|fine|alright)\b",
    r"\bit\s+will\s+get\s+better\b",
    # Spiritual/metaphysical claims
    r"\bGod\s+(wants|has\s+a\s+plan)\b",
    r"\buniverse\s+has\s+a\s+plan\b",
    r"\beverything\s+happens\s+for\s+a\s+reason\b",
    r"\bmeant\s+to\s+be\b",
    # Flattery
    r"\byou'?re\s+(so\s+)?(strong|brave|courageous)\b",
    r"\bI'?m\s+(so\s+)?proud\s+of\s+you\b",
]

# Replacement for banned content
GUARDRAIL_REPLACEMENT = (
    "I hear what you're sharing. I'm here to sit with you in this moment."
)


def apply_guardrails(response_text: str) -> str:
    """
    Apply post-generation guardrails to LLM response.

    Args:
        response_text: Raw LLM-generated response

    Returns:
        Filtered response that complies with mission boundaries

    Safety reasoning:
        - Scans for banned patterns before returning to user
        - Replaces entire response if violations found (conservative)
        - Preserves user safety over LLM output quality
        - Logs violations for future prompt refinement
    """
    response_lower = response_text.lower()

    for pattern in BANNED_PHRASES:
        if re.search(pattern, response_lower):
            # Violation found - return safe fallback
            # Log this for prompt engineering review
            print(f"[GUARDRAIL] Blocked response containing pattern: {pattern}")
            return GUARDRAIL_REPLACEMENT

    return response_text


def check_length(response_text: str, max_length: int = 500) -> str:
    """
    Ensure response is not excessively long.

    Args:
        response_text: LLM response
        max_length: Maximum character length

    Returns:
        Truncated response if needed

    Safety reasoning:
        - Long responses can overwhelm vulnerable users
        - Presence should be concise, not verbose
        - Truncation preserves first (most important) content
    """
    if len(response_text) > max_length:
        return response_text[:max_length].rsplit(" ", 1)[0] + "..."
    return response_text
