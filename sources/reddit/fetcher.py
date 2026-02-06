# sources/reddit/fetcher

import feedparser

def fetch_posts(subreddit="python",limit=5):
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
    feed = feedparser.parse(url)

    return feed['entries'][:limit]