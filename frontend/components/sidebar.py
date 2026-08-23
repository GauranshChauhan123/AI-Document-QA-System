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
                        "files",
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
                    st.success(data.get("message", "Uploaded successfully!"))

                    st.subheader("📊 Statistics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Docs", data.get("documents", 0))
                    with col2:
                        st.metric("Chunks", data.get("chunks", 0))

                    st.divider()
                    st.subheader("📄 Uploaded PDFs")
                    for file in uploaded_files:
                        st.write(f"📄 {file.name}")
                else:
                    err_msg = "Upload failed."
                    try:
                        err_json = response.json()
                        if "detail" in err_json:
                            err_msg = f"Error: {err_json['detail']}"
                    except Exception:
                        if response.text:
                            err_msg = f"Error: {response.text}"
                    st.error(err_msg)

        st.divider()

        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return uploaded_files