from agents.similarity import get_similarity_scores

text = "how to get internship in software engineering"

scores = get_similarity_scores(text, top_k=5)

for s in scores:
    print(s['similarity_score'])
