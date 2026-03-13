# memory/vector_repo.py

from memory.chroma_client import get_chroma_client
from memory.embedder import get_embedding


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name='content_memory',
        metadata={
            'embedding_model' : 'BAAI/bge-small-en-v1.5',
            'hnsw:space' : "cosine"
        }
    )

def upsert_content_embedding(item : dict):
    """
    Store embedding for a content item
    """

    collection = get_collection()

    embedding = get_embedding(item['full_text'])

    collection.upsert(
        ids=[item['id']],
        embeddings=[embedding],
        metadatas=[
            {
                'source' : item['source'],
            }
        ]
    )


def find_similar_content(text : str, top_k : int = 5):
    """
    Perform semantic similarity search

    Return raw Chroma result (ids + distances)
    """

    collection = get_collection()
    embedding = get_embedding(text)

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return result