# voice_bot app.py
import streamlit as st
import os
from utils.groq_client import transcribe_audio, chat_reply, text_to_speech  # functions from groq_client.py
from utils.audio_utils import save_uploaded_audio  # functions from audio_utils.py

# Streamlit page config
st.set_page_config(
    page_title="🎙️ Groq Voice Assistant | Tauha",
    page_icon="🧠",
    layout="centered"
)

# App Title
st.title("🎧 Voice Chatbot — Groq API \n Tauha - Week-4 Task | Buildables AI Fellowship)")

# ---- 📎 Project Links Section ----
st.markdown(
    """
    <div style="text-align:center; font-size:16px;">
        🔗 <a href="https://github.com/tauhaimran/Buildables-AI-fellowship/tree/main/week-4/voice_bot" target="_blank">GitHub Repository</a> |
        🌐 <a href="https://tauhaimran.github.io/" target="_blank">Tauha Imran</a>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- 📤 File Uploader ----
uploaded = st.file_uploader(
    "Upload an audio file (wav/mp3/m4a/ogg)",
    type=["wav", "mp3", "m4a", "ogg"]
)

# ▶️ Play Uploaded Audio
if uploaded:
    st.audio(uploaded)  # let user listen to uploaded file

    if st.button("Run Voice Assistant ..."):
        with st.spinner("Transcribing..."):
            tmp_path = save_uploaded_audio(uploaded)
            with open(tmp_path, "rb") as f:  # open temp file in read-binary mode
                text = transcribe_audio(f)  # call transcribe_audio function
        st.success("✅ Transcription complete")
        st.write("**You said:**", text)

        with st.spinner("Getting LLM reply..."):
            reply = chat_reply(text)  # call chat_reply function
        st.write("**Assistant:**", reply)

        with st.spinner("Generating TTS..."):
            # ✅ Truncate to stay under free-tier token limit
            MAX_CHARS = 3500   # ~1000 tokens
            safe_reply = reply[:MAX_CHARS]

            out_path = os.path.join("assets", "reply.wav")
            text_to_speech(reply, out_path)  # call text_to_speech function
            
        st.audio(out_path)  # play generated audio
        st.success("✅ Done!")