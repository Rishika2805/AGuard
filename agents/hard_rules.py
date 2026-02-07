# agents/hard_rules.py

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from config.loader import load_user_preferences

# load user preferences
prefs = load_user_preferences()
'''
Drop / Pass helper functions
'''

def drop(item : dict, reason : str, score : float = 0.0) -> dict:
    return {
        "content_id" : item["id"],
        "decision" : "DROP",
        "score" : score,
        "reason" : reason,
        "stage" : "hard_rules"
    }

def pass_to_llm(item : dict, reason : str, score : float) -> dict:
    return {
        "content_id": item["id"],
        "decision": "PASS_TO_LLM",
        "score": score,
        "reason": reason,
        "stage": "hard_rules"
    }


'''
Unwanted Words (shared reddit + email)
'''

def contains_unwanted_words(item : dict) -> bool:
    text = item.get("full_text", "")

    unwanted = (
        prefs.get('reddit',{}).get('exclude_fields', []) + prefs.get('email',{}).get('ignore_keywords',[])
    )

    return any(word.lower() in text for word in unwanted)

'''
Blacklisted senders (Email only)
'''

def blacklist_senders(item : dict) -> bool:
    sender = item.get("sender", "").lower()
    blacklisted = prefs['email'].get('blacklisted_senders', [])

    return any(b.lower() in sender for b in blacklisted)

'''
Staleness check(time-based)
'''

def is_stale(item : dict) -> bool:
    max_days = prefs.get('email',{}).get('max_age_days', 7)
    ts = item.get('timestamp')

    if not ts:
        return True

    try:
        item_ts = parsedate_to_datetime(ts)
        if item_ts.tzinfo is None:
            item_ts = item_ts.replace(tzinfo=timezone.utc)

        age_days = (datetime.now(timezone.utc) - item_ts).days
        return age_days > max_days

    except Exception:
        return True


'''
Image only detection
'''

def is_image_only(item : dict) -> bool:
    text = item.get("full_text", "").strip()
    url = item.get("url", "") or ""

    image_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

    return (
        not text
        and url.lower().endswith(image_exts)
    )

'''
Link only with no content
'''

def is_link_only(item : dict) -> bool:
    text = item.get("full_text", "").strip()
    url = item.get("url", "") or ""

    if not url:
        return False

    return len(text.strip()) < 10

'''
Megathread detection
'''

def is_megathread(item : dict) -> bool:
    title = item.get("title", "").lower()

    patterns = [
        "daily discussion",
        "weekly discussion",
        "daily megathread",
        "weekly megathread",
        "monthly megathread",
    ]
    return any(p in title for p in patterns)

'''
Preferred Keyword scoring
'''

def count_preferred_keywords(item : dict) -> dict:
    text = item.get("full_text", "").lower()

    preferred = (
        prefs.get('email',{}).get('important_keywords', []) +
        prefs.get('reddit',{}).get('include_fields', [])
    )
    return sum(1 for kw in preferred if kw.lower() in text)


'''
Hard_rule function
'''

def apply_hard_rules(item : dict) -> dict:

    if item['word_count'] < prefs['general']['min_content_length']:
        return drop(item, "Low Content Length")

    if contains_unwanted_words(item):
        return drop(item, "Unwanted Content")

    if item['source'] == 'gmail' and blacklist_senders(item):
        return drop(item, "Blacklisted Senders")

    if is_stale(item):
        return drop(item, "Stale Content")

    if is_image_only(item):
        return drop(item, "Image Only")

    if is_link_only(item):
        return drop(item, "Link Only")

    if item['source'] == 'reddit' and len(item['title']) < 15:
        return drop(item, "Low Effort Title")

    if is_megathread(item):
        return drop(item, "Megathread")

    #--------------- SCORING ---------------------

    score = 0.0

    matches = count_preferred_keywords(item)

    if matches > 0:
        score += 0.3
    if matches > 2:
        score += 0.2

    if score > 0.5:
        return pass_to_llm(item,score,"Relevant Content")
    else:
        return drop(item, "Low Relevance", score)

