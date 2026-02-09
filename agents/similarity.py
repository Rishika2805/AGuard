from memory.vector_repo import find_similar_content


def cosine_dist_to_similarity(dist : float) -> float:
    """
    Convert Chroma cosine distance to similarity score [0 , 1]
    """

    if dist is None:
        return 0.0

    similarity = 1.0 - dist
    return round(max(0.0, similarity), 3)



def get_similarity_scores(item : dict, top_k : int = 5):
    """
    Agent-level helper.
    Interprets vector search results
    """

    text = item.get("full_text","")

    results = find_similar_content(text, top_k=top_k)

    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]

    scored = []

    for cid,dist, in zip(ids, distances):
        scored.append(
            {
                'content_id': cid,
                'similarity_score': cosine_dist_to_similarity(dist),
            }
        )

    if scored:
        avg_similarity = sum(s["similarity_score"] for s in scored) / len(scored)
    else:
        avg_similarity = 0.0

    # store back into item
    item["similarity_score"] = round(avg_similarity, 4)
