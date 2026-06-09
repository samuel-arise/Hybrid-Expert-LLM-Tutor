"""
app.py
======
User Interface Layer — Streamlit Frontend
Hybrid Expert-LLM Tutor for Accurate Self-Learning Support in Computer Science
Author: Arise Steven Samuel

Features:
    - Dark / Light theme toggle in sidebar
    - Enter-to-submit via st.form
    - Input clears after submission via input_key counter
    - No duplicate messages via pending_query pattern
    - Casual greeting detection — no badge on non-CS queries
"""

import compat  # must be first — patches collections for Python 3.10+
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
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# =============================================================================
# THEME VARIABLES
# =============================================================================

D = st.session_state.dark_mode

# Colours
BG          = "#0D0D0D"       if D else "#FFFFFF"
BG2         = "#0A0A0A"       if D else "#F5F5F5"
SURFACE     = "#141414"       if D else "#FFFFFF"
SURFACE2    = "#1A1A1A"       if D else "#F9F9F9"
BORDER      = "#2A2040"       if D else "#E0D9F5"
BORDER2     = "#1C1C2E"       if D else "#E5E0F0"
TEXT        = "#F0EEF8"       if D else "#1E1B4B"
TEXT2       = "#4A4060"       if D else "#6D5DAB"
TEXT3       = "#3D3550"       if D else "#9CA3AF"
ACCENT      = "#7C3AED"
ACCENT_LITE = "rgba(124,58,237,0.12)" if D else "rgba(124,58,237,0.08)"
ACCENT_BDR  = "rgba(124,58,237,0.35)" if D else "rgba(124,58,237,0.25)"
BTN_TEXT    = "#FFFFFF"       if D else "#FFFFFF"
MSG_STUDENT_BG  = "#141414"   if D else "#F3F0FF"
MSG_STUDENT_BDR = "#1C1C2E"   if D else "#DDD6FE"
MSG_STUDENT_TXT = "#C8C2E0"   if D else "#3730A3"
MSG_TUTOR_BG    = "#111118"   if D else "#FAFAFE"
MSG_TUTOR_BDR   = "#2A2040"   if D else "#DDD6FE"
INPUT_BG    = "#141414"       if D else "#F9F8FF"
INPUT_BDR   = "#2A2040"       if D else "#C4B5FD"
CHIP_BG     = "#141414"       if D else "#F3F0FF"
CHIP_BDR    = "#1C1C2E"       if D else "#DDD6FE"
CHIP_TXT    = "#3D3550"       if D else "#7C3AED"
TRACE_BG    = "#0A0A0A"       if D else "#F9F8FF"
EXPANDER_BG = "#111111"       if D else "#F9F8FF"
SIDEBAR_BG  = "#0A0A0A"       if D else "#F5F3FF"
SIDEBAR_BDR = "#1C1C2E"       if D else "#E0D9F5"
WELCOME_SUB = "#4A4060"       if D else "#6D5DAB"

# =============================================================================
# CUSTOM CSS — injected dynamically based on theme
# =============================================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

html, body,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main, .stApp {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
}}

p, span, div, label, li, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"] {{
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.block-container {{
    padding-top: 40px !important;
    padding-bottom: 60px !important;
    max-width: 780px !important;
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {{
    background-color: {SIDEBAR_BG} !important;
    border-right: 1px solid {SIDEBAR_BDR} !important;
}}

[data-testid="stSidebar"] .block-container {{
    padding: 28px 20px !important;
    max-width: 100% !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {{
    color: {TEXT} !important;
}}

/* ── FORM ── */
[data-testid="stForm"] {{
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}}

/* ── INPUT ── */
.stTextInput > div > div > input,
[data-testid="stTextInput"] input {{
    background-color: {INPUT_BG} !important;
    border: 1px solid {INPUT_BDR} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 13px 18px !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
    outline: none !important;
}}

.stTextInput > div > div > input::placeholder {{
    color: {TEXT3} !important;
}}

.stTextInput label {{ display: none !important; }}

/* ── BUTTONS ── */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {{
    background-color: {ACCENT} !important;
    color: {BTN_TEXT} !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    padding: 13px 24px !important;
    width: 100% !important;
    transition: opacity 0.2s ease !important;
}}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {{
    opacity: 0.88 !important;
    color: {BTN_TEXT} !important;
}}

.stButton > button p,
[data-testid="stFormSubmitButton"] > button p {{
    color: {BTN_TEXT} !important;
}}

/* ── TOGGLE BUTTON (theme switch) ── */
.stCheckbox label {{
    color: {TEXT} !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}}

/* ── EXPANDER ── */
[data-testid="stExpander"] {{
    background-color: {EXPANDER_BG} !important;
    border: 1px solid {BORDER2} !important;
    border-radius: 10px !important;
}}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {{
    color: {ACCENT} !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

[data-testid="stExpander"] svg {{ fill: {ACCENT} !important; }}

.stSpinner > div {{ border-top-color: {ACCENT} !important; }}

/* ── DIVIDER ── */
.arise-divider {{
    border: none;
    border-top: 1px solid {BORDER2};
    margin: 20px 0;
}}

/* ── SECTION LABEL ── */
.section-label {{
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: {ACCENT} !important;
    margin-bottom: 4px !important;
}}

/* ── APP HEADER ── */
.app-title {{
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
}}

.app-title span {{ color: {ACCENT} !important; }}

.app-tagline {{
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 300 !important;
    color: {TEXT2} !important;
    margin-top: 4px !important;
}}

/* ── CHAT MESSAGES ── */
.msg-wrapper {{
    margin-bottom: 28px;
    animation: fadeUp 0.25s ease forwards;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.msg-role {{
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: {TEXT3} !important;
    margin-bottom: 7px !important;
}}

.msg-role-tutor {{ color: {ACCENT} !important; }}

.msg-bubble-student {{
    font-size: 14px;
    line-height: 1.7;
    color: {MSG_STUDENT_TXT} !important;
    padding: 14px 18px;
    background: {MSG_STUDENT_BG};
    border-radius: 12px;
    border: 1px solid {MSG_STUDENT_BDR};
    margin-left: 24px;
}}

.msg-bubble-tutor {{
    font-size: 14px;
    line-height: 1.75;
    color: {TEXT} !important;
    padding: 16px 20px;
    background: {MSG_TUTOR_BG};
    border-radius: 12px;
    border: 1px solid {MSG_TUTOR_BDR};
    border-left: 3px solid {ACCENT};
}}

/* ── BADGES ── */
.badge-row {{
    display: flex;
    gap: 7px;
    margin-top: 10px;
    flex-wrap: wrap;
    align-items: center;
}}

.badge {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    padding: 3px 10px !important;
    border-radius: 6px !important;
    border: 1px solid !important;
    display: inline-block !important;
}}

.badge-verified {{
    color: {ACCENT} !important;
    background: {ACCENT_LITE} !important;
    border-color: {ACCENT_BDR} !important;
}}

.badge-unverified {{
    color: #D97706 !important;
    background: rgba(245,158,11,0.08) !important;
    border-color: rgba(245,158,11,0.3) !important;
}}

.badge-topic {{
    color: {TEXT2} !important;
    background: {ACCENT_LITE} !important;
    border-color: {BORDER} !important;
}}

/* ── SIDEBAR ELEMENTS ── */
.sidebar-logo {{
    font-family: 'Syne', sans-serif !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    letter-spacing: -0.01em !important;
}}

.sidebar-logo span {{ color: {ACCENT} !important; }}

.sidebar-sub {{
    font-size: 11px !important;
    color: {TEXT3} !important;
    font-weight: 300 !important;
}}

.sidebar-section-title {{
    font-family: 'Syne', sans-serif !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: {ACCENT} !important;
    margin-top: 22px !important;
    margin-bottom: 10px !important;
    padding-bottom: 6px !important;
    border-bottom: 1px solid {BORDER2} !important;
}}

.topic-chip {{
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 6px;
    background: {CHIP_BG};
    border: 1px solid {CHIP_BDR};
    color: {CHIP_TXT} !important;
    margin: 2px 2px 2px 0;
}}

.topic-chip-active {{
    background: {ACCENT_LITE} !important;
    border-color: {ACCENT_BDR} !important;
    color: {ACCENT} !important;
}}

.status-dot {{
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {ACCENT};
    margin-right: 7px;
    vertical-align: middle;
    animation: pulse 2.5s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(124,58,237,0.4); }}
    50%       {{ opacity: 0.7; box-shadow: 0 0 0 5px rgba(124,58,237,0); }}
}}

.status-text {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: {TEXT3} !important;
    vertical-align: middle;
}}

/* ── TRACE PANEL ── */
.trace-container {{
    background: {TRACE_BG};
    border: 1px solid {BORDER2};
    border-radius: 10px;
    padding: 14px;
}}

.trace-header-text {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: {ACCENT} !important;
    margin-bottom: 10px !important;
}}

.trace-rule-block {{
    border: 1px solid {BORDER2};
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    background: {BG};
    border-left: 2px solid {ACCENT};
}}

.trace-rule-id {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: {ACCENT} !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}}

.trace-rule-category {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    display: inline-block !important;
    margin-bottom: 6px !important;
    text-transform: uppercase !important;
    background: {ACCENT_LITE} !important;
    border: 1px solid {ACCENT_BDR} !important;
    color: {ACCENT} !important;
}}

.trace-rule-desc {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: {TEXT2} !important;
    line-height: 1.6 !important;
    word-break: break-word !important;
}}

.trace-empty {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: {TEXT3} !important;
    text-align: center !important;
    padding: 24px 0 !important;
}}

/* ── WELCOME ── */
.welcome-container {{
    text-align: center;
    padding: 70px 20px 40px;
}}

.welcome-label {{
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: {ACCENT} !important;
    margin-bottom: 12px !important;
}}

.welcome-title {{
    font-family: 'Syne', sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    margin-bottom: 12px !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}}

.welcome-sub {{
    font-size: 14px !important;
    color: {WELCOME_SUB} !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    max-width: 460px !important;
    margin: 0 auto 28px !important;
}}

.welcome-chip {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 6px;
    background: {CHIP_BG};
    border: 1px solid {CHIP_BDR};
    color: {CHIP_TXT} !important;
}}

.welcome-chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 520px;
    margin: 0 auto;
}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.markdown(f"""
    <div class="sidebar-logo">◈ ARISE <span>Tutor</span></div>
    <div class="sidebar-sub">Hybrid Expert-LLM · CS Education</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="arise-divider">', unsafe_allow_html=True)

    # ── THEME TOGGLE ──────────────────────────────────────────────────────────
    col_moon, col_toggle = st.columns([1, 3])
    with col_moon:
        st.markdown(
            f"<div style='font-size:18px; padding-top:6px;'>{'🌙' if D else '☀️'}</div>",
            unsafe_allow_html=True
        )
    with col_toggle:
        new_mode = st.toggle(
            "Dark Mode" if D else "Light Mode",
            value=st.session_state.dark_mode,
            key="theme_toggle"
        )
        if new_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = new_mode
            st.rerun()

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
        is_active = (topic == st.session_state.last_topic)
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
            st.markdown(f"""
            <div class="trace-container">
                <div class="trace-empty">No rules fired yet.<br/>Ask a question to begin.</div>
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

    st.markdown(f"""
    <div style="margin-top:28px; font-family:'JetBrains Mono',monospace;
                font-size:9px; color:{'#1C1C2E' if D else '#C4B5FD'}; line-height:2;">
        Arise Steven Samuel<br/>
        Landmark University · CS Dept<br/>
        Final Year Project · 2025
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN AREA
# =============================================================================

st.markdown(f"""
<div style="margin-bottom: 28px;">
    <div class="section-label">Neuro-Symbolic AI · CS Education</div>
    <div class="app-title">ARISE <span>Tutor</span></div>
    <div class="app-tagline">Python · Data Structures · Algorithms · Automata Theory · Verified by Expert System</div>
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
            Ask any question about Python, Data Structures, Algorithms, or Automata Theory.
            Every answer is grounded in verified knowledge — not guesswork.
        </div>
        <div class="welcome-chip-row">{topics_chips}</div>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    role    = msg["role"]
    content = msg["content"]
    grounded = msg.get("grounded", False)
    topic   = msg.get("topic", None)

    if role == "student":
        st.markdown(f"""
        <div class="msg-wrapper">
            <div class="msg-role">You</div>
            <div class="msg-bubble-student">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if grounded is True:
            badge_verified = '<span class="badge badge-verified">✓ Verified by Expert System</span>'
        elif grounded is False:
            badge_verified = '<span class="badge badge-unverified">⚠ Unverified — cross-check advised</span>'
        else:
            badge_verified = ""

        badge_topic = (
            f'<span class="badge badge-topic">{topic.replace("_", " ")}</span>'
            if topic and topic not in ("unknown", "casual") else ""
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
            placeholder="Ask about Python, Data Structures, Algorithms, Automata...",
            label_visibility="collapsed",
        )
    with col2:
        send = st.form_submit_button("Ask →")

# =============================================================================
# QUERY HANDLING — pending_query pattern prevents duplicate messages
# =============================================================================

if send and user_input.strip():
    st.session_state.pending_query = user_input.strip()
    st.session_state.input_key += 1
    st.rerun()

if st.session_state.get("pending_query"):
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    st.session_state.messages.append({
        "role": "student",
        "content": query,
    })

    with st.spinner(""):
        result = get_tutor_response(query) # type: ignore

    if result["error"]:
        response_text = f"An error occurred: {result['error']}"
        grounded = False
        topic = "unknown"
        facts = []
    else:
        response_text = result["response"]
        grounded      = result["grounded"]
        topic         = result["topic"]
        facts         = result["expert_facts"]

    st.session_state.messages.append({
        "role": "tutor",
        "content": response_text,
        "grounded": grounded,
        "topic": topic,
    })

    st.session_state.last_expert_facts = facts
    st.session_state.last_topic        = topic
    st.session_state.last_grounded     = grounded

    st.rerun()