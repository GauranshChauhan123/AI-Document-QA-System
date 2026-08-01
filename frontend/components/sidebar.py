import streamlit as st
from api import upload_documents, check_backend


def render_sidebar():
    uploaded_files = None

    with st.sidebar:

        if check_backend():
           st.success("🟢 Backend Connected")
        else:
           st.error("🔴 Backend Offline")
        st.divider()

        st.title("📂 Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if st.button("📤 Upload PDFs", use_container_width=True):

            if not uploaded_files:
                st.warning("Please select at least one PDF.")

            else:

                files = [
                    (
                        "file",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf",
                        ),
                    )
                    for file in uploaded_files
                ]

                with st.spinner("Building knowledge base..."):

                    response = upload_documents(files)

                if response.status_code in [200, 201]:

                    data = response.json()

                    st.success(data["message"])

                    st.subheader("📊 Statistics")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Docs", data["documents"])

                    with col2:
                        st.metric("Chunks", data["chunks"])

                    st.divider()

                    st.subheader("📄 Uploaded PDFs")

                    for file in uploaded_files:
                       st.write(f"📄 {file.name}")
                else:

                    st.error(response.text)

        st.divider()

        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return uploaded_files