# anato_backend/main.py
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from typing import Optional
from rag import SimpleRAG

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set — see .env.example")

client = Groq(api_key=GROQ_API_KEY)
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
#MODEL = "llama-3.3-70b-versatile"   # don't touchy :)

app = FastAPI(title="AnatoBot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize RAG loader (reads markdown files from ./data)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
rag = SimpleRAG(data_dir=DATA_DIR)

class ChatRequest(BaseModel):
    message: str
    use_rag: Optional[bool] = True

@app.post("/chat")
def chat(req: ChatRequest):
    """
    Main chat endpoint.
    If use_rag=True, we prepend top retrieved passages to the system prompt.
    """
    user_message = req.message
    use_rag = req.use_rag

    system_prompt = (
        "You are AnatoBot, an AI anatomy tutor for medical students.\n"
        "- Give clear, structured explanations.\n"
        "- Use bullet points and short numbered steps where helpful.\n"
        "- When relevant, say 'Source: <filename>' for RAG excerpts.\n"
        "- Keep tone friendly and encouraging.\n"
    )

    # Retrieve relevant docs if RAG requested
    rag_context = ""
    sources = []
    if use_rag:
        hits = rag.retrieve(user_message, top_k=3)
        if hits:
            rag_context = "### Relevant knowledge excerpts:\n"
            for h in hits:
                rag_context += f"\n---\nSource: {h['source']}\n{h['text']}\n"
                sources.append(h['source'])

    # Build messages for the model
    messages = [
        {"role": "system", "content": system_prompt + ("\n\n" + rag_context if rag_context else "")},
        {"role": "user", "content": user_message}
    ]

    # Call Groq LLM
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    reply = completion.choices[0].message.content

    return {"reply": reply, "rag_sources": sources}

@app.post("/upload_knowledge")
async def upload_knowledge(file: UploadFile = File(...)):
    """
    Upload a markdown or txt file to the local knowledge base for RAG.
    (Simple — stores file to ./data and reloads rag index)
    """
    filename = file.filename
    if not filename.endswith((".md", ".txt")):
        raise HTTPException(status_code=400, detail="Only .md or .txt files allowed")

    contents = await file.read()
    dest_path = os.path.join(DATA_DIR, filename)
    with open(dest_path, "wb") as f:
        f.write(contents)

    # reload RAG
    rag.reload()
    return {"status": "ok", "saved_as": filename}
