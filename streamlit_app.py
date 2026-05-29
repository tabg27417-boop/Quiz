import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from google import genai

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuizVai AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

  :root {
    --bg:       #0b0f1a;
    --surface:  #131929;
    --border:   #1e2d45;
    --accent:   #38bdf8;
    --accent2:  #818cf8;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --success:  #34d399;
    --error:    #f87171;
  }

  /* ── Base ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
  }

  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse 70% 50% at 20% 10%, rgba(56,189,248,.07) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 80% 90%, rgba(129,140,248,.07) 0%, transparent 60%),
      var(--bg) !important;
  }

  /* ── Hero header ── */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
  }
  .hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(129,140,248,.15));
    border: 1px solid rgba(56,189,248,.3);
    color: var(--accent);
    font-family: 'Syne', sans-serif;
    font-size: .72rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    padding: .3rem .9rem;
    border-radius: 99px;
    margin-bottom: 1.2rem;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #e2e8f0 30%, var(--accent) 70%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }
  .hero-sub {
    color: var(--muted);
    font-size: .85rem;
    margin-top: .7rem;
    letter-spacing: .04em;
  }

  /* ── Card ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .6;
  }
  .card-label {
    font-size: .65rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent);
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    margin-bottom: .5rem;
  }

  /* ── Question box ── */
  .question-box {
    background: linear-gradient(135deg, rgba(56,189,248,.06), rgba(129,140,248,.06));
    border: 1px solid rgba(56,189,248,.2);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 1.2rem 0;
  }
  .question-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1.55;
    margin: 0;
  }
  .q-num {
    font-family: 'Syne', sans-serif;
    font-size: .7rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--accent2);
    margin-bottom: .5rem;
  }

  /* ── Answer box ── */
  .answer-box {
    background: rgba(52,211,153,.04);
    border: 1px solid rgba(52,211,153,.18);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
  }
  .answer-header {
    display: flex;
    align-items: center;
    gap: .5rem;
    font-size: .65rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--success);
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    margin-bottom: .8rem;
  }
  .answer-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.4; transform:scale(.7); }
  }

  /* ── Source badge ── */
  .source-badge {
    display: inline-block;
    font-size: .62rem;
    padding: .2rem .6rem;
    border-radius: 6px;
    font-family: 'Syne', sans-serif;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: .6rem;
  }
  .source-gemini {
    background: rgba(56,189,248,.12);
    border: 1px solid rgba(56,189,248,.25);
    color: var(--accent);
  }
  .source-openrouter {
    background: rgba(129,140,248,.12);
    border: 1px solid rgba(129,140,248,.25);
    color: var(--accent2);
  }

  /* ── Error box ── */
  .error-box {
    background: rgba(248,113,113,.05);
    border: 1px solid rgba(248,113,113,.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: var(--error);
    font-size: .82rem;
  }

  /* ── Divider ── */
  .hl { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

  /* ── Streamlit widget overrides ── */
  [data-testid="stSelectbox"] label,
  [data-testid="stNumberInput"] label {
    font-family: 'Syne', sans-serif !important;
    font-size: .7rem !important;
    letter-spacing: .15em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
  }

  div[data-baseweb="select"] > div,
  div[data-baseweb="input"] > div > input {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
  }

  div[data-baseweb="select"] > div:focus-within,
  div[data-baseweb="input"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.12) !important;
  }

  [data-testid="baseButton-primary"],
  [data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0b0f1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .82rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    padding: .6rem 2rem !important;
    width: 100% !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 20px rgba(56,189,248,.2) !important;
  }
  [data-testid="stButton"] > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
  }

  [data-testid="stSpinner"] {
    color: var(--accent) !important;
  }

  /* hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; max-width: 720px !important; }
</style>
""", unsafe_allow_html=True)


# ─── Firebase Init ───────────────────────────────────────────────────────────────
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()


# ─── Load Quiz List ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_quizzes():
    quizzes = db.collection("quizzes").stream()
    subjects, titles = [], []
    for q in quizzes:
        data = q.to_dict()
        subjects.append(data.get("subject", "Unknown"))
        titles.append(data.get("title", "Untitled"))
    return subjects, titles

arr_sub, arr_title = load_quizzes()


# ─── Helper: call AI models ──────────────────────────────────────────────────────
def ask_gemini(question: str) -> str:
    """Returns answer_text. Raises on failure."""
    GEMINI_API=st.secrets("GEMINI_API")
    client = genai.Client(api_key=GEMINI_API)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"**QuizVai**:{question}",
        config={"system_instruction": "You are QuizVai AI, an expert quiz helper. Give clear, concise, and accurate answers.Give detail explanation"},
    )
    return response.text


def ask_openrouter(question: str, model: str) -> str:
    """Returns answer_text. Raises on failure."""
    api = st.secrets("OPEN_ROU")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "You are QuizVai AI, an expert quiz helper. Never reveal your underlying model name. Always identify yourself as QuizVai AI.Give detail explanation"},
                {"role": "user", "content": question},
            ],
        }),
        timeout=30,
    )
    result = response.json()
    if "choices" not in result:
        raise ValueError(f"No choices in response: {result}")
    return result["choices"][0]["message"]["content"]


def get_answer(question: str) -> str:
    """Try models in order. Returns answer text."""
    # 1. Gemini
    try:
        return ask_gemini(question)
    except Exception:
        pass

    # 2. OpenRouter primary
    try:
        return ask_openrouter(question, "openrouter/owl-alpha")
    except Exception:
        pass

    #3. openrouter
    try:
        return ask_openrouter(question, "liquid/lfm-2.5-1.2b-instruct:free")
    except Exception:
        pass
    #4 openrouter
    try:
        return ask_openrouter(question, "poolside/laguna-m.1:free")
    except Exception:
        pass

    # 5. OpenRouter fallback
    try:
        return ask_openrouter(question, "poolside/laguna-xs.2:free")
    except Exception as e:
        raise RuntimeError("QuizVai AI models are currently unavailable. Please try again later.") from e


# ─── UI ──────────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ AI-Powered Learning</div>
  <h1 class="hero-title">QuizVai AI</h1>
  <p class="hero-sub">Select a subject, pick a question number, and get instant AI explanations</p>
</div>
""", unsafe_allow_html=True)

# Selection card
st.markdown('<div class="card"><div class="card-label">📚 Quiz Selection</div>', unsafe_allow_html=True)

if not arr_sub:
    st.error("⚠️ No quizzes found in the database.")
    st.stop()

quiz_sub = st.selectbox("Subject", arr_sub, key="subject_select")
index_sub = arr_sub.index(quiz_sub)
quiz_title = arr_title[index_sub]

st.markdown(f'<p style="font-size:.72rem;color:#64748b;margin-top:-.3rem;margin-bottom:.8rem;">📖 Topic: <span style="color:#e2e8f0">{quiz_title}</span></p>', unsafe_allow_html=True)

num = st.number_input("Question Number", min_value=1, step=1, value=1, key="q_num")

st.markdown("</div>", unsafe_allow_html=True)

# Submit button
submitted = st.button("🔍 Get Answer", key="submit_btn")

# Answer section
if submitted:
    docs = db.collection("quizzes").where("subject", "==", quiz_sub).where("title", "==", quiz_title).get()

    if not docs:
        st.markdown('<div class="error-box">⚠️ Quiz not found in the database.</div>', unsafe_allow_html=True)
        st.stop()

    quiz = docs[0].to_dict()
    questions = quiz.get("questions", [])

    if num < 1 or num > len(questions):
        st.markdown(f'<div class="error-box">⚠️ Question {num} does not exist. This quiz has {len(questions)} question(s).</div>', unsafe_allow_html=True)
        st.stop()

    question_text = questions[int(num) - 1]["text"]

    # Display question
    st.markdown(f"""
    <div class="question-box">
      <div class="q-num">Question {num} of {len(questions)}</div>
      <p class="question-text">{question_text}</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch answer
    with st.spinner("Thinking…"):
        try:
            answer = get_answer(question_text)
            st.markdown(f"""
            <div class="answer-box">
              <div class="answer-header">
                <span class="answer-dot"></span>
                AI Answer
              </div>
              <span class="source-badge source-gemini">&#129504; QuizVai AI</span>
              <div style="font-size:.88rem;line-height:1.75;color:#cbd5e1;">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
        except RuntimeError as e:
            st.markdown(f'<div class="error-box">❌ {e}</div>', unsafe_allow_html=True)
