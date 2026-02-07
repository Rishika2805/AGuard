# memory/embedder.py

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


load_dotenv()

_embeddings = None

def get_embedding_model():
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
    return _embeddings


def embed_text(text : str) -> list[float]:
    """
    Generate embedding for given text
    """

    model = get_embedding_model()
    return model.embed_query(text)
