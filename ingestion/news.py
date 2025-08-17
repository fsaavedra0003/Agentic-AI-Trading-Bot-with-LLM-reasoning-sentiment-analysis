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
