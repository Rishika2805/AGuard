# utils/stream_utils.py

def deduplicated_items(items):
    seen = set()
    unique = []

    for item in items:
        key = f"{item['source']}::{item['id']}"

        if key not in seen:
            unique.append(item)
            seen.add(key)

    return unique

def sort_items(items):
    return sorted(
        items,
        key=lambda item: item['timestamp'],
        reverse = True
    )

def print_stream(items):
    print(f"\nTotal items: {len(items)}\n")

    for i, item in enumerate(items, start=1):

        if not isinstance(item, dict):
            print(f'{i}. [INVALID ITEM] {item}')
            print('-' * 60)
            continue


        print(f"{i}. [{item['source'].upper()}]")
        print(f"   ID        : {item['id']}")
        print(f"   Title     : {item['title'][:80]}")
        print(f"   Timestamp : {item['timestamp']}")
        print(f"   URL       : {item['url']}")
        print("-" * 60)