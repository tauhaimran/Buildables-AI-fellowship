import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="AnatoBot", page_icon="🧠")
st.title("🧠 AnatoBot; Anatomy Learning Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask something about anatomy…")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.history.append(("user", user_input))

    resp = requests.post(API_URL, json={"message": user_input})
    bot_reply = resp.json()["reply"]

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.history.append(("assistant", bot_reply))

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)


#to run this app, use the command:
#uvicorn anato_backend.main:app --reload
#streamlit run anato_frontend/app.py
