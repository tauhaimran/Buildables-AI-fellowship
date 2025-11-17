# anato_backend/rag.py
import os
from typing import List, Dict
import difflib

class SimpleRAG:
    """
    Simple local RAG: chunk text files in data dir, do fuzzy matching with difflib.
    No ML libraries required — fast and good enough for a prototype.
    """
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.index = []
        self.reload()

    def reload(self):
        self.index = []
        for fname in os.listdir(self.data_dir):
            if not fname.lower().endswith((".md", ".txt")):
                continue
            path = os.path.join(self.data_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception:
                continue
            # naive chunking: split by paragraphs, keep 400-char chunks
            paras = [p.strip() for p in text.split("\n\n") if p.strip()]
            for p in paras:
                if len(p) > 600:
                    # split large paragraph into sliding windows
                    for i in range(0, len(p), 500):
                        chunk = p[i:i+600].strip()
                        if chunk:
                            self.index.append({"source": fname, "text": chunk})
                else:
                    self.index.append({"source": fname, "text": p})

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Return top_k matching chunks using difflib SequenceMatcher ratio.
        """
        if not self.index:
            return []
        scores = []
        for item in self.index:
            # compare query to chunk text — lowercased to reduce noise
            ratio = difflib.SequenceMatcher(None, query.lower(), item["text"].lower()).ratio()
            scores.append((ratio, item))
        scores.sort(key=lambda x: x[0], reverse=True)
        results = [s[1] for s in scores[:top_k] if s[0] > 0.05]  # filter near-zero
        return results
