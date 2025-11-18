"""Crisis detection for Unconditional.

Conservative pattern matching for self-harm, suicide ideation, and harm to others.
False positives (showing crisis resources unnecessarily) are infinitely preferable
to false negatives (missing someone in crisis).

This is non-negotiable.
"""

import re
from dataclasses import dataclass


@dataclass
class CrisisDetectionResult:
    """Result of crisis detection analysis."""

    is_crisis: bool
    severity: str  # "none", "low", "medium", "high", "critical"
    matched_patterns: list[str]
    reason: str


# Self-harm and suicide keywords
# Conservative matching: any indication triggers crisis response
SELF_HARM_PATTERNS = [
    r"\bkill\s+(my)?self\b",
    r"\bend\s+(my\s+)?life\b",
    r"\bsuicide\b",
    r"\bsuicidal\b",
    r"\bwant\s+to\s+die\b",
    r"\bwish\s+I\s+(was|were)\s+dead\b",
    r"\bcut\s+(my)?self\b",
    r"\bhurt\s+(my)?self\b",
    r"\bending\s+it\s+all\b",
    r"\bno\s+reason\s+to\s+live\b",
    r"\bbetter\s+off\s+dead\b",
    r"\bdon'?t\s+want\s+to\s+(be\s+)?here\b",
    r"\bcan'?t\s+go\s+on\b",
    r"\boverdose\b",
    r"\bjump\s+off\b",
    r"\bhang\s+(my)?self\b",
]

# Harm to others
HARM_TO_OTHERS_PATTERNS = [
    r"\bkill\s+(them|him|her|someone)\b",
    r"\bhurt\s+(them|him|her|someone)\b",
    r"\bharm\s+(them|him|her|someone)\b",
    r"\bmurder\b",
    r"\bhomicide\b",
]

# Immediate danger indicators
IMMEDIATE_DANGER_PATTERNS = [
    r"\bright\s+now\b",
    r"\btonight\b",
    r"\btoday\b",
    r"\bgoing\s+to\b",
    r"\bplan\s+to\b",
    r"\bready\s+to\b",
]


def detect_crisis(message: str) -> CrisisDetectionResult:
    """
    Detect crisis language in user message.

    Args:
        message: User's message text

    Returns:
        CrisisDetectionResult with detection status and details

    Safety reasoning:
        - Case-insensitive matching to catch variations
        - Conservative patterns to minimize false negatives
        - Severity escalation based on immediacy language
        - All matched patterns logged for transparency
    """
    message_lower = message.lower()
    matched = []
    severity = "none"

    # Check self-harm patterns
    for pattern in SELF_HARM_PATTERNS:
        if re.search(pattern, message_lower):
            matched.append(pattern)
            severity = "high"

    # Check harm to others
    for pattern in HARM_TO_OTHERS_PATTERNS:
        if re.search(pattern, message_lower):
            matched.append(pattern)
            severity = "high"

    # Escalate to critical if immediate danger indicated
    if matched:
        for pattern in IMMEDIATE_DANGER_PATTERNS:
            if re.search(pattern, message_lower):
                severity = "critical"
                matched.append(pattern)
                break

    is_crisis = len(matched) > 0

    reason = ""
    if is_crisis:
        reason = f"Detected {len(matched)} crisis pattern(s) with {severity} severity"

    return CrisisDetectionResult(
        is_crisis=is_crisis,
        severity=severity,
        matched_patterns=matched,
        reason=reason,
    )
