# memory/embedder.py

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def get_embedding(text):
    _embeddings = model.encode(
        text,
        normalize_embeddings=True # Important for cosine similarity
        )
    return _embeddings


def embed_text(text : str) -> list[float]:
    """
    Generate embedding for given text
    """

    return get_embedding(text)
