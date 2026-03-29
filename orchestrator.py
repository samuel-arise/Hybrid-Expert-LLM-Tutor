# pylint: disable=invalid-name
"""
orchestrator.py
===============
Orchestration Layer — The LangChain Middleware
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

Architecture Role:
    This module implements Layer 2 of the Hybrid Architecture described in Chapter 3.
    It acts as the central controller between the student's query, the Expert System
    (Layer 3), and the LLM (Layer 4).

    Context-Oriented Workflow (as described in Section 3.2, Point 2):
        1. Receive the student's natural language query.
        2. Extract the CS topic being asked about.
        3. Query the Expert System (expert_engine.py) for verified ground-truth facts.
        4. Inject those verified facts into the LLM prompt as hard constraints.
        5. Return the LLM's grounded, verified response to the UI (app.py).

    The LLM's role is strictly LINGUISTIC — it articulates and explains.
    The Expert System's role is strictly LOGICAL — it verifies and constrains.
    The LLM is never allowed to reason freely outside the verified facts.
"""
import os
from dotenv import load_dotenv
from expert_engine import get_expert_facts, SUPPORTED_TOPICS, TOPIC_ALIASES

# Load HF_TOKEN from .env file
load_dotenv()


# =============================================================================
# TOPIC EXTRACTION
# Identifies which CS topic the student is asking about by scanning the query
# for known topic aliases from the Expert System's alias map.
# =============================================================================

def extract_topic(query: str) -> str | None:
    """
    Scans the student's query for known topic keywords using the Expert
    System's alias map. Returns the canonical topic name if found, else None.

    This is a keyword-matching approach — simple, transparent, and deterministic.
    It directly supports the Constraint-Based Modelling philosophy: the system
    knows exactly what it is and is not able to answer.

    Args:
        query (str): The student's raw natural language question.

    Returns:
        str | None: Canonical topic name (e.g. 'linked_lists') or None.
    """
    query_lower = query.strip().lower()

    # Check multi-word aliases first (longest match wins)
    # Sorting by length descending ensures "binary search tree" is matched
    # before "tree" on the same query.
    sorted_aliases = sorted(TOPIC_ALIASES.keys(), key=len, reverse=True)

    for alias in sorted_aliases:
        if alias in query_lower:
            return TOPIC_ALIASES[alias]

    return None


# =============================================================================
# PROMPT TEMPLATES
# Two templates — one for when the Expert System has verified facts,
# one for when the topic is outside the knowledge base.
# =============================================================================

GROUNDED_PROMPT_TEMPLATE = """You are a precise and helpful Computer Science tutor for undergraduate students.

A student has asked the following question:
"{query}"

The Expert System has retrieved the following VERIFIED FACTS from the knowledge base.
These facts are mathematically and logically correct. You MUST use them as the
foundation of your answer. Do NOT contradict them. Do NOT add unverified claims.
Do NOT hallucinate definitions, complexities, or rules beyond what is provided below.

{expert_facts}

Using ONLY the verified facts above, write a clear, friendly, and well-structured
explanation that directly answers the student's question.
- Use simple language suitable for an undergraduate student.
- Where relevant, give a short illustrative example.
- If the student's question is specifically about a common mistake or error,
  make sure to address it directly using the error facts provided.
- End with one sentence summarising the key takeaway.
"""

FALLBACK_PROMPT_TEMPLATE = """You are a helpful Computer Science tutor for undergraduate students.

A student has asked the following question:
"{query}"

This topic is not currently covered in the verified knowledge base.
Answer the question as accurately and carefully as possible, but make it clear
to the student that this answer has not been verified by the Expert System
and they should cross-check with their course material.

Supported topics in the knowledge base are:
{supported_topics}
"""


# =============================================================================
# LLM INFERENCE
# Uses Groq Inference API with chat completions.
# llama-3.1-8b-instant intruct is actively maintained by Meta on the free tier
# and supports the chat completions format natively.
# =============================================================================

def get_llm_response(prompt: str) -> str:
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please add it to your .env file or Streamlit Secrets."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.3,
    )

    content = response.choices[0].message.content
    return content.strip() if content else ""
# =============================================================================
# CORE ORCHESTRATION FUNCTION
# This is the single function that app.py calls for every student query.
# =============================================================================

# ── GREETING / CASUAL DETECTION ──────────────────────────────────────────
CASUAL_PHRASES = {
    "hello", "hi", "hey", "good morning", "good afternoon",
    "good evening", "how are you", "what's up", "whats up",
    "who are you", "what are you", "what can you do",
    "thank you", "thanks", "bye", "goodbye", "ok", "okay",
    "cool", "great", "nice", "sure", "please", "help"
}

def is_casual(query: str) -> bool:
    """Returns True if the query is a greeting or casual interaction."""
    q = query.strip().lower()
    # Direct match
    if q in CASUAL_PHRASES:
        return True
    # Short query with no CS keywords — likely casual
    if len(q.split()) <= 3:
        for phrase in CASUAL_PHRASES:
            if phrase in q:
                return True
    return False

def get_tutor_response(query: str) -> dict:

    # Handle casual greetings — no badge, no Expert System
    if is_casual(query):
        try:
            casual_prompt = (
                f"You are ARISE Tutor, a friendly Computer Science tutor. "
                f"A student said: '{query}'. "
                f"Respond warmly and briefly. If it is a greeting, greet back and "
                f"mention you can help with Python programming, Data Structures, "
                f"Algorithms, and Automata Theory."
            )
            response = get_llm_response(casual_prompt)
        except Exception as e:
            response = "Hello! I am ARISE Tutor. Ask me anything about Python, Data Structures, Algorithms, or Automata Theory."

        return {
            "response":     response,
            "topic":        "casual",
            "expert_facts": [],
            "facts_string": "",
            "grounded":     None,   # None = no badge at all
            "error":        None
        }

    """
    The primary orchestration pipeline. Executes the full
    Context-Oriented Workflow described in Chapter 3, Section 3.2.

    Pipeline:
        1. Extract topic from student query.
        2. Query Expert System for verified facts.
        3. Build grounded prompt with verified facts injected.
        4. Send prompt to LLM via HuggingFace Inference API.
        5. Return structured response dict to the UI.

    Args:
        query (str): The student's raw natural language question.

    Returns:
        dict with keys:
            "response"        (str)  : The LLM's final grounded answer.
            "topic"           (str)  : Detected topic (or 'unknown').
            "expert_facts"    (list) : List of fact dicts from the Expert System.
            "facts_string"    (str)  : Formatted facts string for the UI trace panel.
            "grounded"        (bool) : True if Expert System facts were used.
            "error"           (str)  : Error message if something failed, else None.
    """

    # ------------------------------------------------------------------
    # STEP 1: Topic Extraction
    # ------------------------------------------------------------------
    topic = extract_topic(query)

    # ------------------------------------------------------------------
    # STEP 2: Expert System Query
    # ------------------------------------------------------------------
    if topic:
        expert_result = get_expert_facts(topic)
    else:
        expert_result = {
            "success": False,
            "facts": [],
            "facts_string": "",
            "topic": "unknown"
        }

    # ------------------------------------------------------------------
    # STEP 3: Prompt Construction
    # ------------------------------------------------------------------
    if expert_result["success"]:
        # Grounded path — facts injected as hard constraints
        prompt = GROUNDED_PROMPT_TEMPLATE.format(
            query=query,
            expert_facts=expert_result["facts_string"]
        )
        grounded = True
    else:
        # Fallback path — topic not in knowledge base
        supported = "\n".join(
            f"- {t.replace('_', ' ').title()}" for t in SUPPORTED_TOPICS
        )
        prompt = FALLBACK_PROMPT_TEMPLATE.format(
            query=query,
            supported_topics=supported
        )
        grounded = False

    # ------------------------------------------------------------------
    # STEP 4: LLM Inference
    # ------------------------------------------------------------------
    try:
        llm_response = get_llm_response(prompt)

    except Exception as e:
        return {
            "response":     None,
            "topic":        topic or "unknown",
            "expert_facts": expert_result.get("facts", []),
            "facts_string": expert_result.get("facts_string", ""),
            "grounded":     grounded,
            "error":        f"LLM Inference Error: {str(e)}"
        }

    # ------------------------------------------------------------------
    # STEP 5: Return structured result to the UI
    # ------------------------------------------------------------------
    return {
        "response":     llm_response,
        "topic":        topic or "unknown",
        "expert_facts": expert_result.get("facts", []),
        "facts_string": expert_result.get("facts_string", ""),
        "grounded":     grounded,
        "error":        None
    }


# =============================================================================
# STANDALONE TEST — run `python orchestrator.py` to verify the pipeline
# =============================================================================

if __name__ == "__main__":
    test_queries = [
        "What is a linked list and how does it work?",
        "What are common mistakes students make with recursion?",
        "Explain how a stack works in Python.",
        "What is the difference between a Binary Tree and a BST?",
        "How do I use a dictionary in Python?",
        "What is a sorting algorithm?",   # Outside KB — tests fallback path
    ]

    for q in test_queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {q}")
        print("-" * 70)
        result = get_tutor_response(q)

        if result["error"]:
            print(f"[ERROR] {result['error']}")
        else:
            print(f"TOPIC DETECTED : {result['topic']}")
            print(f"GROUNDED       : {result['grounded']}")
            print(f"\nRESPONSE:\n{result['response']}")
