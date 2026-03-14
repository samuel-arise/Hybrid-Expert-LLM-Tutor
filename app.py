"""
app.py
======
User Interface Layer — Streamlit Frontend
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

Design:
    Theme  : Clean minimal — dark background, white text, ChatGPT-style
    Font   : Inter throughout
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
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── FORCE DARK MODE ON EVERYTHING ── */
html, body,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
section.main,
.stApp {
    background-color: #212121 !important;
    color: #ECECEC !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── FORCE ALL TEXT WHITE ── */
p, span, div, label, li, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"] {
    color: #ECECEC !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 40px !important;
    padding-bottom: 40px !important;
    max-width: 760px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: #171717 !important;
    border-right: 1px solid #2F2F2F !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 24px 16px !important;
    max-width: 100% !important;
}

/* Force sidebar text white */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #ECECEC !important;
}

/* ── SIDEBAR TOGGLE BUTTON ── */
[data-testid="collapsedControl"] {
    background-color: #2A2A2A !important;
    color: #ECECEC !important;
    border: 1px solid #333 !important;
}

button[kind="header"] {
    background-color: #2A2A2A !important;
    color: #ECECEC !important;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background-color: #2A2A2A !important;
    border: 1px solid #444 !important;
    border-radius: 12px !important;
    color: #ECECEC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #666 !important;
    box-shadow: none !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: #666 !important;
}

.stTextInput label {
    display: none !important;
}

/* ── BUTTON ── */
.stButton > button {
    background-color: #ECECEC !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: opacity 0.2s ease !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    background-color: #ECECEC !important;
    color: #111111 !important;
}

.stButton > button p {
    color: #111111 !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background-color: #1A1A1A !important;
    border: 1px solid #2F2F2F !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #888 !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stExpander"] svg {
    fill: #888 !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: #ECECEC !important;
}

/* ── DIVIDER ── */
.arise-divider {
    border: none;
    border-top: 1px solid #2F2F2F;
    margin: 16px 0;
}

/* ── CHAT MESSAGES ── */
.msg-wrapper {
    margin-bottom: 28px;
}

.msg-role {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #666 !important;
    margin-bottom: 6px !important;
}

.msg-role-tutor {
    color: #ECECEC !important;
}

.msg-bubble-student {
    font-size: 14px;
    line-height: 1.7;
    color: #ECECEC !important;
    padding: 12px 16px;
    background: #2A2A2A;
    border-radius: 12px;
    border: 1px solid #333;
}

.msg-bubble-tutor {
    font-size: 14px;
    line-height: 1.7;
    color: #ECECEC !important;
}

/* ── BADGES ── */
.badge-row {
    display: flex;
    gap: 6px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.badge {
    font-size: 10px !important;
    font-weight: 500 !important;
    padding: 2px 9px !important;
    border-radius: 20px !important;
    border: 1px solid #444 !important;
    display: inline-block !important;
    background: #2A2A2A !important;
}

.badge-verified {
    color: #ECECEC !important;
    border-color: #555 !important;
}

.badge-unverified {
    color: #888 !important;
    border-color: #333 !important;
}

.badge-topic {
    color: #888 !important;
    border-color: #333 !important;
}

/* ── SIDEBAR ELEMENTS ── */
.sidebar-logo {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #ECECEC !important;
    letter-spacing: -0.01em !important;
}

.sidebar-sub {
    font-size: 11px !important;
    color: #555 !important;
}

.sidebar-section-title {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    margin-top: 20px !important;
    margin-bottom: 8px !important;
}

.topic-chip {
    display: inline-block;
    font-size: 11px;
    padding: 3px 9px;
    border-radius: 6px;
    background: #2A2A2A;
    border: 1px solid #333;
    color: #888 !important;
    margin: 2px 2px 2px 0;
}

.topic-chip-active {
    background: #333 !important;
    border-color: #555 !important;
    color: #ECECEC !important;
}

.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #555;
    margin-right: 6px;
    vertical-align: middle;
}

.status-text {
    font-size: 10px !important;
    color: #555 !important;
    vertical-align: middle;
}

/* ── TRACE PANEL ── */
.trace-container {
    background: #1A1A1A;
    border: 1px solid #2F2F2F;
    border-radius: 10px;
    padding: 12px;
}

.trace-header-text {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    margin-bottom: 10px !important;
}

.trace-rule-block {
    border: 1px solid #2F2F2F;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    background: #212121;
}

.trace-rule-id {
    font-size: 10px !important;
    color: #ECECEC !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

.trace-rule-category {
    font-size: 9px !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-bottom: 6px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    background: #2A2A2A !important;
    border: 1px solid #333 !important;
    color: #888 !important;
}

.trace-rule-desc {
    font-size: 11px !important;
    color: #888 !important;
    line-height: 1.6 !important;
    word-break: break-word !important;
}

.trace-empty {
    font-size: 11px !important;
    color: #444 !important;
    text-align: center !important;
    padding: 20px 0 !important;
}

/* ── WELCOME ── */
.welcome-container {
    text-align: center;
    padding: 80px 20px 40px;
}

.welcome-title {
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #ECECEC !important;
    margin-bottom: 10px !important;
    letter-spacing: -0.02em !important;
}

.welcome-sub {
    font-size: 14px !important;
    color: #666 !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    max-width: 440px !important;
    margin: 0 auto 28px !important;
}

.welcome-chip {
    font-size: 12px;
    padding: 5px 12px;
    border-radius: 8px;
    background: #2A2A2A;
    border: 1px solid #333;
    color: #666 !important;
}

.welcome-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 500px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
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
    <div class="sidebar-logo">ARISE Tutor</div>
    <div class="sidebar-sub">Hybrid Expert-LLM · CS Education</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    st.markdown("""
    <span class="status-dot"></span>
    <span class="status-text">Expert Engine Active</span>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Supported Topics</div>',
                unsafe_allow_html=True)

    topic_html = '<div style="line-height:2.2;">'
    for topic in SUPPORTED_TOPICS:
        label = topic.replace("_", " ").title()
        is_active = (topic == st.session_state.last_topic)
        css_class = "topic-chip topic-chip-active" if is_active else "topic-chip"
        topic_html += f'<span class="{css_class}">{label}</span>'
    topic_html += '</div>'
    st.markdown(topic_html, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Expert System Trace</div>',
                unsafe_allow_html=True)

    with st.expander("View fired rules", expanded=False):
        if st.session_state.last_expert_facts:
            topic_display = (st.session_state.last_topic or "").replace("_", " ").upper()
            st.markdown(f"""
            <div class="trace-container">
                <div class="trace-header-text">Rules fired — {topic_display}</div>
            """, unsafe_allow_html=True)

            for fact in st.session_state.last_expert_facts:
                category = fact.get("category", "")
                st.markdown(f"""
                <div class="trace-rule-block">
                    <div class="trace-rule-id">{fact.get('rule_id', '')}</div>
                    <span class="trace-rule-category">{category}</span>
                    <div class="trace-rule-desc">{fact.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="trace-container">
                <div class="trace-empty">
                    No rules fired yet.<br/>Ask a question to begin.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.last_expert_facts = []
        st.session_state.last_topic = None
        st.session_state.last_grounded = False
        st.rerun()

    st.markdown("""
    <div style="margin-top:24px; font-size:10px; color:#333; line-height:1.8;">
        Arise Steven Samuel<br/>
        Landmark University · CS Dept
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN AREA
# =============================================================================

st.markdown("""
<div class="arise-header" style="margin-bottom:24px;">
    <div style="font-size:20px; font-weight:600; color:#ECECEC; letter-spacing:-0.02em;">
        ARISE Tutor
    </div>
    <div style="font-size:13px; font-weight:300; color:#555; margin-top:3px;">
        Python Programming & Data Structures · Verified by Expert System
    </div>
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
        <div class="welcome-title">What can I help you learn?</div>
        <div class="welcome-sub">
            Ask any question about Python or Data Structures.
            Every answer is grounded in verified knowledge — not guesswork.
        </div>
        <div class="welcome-chip-row">{topics_chips}</div>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    grounded = msg.get("grounded", False)
    topic = msg.get("topic", None)

    if role == "student":
        st.markdown(f"""
        <div class="msg-wrapper">
            <div class="msg-role">You</div>
            <div class="msg-bubble-student">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        badge_verified = (
            '<span class="badge badge-verified">✓ Verified</span>'
            if grounded else
            '<span class="badge badge-unverified">⚠ Unverified</span>'
        )
        badge_topic = (
            f'<span class="badge badge-topic">{topic.replace("_", " ")}</span>'
            if topic and topic != "unknown" else ""
        )
        st.markdown(f"""
        <div class="msg-wrapper">
            <div class="msg-role msg-role-tutor">ARISE Tutor</div>
            <div class="msg-bubble-tutor">{content}</div>
            <div class="badge-row">{badge_verified}{badge_topic}</div>
        </div>
        """, unsafe_allow_html=True)

# Input
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
    send = st.button("Send")

# =============================================================================
# QUERY HANDLING
# =============================================================================

if send and user_input.strip():

    query = user_input.strip()

    st.session_state.messages.append({
        "role": "student",
        "content": query,
    })

    with st.spinner("Thinking..."):
        result = get_tutor_response(query)

    if result["error"]:
        response_text = f"An error occurred: {result['error']}"
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