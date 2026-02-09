# sources/reddit/parser.py

from datetime import datetime
from urllib.parse import urlparse


REDDIT_BASE = "https://www.reddit.com"


# -----------------------------
# Sender / Author
# -----------------------------
def extract_sender(entry):
    return (
        entry.get("author")
        or entry.get("dc_creator")
        or entry.get("author_detail", {}).get("name")
        or "unknown"
    )


# -----------------------------
# Content / Body
# -----------------------------
def extract_content(entry):
    if entry.get("summary"):
        return entry["summary"]

    if entry.get("content"):
        # feedparser content is a list of dicts
        return entry["content"][0].get("value", "")

    return ""


# -----------------------------
# Timestamp
# -----------------------------
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


# -----------------------------
# ID (normalize Reddit IDs)
# -----------------------------
def extract_id(entry):
    """
    Extract clean Reddit post ID (no t3_, no URL junk)
    """
    # Prefer Reddit-style IDs
    raw_id = entry.get("id") or entry.get("guid") or ""

    # Handle t3_ IDs
    if raw_id.startswith("t3_"):
        return raw_id.replace("t3_", "")

    # Extract from permalink or link if needed
    link = entry.get("permalink") or entry.get("link") or ""
    if "/comments/" in link:
        try:
            return link.split("/comments/")[1].split("/")[0]
        except Exception:
            pass

    return raw_id


# -----------------------------
# Tags
# -----------------------------
def extract_tags(entry):
    tags = entry.get("tags", [])
    return [t.get("term", "") for t in tags if t.get("term")]


# -----------------------------
# URL (THE IMPORTANT FIX)
# -----------------------------
def extract_reddit_url(entry):
    """
    Always return a valid Reddit post URL.
    """
    # BEST source: permalink
    permalink = entry.get("permalink")
    if permalink:
        if permalink.startswith("/"):
            return f"{REDDIT_BASE}{permalink}"
        return permalink

    # Fallback: try to repair link
    link = entry.get("link", "")
    if not link:
        return None

    # Relative paths
    if link.startswith("/r/"):
        return f"{REDDIT_BASE}{link}"

    # Old / malformed reddit URLs
    parsed = urlparse(link)
    if parsed.netloc.endswith("reddit.com") and "/comments/" in parsed.path:
        return f"{REDDIT_BASE}{parsed.path}"

    # Last resort: drop bad URL
    return None


# -----------------------------
# Main Parser
# -----------------------------
def parse_post(entry):
    return {
        "source": "reddit",
        "id": extract_id(entry),
        "sender": extract_sender(entry) or "",
        "title": entry.get("title", ""),
        "content": extract_content(entry) or "",
        "url": extract_reddit_url(entry),
        "timestamp": extract_date(entry) or "",
        "tags": extract_tags(entry) or [],
    }
