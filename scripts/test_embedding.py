from memory.embedder import get_embedding


print(get_embedding('''
"content": "I've been working remotely for years and noticed city centers changing. Offices are emptier, but neighborhoods feel more active.",
  "title": "Remote Work and Urban Change",
  "source": "Reddit r/UrbanPlanning",
  "similarity_scores": [0.61, 0.58, 0.55],
  "user_preferences": {
    "topics": ["technology", "future of work"],
    "preferred_sources": ["Wired"],
    "content_sensitivity": "low"'''))