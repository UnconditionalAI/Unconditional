# Agent Guidelines for Unconditional API

This document defines code style and architectural standards for AI agents and human contributors working on the Unconditional API backend. These guidelines ensure consistency, safety, and maintainability across the codebase.

---

## Import Style

### One Symbol Per Line
Every imported symbol must appear on its own line. No exceptions.

**Correct:**
```python
from typing import Annotated
from typing import Any
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
```

**Incorrect:**
```python
from typing import Annotated, Any
from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
```

### Absolute Imports Only
All imports must use absolute paths from the project root. Relative imports are forbidden.

**Correct:**
```python
from src.safety.crisis_detection import detect_crisis
from src.models.message import Message
from src.services.llm.factory import create_llm_service
```

**Incorrect:**
```python
from ..safety.crisis_detection import detect_crisis
from .message import Message
from ...services.llm.factory import create_llm_service
```

### Import Grouping and Sorting
Imports must be sorted alphabetically within three distinct groups:

1. **Built-in modules** (Python standard library)
2. **Third-party packages** (installed dependencies)
3. **Local modules** (project code)

Separate each group with a single blank line.

**Example:**
```python
import json
import logging
from pathlib import Path
from typing import Any

import fastapi
from pydantic import BaseModel
from pydantic import Field
from pydantic_ai import Agent

from src.core.config import settings
from src.models.message import Message
from src.safety.guardrails import apply_guardrails
```

---

## Type Hints

### Modern Type Syntax Only
Use Python 3.10+ type syntax. Legacy typing module aliases are forbidden.

**Correct:**
```python
def process_messages(messages: list[str]) -> dict[str, Any]:
    cache: dict[str, int] = {}
    results: set[str] = set()
    return {"count": len(messages)}
```

**Incorrect:**
```python
from typing import Dict, List, Set

def process_messages(messages: List[str]) -> Dict[str, Any]:
    cache: Dict[str, int] = {}
    results: Set[str] = set()
    return {"count": len(messages)}
```

### Modern Union Syntax
Use the pipe operator (`|`) for unions. Do not use `Optional` or `Union`.

**Correct:**
```python
def get_user(user_id: str) -> User | None:
    pass

def process(value: int | str | float) -> bool:
    pass
```

**Incorrect:**
```python
from typing import Optional, Union

def get_user(user_id: str) -> Optional[User]:
    pass

def process(value: Union[int, str, float]) -> bool:
    pass
```

### Explicit Return Types
All functions must declare explicit return types, even for `None`.

**Correct:**
```python
def send_notification(message: str) -> None:
    print(message)

def calculate_score(values: list[int]) -> float:
    return sum(values) / len(values)
```

**Incorrect:**
```python
def send_notification(message: str):
    print(message)

def calculate_score(values: list[int]):
    return sum(values) / len(values)
```

---

## Code Organization

### Small, Focused Functions
Functions should do one thing well. Extract complex logic into named helper functions.

**Preferred:**
```python
def validate_message_content(content: str) -> bool:
    return len(content) > 0 and len(content) <= 5000

def sanitize_message_content(content: str) -> str:
    return content.strip()

def process_user_message(content: str) -> Message:
    if not validate_message_content(content):
        raise ValueError("Invalid message content")
    sanitized = sanitize_message_content(content)
    return Message(content=sanitized)
```

### Explicit Over Clever
Prioritize clarity over brevity. Code should be immediately understandable.

**Correct:**
```python
def is_crisis_message(text: str) -> bool:
    crisis_keywords = ["suicide", "kill myself", "end it all"]
    normalized_text = text.lower()
    return any(keyword in normalized_text for keyword in crisis_keywords)
```

**Avoid:**
```python
def is_crisis(t: str) -> bool:
    return any(k in t.lower() for k in ["suicide", "kill myself", "end it all"])
```

### Meaningful Names
Use descriptive names that communicate intent. Avoid abbreviations except for universally understood conventions.

**Correct:**
```python
user_message_content: str
crisis_detection_result: bool
llm_response_text: str
```

**Incorrect:**
```python
msg: str
res: bool
txt: str
```

---

## Safety and Documentation

### Document Safety Reasoning
When implementing safety-critical logic, include comments explaining the reasoning.

```python
def check_for_self_harm_intent(message: str) -> bool:
    """
    Detects potential self-harm intent in user messages.

    This check is intentionally conservative. False positives are acceptable
    because they route users to crisis resources. False negatives are dangerous
    because they leave vulnerable users without intervention.
    """
    keywords = load_self_harm_keywords()
    return any(keyword in message.lower() for keyword in keywords)
```

### Explicit Error Handling
Handle errors explicitly. Don't let exceptions propagate silently.

```python
def load_system_prompt() -> str:
    try:
        with open("prompts/system.txt") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("System prompt file not found")
        raise RuntimeError("Critical configuration missing")
```

---

## Pydantic Models

### Field Descriptions
All Pydantic fields should include descriptions.

```python
class Message(BaseModel):
    content: str = Field(description="The text content of the user's message")
    timestamp: float = Field(description="Unix timestamp when message was created")
    session_id: str | None = Field(default=None, description="Optional session identifier")
```

### Validation Logic
Use Pydantic validators for data validation, not manual checks in business logic.

```python
from pydantic import field_validator

class ConversationRequest(BaseModel):
    message: str = Field(description="User message content")

    @field_validator("message")
    @classmethod
    def validate_message_length(cls, value: str) -> str:
        if len(value) == 0:
            raise ValueError("Message cannot be empty")
        if len(value) > 5000:
            raise ValueError("Message exceeds maximum length")
        return value
```

---

## Testing

### Test Files Mirror Source Structure
Test files should mirror the `src/` structure and use the `test_` prefix.

```
src/
  safety/
    crisis_detection.py
tests/
  unit/
    safety/
      test_crisis_detection.py
```

### Descriptive Test Names
Test function names should describe the behavior being tested.

```python
def test_crisis_detection_identifies_self_harm_keywords() -> None:
    assert detect_crisis("I want to end my life") is True

def test_crisis_detection_allows_safe_messages() -> None:
    assert detect_crisis("I'm having a difficult day") is False
```

---

## Philosophical Alignment

These technical guidelines serve Unconditional's mission:

- **Clarity protects safety.** Explicit code prevents mistakes with vulnerable users.
- **Simplicity enables maintenance.** Future contributors must understand safety logic immediately.
- **Consistency builds trust.** Predictable patterns reduce cognitive load during reviews.
- **Documentation preserves intent.** Safety reasoning must survive beyond the original author.

Every line of code in this project exists to support people during difficult moments. Write accordingly.

---

## Additional Style Guidelines

### Use Modern Python Features
Take advantage of Python 3.14 features where appropriate:
- `match` statements for complex conditionals
- Structural pattern matching for data validation
- `TypedDict` for dictionary schemas when not using Pydantic

### Avoid Magic
- No dynamic attribute access unless necessary
- No metaprogramming without explicit justification
- No monkey patching

### Logging Over Print
Use structured logging, not print statements.

```python
import logging

logger = logging.getLogger(__name__)

def process_request(message: str) -> None:
    logger.info("Processing user message", extra={"message_length": len(message)})
```

### Immutability Preference
Prefer immutable data structures when possible.

```python
from typing import Final

CRISIS_KEYWORDS: Final[frozenset[str]] = frozenset([
    "suicide",
    "kill myself",
    "end it all",
])
```

---

## Enforcement

These guidelines are enforced through:
- **Ruff** for formatting and linting
- **ty** for type checking
- **Pre-commit hooks** to catch violations before commit
- **Code review** to ensure philosophical alignment

When in doubt, prioritize safety, clarity, and user dignity over technical elegance.
