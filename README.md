# ◈ ARISE Tutor

**Hybrid Neuro-Symbolic AI Tutoring System for Computer Science Education**

> *Accurate. Transparent. Accessible — from Lagos to rural Kwara.*

---

## Table of Contents

- [Overview](#overview)
- [The Problem: Hallucination in AI Tutoring](#the-problem-hallucination-in-ai-tutoring)
- [The Solution: Neuro-Symbolic Architecture](#the-solution-neuro-symbolic-architecture)
- [Architecture Deep Dive](#architecture-deep-dive)
- [Knowledge Base](#knowledge-base)
- [Accessibility and Scalability](#accessibility-and-scalability)
- [Evaluation Results](#evaluation-results)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Technology Stack](#technology-stack)
- [Roadmap](#roadmap)
- [Academic Context](#academic-context)
- [Author](#author)

---

## Overview

ARISE Tutor is a fully deployed, open-source AI tutoring system for undergraduate Computer Science students. It was developed as a final year research project at **Landmark University, Omu-Aran, Kwara State, Nigeria**, and is designed to work anywhere — on a laptop in Lagos, a shared desktop in a rural secondary school, or a mobile device with an intermittent connection.

The system solves a problem that most AI tutoring tools quietly ignore: **Large Language Models hallucinate**. They generate fluent, confident-sounding explanations that are sometimes factually wrong — and in a subject like Computer Science, where the time complexity of an algorithm or the conditions for a recursive base case are formally defined, "sometimes wrong" is not good enough.

ARISE Tutor addresses this through a **Hybrid Neuro-Symbolic Architecture** that couples a rule-based Expert System with a Large Language Model. The Expert System encodes verified, textbook-sourced facts as production rules. The LLM transforms those facts into natural, student-friendly explanations. The result is a tutoring system that is simultaneously **conversational** (you can ask it anything in plain English) and **verifiably accurate** (every answer is traceable to a specific academic source).

---

## The Problem: Hallucination in AI Tutoring

When students use a standard AI chatbot (like ChatGPT or any unconstrained LLM) to study Computer Science, they are gambling. The model might answer correctly. It might also:

- State that Binary Search runs in **O(1)** instead of O(log n)
- Describe Quick Sort as **always O(n log n)**, omitting the O(n²) worst case
- Invent a data structure ("an indexed doubly-linked list") that does not exist
- Claim that a **linked list supports O(1) index access** — the opposite of the truth
- Omit that Binary Search **requires a sorted array** before it can be applied
- Describe recursion errors without mentioning the **missing base case** as the primary cause

These are not hypothetical examples. They are observed errors from the evaluation conducted as part of this project, in which the same LLM used in ARISE Tutor was tested without symbolic grounding. **40% of responses contained at least one factual error** under those conditions.

The danger is not that the errors are obvious — they are not. They are embedded in fluent, well-structured, authoritative-sounding prose. A student encountering a concept for the first time has no way to identify which part of the explanation is wrong. This is what this project calls the **Fluency Trap**: the risk that students accept an LLM explanation as correct simply because it sounds correct.

---

## The Solution: Neuro-Symbolic Architecture

ARISE Tutor escapes the Fluency Trap through a design principle called **Constraint-Based Symbolic Grounding**.

The core idea is simple: **separate the job of knowing what is true from the job of saying it fluently**.

```
Student Query
      │
      ▼
┌─────────────────────────────┐
│     ORCHESTRATION LAYER     │  ← Identifies topic, routes query
└─────────────┬───────────────┘
              │
      ┌───────┴────────┐
      ▼                ▼
┌──────────────┐  ┌──────────────────────┐
│ EXPERT SYSTEM│  │   FALLBACK PATH      │
│  (Experta)   │  │ (Unverified LLM)     │
│              │  │                      │
│ Fires rules  │  │ Used when topic is   │
│ Returns 3–5  │  │ outside knowledge    │
│ verified     │  │ base. Clearly        │
│ facts        │  │ labelled ⚠ Unverified│
└──────┬───────┘  └──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│    PROMPT CONSTRUCTION      │
│                             │
│  "These facts are verified. │
│   Do NOT contradict them.   │
│   Do NOT add unverified     │
│   claims beyond what is     │
│   provided below."          │
│                             │
│   [Verified Facts Injected] │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│     LLM (via Groq API)      │  ← Articulates. Never decides facts.
│  Qwen3-32B / Kimi K2        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│    VERIFIED RESPONSE        │
│    ✓ Verified by Expert     │
│      System                 │
│    [Expert System Trace     │
│     Panel available]        │
└─────────────────────────────┘
```

### Why This Works

| Component | Role | Why It Can't Do the Other's Job |
|-----------|------|----------------------------------|
| **Expert System** | Determines what is true | Cannot generate fluent natural language |
| **LLM** | Expresses truth fluently | Cannot reliably determine what is true |
| **Orchestrator** | Mediates between both | Neither stores knowledge nor generates text |

By keeping these roles strictly separated, ARISE Tutor guarantees that the LLM never has to decide — on its own — what the correct time complexity, prerequisite condition, or common error for a topic is. Those decisions are made by the Expert System, encoded by a human knowledge engineer from verified academic sources, before the LLM generates a single word.

### The Expert System Trace Panel

Every verified response in ARISE Tutor comes with a transparent audit trail. Students and instructors can expand the **Expert System Trace** panel in the sidebar to see exactly which production rules fired, identified by unique rule IDs (e.g., `LL-DEF-01`, `BST-PROP-02`), categorised by semantic type (`definition`, `property`, `step`, `error`, `use_case`), and traceable to specific academic sources.

This is the feature that makes ARISE Tutor not just accurate, but **accountable**. A student can always ask: *how does this system know that?* — and get a specific, verifiable answer.

---

## Architecture Deep Dive

ARISE Tutor is structured as a **four-layer pipeline**. Each layer has exactly one responsibility.

### Layer 1 — User Interface (`app.py`)

Built with **Streamlit**, the UI provides:

- A conversational chat interface with distinct visual styling for student and tutor messages
- A sidebar with topic chips showing all supported topics (active topic highlighted)
- An **Expert System Trace panel** (collapsible) showing fired rules for the last query
- A **dark/light theme toggle** for accessibility and presentation flexibility
- Enter-to-submit support via `st.form` with reliable input clearing

The UI is deliberately lightweight. It requires no JavaScript, no React, no separate backend. This is a deliberate accessibility decision — it keeps the deployment footprint small and the system usable on low-powered devices.

### Layer 2 — Orchestration Layer (`orchestrator.py`)

The central controller. On each query, it:

1. Runs a **casual-intent classifier** to detect greetings and non-substantive messages (no badge applied)
2. Runs **topic extraction** via `extract_topic()` — scanning against 80+ aliases with a longest-match-first strategy
3. If a topic is matched: invokes the Expert System and constructs the **grounded prompt**
4. If no topic is matched: uses the **fallback prompt** and marks the response as Unverified
5. Calls the LLM via Groq and returns a structured result dictionary to the UI

The orchestrator is provider-agnostic: the LLM integration is contained in a single function (`get_llm_response()`). Switching providers requires changing exactly one function.

### Layer 3 — Symbolic Reasoning Layer (`expert_engine.py`)

The **Truth Engine**. Implemented using **Experta** — a Python port of CLIPS, the NASA-developed expert system shell. Internally uses the **Rete Algorithm** for efficient pattern-matching.

Key design decisions:

- **Fresh engine instance per query** — ensures statelessness and thread safety across concurrent sessions
- **Constraint-Based Modelling** — rules encode what any correct answer *must satisfy*, not what a correct answer *looks like*
- **Five semantic categories** — `definition`, `property`, `step`, `error`, `use_case`
- **Priority-ordered output** — facts are sorted by priority before injection, ensuring the LLM always receives information in pedagogically coherent order



### Layer 4 — Generative Layer (Groq API)

The LLM handles **linguistic articulation only**. It receives:

- The student's query
- The verified facts from the Expert System
- Explicit constraint instructions: *do not contradict the facts, do not add unverified claims, do not hallucinate*

Current model: **Qwen3-32B** (or Kimi K2) via Groq. Temperature: `0.3`. Max tokens: `700`.

---

## Knowledge Base

The knowledge base contains **70 production rules across 15 topics in 4 domains**, sourced from peer-reviewed textbooks published 2020–2023.

### Coverage

| Domain | Topics | Rules |
|--------|--------|-------|
| **Python Programming** | Variables & Data Types, Control Flow, Functions & Recursion, Object-Oriented Programming | 15 |
| **Data Structures** | Lists/Arrays, Stacks, Queues, Linked Lists, Trees & BST, Hash Tables | 21 |
| **Algorithms** | Sorting, Searching, Big-O Notation, Graph Theory & BFS/DFS | 17 |
| **Theory of Computation** | Automata Theory (DFA, NFA, Finite Automata) | 5 |
| | **Total** | **70** |

### Academic Sources

| Source | Domain Coverage |
|--------|----------------|
| Liang, Y. D. (2022). *Introduction to Python Programming and Data Structures* (3rd ed.). Pearson. | Python Programming |
| Wengrow, J. (2023). *A Common-Sense Guide to Data Structures and Algorithms in Python*. Pragmatic Bookshelf. | Data Structures, Algorithms |
| Agarwal, B. (2023). *Hands-On Data Structures and Algorithms with Python* (3rd ed.). Packt. | Data Structures, Algorithms |
| Sipser, M. (2020). *Introduction to the Theory of Computation* (3rd ed.). Cengage. | Automata Theory |

### Extending the Knowledge Base

Adding a new topic requires only adding rules to `expert_engine.py` and alias entries to `TOPIC_ALIASES`. No changes to the orchestrator, UI, or LLM integration are required. This is by design.


# And add aliases:
TOPIC_ALIASES["bubble sort"] = "sorting"
TOPIC_ALIASES["merge sort"] = "sorting"
```

---

## Accessibility and Scalability

### Designed for Underserved Environments

ARISE Tutor was built with a specific context in mind: **Nigerian higher education**, where many students at institutions outside major urban centres study with limited access to academic support infrastructure — no tutoring centres, limited library resources, and instructors stretched across large class sizes.

But the problem it addresses is not uniquely Nigerian. Anywhere that students lack access to reliable, personalised academic support — rural universities in Sub-Saharan Africa, community colleges in underserved regions, distance learning programmes in developing economies — the Fluency Trap is active and the consequences are real.

The system's architecture is designed to be as accessible as possible at every level:

#### No Hardware Requirements

ARISE Tutor runs entirely in a web browser. There is nothing to install. The LLM runs on Groq's servers in the cloud — the student's device only sends and receives text. A device capable of browsing the web can use ARISE Tutor.

#### No Bandwidth-Intensive Operations

The system does not transmit images, audio, or video. Every interaction is a short text query and a text response. This makes ARISE Tutor usable on **low-bandwidth connections** — including mobile data connections on 3G networks, which are the reality for many students in rural Nigeria and across sub-Saharan Africa.

#### No Cost to the Student

The live deployment at [arisetutor.streamlit.app](https://arisetutor.streamlit.app) is **completely free** for students to use. There is no registration, no subscription, no paywall. A student with a phone and a data connection can access the same verified CS tutoring as a student at a well-resourced institution.

#### No Institutional Infrastructure Required

ARISE Tutor requires no server, no IT department, no institutional account. A student can bookmark the URL and use it from any device, at any time. For institutions that want to deploy their own instance, the entire system can be deployed in under 30 minutes using Streamlit Community Cloud and a free Groq API key.

#### Works on Mobile Devices

The Streamlit interface renders on mobile browsers. Students can use ARISE Tutor on the same smartphone they use for everything else — no dedicated computer required.

### Scalability for Institutional Deployment

For institutions that want to deploy ARISE Tutor at scale, the architecture supports this without modification:

#### Horizontal Scalability

Streamlit Community Cloud handles concurrent sessions natively. The Expert System is stateless (fresh engine instance per query) and thread-safe, so multiple students querying simultaneously do not interfere with each other.

#### Knowledge Base Scalability

The Rete Algorithm at the heart of the Expert System is designed for efficient scaling. Adding new topics and rules does not degrade performance — the incremental pattern-matching architecture means inference time grows slowly with knowledge base size, remaining suitable for real-time interactive use even as coverage expands to hundreds of topics.

#### Geographic Scalability

Because ARISE Tutor is a web application with no geographic restriction, it can serve students at any institution — urban or rural, well-resourced or under-resourced — from a single deployment. An institution in rural Kwara State and a university in Lagos access the same verified knowledge base from the same endpoint.

#### Domain Scalability

The modular architecture allows the knowledge base to be extended to new academic disciplines without architectural changes. A version of ARISE Tutor covering Mathematics, Physics, or Law would require only a new set of production rules and a new alias map — the orchestration layer, the UI, and the LLM integration would be unchanged.

### A Vision for Equitable CS Education

The deeper aspiration behind ARISE Tutor is to demonstrate that **accuracy and accessibility are not in tension**. The assumption that reliable AI tutoring requires expensive infrastructure, commercial subscriptions, or institutional resources is false. The Neuro-Symbolic architecture demonstrates that a system built from open-source components, deployed on a free platform, and accessible via a web browser can provide a quality of educational support that is verifiably superior — in factual accuracy — to commercial AI tools that students are already using.

For a student at a rural university with no tutoring centre, no academic support service, and limited library access, ARISE Tutor is not a supplement to existing support — it may be the primary support available. The system is built with that student in mind, and every architectural decision reflects the goal of making verified, trustworthy CS tutoring available to anyone with a device and a connection.

---

## Evaluation Results

A controlled comparative evaluation was conducted using **the same LLM in both conditions**, isolating the contribution of symbolic grounding from any model-selection effect.

| Metric | Baseline LLM (No Grounding) | ARISE Tutor (Symbolic Grounding) | Change |
|--------|----------------------------|-----------------------------------|--------|
| **Hallucination Rate** | 40% | 5% | −87.5% |
| **Logical Accuracy Rate** | 62% | 95% | +53.2% |
| **Consistency Score** | 55% | 91% | +65.5% |

The single hallucination in the ARISE Tutor condition occurred on a fallback-path query (topic outside the knowledge base). **All grounded responses within the system's encoded scope were hallucination-free.**

---

## Technology Stack

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Expert System | Experta | 1.9.4 | Forward-chaining, Rete Algorithm |
| Dependency pin | frozendict | **1.2** | **Must not be upgraded** |
| Python patch | compat.py | Custom | Restores collections attrs removed in Python 3.10+ |
| Orchestration | LangChain | 0.2.16 | Prompt template management |
| LLM Provider | Groq Inference API | — | Free tier: 14,400 req/day |
| LLM Model | Qwen3-32B / Kimi K2 | — | Temperature=0.3, max_tokens=700 |
| Frontend | Streamlit | 1.37.1 | No separate frontend or backend |
| Deployment | Streamlit Community Cloud | — | Free, GitHub-integrated |
| Environment | python-dotenv | 1.0.1 | Local credential management |

---

## Roadmap

### Near-Term
- [ ] **Semantic intent classification** — replace keyword matching with a lightweight encoder model for broader topic coverage
- [ ] **Curriculum sequencing** — encode prerequisite relationships between topics so the system can identify and proactively address foundational gaps
- [ ] **Expanded knowledge base** — Operating Systems, Discrete Mathematics, Database Systems, Computer Networks

### Medium-Term
- [ ] **Student model** — track query history within a session to personalise explanation depth and flag recurring errors
- [ ] **Multi-turn conversation memory** — maintain context across turns for scaffolded, progressive explanations
- [ ] **Offline mode** — local LLM support for environments with no internet access (using Ollama or similar)

### Long-Term
- [ ] **Learning outcomes evaluation** — longitudinal study comparing student performance with ARISE Tutor vs unconstrained LLM alternatives
- [ ] **Multi-language support** — Yoruba, Hausa, Igbo, and other Nigerian languages for broader rural accessibility
- [ ] **Instructor dashboard** — analytics on the most frequently queried topics and most common error patterns across a student cohort

---

## Academic Context

ARISE Tutor was developed as a final year Computer Science project at **Landmark University, Omu-Aran, Kwara State, Nigeria**, under the title:

> *Design of a Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science*

A full academic chapter based on this project has been submitted for inclusion in the IGI Global edited volume *Securing Data Privacy in Education With AI-Powered Cybersecurity* (2026).

**Evaluation metrics used:**
- **Hallucination Rate (HR)** — proportion of responses containing at least one factual error
- **Logical Accuracy Rate (LAR)** — proportion of fully correct responses satisfying all encoded rule constraints
- **Consistency Score (CS)** — proportion of semantically equivalent queries that receive factually equivalent responses

---

## Author

**Arise Steven Samuel**
Department of Computer Science
Landmark University, Omu-Aran, Kwara State, Nigeria

Founder & Lead Organiser, Creative Minds' Forum (CMF)

---

## License

This project is open-source and available for academic and educational use. If you extend or build on ARISE Tutor, a citation to the original project is appreciated.

---

**Built to make verified CS knowledge accessible — everywhere.**

*From urban universities to rural learning centres, ARISE Tutor brings the same verified, hallucination-resistant tutoring to every student with a device and a connection.*

⬡ ARISE Tutor · Landmark University · 2025
