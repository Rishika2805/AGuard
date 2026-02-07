# memory/chroma_client.py

import chromadb
from pathlib import Path

# This resolves to: AGuard-AI-Agent/
BASE_DIR = Path(__file__).resolve().parents[1]

def get_chroma_client():
    return chromadb.PersistentClient(
        path=str(BASE_DIR / "memory" / "chroma_store")
    )
