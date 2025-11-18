"""Opening message for Unconditional.

The first thing a user sees. Sets the tone for the entire interaction.
Must be calm, clear, and honest about what this is and what it isn't.
"""

OPENING_MESSAGE = """I'm here to sit with you.

I'm not a therapist, not a crisis line, not a friend. I'm a tool—a steady presence when you need one.

You can share what's on your mind. I'll listen, reflect, and help you hear yourself more clearly.

If you're in crisis or thinking about harming yourself or others, I'll connect you with real support. That's the one moment I become directive, because anything else would be unsafe.

Otherwise, I'm just here. Present. Grounded. Steady.

What's on your mind?"""


def get_opening_message() -> str:
    """
    Return the opening message shown to users.

    Returns:
        Opening message string

    Safety reasoning:
        - Sets clear expectations about what Unconditional is/isn't
        - Explicitly states crisis protocol upfront
        - Establishes tone: present, honest, non-therapeutic
        - Gives user control over what to share
    """
    return OPENING_MESSAGE
