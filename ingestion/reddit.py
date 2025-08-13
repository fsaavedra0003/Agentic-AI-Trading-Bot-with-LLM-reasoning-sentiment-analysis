# ingestion/reddit.py
"""
Reddit ingestion via Pushshift (good for historical / keyword search)
- Uses Pushshift public API (no auth) for submissions/comments
- Stores results to SQLite by default
- If you want PRAW (official Reddit) streaming, I can provide a variant
- Now supports .env files for environment variables (via python-dotenv)
"""

import os
import time
import json
import logging
import sqlite3
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv  # NEW: for .env file loading

# Load environment variables from .env file if present
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SQLiteStorage:
    def __init__(self, path: str = "data/reddit.db"):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reddit_submissions (
                id TEXT PRIMARY KEY,
                title TEXT,
                selftext TEXT,
                subreddit TEXT,
                author TEXT,
                created_utc INTEGER,
                raw_json TEXT
            );
            """
        )
        self.conn.commit()

    def save_submission(self, sub: Dict):
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO reddit_submissions (id, title, selftext, subreddit, author, created_utc, raw_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    sub.get("id"),
                    sub.get("title"),
                    sub.get("selftext"),
                    sub.get("subreddit"),
                    sub.get("author"),
                    sub.get("created_utc"),
                    json.dumps(sub, ensure_ascii=False),
                ),
            )
            self.conn.commit()
        except Exception:
            logger.exception("Failed to save submission %s", sub.get("id"))


class PushshiftRedditIngestor:
    BASE = "https://api.pushshift.io/reddit/search/submission/"

    def __init__(self, storage: Optional[SQLiteStorage] = None):
        # Example: If later you want to use an API key from .env
        # self.api_key = os.getenv("PUSHSHIFT_API_KEY")
        self.storage = storage or SQLiteStorage()

    def fetch_submissions(
        self,
        subreddit: Optional[str] = None,
        query: Optional[str] = None,
        after: Optional[int] = None,
        before: Optional[int] = None,
        size: int = 100,
    ) -> List[Dict]:
        """
        Query Pushshift for submissions.
        - subreddit: e.g. 'wallstreetbets'
        - query: text search
        - after/before: unix timestamps
        - size: max results (api may cap)
        """
        params = {"size": min(size, 500)}
        if subreddit:
            params["subreddit"] = subreddit
        if query:
            params["q"] = query
        if after:
            params["after"] = str(after)
        if before:
            params["before"] = str(before)

        backoff = 1
        for attempt in range(5):
            resp = requests.get(self.BASE, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json().get("data", []) or []
                logger.info("Pushshift returned %d submissions", len(data))
                for s in data:
                    self.storage.save_submission(s)
                return data
            else:
                logger.warning("Pushshift error %s: %s", resp.status_code, resp.text)
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
        raise RuntimeError("Pushshift API failed after retries")


if __name__ == "__main__":
    # Example: If you later want subreddit/query from .env:
    subreddit = os.getenv("REDDIT_SUBREDDIT", "wallstreetbets")
    query = os.getenv("REDDIT_QUERY", "GME")

    ingestor = PushshiftRedditIngestor()
    subs = ingestor.fetch_submissions(subreddit=subreddit, query=query, size=25)
    print(f"Saved {len(subs)} submissions.")
