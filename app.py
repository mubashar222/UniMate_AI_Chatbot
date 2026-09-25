import os
import streamlit as st
from huggingface_hub import InferenceClient

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="UniMate AI • Mubashar Khan project",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# HUGGING FACE CONFIG
# =========================================================

HF_TOKEN = os.getenv("HF_TOKEN")

# Free/low-cost friendly model policy
MODEL = "openai/gpt-oss-20b:cheapest"

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
Explain academic concepts clearly and step-by-step.
Use simple examples where useful.
If the user asks in Urdu or Roman Urdu, answer in the same language.
Do not invent university-specific policies or facts.""",

    "quiz": """You are UniMate AI in Quiz Mode.
Create useful university-level practice questions from the user's topic.
Ask one question at a time unless the user explicitly asks for a full quiz.
Give explanations after the user answers.""",

    "assignment": """You are UniMate AI in Assignment Mode.
Help students understand topics, brainstorm ideas, create outlines,
improve drafts, and plan assignments.
Do not claim to know university requirements unless the user provides them.
Help the student learn rather than simply pretending to complete
academic work dishonestly."""
}


# =========================================================
# SESSION STATE
# =========================================================

def init_state():

    if "chats" not in st.session_state:
        st.session_state.chats = [
            {
                "title": "New Chat",
                "messages": []
            }
        ]
        st.session_state.active_chat = 0

    if "language" not in st.session_state:
        st.session_state.language = "English"

    if "mode" not in st.session_state:
        st.session_state.mode = "🎓 Study Mode"


def new_chat():

    st.session_state.chats.append(
        {
            "title": "New Chat",
            "messages": []
        }
    )

    st.session_state.active_chat = len(st.session_state.chats) - 1


def clear_current_chat():

    st.session_state.chats[
        st.session_state.active_chat
    ]["messages"] = []

    st.session_state.chats[
        st.session_state.active_chat
    ]["title"] = "New Chat"


# =========================================================
# AI FUNCTION
# =========================================================

def ask_huggingface(messages, language, mode):

    if not HF_TOKEN:
        return (
            "⚠️ HF_TOKEN is missing.\n\n"
            "Please add your Hugging Face token in "
            "Streamlit Cloud → Settings → Secrets."
        )

    system = MODE_PROMPTS[MODES[mode]]

    system += (
        f"\nPreferred response language: "
        f"{LANGUAGES[language]}."
    )

    system += (
        "\nThe interface belongs to an University "
        "student project called UniMate AI."
    )

    try:

        client = InferenceClient(
            api_key=HF_TOKEN
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system
                }
            ] + messages,
            temperature=0.6,
            max_tokens=700,
        )

        answer = response.choices[0].message.content

        if answer:
            return answer.strip()

        return "⚠️ I couldn't generate a response."

    except Exception as e:

        error = str(e)

        if "401" in error or "Unauthorized" in error:
            return (
                "⚠️ Hugging Face token is invalid or "
                "does not have Inference permission."
            )

        if "429" in error:
            return (
                "⚠️ The AI provider is temporarily rate-limited. "
                "Please try again in a little while."
            )

        return f"⚠️ AI connection error: {error}"


# =========================================================
# INITIALIZE
# =========================================================

init_state()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111936 0%, #1c2860 100%);
}

[data-testid="stSidebar"] * { color: #f4f7ff !important; }
/* Sidebar buttons / boxes - white text */
[data-testid="stSidebar"] button {
    color: #ffffff !important;
}

/* Button ke andar text */
[data-testid="stSidebar"] button * {
    color: #ffffff !important;
}

.hero {
    padding: 28px 32px;
    border-radius: 28px;
    color: white;

    background:
    linear-gradient(
        120deg,
        #25256f,
        #087f8c
    );
    box-shadow:
    0 18px 45px rgba(28, 43, 100, .18);

    margin-bottom: 20px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;

    background:
    rgba(255,255,255,.14);

    border:
    1px solid rgba(255,255,255,.25);

    font-size: 12px;
    font-weight: 700;
    letter-spacing: .4px;
}

.hero h1 {
    margin: 12px 0 4px 0;
    font-size: 42px;
}

.hero p {
    margin: 0;
    opacity: .9;
}

.card {
    background:
    rgba(255,255,255,.9);

    border:
    1px solid rgba(100,120,180,.12);

    border-radius: 18px;

    padding: 17px;

    box-shadow:
    0 8px 24px rgba(32,49,100,.06);
}

.small-muted {
    color: #6d7895;
    font-size: 13px;
}

.chat-title {
    font-size: 26px;
    font-weight: 800;
    color: #17235b;
    margin-top: 5px;
}

div.stButton > button {
    border-radius: 12px;
    border:
    1px solid rgba(120,130,180,.18);

    font-weight: 600;
}

div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border-radius: 16px;
    color: #172033 !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] strong,
div[data-testid="stChatMessage"] em {
    color: #172033 !important;
}

.mode-pill {
    padding: 8px 12px;
    border-radius: 10px;

    background: #eef2ff;
    color: #303d88;

    font-size: 13px;
    font-weight: 700;
}
/* Front page text - black */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp .card,
.stApp .card * {
    color: #000000 !important;
}
/* AI response text - black */
div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3,
div[data-testid="stChatMessage"] h4,
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] strong {
    color: #000000 !important;
}

/* Code box */
div[data-testid="stChatMessage"] pre {
    background: #f1f3f7 !important;
    color: #000000 !important;
}

div[data-testid="stChatMessage"] pre code {
    background: #f1f3f7 !important;
    color: #000000 !important;
}
/* Online AI Assistant */
[data-testid="stSidebar"] .stCaption {
    color: #ffffff !important;
}

/* New Chat & Clear Current Chat buttons */
[data-testid="stSidebar"] button {
    background: #000000 !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] button * {
    color: #ffffff !important;
}
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🎓 UniMate AI")
    st.caption("Online AI Assistant")

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        new_chat()
        st.rerun()

    if st.button(
        "🗑️ Clear Current Chat",
        use_container_width=True
    ):
        clear_current_chat()
        st.rerun()

    st.markdown("### 🌐 Language")

    st.session_state.language = st.selectbox(
        "Response language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(
            st.session_state.language
        ),
        label_visibility="collapsed",
    )

    st.markdown("### 🎯 AI Mode")

    st.session_state.mode = st.radio(
        "Choose mode",
        list(MODES.keys()),
        index=list(MODES.keys()).index(
            st.session_state.mode
        ),
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### 💬 Chat History")

    for i, chat in enumerate(
        st.session_state.chats
    ):

        title = chat["title"]

        if (
            title == "New Chat"
            and chat["messages"]
        ):

            first = next(
                (
                    m["content"]
                    for m in chat["messages"]
                    if m["role"] == "user"
                ),
                ""
            )

            title = (
                first[:25] + "..."
                if len(first) > 25
                else first or "New Chat"
            )

        if st.button(
            f"{'● ' if i == st.session_state.active_chat else ''}{title}",
            key=f"chat_{i}",
            use_container_width=True,
        ):

            st.session_state.active_chat = i
            st.rerun()

    st.divider()

    st.markdown("**AI Engine**")

    if HF_TOKEN:
        st.success("Cloud AI Ready")
    else:
        st.error("HF Token Missing")

    st.caption("Model: GPT-OSS 20B")
    st.caption("Backend: Hugging Face")
    st.caption("Secure token: Streamlit Secrets")


# =========================================================
# MAIN
# =========================================================

chat = st.session_state.chats[
    st.session_state.active_chat
]


# =========================================================
# HERO
# =========================================================

st.title("🎓 UniMate AI")
st.subheader("MUBASHAR REHMAN PROJECT")
st.write("Your intelligent study companion — powered by online AI.")


# =========================================================
# STATUS CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        """
        <div class="card">
            <div class="small-muted">
                AI STATUS
            </div>
            <h3>🟢 Online</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="card">
            <div class="small-muted">
                MODEL
            </div>
            <h3>GPT-OSS 20B</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="card">
            <div class="small-muted">
                SECURITY
            </div>
            <h3>🔐 Secure</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="card">
            <div class="small-muted">
                MODE
            </div>
            <h3>{st.session_state.mode}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHAT AREA
# =========================================================

st.markdown("### 🎓 MUBASHAR REHMAN PROJECT")

st.title("UniMate AI")

st.write(
    "Your intelligent university study companion — "
    "powered by online AI."
)

st.write("")


if not chat["messages"]:

    st.info(
        "👋 Assalam-o-Alaikum! "
        "I'm UniMate AI. Ask me anything about "
        "your studies, coding, assignments, "
        "or university learning."
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in chat["messages"]:

    with st.chat_message(
        message["role"],
        avatar=(
            "🎓"
            if message["role"] == "assistant"
            else "🧑‍🎓"
        ),
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input(
    "Ask UniMate anything..."
)


if prompt:

    # Add user message
    chat["messages"].append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Set chat title
    if chat["title"] == "New Chat":

        chat["title"] = (
            prompt[:35]
            + ("..." if len(prompt) > 35 else "")
        )

    # Show user message
    with st.chat_message(
        "user",
        avatar="🧑‍🎓"
    ):

        st.markdown(prompt)

    # Generate AI response
    with st.chat_message(
        "assistant",
        avatar="🎓"
    ):

        with st.spinner(
            "UniMate is thinking..."
        ):

            answer = ask_huggingface(
                chat["messages"],
                st.session_state.language,
                st.session_state.mode,
            )

        st.markdown(answer)

    # Save AI response
    chat["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🎓 UniMate AI • Student Project"
)
