#pip install streamlit streamlit-chat markdown
import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load env variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("<< ERROR >> GROQ API KEY NOT FOUND - please check your .env file!")
    st.stop()

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"   # don't touchy :)

def travel_bot(query, history=None):
    if history is None:
        history = []

    system_message = {
        "role": "system",
        "content": (
            "You are a friendly travel planner bot ✈️🌍. "
            "Always reply with structured, easy-to-read text. "
            "When giving itineraries, use bullet points or numbered days. "
            "Keep responses helpful, concise, and warm."
        )
    }

    messages = [system_message] + history + [{"role": "user", "content": query}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": reply})

    return reply, history


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="🌍 Travel Planner Bot", page_icon="✈️")
st.title("🌍 Travel Planner Bot")
st.write("Plan trips, get itineraries, and explore destinations!")

if "history" not in st.session_state:
    st.session_state.history = []

# Chat input at the bottom
user_input = st.chat_input("Where would you like to travel?")

if user_input:
    reply, st.session_state.history = travel_bot(user_input, st.session_state.history)

# Render chat messages
for i, msg in enumerate(st.session_state.history):
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])   # <-- markdown makes bold, bullet points look good
# ---------------- END STREAMLIT UI ----------------