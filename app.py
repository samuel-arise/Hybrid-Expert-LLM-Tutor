"""
app.py
======
User Interface Layer — Streamlit Frontend
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

Design:
    Theme          : Gemini-inspired — deep navy dark background with
                     soft purple-to-blue gradient accents
    Display font   : Syne (headings, labels)
    Body font      : Inter (chat, descriptions)
    Monospace font : JetBrains Mono (trace panel, rule IDs)
"""

import compat  # must be first — patches collections for Python 3.10+
import streamlit as st
from orchestrator import get_tutor_response, SUPPORTED_TOPICS

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="ARISE Tutor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS — Gemini-style Theme
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D0F1A;
    color: #E2E8F8;
}

.stApp {
    background-color: #0D0F1A;
}

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 32px !important;
    padding-bottom: 32px !important;
    max-width: 860px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #0B0D18 !important;
    border-right: 1px solid #1E2140 !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 24px 20px !important;
    max-width: 100% !important;
}

/* ── GRADIENT UTILITY ── */
.gradient-text {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── APP HEADER ── */
.arise-header {
    margin-bottom: 28px;
}

.arise-logo {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1;
}

.arise-logo span {
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    opacity: 0.6;
}

.arise-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 300;
    color: #4A5070;
    margin-top: 4px;
    letter-spacing: 0.02em;
}

/* ── CHAT MESSAGES ── */
.msg-wrapper {
    margin-bottom: 20px;
    animation: fadeUp 0.3s ease forwards;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-role {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
    padding-left: 2px;
}

.msg-role-student { color: #4A5070; }
.msg-role-tutor {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.msg-bubble {
    border-radius: 14px;
    padding: 14px 18px;
    font-size: 14px;
    line-height: 1.65;
    font-weight: 400;
    border: 1px solid;
}

.msg-bubble-student {
    background: #13162A;
    border-color: #1E2140;
    color: #B0BAD8;
    margin-left: 32px;
}

.msg-bubble-tutor {
    background: linear-gradient(135deg, rgba(139,92,246,0.06), rgba(59,130,246,0.06));
    border-color: rgba(139,92,246,0.2);
    color: #E2E8F8;
}

/* ── BADGES ── */
.badge-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid;
    letter-spacing: 0.05em;
    display: inline-block;
}

.badge-verified {
    color: #3B82F6;
    background: rgba(59,130,246,0.08);
    border-color: rgba(59,130,246,0.25);
}

.badge-unverified {
    color: #F59E0B;
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.25);
}

.badge-topic {
    color: #8B5CF6;
    background: rgba(139,92,246,0.08);
    border-color: rgba(139,92,246,0.2);
}

/* ── INPUT AREA ── */
.stTextInput > div > div > input {
    background-color: #13162A !important;
    border: 1px solid #1E2140 !important;
    border-radius: 12px !important;
    color: #E2E8F8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.08) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #2A2F50 !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── SIDEBAR ELEMENTS ── */
.sidebar-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2A2F50;
    margin-bottom: 10px;
    margin-top: 20px;
    padding-bottom: 6px;
    border-bottom: 1px solid #1E2140;
}

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    margin-bottom: 2px;
}

.sidebar-tagline {
    font-size: 11px;
    color: #2A2F50;
    font-weight: 300;
    margin-bottom: 4px;
}

.topic-chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 6px;
    background: #13162A;
    border: 1px solid #1E2140;
    color: #3A4268;
    margin: 3px 3px 3px 0;
}

.topic-chip-active {
    background: rgba(139,92,246,0.1);
    border-color: rgba(139,92,246,0.3);
    color: #8B5CF6;
}

/* ── EXPERT SYSTEM TRACE ── */
.trace-container {
    background: #090B16;
    border: 1px solid #1E2140;
    border-radius: 12px;
    padding: 14px;
    margin-top: 4px;
}

.trace-header-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}

.trace-rule-block {
    background: rgba(139,92,246,0.03);
    border: 1px solid #1E2140;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
}

.trace-rule-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #8B5CF6;
    opacity: 0.7;
    margin-bottom: 4px;
}

.trace-rule-category {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    padding: 2px 7px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.cat-definition  { background: rgba(59,130,246,0.12);  color: #3B82F6; }
.cat-property    { background: rgba(139,92,246,0.12);  color: #8B5CF6; }
.cat-step        { background: rgba(168,85,247,0.12);  color: #A855F7; }
.cat-error       { background: rgba(239,68,68,0.12);   color: #EF4444; }
.cat-use_case    { background: rgba(245,158,11,0.12);  color: #F59E0B; }

.trace-rule-desc {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #6B7AA0;
    line-height: 1.6;
    word-break: break-word;
}

.trace-empty {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #1E2140;
    text-align: center;
    padding: 20px 0;
}

/* ── EXPANDER OVERRIDE ── */
[data-testid="stExpander"] {
    background: #0B0D18 !important;
    border: 1px solid #1E2140 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: #8B5CF6 !important;
    padding: 12px 16px !important;
}

/* ── DIVIDER ── */
.arise-divider {
    border: none;
    border-top: 1px solid #1E2140;
    margin: 20px 0;
}

/* ── STATUS INDICATOR ── */
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    margin-right: 6px;
    animation: pulse 2.5s infinite;
    vertical-align: middle;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(139,92,246,0.4); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 5px rgba(139,92,246,0); }
}

.status-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #2A2F50;
    vertical-align: middle;
}

/* ── WELCOME SCREEN ── */
.welcome-container {
    text-align: center;
    padding: 60px 20px;
}

.welcome-icon {
    font-size: 48px;
    margin-bottom: 16px;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #E2E8F8;
    margin-bottom: 8px;
}

.welcome-sub {
    font-size: 14px;
    color: #4A5070;
    font-weight: 300;
    line-height: 1.6;
    max-width: 480px;
    margin: 0 auto 24px;
}

.welcome-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 520px;
    margin: 0 auto;
}

.welcome-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 8px;
    background: #13162A;
    border: 1px solid #1E2140;
    color: #3A4268;
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALISATION
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_expert_facts" not in st.session_state:
    st.session_state.last_expert_facts = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if "last_grounded" not in st.session_state:
    st.session_state.last_grounded = False


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">✦ ARISE</div>
    <div class="sidebar-tagline">Hybrid Expert-LLM Tutor</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    st.markdown("""
    <span class="status-dot"></span>
    <span class="status-text">SYSTEM ONLINE · Expert Engine Active</span>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Knowledge Domain</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:#2A2F50; font-weight:300; margin-bottom:10px;">
        Python Programming & Data Structures
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Supported Topics</div>', unsafe_allow_html=True)

    topic_html = '<div style="line-height:2;">'
    for topic in SUPPORTED_TOPICS:
        label = topic.replace("_", " ").title()
        is_active = (topic == st.session_state.last_topic)
        css_class = "topic-chip topic-chip-active" if is_active else "topic-chip"
        topic_html += f'<span class="{css_class}">{label}</span>'
    topic_html += '</div>'
    st.markdown(topic_html, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    # Expert System Trace Panel
    st.markdown('<div class="sidebar-section-title">Expert System Trace</div>', unsafe_allow_html=True)

    with st.expander("▸ View Fired Rules", expanded=False):
        if st.session_state.last_expert_facts:
            topic_display = (st.session_state.last_topic or "").replace("_", " ").upper()
            st.markdown(f"""
            <div class="trace-container">
                <div class="trace-header-text">● RULES FIRED — {topic_display}</div>
            """, unsafe_allow_html=True)

            for fact in st.session_state.last_expert_facts:
                category = fact.get("category", "")
                st.markdown(f"""
                <div class="trace-rule-block">
                    <div class="trace-rule-id">{fact.get('rule_id', '')}</div>
                    <span class="trace-rule-category cat-{category}">{category}</span>
                    <div class="trace-rule-desc">{fact.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="trace-container">
                <div class="trace-empty">
                    No rules fired yet.<br/>Ask a question to activate the engine.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    if st.button("⟳  Clear Conversation"):
        st.session_state.messages = []
        st.session_state.last_expert_facts = []
        st.session_state.last_topic = None
        st.session_state.last_grounded = False
        st.rerun()

    st.markdown("""
    <div style="margin-top:24px; font-family:'JetBrains Mono',monospace;
                font-size:9px; color:#1A1E36; line-height:1.8;">
        ARISE Tutor · Neuro-Symbolic AI<br/>
        Landmark University · CS Dept<br/>
        Arise Steven Samuel
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN CHAT AREA
# =============================================================================

st.markdown("""
<div class="arise-header">
    <div class="arise-logo">✦ ARISE <span>Tutor</span></div>
    <div class="arise-tagline">Neuro-Symbolic AI · Verified Knowledge · Python & Data Structures</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

# Welcome screen
if not st.session_state.messages:
    topics_chips = "".join(
        f'<span class="welcome-chip">{t.replace("_", " ").title()}</span>'
        for t in SUPPORTED_TOPICS
    )
    st.markdown(f"""
    <div class="welcome-container">
        <div class="welcome-icon">✦</div>
        <div class="welcome-title">Ask anything about CS</div>
        <div class="welcome-sub">
            ARISE Tutor combines a Rule-Based Expert System with a Large Language Model
            to give you accurate, verified answers — not hallucinations.
        </div>
        <div class="welcome-chip-row">{topics_chips}</div>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    grounded = msg.get("grounded", False)
    topic = msg.get("topic", None)

    if role == "student":
        st.markdown(f"""
        <div class="msg-wrapper">
            <div class="msg-role msg-role-student">You</div>
            <div class="msg-bubble msg-bubble-student">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        badge_verified = (
            '<span class="badge badge-verified">✓ Verified by Expert System</span>'
            if grounded else
            '<span class="badge badge-unverified">⚠ Unverified — cross-check advised</span>'
        )
        badge_topic = (
            f'<span class="badge badge-topic">{topic.replace("_", " ")}</span>'
            if topic and topic != "unknown" else ""
        )
        st.markdown(f"""
        <div class="msg-wrapper">
            <div class="msg-role msg-role-tutor">ARISE Tutor</div>
            <div class="msg-bubble msg-bubble-tutor">{content}</div>
            <div class="badge-row">{badge_verified}{badge_topic}</div>
        </div>
        """, unsafe_allow_html=True)

# Input area
st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        label="query",
        placeholder="Ask a question about Python or Data Structures...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send = st.button("Ask →")

# =============================================================================
# QUERY HANDLING
# =============================================================================

if send and user_input.strip():

    query = user_input.strip()

    st.session_state.messages.append({
        "role": "student",
        "content": query,
    })

    with st.spinner(""):
        result = get_tutor_response(query)

    if result["error"]:
        response_text = f"⚠ An error occurred: {result['error']}"
        grounded = False
        topic = "unknown"
        facts = []
    else:
        response_text = result["response"]
        grounded = result["grounded"]
        topic = result["topic"]
        facts = result["expert_facts"]

    st.session_state.messages.append({
        "role": "tutor",
        "content": response_text,
        "grounded": grounded,
        "topic": topic,
    })

    st.session_state.last_expert_facts = facts
    st.session_state.last_topic = topic
    st.session_state.last_grounded = grounded

    st.rerun()