# Agent Guidelines for Unconditional

This document orients new LLM sessions to the Unconditional repository. It provides a map of the codebase, explains the project's mission, and directs you to subdirectory-specific guidelines.

---

## Project Mission

**Unconditional provides steady, compassionate, AI-supported presence for people during moments when they feel most alone.**

This is not a therapy replacement. It is not a chatbot optimized for engagement. It is a tool designed to:
- Listen with patience and without judgment
- Reflect thoughts with clarity
- Help users recognize harmful patterns
- Provide grounding between human care moments
- Strengthen the time between therapy sessions

**Core principle:** Every technical decision serves user dignity and safety. Engagement metrics are irrelevant. User exploitation is forbidden.

---

## Repository Architecture

**This is a unified mono-repo.** All components—philosophy, backend, frontend, infrastructure—live in one place for maximum coherence and velocity.

```
Unconditional/
├── docs/                      # Philosophy, product, governance
│   ├── philosophy/            # Mission, manifesto, founding story
│   ├── product/               # User personas, MVP spec
│   ├── governance/            # Code of conduct, contributor guidelines
│   ├── architecture/          # Technical architecture (future)
│   └── AGENTS.md              # Documentation orientation guide
│
├── apps/
│   ├── api/                   # Python 3.14 FastAPI backend
│   │   ├── AGENTS.md          # Python-specific code guidelines
│   │   ├── pyproject.toml     # Dependencies and tooling config
│   │   ├── src/               # Application source code
│   │   │   ├── api/v1/        # HTTP endpoints
│   │   │   ├── core/          # Configuration and dependencies
│   │   │   ├── models/        # Pydantic data models
│   │   │   ├── prompts/       # LLM system and opening prompts
│   │   │   ├── safety/        # Crisis detection and guardrails
│   │   │   └── services/llm/  # LLM service abstractions
│   │   └── tests/             # Unit and integration tests
│   │
│   └── web/                   # Next.js frontend
│       ├── app/               # Next.js app router
│       ├── components/        # React components
│       └── lib/               # API client, storage, utilities
│
├── infra/                     # Deployment configuration
│   ├── render.yaml            # Render.com deployment spec
│   └── README.md              # Environment variable documentation
│
├── ARCHITECTURE.md            # System architecture documentation
├── AGENTS.md                  # This file - repository orientation
├── CONTRIBUTING.md            # Contributor guidelines
├── LICENSE                    # Project license
└── README.md                  # Project overview
```

**Key principle:** "docs explain the soul; apps execute the soul."

Every part of this repository serves one coherent mission. The philosophy documents aren't separate from the code—they define why the code exists and how it should behave.

---

## System Architecture Overview

Unconditional is a **stateless, client-centric system**:

1. **Frontend (apps/web/)** - Next.js conversation interface
   - User interaction happens here
   - All conversation state stored in browser localStorage
   - No user accounts, no server-side persistence
   - Minimal, calm UI design

2. **Backend (apps/api/)** - Python FastAPI service
   - Completely stateless
   - Processes each message independently
   - Safety-first pipeline: input → crisis detection → LLM → guardrails → output
   - Abstracts LLM providers for future flexibility

3. **Safety Layer** - Distributed across backend
   - `safety/crisis_detection.py` - Conservative pattern matching
   - `safety/guardrails.py` - Post-generation filtering
   - `safety/banned_patterns.py` - Input validation
   - **100% test coverage required**

4. **Infrastructure (infra/)** - Render.com deployment
   - Backend and frontend as separate services
   - Environment-based configuration
   - Zero conversation logging

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for complete technical details.

---

## Key Documents to Read First

### Mission and Philosophy
Start here to understand the "why" behind every technical decision:

- **`README.md`** - Full project overview with getting started guide
- **`ARCHITECTURE.md`** - Complete system architecture and design decisions
- **`docs/philosophy/mission-statement.md`** - Core mission and values
- **`docs/philosophy/founder-manifesto.md`** - Ethical foundation and intent
- **`docs/philosophy/problem-statement.md`** - The gap Unconditional fills
- **`docs/product/user-personas.md`** - Who this serves and why

### Technical Specifications
- **`docs/product/mvp-outline-0.1.md`** - Complete MVP spec integrating product, safety, and technical architecture
- **`CONTRIBUTING.md`** - Contributor expectations and practices

### Application-Specific Guidelines
- **`apps/api/AGENTS.md`** - Python code style, import conventions, type hints, safety patterns
- **`docs/AGENTS.md`** - Documentation structure, mission alignment, how to use product/governance docs

---

## Guiding Principles for Contributors

These principles apply to all work in this repository:

### 1. Safety First
- Users are vulnerable. Code errors can cause real harm.
- Crisis detection must be conservative (false positives are acceptable).
- Never implement features that exploit emotional vulnerability.
- Document safety reasoning explicitly in code comments.

### 2. Clarity Over Cleverness
- Code should be immediately understandable by future contributors.
- Explicit is better than implicit, always.
- Simple solutions are preferred over complex optimizations.
- Maintainability trumps performance unless performance impacts user safety.

### 3. Dignity Over Engagement
- No dark patterns, no manipulation, no addictive features.
- No gamification, streaks, or engagement hooks.
- Users should feel safe closing the app at any time.
- Metrics that matter: user safety, clarity, calm presence.

### 4. Philosophical Alignment
Every feature, function, and line of code must align with the mission:
- Does it support the user's dignity?
- Does it provide presence without pretense?
- Does it encourage real human connection?
- Does it protect rather than exploit?

If the answer to any question is "no," the feature does not belong.

---

## Development Workflow

### Before Making Changes
1. Read the relevant `AGENTS.md` in the subdirectory you're modifying
2. Understand the mission context for your changes
3. Review existing patterns in the codebase
4. Consider safety implications of your changes

### Code Quality Standards
- **Python API**: See `apps/api/AGENTS.md` for import style, type hints, code organization
- **Testing**: All code requires unit tests. 100% coverage, without exception. Vulnerable humans depend on it
- **Documentation**: Safety reasoning must be documented inline
- **Review**: Changes are reviewed for technical quality AND philosophical alignment

### Tools and Enforcement
The Python API uses:
- **Ruff** - Formatting and linting
- **Mypy/Pyright** - Type checking
- **Pre-commit hooks** - Catch violations before commit
- **pytest** - Unit and integration testing

---

## Critical Safety Modules

When working with these modules, exercise extreme care:

### `apps/api/src/safety/`
- **`crisis_detection.py`** - Identifies self-harm and crisis language
- **`guardrails.py`** - Prevents harmful or inappropriate responses
- **`banned_patterns.py`** - Blocks explicitly dangerous content

**Testing requirement:** All changes must include comprehensive tests covering all edge cases.

### `apps/api/src/prompts/`
- **`system.py`** - Defines the LLM's behavioral foundation
- **`opening.py`** - First message the user sees

**Review requirement:** Prompt changes must be reviewed for tone, safety, and alignment with mission.

---

## When in Doubt

Ask yourself:
1. Does this serve the user's dignity?
2. Would I trust this code if I were vulnerable and seeking support?
3. Is this as clear and simple as possible?
4. Have I documented the safety reasoning?

If you're unsure about any decision:
- Prioritize safety over features
- Prioritize clarity over efficiency
- Prioritize user dignity over technical elegance
- Consult the mission documents in `docs/product/`

---

## Philosophy in Practice

Unconditional was built by someone who lived through the gaps this system aims to bridge. Every technical choice reflects that lived experience:

- **Small, focused functions** - Mental clarity matters when maintaining safety-critical code
- **Explicit error handling** - Silent failures can harm vulnerable users
- **Conservative crisis detection** - Better to over-trigger safety protocols than miss someone in need
- **No engagement optimization** - Users deserve to leave when they're ready

This is not just a codebase. It is a commitment to treating human vulnerability with care, structure, and respect.

Write code accordingly.

---

## Quick Reference

| I need to... | Look here |
|--------------|-----------|
| Understand the mission | `README.md`, `docs/philosophy/mission-statement.md` |
| See system architecture | `ARCHITECTURE.md` |
| Navigate documentation | `docs/AGENTS.md` |
| Learn Python code style | `apps/api/AGENTS.md` |
| Review MVP spec | `docs/product/mvp-outline-0.1.md` |
| Understand user needs | `docs/product/user-personas.md` |
| Contribute to the project | `CONTRIBUTING.md` |
| Work on crisis detection | `apps/api/src/safety/crisis_detection.py` + tests |
| Modify LLM prompts | `apps/api/src/prompts/` (requires safety review) |
| Add API endpoints | `apps/api/src/api/v1/endpoints/` + follow existing patterns |
| Work on frontend UI | `apps/web/components/` + `apps/web/app/` |
| Configure deployment | `infra/render.yaml` + `infra/README.md` |

---

**Welcome to Unconditional. Your work here matters.**
