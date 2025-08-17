 ingestion/news.py
"""
News ingestion:
- Primary: NewsAPI.org (requires API key)
- Fallback: RSS via feedparser for keyword feeds
- Stores to SQLite by default
"""

import os
import time
