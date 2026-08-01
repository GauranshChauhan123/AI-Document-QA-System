import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .main{
        padding-top:1rem;
    }

    .stChatMessage{
        border-radius:18px;
        padding:15px;
        margin-bottom:10px;
        border:1px solid #ddd;
    }

    .stButton>button{
        width:100%;
        border-radius:12px;
        height:45px;
        font-weight:600;
    }

    .stFileUploader{
        border:2px dashed #4CAF50;
        border-radius:15px;
        padding:15px;
    }

    </style>
    """, unsafe_allow_html=True)