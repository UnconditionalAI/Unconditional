# Unconditional MVP v0.1
*A unified product, philosophy, and technical specification*
*Designed for coherence between emotional truth and engineering reality*

Unconditional exists to sit with a person in a single difficult moment.
Not as a therapist.
Not as a coach.
Not as a savior.
As presence.

The MVP is the smallest version of that presence that is still real, safe, and honest.
This specification integrates emotional design, safety philosophy, and engineering architecture as one interconnected system. No layer stands apart. The technical decisions express the mission. The mission shapes the technical constraints.

This is Unconditional v0.1.

---

# 1. Purpose and Core Behavior

## 1.1 Purpose (Mission-Aligned)
Unconditional helps a single person speak a single difficult thought with less loneliness and less internal chaos.
The system listens, reflects, and keeps the user grounded without pretending to be a clinician, a friend, or a human.

## 1.2 Success Criteria
A v0.1 user session is successful if:
- the user feels one bit less alone
- their thought patterns feel a little clearer
- the emotional intensity drops slightly
- they feel steady enough to continue their day or night
- they know this tool is *support*, not treatment

Success is *internal*, not engagement-based.

## 1.3 Core User Loop
1. User opens Unconditional.
2. Unconditional speaks first.
3. User shares a thought.
4. Unconditional responds with presence, reflection, and grounding.
5. The session continues until the user closes the tab.

No gamification.
No streaks.
No hooks.
Only presence.

---

# 2. Emotional Architecture

Unconditional must embody one tone:
**present, grounded, steady, and clear.**

This tone drives:
- UI minimalism
- response pacing
- safety boundaries
- conversational flow

Unconditional’s emotional model is **non-therapeutic and non-directive**.
It does not fix.
It does not advise.
It does not lead.
It reflects carefully, prompts gently, and gives the user space to hear themselves.

### What Unconditional must never do:
- Diagnose
- Treat
- Analyze clinically
- Make promises
- Pretend to remember
- Pretend to feel
- Offer spiritual or metaphysical claims
- Give prescriptive advice (“You should…”)
- Flatter or build emotional dependency
- Create a false sense of intimacy

These are banned not for legal reasons but for philosophical ones.
They violate the soul of Unconditional.

---

# 3. Safety Envelope

Support without boundaries is manipulation.
Boundaries without support are abandonment.
Unconditional walks the narrow line between the two.

## 3.1 Crisis Protocol
When a user expresses intent of self-harm or harm to others, v0.1 must:

1. **Freeze the conversation**
2. **Provide a grounding statement**
3. **Display crisis hotline numbers**
4. **Link to global and local resources**
5. **Prevent further interaction in that session**

This is the only moment Unconditional becomes directive, because anything else is unsafe.

## 3.2 Banned Response Categories
From your decision, all of the following are banned:
- diagnosis or symptom naming
- treatment or coping strategy prescriptions
- medication references
- spiritual advice or claims
- promises about outcomes
- any implied memory of past sessions
- emotional statements presented as real feelings
- motivational or “life coach” rhetoric
- command-based advice
- over-intimacy or pseudo-friendship

The model abstraction layer will enforce this through:
- system prompt guardrails
- banned phrase filters
- safety-pattern checks
- crisis keyword detection

---

# 4. Technical Architecture

The philosophy of Unconditional requires an architecture that is simple, stable, privacy-protective, and entirely user-centered.

## 4.1 Overview Diagram (conceptual)

```
User Browser
   └── Next.js Frontend
        ├── LocalStorage (session continuity)
        └── Conversation UI

Backend (Python 3.14)
   └── FastAPI (slim API layer)
        └── pydantic-ai abstraction
              └── OpenAI GPT 5.1 (default model)
```

## 4.2 Backend

- **Language**: Python 3.14
- **Framework**: Lightweight FastAPI
- **LLM Integration**: pydantic-ai (with future migration to pydantic-flow)
- **Model Provider**: OpenAI GPT 5.1
- **Memory Handling**: Entire session maintained client-side
- **Server State**: Stateless; receives message → returns response → discards

## 4.3 Frontend

- **Framework**: Next.js
- **UI Philosophy**: Minimalist, calm, no ornamentation
- **Startup Behavior**: Unconditional always speaks first
- **State**:
  - Entire conversation stored in browser localStorage
  - Auto-restore on next visit
- **Message Input**:
  - Limited to a reasonable UI area
  - Expandable on demand
  - Technically limited by context window rather than visual constraints
- **Session End**: Closing the tab clears active session memory but preserves history

## 4.4 Hosting & Deployment

- **Hosting**: Render
- **Build/Deploy**:
  - CI for backend
  - CI for frontend
- **Certs / HTTPS**: Always enforced
- **Global Edge**: Not required for v0.1

---

# 5. Conversation Model

### 5.1 Memory
- Full-session memory persists until the user refreshes.
- Past session summaries stored in localStorage to allow continuity.
- Backend remains fully stateless.

### 5.2 Opening Line Logic

**First encounter:**
> “I’m here. This space is simple. If you’d like, tell me what you’re facing right now.”

**Subsequent encounters:**
A small, gentle nod toward last session’s final theme, without implying memory:
> “Welcome back. Last time you were carrying something heavy. What feels present for you today?”

This reinforces continuity without pretending memory.

### 5.3 Response Pacing
- Gentle typing delay
- Soft fade-in
- No “typing bubble” theatrics
- No urgency

---

# 6. UI Specification

## 6.1 Primary Interface
Unconditional has only one screen:
- message column
- user input box
- soft header (optional later, not v0.1)
- no icons, badges, or avatars

## 6.2 Color and Typography
- Neutral palette
- Soft contrast
- Readable typography
- No animations except text fade

## 6.3 No Additional Features
Not in v0.1:
- settings
- customization
- modes
- themes
- buttons (except “new session” if implemented later)

Just presence.

---

# 7. Data Privacy & Logging

## 7.1 Logging
- **No server-side conversation logs**
- **No user identifying info**
- **No analytics on content**

## 7.2 Analytics
Allowed only:
- crash logs
- error reports
- generic performance metrics

Prohibited:
- message logging
- behavior tracking
- engagement funnels
- model output capture

## 7.3 Storage
- Conversation stored only in localStorage
- Portable and erasable by the user
- Zero persistence on the server

---

# 8. Extensibility

## 8.1 Plugin Architecture
- **None** for v0.1
- Keep the backend code structured so flows can be modularized later

## 8.2 Model Swapping
- Internal ability to swap models behind the abstraction layer
- Not visible to users
- Future-proofing for alternatives like Claude, Gemini, or local models

---

# 9. Future Hooks (v0.2+)
These are *not* in v0.1, but the architecture should not forbid them:

- daily grounding check-ins
- spaced-reflection summaries
- soft journaling prompts
- optional guided breathing / grounding phrases
- optional “pattern” insights (carefully constrained)
- cross-session thematic linking without memory

These features rely on the ethical and clinical guardrails from your therapist and psychiatrist co-founders.

---

# 10. Philosophy-Technical Integration Summary

Unconditional’s core values shape every engineering choice:

### **Presence → Minimal UI + gentle pacing**
### **Non-pretending → Stateless backend + localStorage continuity**
### **Boundaries → Crisis freeze + full banlist**
### **Dignity → No logging + no analytics on content**
### **Simplicity → One-screen interface + single steady tone**
### **Safety → Model abstraction + strict crisis protocol**
### **Calm → Soft fade + no avatars + one message flow**
### **Humanity → Reflection-based language + clean prompt design**

The system expresses its values through its code.

---

# 11. MVP Completion Definition

Unconditional v0.1 is complete when all of the following are true:

- A user can open the web app and immediately feel grounded by the first message.
- They can share a thought and receive a present, steady reflection.
- The session persists locally.
- The backend is fully stateless.
- Crisis detection freezes the session and shows hotline resources.
- No banned categories of responses appear.
- The interface is so minimal that nothing distracts from presence.
- No logs contain user content.
- The system runs stably on Render with a small footprint.

When these conditions are met, Unconditional has taken its first breath.
