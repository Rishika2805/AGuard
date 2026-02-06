# sources/reddit/parser

from datetime import datetime


def extract_sender(entry):
    return (
        entry.get("author")
        or entry.get("dc_creator")
        or entry.get("author_detail", {}).get("name")
        or "unknown"
    )


def extract_content(entry):
    if entry.get("summary"):
        return entry["summary"]

    if entry.get("content"):
        # feedparser content is a list of dicts
        return entry["content"][0].get("value", "")

    return ""


def extract_date(entry):
    if entry.get("published"):
        return entry["published"]

    if entry.get("updated"):
        return entry["updated"]

    if entry.get("published_parsed"):
        return datetime(*entry["published_parsed"][:6]).isoformat()

    if entry.get("updated_parsed"):
        return datetime(*entry["updated_parsed"][:6]).isoformat()

    return datetime.utcnow().isoformat()


def extract_id(entry):
    return (
        entry.get("id")
        or entry.get("guid")
        or entry.get("link")
        or ""
    )


def extract_tags(entry):
    tags = entry.get("tags", [])
    return [t.get("term", "") for t in tags if t.get("term")]



def parse_post(entry):
    return {
        "source": "reddit",
        "id": extract_id(entry),
        "sender": extract_sender(entry) or "",
        "title": entry.get("title", ""),
        "content": extract_content(entry) or "",
        "url": entry.get("link", ""),
        "timestamp": extract_date(entry) or "",
        "tags": extract_tags(entry) or [],
    }
