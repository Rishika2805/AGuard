# agents/fetch_data.py

from sources.gmail.auth.auth import get_gmail_service
from sources.gmail.fetcher import fetch_full_message, fetch_message_ids
from sources.gmail.parser import parse_email

from sources.reddit.fetcher import fetch_posts
from sources.reddit.parser import parse_post

from config.loader import load_user_preferences

from utils.stream_utils import deduplicated_items, sort_items
prefs = load_user_preferences()

def is_valid_reddit_post(url: str) -> bool:
    return "/comments/" in url or "/t3_" in url

def collect_from_gmail():
    service = get_gmail_service()

    emails = []
    message_ids = fetch_message_ids(service,max_results=5)
    for message_id in message_ids:
        full_message = fetch_full_message(service,message_id['id'])
        parsed = parse_email(full_message)
        emails.append(parsed)

    return emails

def collect_from_reddit(limit=5):
    all_posts = []

    for subreddit in prefs['reddit']['subreddits']:
        posts = fetch_posts(subreddit,limit=limit)
        for post in posts:
            parsed = parse_post(post)
            if not is_valid_reddit_post(parsed["url"]):
                continue
            all_posts.append(parsed)
    return all_posts

def collect_all_data(limit=5):
    items = collect_from_gmail() + collect_from_reddit()
    items = deduplicated_items(items)
    items = sort_items(items)

    return items