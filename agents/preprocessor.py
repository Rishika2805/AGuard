# agents/preprocessor.py

import re
import unicodedata
from html import unescape

from config.loader import load_user_preferences

prefs = load_user_preferences()

MIN_CONTENT_LENGTH = prefs['general']["min_content_length"]

def normalized_text(text: str) -> str:
    # unicoded normalization
    text =  unicodedata.normalize("NFKC", text)

    # HTML entities
    text = unescape(text)

    # lowercase
    text = text.lower()

    # trim whitespace
    text = re.sub(r"\s+", " ", text)

    return text

def strip_html(text: str) -> str:
    # remove html tags
    return re.sub(r"<[^>]>", "", text)

def remove_boilerplate(text: str) -> str:
    boilerplate_patterns = [
        r"unsubscribe",
        r"view in browser",
        r"privacy policy",
        r"terms and conditions",
    ]

    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()

def detect_links(text: str) -> bool:
    return bool(re.search(r"https?://|www\.]",text))

def preprocessor(item : dict) -> dict:
    """
    Preprocess content item.
    IMPORTANT : This function does NOT make decision.
    It only cleans and enriches
    """

    title = item.get("title","")
    content = item.get("content","")

    # combine title + content
    full_text = f'{title}\n{content}'

    # strip HTML if present
    full_text = strip_html(full_text)

    # remove boilerplate
    full_text = remove_boilerplate(full_text)

    # normalize text
    full_text = normalized_text(full_text)

    # Enrichment (metadata, NOT decision)

    word_count = len(full_text.split())
    has_links = detect_links(full_text)

    # Attach Preprocessing output
    item['full_text'] = full_text
    item['word_count'] = word_count
    item['has_links'] = has_links

    return item


