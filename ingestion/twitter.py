# ingestion/twitter.py
"""
Twitter ingestion helper (Twitter API v2 recent search)
- Uses Bearer Token for auth (env var or passed in)
- Stores tweets to a local SQLite DB by default
- Simple retry/backoff and basic rate-limit handling
"""

import os
import time
import json
import logging
import sqlite3
from typing import List, Dict, Optional
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SQLiteStorage:
    """Simple SQLite storage for ingestion artifacts."""
    def __init__(self, path: str = "data/twitter.db"):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id TEXT PRIMARY KEY,
                text TEXT,
                created_at TEXT,
                author_id TEXT,
                raw_json TEXT
            );
            """
        )
        self.conn.commit()

    def save_tweet(self, tweet: Dict):
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO tweets (id, text, created_at, author_id, raw_json) VALUES (?, ?, ?, ?, ?)",
                (
                    tweet.get("id"),
                    tweet.get("text"),
                    tweet.get("created_at"),
                    tweet.get("author_id"),
                    json.dumps(tweet, ensure_ascii=False),
                ),
            )
            self.conn.commit()
        except Exception:
            logger.exception("Failed to save tweet %s", tweet.get("id"))


class TwitterIngestor:
    SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, bearer_token: Optional[str] = None, storage: Optional[SQLiteStorage] = None):
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        if not self.bearer_token:
            raise ValueError("Twitter bearer token required (env TWITTER_BEARER_TOKEN or param).")
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}
        self.storage = storage or SQLiteStorage()

    def _request(self, params: Dict) -> Dict:
        backoff = 1
        for attempt in range(6):
            resp = requests.get(self.SEARCH_URL, headers=self.headers, params=params, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                # Rate limit, backoff
                logger.warning("Twitter rate-limited. Sleeping %s seconds.", backoff)
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
            else:
                logger.warning("Twitter API returned %s: %s", resp.status_code, resp.text)
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
        raise RuntimeError("Twitter API failed after retries")

    def fetch_recent(self, query: str, max_results: int = 100, lang: str = "en") -> List[Dict]:
        """
        Fetch recent tweets for a query.
        Parameters:
            query: search query (Twitter v2 query).
            max_results: up to 100 per request (Twitter limit).
        Returns:
            list of tweet dicts (with created_at if requested).
        """
        params = {
            "query": query,
            "max_results": str(min(max_results, 100)),
            "tweet.fields": "created_at,lang,author_id",
        }
        if lang:
            params["query"] = f"{query} lang:{lang}"

        data = self._request(params)
        tweets = data.get("data", []) or []
        logger.info("Fetched %d tweets for query '%s'", len(tweets), query)
        for t in tweets:
            self.storage.save_tweet(t)
        return tweets


if __name__ == "__main__":
    # quick demo (set env TWITTER_BEARER_TOKEN before running)
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--q", default="bitcoin", help="Search query")
    parser.add_argument("--n", type=int, default=10)
    args = parser.parse_args()

    ingestor = TwitterIngestor()  # reads TWITTER_BEARER_TOKEN
    tweets = ingestor.fetch_recent(args.q, max_results=args.n)
    print(f"Saved {len(tweets)} tweets.")