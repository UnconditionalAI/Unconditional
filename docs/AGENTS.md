# Agent Guidelines for Unconditional Documentation

This document orients LLM sessions working with the Unconditional documentation. The docs directory contains the philosophical foundation, mission alignment, governance structure, and technical specifications that guide all work on this project.

---

## Purpose of This Directory

The `docs/` directory is not just supplementary material. It is the **source of truth** for:
- Why Unconditional exists
- Who it serves
- What it will and will not do
- How contributors should approach their work
- What technical decisions must honor

Every code change, design choice, and feature proposal must trace back to these documents. If something conflicts with the mission, vision, or safety principles documented here, it does not belong in the project.

---

## Directory Structure

```
docs/
├── governance/          # How we work together and what we expect
│   ├── code-of-conduct.md
│   ├── contributor-guidelines.md
│   ├── ideal-founding-engineer.md
│   ├── ideal-founding-psychiatrist.md
│   ├── ideal-founding-team.md
│   └── ideal-founding-therapist.md
│
├── product/            # The mission, vision, and user understanding
│   ├── founder-manifesto.md
│   ├── founding-story.md
│   ├── mission-statement.md
│   ├── one-sentence-description.md
│   ├── problem-statement.md
│   ├── user-personas.md
│   └── why-now.md
│
└── specs/              # Technical specifications and architecture
    └── mvp-outline-0.1.md
```

---

## Reading Order for New Contributors

### Start Here: Mission and Philosophy (Required)
1. **`product/mission-statement.md`** - The core purpose of Unconditional
2. **`product/founder-manifesto.md`** - Ethical foundation and constraints
3. **`product/problem-statement.md`** - The gap this project fills
4. **`governance/contributor-guidelines.md`** - How to contribute responsibly

These four documents establish the "why" and "how" of every technical decision.

### Understanding Users (Required for Feature Work)
5. **`product/user-personas.md`** - Who needs this and what they struggle with
6. **`product/founding-story.md`** - Personal context that shaped the project
7. **`product/why-now.md`** - Why this matters now

### Technical Specifications
8. **`specs/mvp-outline-0.1.md`** - Complete product, safety, and technical architecture

### Governance and Team Culture
9. **`governance/code-of-conduct.md`** - Expected behavior and community standards
10. **`governance/ideal-founding-*.md`** - What kind of expertise and mindset we're looking for

---

## Document Categories Explained

### Product Documents (`product/`)
These define **what Unconditional is and why it exists**:

- **Mission-critical context** - Every feature must align with these documents
- **User understanding** - Who we serve and what they need
- **Philosophical boundaries** - What we will never do, and why
- **Emotional foundation** - The tone, presence, and values we embody

**When to reference:**
- Before proposing new features
- When questioning design decisions
- When writing user-facing content (prompts, UI copy)
- When evaluating whether something "feels right"

### Governance Documents (`governance/`)
These define **how we work together**:

- **Contributor expectations** - Safety, care, transparency, restraint
- **Code of conduct** - How we treat each other
- **Team composition** - What skills and mindsets we need

**When to reference:**
- Before making your first contribution
- When reviewing others' work
- When resolving disagreements
- When recruiting or evaluating team fit

### Technical Specifications (`specs/`)
These define **how the system works**:

- **Architecture** - Backend, frontend, safety systems
- **Behavior** - How the system responds and when it intervenes
- **Constraints** - Technical boundaries that protect users

**When to reference:**
- When implementing features
- When debugging behavior
- When proposing architectural changes
- When writing safety-critical code

---

## Core Principles from Documentation

These principles appear repeatedly across all docs and must guide every contribution:

### 1. Safety as Foundation
From `contributor-guidelines.md`:
> "If a feature could confuse, mislead, or emotionally harm a vulnerable person, it does not belong in the system."

- Crisis detection must be conservative (false positives are acceptable)
- Never pretend the system can do more than it can
- Transparent about limitations
- Always provide real crisis resources when needed

### 2. Dignity Over Engagement
From `mission-statement.md`:
> "Unconditional does not replace human care. It strengthens it."

- No gamification, streaks, or engagement hooks
- No dark patterns or manipulation
- No building emotional dependency
- Users should feel safe to close the app at any time

### 3. Boundaries as Care
From `mvp-outline-0.1.md`:
> "Support without boundaries is manipulation. Boundaries without support are abandonment."

- Not therapy, not diagnosis, not treatment
- No pretending to be human or have feelings
- No prescriptive advice ("You should...")
- Clear about what the system is and isn't

### 4. Clarity and Simplicity
From `contributor-guidelines.md`:
> "The goal is clarity, safety, and stability. Avoid unnecessary complexity."

- Simple over clever
- Explicit over implicit
- Maintainable over performant (unless performance affects safety)
- Clear reasoning in all documentation

---

## How to Use These Documents

### When Writing Code
1. Check if your feature aligns with `mission-statement.md`
2. Verify it doesn't violate boundaries in `mvp-outline-0.1.md`
3. Consider how it serves users in `user-personas.md`
4. Follow safety principles in `contributor-guidelines.md`

### When Writing Prompts or UI Copy
1. Study the tone in `mvp-outline-0.1.md` (Section 2: Emotional Architecture)
2. Review boundaries: what Unconditional never does
3. Test against user personas to ensure it serves their needs
4. Ensure it maintains calm, steady, grounded presence

### When Proposing Features
1. Explain how it serves the mission in `mission-statement.md`
2. Show which user personas benefit (from `user-personas.md`)
3. Demonstrate alignment with `contributor-guidelines.md`
4. Address safety implications explicitly

### When Reviewing Contributions
1. Does it align with the mission?
2. Does it respect user dignity?
3. Does it maintain appropriate boundaries?
4. Is the safety reasoning documented?
5. Would you trust this if you were vulnerable?

---

## Red Flags: What Doesn't Belong

Based on the mission documents, reject anything that:

- **Exploits vulnerability** - Manipulates emotions, builds dependency, uses dark patterns
- **Pretends to be more** - Claims to diagnose, treat, remember, or feel
- **Violates boundaries** - Acts as therapy, gives prescriptive advice, makes promises
- **Optimizes for engagement** - Gamification, streaks, hooks, notifications
- **Harms through negligence** - Missing crisis detection, unclear about limitations
- **Adds complexity without purpose** - Features that don't serve user dignity

If you see these patterns, they must be addressed or rejected, regardless of technical quality.

---

## Documentation Standards

When contributing to or referencing these documents:

### Writing Style
- **Clear and direct** - No jargon unless necessary
- **Human and grounded** - Match the tone of the product
- **Specific over abstract** - Concrete examples when possible
- **Mission-aligned** - Every word should reflect the values

### Document Updates
- **Require review** - Mission docs need careful oversight
- **Explain reasoning** - Why the change serves users
- **Consider ripple effects** - How it affects code, design, prompts
- **Preserve intent** - Don't dilute the philosophical foundation

### Safety Documentation
- **Must be explicit** - No assumptions about "obvious" safety concerns
- **Include reasoning** - Why this boundary exists
- **Link to mission** - How it protects user dignity
- **Update with code** - Keep safety docs in sync with implementation

---

## Integration with Code

The documentation in this directory is not separate from the codebase:

- **Prompts** (`apps/api/src/prompts/`) must reflect `mvp-outline-0.1.md` Section 2 (Emotional Architecture)
- **Safety modules** (`apps/api/src/safety/`) must implement `mvp-outline-0.1.md` Section 3 (Safety Envelope)
- **API behavior** must honor boundaries defined in `contributor-guidelines.md`
- **All features** must trace back to user needs in `user-personas.md`

When code and docs diverge, the docs are the source of truth. Update code to match, or propose a doc change with clear reasoning.

---

## For LLM Agents

When working on this project:

1. **Read mission docs first** - Don't write code until you understand the "why"
2. **Check alignment constantly** - Every technical decision serves user dignity
3. **Question misalignment** - If something feels wrong, consult these docs
4. **Document safety reasoning** - Inline comments must explain protection mechanisms
5. **Preserve philosophical integrity** - Technical elegance never trumps mission alignment

The documentation is not decorative. It is the foundation. Code without mission alignment does not belong here, no matter how well-written.

---

## Quick Reference

| I need to... | Read this document |
|--------------|-------------------|
| Understand the mission | `product/mission-statement.md` |
| Know what features are allowed | `product/founder-manifesto.md`, `specs/mvp-outline-0.1.md` |
| Learn who we serve | `product/user-personas.md` |
| Understand tone and voice | `specs/mvp-outline-0.1.md` (Section 2) |
| Know safety requirements | `specs/mvp-outline-0.1.md` (Section 3) |
| Contribute responsibly | `governance/contributor-guidelines.md` |
| Understand team culture | `governance/code-of-conduct.md` |
| Know why this exists now | `product/why-now.md` |
| See the founder's intent | `product/founder-manifesto.md` |

---

**These documents are not guidelines. They are commitments.**

Every contributor, every line of code, and every design choice must honor them. This is how we keep Unconditional true to the people it serves.
