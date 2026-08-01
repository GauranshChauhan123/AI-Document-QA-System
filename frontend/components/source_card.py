import streamlit as st


def show_sources(sources):

    if not sources:
        return

    with st.expander("📄 Sources Used"):

        for source in sources:

            with st.container(border=True):

                st.markdown(f"### 📄 {source['file']}")

                st.caption(f"📍 Page {source['page']}")

                if source.get("content"):

                    st.write(source["content"][:250] + "...")