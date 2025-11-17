# anato_frontend/app.py
import streamlit as st
from client import chat, upload_knowledge
import os

st.set_page_config(page_title="AnatoBot", page_icon="🧠")
st.title("🧠 AnatoBot — Prototype Anatomy Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Settings")
use_rag = st.sidebar.checkbox("Use local knowledge (RAG)", value=True)
st.sidebar.markdown("Upload a markdown file to add to local knowledge:")
uploaded = st.sidebar.file_uploader("Upload .md or .txt", type=["md", "txt"])

if uploaded:
    with open("tmp_upload.md", "wb") as f:
        f.write(uploaded.getbuffer())
    try:
        res = upload_knowledge("tmp_upload.md")
        st.sidebar.success(f"Uploaded: {res.get('saved_as')}")
    except Exception as e:
        st.sidebar.error(f"Upload failed: {e}")

st.write("Ask anatomy questions, request quizzes, or ask for explanations.")

user_input = st.chat_input("Type your question…")

if user_input:
    st.session_state.history.append(("user", user_input))
    with st.spinner("AnatoBot is thinking..."):
        try:
            resp = chat(user_input, use_rag=use_rag)
            reply = resp.get("reply", "")
            sources = resp.get("rag_sources", [])
        except Exception as e:
            reply = f"Error: {e}"
            sources = []

    st.session_state.history.append(("assistant", reply))

for role, message in st.session_state.history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)
        # If sources were returned, show them under the last assistant message
        if role == "assistant" and sources:
            st.caption("RAG sources: " + ", ".join(sources))
