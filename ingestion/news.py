"""
News Ingestion Script for AI Trading Bot
----------------------------------------
- Fetches latest financial news articles
- Filters by keywords (tickers, company names)
- Saves results to JSON for sentiment analysis
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("Missing NEWS_API_KEY. Please add it to .env")

BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(keywords, limit=20):
    """Fetch news articles containing given keywords."""
    query = " OR ".join(keywords)
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    results = []
    for article in data.get("articles", []):
        results.append({
            "title": article["title"],
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "published_at": article["publishedAt"],
            "source": article["source"]["name"],
            "url": article["url"]
        })
    return results

def save_news_to_json(news, output_path="data/raw/news.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(news, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Saved {len(news)} news articles to {output_path}")

if __name__ == "__main__":
    KEYWORDS = ["Tesla", "Bitcoin", "Apple", "Microsoft"]
    news = fetch_news(KEYWORDS, limit=30)
    save_news_to_json(news)
