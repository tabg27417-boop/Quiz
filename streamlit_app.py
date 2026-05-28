import streamlit as st
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuizVai – AI Doubt Solver",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0A0A0F !important;
    color: #E8E4D9 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #1a1040 0%, #0A0A0F 60%) !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── Block container ── */
.block-container {
    max-width: 860px !important;
    padding: 0 24px 80px 24px !important;
    margin: 0 auto !important;
}

/* ── Hero Header ── */
.hero-wrap {
    text-align: center;
    padding: 64px 0 40px;
    position: relative;
}

.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8B5CF6;
    border: 1px solid #8B5CF633;
    background: #8B5CF610;
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 24px;
}

.hero-title {
    font-size: clamp(48px, 8vw, 80px);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #E8E4D9 30%, #8B5CF6 70%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #8B5CF6;
    letter-spacing: 0.15em;
    margin-bottom: 20px;
}

.hero-desc {
    font-size: 17px;
    color: #9D9A92;
    max-width: 480px;
    margin: 0 auto 40px;
    line-height: 1.7;
    font-weight: 400;
}

/* ── Glowing divider ── */
.glow-line {
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #8B5CF6, #EC4899, transparent);
    margin: 0 auto 48px;
    border-radius: 2px;
}

/* ── Subject Chips ── */
.chips-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5a576e;
    margin-bottom: 14px;
}

.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 32px;
}

.chip {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    padding: 8px 18px;
    border-radius: 100px;
    border: 1px solid #2a2740;
    background: #12111a;
    color: #9D9A92;
    cursor: pointer;
    transition: all 0.2s;
}

.chip:hover, .chip.active {
    border-color: #8B5CF6;
    color: #c4b5fd;
    background: #1e1b2e;
}

/* ── Input Card ── */
.input-card {
    background: #12111a;
    border: 1px solid #1e1b2e;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #8B5CF660, transparent);
}

.input-card-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a576e;
    margin-bottom: 16px;
    font-family: 'Space Mono', monospace;
}

/* ── Streamlit overrides ── */
/* Text area */
.stTextArea textarea {
    background: #0d0c15 !important;
    border: 1px solid #2a2740 !important;
    border-radius: 12px !important;
    color: #E8E4D9 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    padding: 16px !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}

.stTextArea textarea:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 3px #8B5CF620 !important;
    outline: none !important;
}

.stTextArea label {
    color: #5a576e !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

/* Select box */
.stSelectbox > div > div {
    background: #0d0c15 !important;
    border: 1px solid #2a2740 !important;
    border-radius: 12px !important;
    color: #E8E4D9 !important;
    font-family: 'Syne', sans-serif !important;
}

.stSelectbox label {
    color: #5a576e !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7C3AED, #8B5CF6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6D28D9, #7C3AED) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px #8B5CF640 !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Answer card */
.answer-card {
    background: #12111a;
    border: 1px solid #1e1b2e;
    border-radius: 16px;
    padding: 32px;
    margin-top: 28px;
    position: relative;
    overflow: hidden;
    animation: fadeSlideIn 0.4s ease;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.answer-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7C3AED, #EC4899);
}

.answer-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8B5CF6;
    margin-bottom: 20px;
}

.answer-tag::before {
    content: '';
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #8B5CF6;
    box-shadow: 0 0 8px #8B5CF6;
    animation: pulse 2s ease infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.answer-body {
    font-size: 16px;
    line-height: 1.8;
    color: #C9C5BC;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 48px;
}

.stat-card {
    background: #12111a;
    border: 1px solid #1e1b2e;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #8B5CF6, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #5a576e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── History ── */
.history-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 18px;
    background: #0d0c15;
    border: 1px solid #1a1828;
    border-radius: 12px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: border-color 0.2s;
}

.history-item:hover { border-color: #2a2740; }

.history-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: #1e1b2e;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.history-text {
    font-size: 14px;
    color: #9D9A92;
    line-height: 1.5;
}

.history-meta {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #3d3a50;
    margin-top: 4px;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #8B5CF6 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #12111a !important;
    border: 1px solid #1e1b2e !important;
    border-radius: 12px !important;
    color: #9D9A92 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Columns gap ── */
[data-testid="column"] { padding: 0 8px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0A0A0F; }
::-webkit-scrollbar-thumb { background: #2a2740; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8B5CF6; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "answer" not in st.session_state:
    st.session_state.answer = None

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">⚡ Powered by AI</div>
    <div class="hero-title">QuizVai</div>
    <div class="hero-sub">AI Doubt Solver</div>
    <p class="hero-desc">
        Ask any academic doubt and get instant, precise answers.
        From mathematics to literature — we've got you covered.
    </p>
</div>
<div class="glow-line"></div>
""", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-number">50K+</div>
        <div class="stat-label">Doubts Solved</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">12</div>
        <div class="stat-label">Subjects</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">0.8s</div>
        <div class="stat-label">Avg Response</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Card ────────────────────────────────────────────────────────────────



question = st.text_area(
    "Your Question",
    placeholder="কোন কুইজে সমস্যা???",
    height=130,
    label_visibility="visible"
)


#quiz vai AI

import os
from dotenv import load_dotenv
from google.genai import types
from google import genai

load_dotenv()
GEMINI_API=os.getenv("GEMINI_API")

client = genai.Client(api_key=GEMINI_API)














st.markdown('</div>', unsafe_allow_html=True)

# ── Submit ────────────────────────────────────────────────────────────────────
if st.button("⚡ Solve My Doubt", use_container_width=True):
    if question.strip():
        with st.spinner("Thinking…"):
            import time
            time.sleep(1.2) # ← replace with real API call
            # ── Placeholder answer (swap with Claude API response) ──
            mock = (
                f"****\n\n"
                "Here is a detailed explanation for your question. "
                "This is a placeholder response demonstrating the QuizVai interface. "
                
            )
            st.session_state.answer = mock
            
            response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=
            "tomar nam quizvai AI and math,phy,chem expert give answer with explanation and step by step and maintain latex well"
            "always interpret 'm' as meters and 's' as seconds (meters per second), NOT as milliseconds. "
        "Always render physics equations strictly using standard LaTeX format (e.g., \\text{m/s} or \\text{m/s}^2) "
        "and show step-by-step calculations clearly."
            
            
        )
   
    )
        st.write(f"QuizVai(🤖):{response.text}")
    else:
        st.warning("Please type your question first.")

# ── Answer Card ───────────────────────────────────────────────────────────────
if st.session_state.answer:
    st.markdown('<div class="answer-card"><div class="answer-tag">AI Answer</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.answer)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Spacer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

# ── Recent History ────────────────────────────────────────────────────────────


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<br><br>
<div style="text-align:center; font-family:'Space Mono',monospace; font-size:11px;
            color:#2a2740; letter-spacing:0.12em; padding-bottom:40px;">
    QUIZVAI · AI DOUBT SOLVER · BUILT By ABIDUR RAHAMAN 
</div>
""", unsafe_allow_html=True)
