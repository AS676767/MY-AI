
import streamlit as st
import os
from groq import Groq

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="My Generative AI",
    page_icon="✨",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
    .stApp {
        background-color: #f7f8fa;
    }

    header[data-testid="stHeader"] {
        background-color: #f7f8fa;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #202938;
        text-align: center;
        margin-top: 65px;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #778196;
        font-size: 16px;
        margin-bottom: 35px;
    }

    [data-testid="stChatMessage"] {
        background-color: white;
        border: 1px solid #e8ebf0;
        border-radius: 14px;
        padding: 15px;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8ebf0;
    }

    .stChatInput textarea {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- GROQ CONNECTION ----------------

api_key = os.environ.get("GROQ_API_KEY")

try:
    api_key = st.secrets.get("GROQ_API_KEY", api_key)
except Exception:
    pass

if not api_key:
    st.error("Please configure your Groq API key.")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- CHAT HISTORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ✨ My Generative AI")
    st.caption("Your personal AI assistant")

    st.divider()

    if st.button("＋  New Chat", use_container_width=True):
        if st.session_state.messages:
            st.session_state.conversations.append(
                st.session_state.messages.copy()
            )
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Recent conversations")

    for i, conversation in enumerate(
        reversed(st.session_state.conversations)
    ):
        if conversation:
            title = conversation[0]["content"][:25]

            st.caption(f"💬 {title}")

    st.divider()

    if st.button("Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Groq AI")

# ---------------- MAIN SCREEN ----------------

if not st.session_state.messages:

    st.markdown(
        '<div class="main-title">What can I help you with?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Ask questions, explore ideas, '
        'or get help with anything.</div>',
        unsafe_allow_html=True
    )

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("Message My Generative AI...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.messages,
                    max_tokens=1000
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.session_state.messages.pop()

