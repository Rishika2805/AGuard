# notification/console.py


def notify_console(item: dict):
    print("\n🔔 NOTIFICATION")
    print(f"Source    : {item.get('source')}")
    print(f"Title     : {item.get('title')}")
    print(f"Why       : {item.get('reason')}")
    print(f"Confidence: {item.get('confidence')}")

    if item.get("url"):
        print(f"Link      : {item['url']}")
