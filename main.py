from graph.graph import build_graph

if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({})

    print("\n=== FINAL STATE ===")
    for k, v in result.items():
        print(f"{k}: {type(v)}")

    print("\n=== NOTIFY ITEMS ===")
    if result.get("notify_items"):
        for i, item in enumerate(result["notify_items"], start=1):
            print(f"\n{i}. ID: {item.get('id')}")
            print(f"   Source: {item.get('source')}")
            print(f"   Title: {item.get('title')}")
            print(f"   Similarity: {item.get('similarity_score')}")
            print(f"   url: {item.get('url')}")
            print(f"   reason: {item.get('reason')}")
    else:
        print("No items to notify")

    print("\n=== ARCHIVE ITEMS ===")
    if result.get("archive_items"):
        for i, item in enumerate(result["archive_items"], start=1):
            print(f"\n{i}. ID: {item.get('id')}")
            print(f"   Source: {item.get('source')}")
            print(f"   Title: {item.get('title')}")
            print(f"   Similarity: {item.get('similarity_score')}")
            print(f"   url: {item.get('url')}")
            print(f"   reason: {item.get('reason')}")
    else:
        print("No items archived")

