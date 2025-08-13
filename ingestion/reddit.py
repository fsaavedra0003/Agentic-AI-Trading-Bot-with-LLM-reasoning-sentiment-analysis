"""
Reddit Ingestion Script for AI Trading Bot
-------------------------------------------
- Fetches posts from relevant subreddits
- Filters by keywords/tickers
- Saves results to JSON for sentiment analysis
"""

import os
import json
from datetime import datetime
from typing import List
import praw
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Reddit API authentication
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ai-trading-bot/1.0")

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    raise ValueError("Missing Reddit API credentials. Please set them in the .env file.")

# Create Reddit API client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_posts(keywords: List[str], subreddits: List[str], limit: int = 50):
    """Fetch recent Reddit posts containing given keywords."""
    results = []
    subreddit_str = "+".join(subreddits)
    search_query = " OR ".join(keywords)

    print(f"[INFO] Searching for: {search_query} in {subreddit_str}")

    subreddit = reddit.subreddit(subreddit_str)
    for post in subreddit.search(search_query, sort="new", limit=limit):
        results.append({
            "id": post.id,
            "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat(),
            "title": post.title,
            "body": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "url": post.url,
            "subreddit": post.subreddit.display_name
        })
    return results

def save_posts_to_json(posts, output_path: str):
    """Save fetched Reddit posts to JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Saved {len(posts)} posts to {output_path}")

if __name__ == "__main__":
    KEYWORDS = ["Tesla", "TSLA", "Bitcoin", "BTC", "AAPL", "Apple"]
    SUBREDDITS = ["stocks", "wallstreetbets", "investing", "cryptocurrency"]

    posts = fetch_reddit_posts(KEYWORDS, SUBREDDITS, limit=50)
    save_posts_to_json(posts, "data/raw/reddit_posts.json")
