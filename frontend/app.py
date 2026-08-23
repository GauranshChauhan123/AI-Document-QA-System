import sys
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

import streamlit as st

from styles import load_css
from components.sidebar import render_sidebar
from components.chat import (
    show_chat_history,
    handle_chat,
)

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ---------------- Session ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Sidebar ---------------- #

render_sidebar()

# ---------------- Main ---------------- #

st.title("🤖 AI Document Assistant")

st.caption(
    "Upload PDF documents and ask questions using AI."
)

if not st.session_state.messages:

    st.info(
        """
👋 Welcome!

1. Upload one or more PDF documents.

2. Click **Upload PDFs**.

3. Ask any question about the uploaded documents.
"""
    )

show_chat_history()

handle_chat()