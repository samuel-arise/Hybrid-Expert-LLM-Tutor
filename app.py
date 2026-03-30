# pylint: disable=invalid-name
"""
app.py
======
User Interface Layer — Streamlit Frontend
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

    Background    : #0D0D0D deep black
    Accent        : #7C3AED purple (brand colour)
    Display font  : Syne — bold, heavy headings
    Body font     : DM Sans — clean, modern body text
    Mono font     : JetBrains Mono — trace panel
    Cards         : Dark surfaces with purple-tinted borders
    Labels        : Uppercase spaced purple section labels
    Buttons       : Solid purple primary, dark outline secondary
"""
import streamlit as st
from orchestrator import get_tutor_response, SUPPORTED_TOPICS

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="ARISE Tutor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS — Samuel Arise Design Language
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── GLOBAL ── */
html, body,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main, .stApp {
    background-color: #0D0D0D !important;
    color: #F0EEF8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── FORCE ALL TEXT LIGHT ── */
p, span, div, label, li, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"] {
    color: #F0EEF8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 40px !important;
    padding-bottom: 60px !important;
    max-width: 780px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: #0A0A0A !important;
    border-right: 1px solid #1C1C2E !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 28px 20px !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #F0EEF8 !important;
}

/* ── FORM — removes default Streamlit border ── */
[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* ── INPUT ── */
.stTextInput > div > div > input,
[data-testid="stTextInput"] input {
    background-color: #141414 !important;
    border: 1px solid #2A2040 !important;
    border-radius: 10px !important;
    color: #F0EEF8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 13px 18px !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: #3D3550 !important;
}

.stTextInput label { display: none !important; }

/* ── BUTTONS ── */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background-color: #7C3AED !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    padding: 13px 24px !important;
    width: 100% !important;
    transition: background-color 0.2s ease, transform 0.15s ease !important;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #6D28D9 !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}

.stButton > button p,
[data-testid="stFormSubmitButton"] > button p {
    color: #ffffff !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background-color: #111111 !important;
    border: 1px solid #1C1C2E !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #7C3AED !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stExpander"] svg { fill: #7C3AED !important; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #7C3AED !important; }

/* ── DIVIDER ── */
.arise-divider {
    border: none;
    border-top: 1px solid #1C1C2E;
    margin: 20px 0;
}

/* ── SECTION LABEL (matches portfolio style) ── */
.section-label {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7C3AED !important;
    margin-bottom: 4px !important;
}

/* ── APP HEADER ── */
.app-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #F0EEF8 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
}

.app-title span {
    color: #7C3AED !important;
}

.app-tagline {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 300 !important;
    color: #4A4060 !important;
    margin-top: 4px !important;
}

/* ── CHAT MESSAGES ── */
.msg-wrapper {
    margin-bottom: 28px;
    animation: fadeUp 0.25s ease forwards;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-role {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #3D3550 !important;
    margin-bottom: 7px !important;
}

.msg-role-tutor { color: #7C3AED !important; }

.msg-bubble-student {
    font-size: 14px;
    line-height: 1.7;
    color: #C8C2E0 !important;
    padding: 14px 18px;
    background: #141414;
    border-radius: 12px;
    border: 1px solid #1C1C2E;
    margin-left: 24px;
}

.msg-bubble-tutor {
    font-size: 14px;
    line-height: 1.75;
    color: #F0EEF8 !important;
    padding: 16px 20px;
    background: #111118;
    border-radius: 12px;
    border: 1px solid #2A2040;
    border-left: 3px solid #7C3AED;
}

/* ── BADGES ── */
.badge-row {
    display: flex;
    gap: 7px;
    margin-top: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.badge {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    padding: 3px 10px !important;
    border-radius: 6px !important;
    border: 1px solid !important;
    display: inline-block !important;
}

.badge-verified {
    color: #A78BFA !important;
    background: rgba(124, 58, 237, 0.1) !important;
    border-color: rgba(124, 58, 237, 0.3) !important;
}

.badge-unverified {
    color: #F59E0B !important;
    background: rgba(245, 158, 11, 0.08) !important;
    border-color: rgba(245, 158, 11, 0.25) !important;
}

.badge-topic {
    color: #6D5DAB !important;
    background: rgba(124, 58, 237, 0.06) !important;
    border-color: #2A2040 !important;
}

/* ── SIDEBAR ELEMENTS ── */
.sidebar-logo {
    font-family: 'Syne', sans-serif !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    color: #F0EEF8 !important;
    letter-spacing: -0.01em !important;
}

.sidebar-logo span { color: #7C3AED !important; }

.sidebar-sub {
    font-size: 11px !important;
    color: #3D3550 !important;
    font-weight: 300 !important;
}

.sidebar-section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7C3AED !important;
    margin-top: 22px !important;
    margin-bottom: 10px !important;
    padding-bottom: 6px !important;
    border-bottom: 1px solid #1C1C2E !important;
}

.topic-chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 6px;
    background: #141414;
    border: 1px solid #1C1C2E;
    color: #3D3550 !important;
    margin: 2px 2px 2px 0;
    transition: all 0.15s ease;
}

.topic-chip-active {
    background: rgba(124, 58, 237, 0.12) !important;
    border-color: rgba(124, 58, 237, 0.35) !important;
    color: #A78BFA !important;
}

.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #7C3AED;
    margin-right: 7px;
    vertical-align: middle;
    animation: pulse 2.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(124,58,237,0.4); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 5px rgba(124,58,237,0); }
}

.status-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: #3D3550 !important;
    vertical-align: middle;
}

/* ── TRACE PANEL ── */
.trace-container {
    background: #0A0A0A;
    border: 1px solid #1C1C2E;
    border-radius: 10px;
    padding: 14px;
}

.trace-header-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #7C3AED !important;
    margin-bottom: 10px !important;
    display: flex;
    align-items: center;
    gap: 6px;
}

.trace-rule-block {
    border: 1px solid #1C1C2E;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    background: #0D0D0D;
    border-left: 2px solid #7C3AED;
}

.trace-rule-id {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: #A78BFA !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

.trace-rule-category {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-bottom: 6px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    background: rgba(124,58,237,0.1) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    color: #A78BFA !important;
}

.trace-rule-desc {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: #4A4060 !important;
    line-height: 1.6 !important;
    word-break: break-word !important;
}

.trace-empty {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: #1C1C2E !important;
    text-align: center !important;
    padding: 24px 0 !important;
}

/* ── WELCOME ── */
.welcome-container {
    text-align: center;
    padding: 70px 20px 40px;
}

.welcome-label {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7C3AED !important;
    margin-bottom: 12px !important;
}

.welcome-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #F0EEF8 !important;
    margin-bottom: 12px !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}

.welcome-sub {
    font-size: 14px !important;
    color: #4A4060 !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    max-width: 460px !important;
    margin: 0 auto 28px !important;
}

.welcome-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 6px;
    background: #141414;
    border: 1px solid #1C1C2E;
    color: #3D3550 !important;
}

.welcome-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 520px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_expert_facts" not in st.session_state:
    st.session_state.last_expert_facts = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if "last_grounded" not in st.session_state:
    st.session_state.last_grounded = False

if "input_key" not in st.session_state:
    st.session_state.input_key = 0


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">◈ ARISE <span>Tutor</span></div>
    <div class="sidebar-sub">Hybrid Expert-LLM · CS Education</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    st.markdown("""
    <span class="status-dot"></span>
    <span class="status-text">Expert Engine Active</span>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Supported Topics</div>',
                unsafe_allow_html=True)

    topic_html = '<div style="line-height:2.4;">'
    for topic in SUPPORTED_TOPICS:
        label = topic.replace("_", " ").title()
        is_active = topic == st.session_state.last_topic
        css_class = "topic-chip topic-chip-active" if is_active else "topic-chip"
        topic_html += f'<span class="{css_class}">{label}</span>'
    topic_html += '</div>'
    st.markdown(topic_html, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Expert System Trace</div>',
                unsafe_allow_html=True)

    with st.expander("▸ View fired rules", expanded=False):
        if st.session_state.last_expert_facts:
            topic_display = (st.session_state.last_topic or "").replace("_", " ").upper()
            st.markdown(f"""
            <div class="trace-container">
                <div class="trace-header-text">● Rules fired — {topic_display}</div>
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

    if st.button("↺  Clear Conversation"):
        st.session_state.messages = []
        st.session_state.last_expert_facts = []
        st.session_state.last_topic = None
        st.session_state.last_grounded = False
        st.session_state.input_key += 1
        st.rerun()

    st.markdown("""
    <div style="margin-top:28px; font-family:'JetBrains Mono',monospace;
                font-size:9px; color:#1C1C2E; line-height:2;">
        Arise Steven Samuel<br/>
        Landmark University · CS Dept<br/>
        Final Year Project · 2025
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN AREA
# =============================================================================

# Header
st.markdown("""
<div style="margin-bottom: 28px;">
    <div class="section-label">Neuro-Symbolic AI · CS Education</div>
    <div class="app-title">ARISE <span>Tutor</span></div>
    <div class="app-tagline">Python Programming, Data Structures, Algorithms & More · Verified by Expert System</div>
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
        <div class="welcome-label">Ask · Learn · Verify</div>
        <div class="welcome-title">What can I help<br/>you learn today?</div>
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
        
    if grounded is True:
     badge_verified = '<span class="badge badge-verified">✓ Verified by Expert System</span>'
    elif grounded is False:
     badge_verified = '<span class="badge badge-unverified">⚠ Unverified — cross-check advised</span>'
    else:
     badge_verified = ""  # No badge for casual interactions
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

# =============================================================================
# INPUT FORM
# =============================================================================

st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

with st.form(key=f"query_form_{st.session_state.input_key}", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            label="query",
            placeholder="Ask about Python, Data Structures, OOP...",
            label_visibility="collapsed",
        )
    with col2:
        send = st.form_submit_button("Ask →")

# =============================================================================
# QUERY HANDLING
# =============================================================================

if send and user_input.strip():
    st.session_state.pending_query = user_input.strip()
    st.session_state.input_key += 1
    st.rerun()

if st.session_state.get("pending_query"):
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    # Append student message
    st.session_state.messages.append({
        "role": "student",
        "content": query,
    })

    with st.spinner(""):
        if query is not None:
            result = get_tutor_response(query)
        else:
            result = {"error": "Query is empty", "response": "", "grounded": False, "topic": "unknown", "expert_facts": []}

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