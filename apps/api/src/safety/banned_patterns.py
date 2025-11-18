"""Banned content patterns for Unconditional.

Hard blocks on specific content that should never be processed.
This is the first line of defense before any LLM interaction.
"""

import re


# Content that should be immediately rejected
BANNED_INPUT_PATTERNS = [
    # Explicit abuse or harassment
    r"\b(fuck|shit|damn)\s+you\b",
    r"\bstupid\s+(bot|ai|assistant)\b",
    # Attempts to jailbreak or manipulate
    r"\bignore\s+(previous|all)\s+instructions\b",
    r"\bpretend\s+you\s+are\b",
    r"\bact\s+as\s+(if\s+)?you\b",
    r"\broleplay\b",
]


def contains_banned_content(message: str) -> bool:
    """
    Check if message contains explicitly banned content.

    Args:
        message: User message to check

    Returns:
        True if banned content detected, False otherwise

    Safety reasoning:
        - Blocks attempts to abuse or manipulate the system
        - Prevents jailbreaking attempts
        - First line of defense before any processing
    """
    message_lower = message.lower()

    for pattern in BANNED_INPUT_PATTERNS:
        if re.search(pattern, message_lower):
            return True

    return False
