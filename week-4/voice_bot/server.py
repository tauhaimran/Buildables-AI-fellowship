# server.py
import os
import base64
import queue
import threading
import time
from dotenv import load_dotenv
from groq import Groq
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import soundfile as sf
import numpy as np
import pyttsx3
from vosk import Model, KaldiRecognizer, SetLogLevel

# Load envs
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client (you already have this pattern)
client = Groq(api_key=GROQ_API_KEY)

# A tiny in-memory memory for last N turns (list of dicts)
CONTEXT_MEMORY = []
MAX_MEMORY_TURNS = 6

# Initialize Flask + SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")