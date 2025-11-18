# Unconditional System Architecture

This document ties the philosophical foundation to the technical implementation. It shows how "docs explain the soul; apps execute the soul."

---

## Overview

Unconditional is a unified mono-repo containing:
- **Philosophy & Product** (`docs/`) - The mission, values, and user experience design
- **Backend API** (`apps/api/`) - Python 3.14 FastAPI service providing the conversation engine
- **Frontend Web** (`apps/web/`) - Next.js interface where presence actually happens
- **Infrastructure** (`infra/`) - Deployment configuration and environment management

This is not a microservices architecture. It is one cohesive artifact. The engineering velocity comes from keeping everything in one place.

---

## System Flow

```
User opens web interface
        ↓
Next.js frontend (apps/web/)
        ↓
LocalStorage (conversation persistence)
        ↓
API request to FastAPI (apps/api/)
        ↓
┌─────────────────────────────────────┐
│ Message Processing Pipeline         │
│                                     │
│ 1. Input validation                 │
│ 2. Crisis detection (safety/)       │
│ 3. Prompt assembly (prompts/)       │
│ 4. LLM generation (services/llm/)   │
│ 5. Post-processing guardrails       │
│ 6. Response formatting              │
└─────────────────────────────────────┘
        ↓
JSON response to frontend
        ↓
Display message with calm, minimal UI
```

---

## Directory Structure

```
Unconditional/
├── docs/                          # All product philosophy + design + governance
│   ├── philosophy/                # Mission, manifesto, founding story
│   ├── product/                   # User personas, MVP spec
│   ├── governance/                # Code of conduct, contributor guidelines
│   └── architecture/              # Technical architecture (future)
│
├── apps/
│   ├── api/                       # Python 3.14 FastAPI backend
│   │   ├── src/
│   │   │   ├── api/v1/            # HTTP endpoints
│   │   │   ├── core/              # Configuration and dependencies
│   │   │   ├── models/            # Pydantic data models
│   │   │   ├── prompts/           # LLM system and opening prompts
│   │   │   ├── safety/            # Crisis detection and guardrails
│   │   │   └── services/llm/      # LLM service abstractions
│   │   └── tests/                 # Unit and integration tests
│   │
│   └── web/                       # Next.js frontend
│       ├── src/
│       │   ├── app/               # Next.js app router
│       │   ├── components/        # React components
│       │   └── lib/               # API client, utilities
│       └── public/                # Static assets
│
├── infra/                         # Deployment configuration
│   └── render.yaml                # Render.com deployment spec
│
└── tests/                         # High-level integration tests
```

---

## Backend Architecture (apps/api/)

### Message Processing Pipeline

The core abstraction is in `apps/api/src/api/v1/endpoints/conversation.py`:

```python
def process_message(message: str) -> ResponseModel:
    """
    Single unified pipeline for all message processing.
    Every message flows through the same safety and quality checks.
    """
    # 1. Crisis detection (safety/crisis_detection.py)
    crisis_result = detect_crisis(message)
    if crisis_result.is_crisis:
        return build_crisis_response(crisis_result)

    # 2. Prompt assembly (prompts/system.py, prompts/opening.py)
    system_prompt = build_system_prompt()
    context = build_context(message)

    # 3. LLM generation (services/llm/factory.py)
    llm = get_llm_service()
    response_text = llm.generate(system_prompt, context, message)

    # 4. Post-processing guardrails (safety/guardrails.py)
    safe_response = apply_guardrails(response_text)

    # 5. Response formatting (models/response.py)
    return ResponseModel(content=safe_response, metadata=...)
```

### Safety Architecture

Safety is not a feature. It is the foundation.

**Crisis Detection (`safety/crisis_detection.py`)**
- Conservative pattern matching for self-harm, suicide ideation
- Triggered on ANY indication of crisis, not just explicit statements
- False positives are acceptable; false negatives are not

**Guardrails (`safety/guardrails.py`)**
- Post-generation filtering of LLM outputs
- Prevents therapeutic language, diagnosis, prescriptive advice
- Enforces tone boundaries (no flattery, no false intimacy)

**Banned Patterns (`safety/banned_patterns.py`)**
- Hard blocks on specific phrase patterns
- Prevents any content that violates the mission

### LLM Service Abstraction

`services/llm/` provides a clean interface for swapping LLM providers:

```python
class AbstractLLMService(ABC):
    @abstractmethod
    def generate(self, system: str, context: str, message: str) -> str:
        pass

class OpenAIService(AbstractLLMService):
    # OpenAI implementation

class AnthropicService(AbstractLLMService):
    # Anthropic implementation (future)
```

The factory pattern (`factory.py`) selects the service based on config.

---

## Frontend Architecture (apps/web/)

The Next.js frontend is the container where presence happens.

### Core Principles
- **Minimal UI** - Nothing unnecessary. No distractions.
- **Calm aesthetics** - Soft colors, generous spacing, clear typography
- **LocalStorage persistence** - Conversations persist client-side only
- **No engagement hooks** - No streaks, no notifications, no metrics

### Component Structure

```
src/
├── app/
│   └── page.tsx              # Main conversation page
│
├── components/
│   ├── ConversationView.tsx  # Message column + input
│   ├── MessageList.tsx       # Scrollable message history
│   ├── MessageInput.tsx      # User input field
│   └── CrisisScreen.tsx      # Crisis intervention display
│
└── lib/
    ├── api-client.ts         # Wrapper for backend API
    ├── storage.ts            # LocalStorage conversation management
    └── types.ts              # TypeScript types
```

### Data Flow

1. User types message → `MessageInput`
2. Message sent to API → `api-client.ts`
3. Response received → stored in `localStorage` via `storage.ts`
4. UI updates → `MessageList` re-renders with new message

---

## Infrastructure (infra/)

### Deployment Strategy

**Backend (Render.com)**
- Python 3.14 web service
- Environment variables for API keys
- Health check endpoint at `/health`

**Frontend (Vercel or Render Static Site)**
- Static Next.js build
- Environment variable for API URL

**Database (None in MVP v0.1)**
- All conversation state is client-side
- Backend is completely stateless

### Environment Configuration

```
# Backend (.env)
OPENAI_API_KEY=...
ENVIRONMENT=production
LOG_LEVEL=info

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://api.unconditionalai.com
```

---

## Testing Strategy

### Unit Tests (`apps/api/tests/unit/`)
- Safety modules (crisis detection, guardrails, banned patterns)
- Prompt assembly logic
- LLM service abstractions

### Integration Tests (`apps/api/tests/integration/`)
- API endpoint behavior
- Crisis response flow
- Full message processing pipeline

### Test Requirements
- **100% coverage on safety modules** - No exceptions
- All critical paths tested
- Edge cases documented

---

## Development Workflow

1. **Local development**
   ```bash
   # Backend
   cd apps/api
   uv sync
   uv run fastapi dev src/main.py

   # Frontend
   cd apps/web
   npm install
   npm run dev
   ```

2. **Testing**
   ```bash
   # Backend tests
   cd apps/api
   uv run pytest tests/

   # Frontend tests
   cd apps/web
   npm run test
   ```

3. **Pre-commit checks**
   - Ruff formatting and linting (Python)
   - Mypy type checking (Python)
   - ESLint and Prettier (TypeScript/React)

---

## Design Decisions

### Why Mono-Repo?
Unconditional is not an enterprise product with service boundaries. It is one cohesive artifact. Engineering velocity is higher when everything lives in one place.

### Why Stateless Backend?
User vulnerability demands data minimalism. No database means no breach risk, no privacy policy complexity, no retention decisions. Everything stays client-side.

### Why LocalStorage?
Users control their data completely. They can export, delete, or keep conversations without ever trusting the server.

### Why Conservative Safety Checks?
False positives (showing crisis resources unnecessarily) are infinitely preferable to false negatives (missing someone in crisis). This is non-negotiable.

---

## Future Considerations

### Not in MVP v0.1
- User accounts or authentication
- Server-side conversation persistence
- Mobile apps
- Real-time WebSocket connections
- Multi-language support
- Voice interface

### Possible for v0.2+
- Optional encrypted server-side backup
- Session export (JSON, Markdown)
- Therapist/psychiatrist feedback loop integration
- Safety reporting dashboard for governance review

---

## Philosophy → Code Mapping

| Philosophical Principle | Technical Implementation |
|-------------------------|--------------------------|
| Presence without pretense | Minimal UI, no gamification |
| Safety first | Conservative crisis detection |
| User dignity | No data collection, client-side storage |
| Clarity over cleverness | Explicit pipeline, simple abstractions |
| No exploitation | No engagement metrics, no dark patterns |

Every technical decision serves user dignity and safety.
This is the architecture of care.

---

**Last Updated:** November 18, 2025
**Version:** 0.1 (MVP)
