# memory/vector_repo.py

from memory.chroma_client import get_chroma_client
from memory.embedder import embed_text


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name='content_memory',
        metadata={
            'embedding_model' : 'text-embedding-3-small',
            'hnsw:space' : "cosine"
        }
    )

def upsert_content_embedding(item : dict):
    """
    Store embedding for a content item
    """

    client,collection = get_collection()

    embedding = embed_text(item['full_text'])

    collection.upsert(
        ids=item['id'],
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
    embedding = embed_text(text)

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return result