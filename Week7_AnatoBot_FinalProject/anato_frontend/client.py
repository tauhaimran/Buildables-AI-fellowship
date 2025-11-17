# anato_frontend/client.py
import requests

API_BASE = "http://localhost:8000"

def chat(message: str, use_rag: bool = True):
    resp = requests.post(f"{API_BASE}/chat", json={"message": message, "use_rag": use_rag}, timeout=60)
    resp.raise_for_status()
    return resp.json()

def upload_knowledge(file_path: str):
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        resp = requests.post(f"{API_BASE}/upload_knowledge", files=files, timeout=60)
        resp.raise_for_status()
        return resp.json()
