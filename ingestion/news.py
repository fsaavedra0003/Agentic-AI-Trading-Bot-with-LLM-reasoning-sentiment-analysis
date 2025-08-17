 ingestion/news.py
"""
News ingestion:
- Primary: NewsAPI.org (requires API key)
- Fallback: RSS via feedparser for keyword feeds
- Stores to SQLite by default
"""

import os
import time
import json
import logging
import sqlite3
from typing import List, Dict, Optional
import requests
import feedparser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SQLiteStorage:
    def __init__(self, path: str = "data/news.db"):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_table()
        def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS news (
                id TEXT PRIMARY KEY,
                source TEXT,
                author TEXT,
                title TEXT,
                description TEXT,
                url TEXT,
                published_at TEXT,
                raw_json TEXT
            );
            """
        )
        self.conn.commit()

