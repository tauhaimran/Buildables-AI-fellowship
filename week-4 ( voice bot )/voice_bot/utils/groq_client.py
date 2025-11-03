import os
from dotenv import load_dotenv
from groq import Groq


#load environment variables once
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")


# A single cllient to be shared across the app
client = Groq(api_key= API_KEY)


def transcribe_audio(file):
    #transcribe audio file using Groq's Whisper model
    transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3-turbo",
        response_format="text"
    )
    return getattr(transcription, "text", str(transcription))

def chat_reply(prompt):
    #get LLM chat reply from Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a concise, friendly assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def text_to_speech(text, out_path):
    #convert text to speech and save wav file
    response = client.audio.speech.create(
        model="playai-tts",
        voice="Fritz-PlayAI",
        input=text,
        response_format="wav"
    )
    response.write_to_file(out_path)
    return out_path