import streamlit as st
import time
from api import ask_question
from components.source_card import show_sources


def show_chat_history():
    """Display all previous chat messages."""

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":
                show_sources(message.get("sources", []))


def handle_chat():
    """Handle new user questions."""

    question = st.chat_input("Ask a question about your PDFs...")

    if not question:
        return

    # ---------- User Message ---------- #

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # ---------- Assistant ---------- #

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = ask_question(question)

        if response.status_code == 200:

            result = response.json()

            answer = result["answer"]
            sources = result["sources"]

            def stream_generator():
                for word in answer.split(" "):
                    yield word + " "
                    time.sleep(0.01)

            st.write_stream(stream_generator)

            show_sources(sources)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )

        else:
            error_detail = "Unable to get an answer from the backend."
            try:
                err_json = response.json()
                if "detail" in err_json:
                    error_detail = f"Backend Error: {err_json['detail']}"
            except Exception:
                if response.text:
                    error_detail = f"Backend Error: {response.text}"
            st.error(error_detail)