import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="UniMate AI • Mubashar Khan project",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

LANGUAGES = {
    "English": "English",
    "اردو": "Urdu",
    "Roman Urdu": "Roman Urdu",
}

MODES = {
    "🎓 Study Mode": "study",
    "🧠 Quiz Mode": "quiz",
    "📝 Assignment Mode": "assignment",
}

MODE_PROMPTS = {
    "study": """You are UniMate AI, a university study assistant.
Explain academic concepts clearly and step-by-step. Use simple examples.
If the user asks in Urdu or Roman Urdu, answer in the same language.
Do not invent university-specific policies or facts.""",
    "quiz": """You are UniMate AI in Quiz Mode.
Create useful university-level practice questions from the user's topic.
Ask one question at a time unless the user explicitly asks for a full quiz.
Give explanations after the user answers.""",
    "assignment": """You are UniMate AI in Assignment Mode.
Help students understand topics, brainstorm ideas, create outlines,
improve drafts, and plan assignments. Do not claim to have personal
university requirements unless the user provides them.""",
}

def init_state():
    if "chats" not in st.session_state:
        st.session_state.chats = [{"title": "New Chat", "messages": []}]
        st.session_state.active_chat = 0
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "mode" not in st.session_state:
        st.session_state.mode = "🎓 Study Mode"

def new_chat():
    st.session_state.chats.append({"title": "New Chat", "messages": []})
    st.session_state.active_chat = len(st.session_state.chats) - 1

def clear_current_chat():
    st.session_state.chats[st.session_state.active_chat]["messages"] = []
    st.session_state.chats[st.session_state.active_chat]["title"] = "New Chat"

def ask_ollama(messages, language, mode):
    system = MODE_PROMPTS[MODES[mode]]
    system += f"\nPreferred response language: {LANGUAGES[language]}."
    system += "\nThe interface belongs to an HMRA University student project called UniMate AI."
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [{"role": "system", "content": system}] + messages,
        "options": {"temperature": 0.6},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content", "").strip() or "I couldn't generate a response."
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama is not running. Please start Ollama and make sure `llama3.2:3b` is installed."
    except requests.exceptions.Timeout:
        return "⚠️ The local AI took too long to respond. Please try a shorter question."
    except Exception as e:
        return f"⚠️ AI connection error: {e}"

init_state()

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: Inter, sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7ff 0%, #eef8ff 55%, #f4fffb 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111936 0%, #1c2860 100%);
}

[data-testid="stSidebar"] * { color: #f4f7ff !important; }

.hero {
    padding: 28px 32px;
    border-radius: 28px;
    color: white;
    background: linear-gradient(120deg, #25256f, #087f8c);
    box-shadow: 0 18px 45px rgba(28, 43, 100, .18);
    margin-bottom: 20px;
}

.hero-badge {
    display:inline-block;
    padding:7px 13px;
    border-radius:999px;
    background:rgba(255,255,255,.14);
    border:1px solid rgba(255,255,255,.25);
    font-size:12px;
    font-weight:700;
    letter-spacing:.4px;
}

.hero h1 { margin: 12px 0 4px 0; font-size: 42px; }
.hero p { margin:0; opacity:.9; }

.card {
    background: rgba(255,255,255,.9);
    border: 1px solid rgba(100,120,180,.12);
    border-radius: 18px;
    padding: 17px;
    box-shadow: 0 8px 24px rgba(32,49,100,.06);
}

.small-muted { color:#6d7895; font-size:13px; }

.chat-title {
    font-size: 26px;
    font-weight: 800;
    color:#17235b;
    margin-top: 5px;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(120,130,180,.18);
    font-weight: 600;
}

div[data-testid="stChatMessage"] {
    border-radius: 16px;
}

.mode-pill {
    padding: 8px 12px;
    border-radius: 10px;
    background: #eef2ff;
    color: #303d88;
    font-size: 13px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🎓 UniMate AI")
    st.caption("Local AI Assistant")
    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        clear_current_chat()
        st.rerun()

    st.markdown("### 🌐 Language")
    st.session_state.language = st.selectbox(
        "Response language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        label_visibility="collapsed",
    )

    st.markdown("### 🎯 AI Mode")
    st.session_state.mode = st.radio(
        "Choose mode",
        list(MODES.keys()),
        index=list(MODES.keys()).index(st.session_state.mode),
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 💬 Chat History")

    for i, chat in enumerate(st.session_state.chats):
        title = chat["title"]
        if title == "New Chat" and chat["messages"]:
            first = next((m["content"] for m in chat["messages"] if m["role"] == "user"), "")
            title = (first[:25] + "...") if len(first) > 25 else (first or "New Chat")
        if st.button(f"{'● ' if i == st.session_state.active_chat else ''}{title}",
                     key=f"chat_{i}", use_container_width=True):
            st.session_state.active_chat = i
            st.rerun()

    st.divider()
    st.markdown("**AI Engine**")
    st.success("Local AI Ready")
    st.caption(f"Model: {MODEL}")
    st.caption("Backend: Ollama • Local")
    st.caption("API key: Not required")

# ---------- Main ----------
chat = st.session_state.chats[st.session_state.active_chat]

st.markdown("""
<div class="hero">
  <span class="hero-badge">🎓 MUBASHAR KHAN PROJECT</span>
  <h1>UniMate AI</h1>
  <p>Your intelligent university study companion — powered by a local AI model.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="card"><div class="small-muted">AI STATUS</div><h3>🟢 Local</h3></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><div class="small-muted">MODEL</div><h3>Llama 3.2</h3></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><div class="small-muted">API KEY</div><h3>Not Required</h3></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="card"><div class="small-muted">MODE</div><h3>{st.session_state.mode}</h3></div>', unsafe_allow_html=True)

st.markdown(f'<div class="chat-title">💬 AI Conversation</div><div class="small-muted">Language: {st.session_state.language} &nbsp; • &nbsp; Mode: {st.session_state.mode}</div>', unsafe_allow_html=True)
st.write("")

if not chat["messages"]:
    st.info("👋 Assalam-o-Alaikum! I'm UniMate AI. Ask me anything about your studies, coding, assignments, or university learning.")

for message in chat["messages"]:
    with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else "🧑‍🎓"):
        st.markdown(message["content"])

prompt = st.chat_input("Ask UniMate anything...")

if prompt:
    chat["messages"].append({"role": "user", "content": prompt})
    if chat["title"] == "New Chat":
        chat["title"] = prompt[:35] + ("..." if len(prompt) > 35 else "")

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("UniMate is thinking..."):
            answer = ask_ollama(chat["messages"], st.session_state.language, st.session_state.mode)
        st.markdown(answer)

    chat["messages"].append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown("---")
st.caption("🎓 UniMate AI  ")
