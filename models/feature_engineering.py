# models/feature_engineering.py
"""
Feature Engineering for Trading Bot
-----------------------------------
- Combines sentiment data (Reddit + News) with market price snapshots
- Produces a feature dataset for modeling
"""

import os
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Paths
DATA_DIR = "data/processed"
SENTIMENT_FILES = [
    os.path.join(DATA_DIR, "reddit_with_sentiment.json"),
    os.path.join(DATA_DIR, "news_with_sentiment.json")
]
MARKET_FILE = os.path.join(DATA_DIR, "market_prices.json")
OUTPUT_FILE = os.path.join("data/features", "features_dataset.csv")


def load_sentiment_data():
    """Load sentiment JSON files and merge into one DataFrame."""
    dfs = []
    for path in SENTIMENT_FILES:
        if not os.path.exists(path):
            print(f"[WARN] Missing: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):  # edge case: JSON saved as dict
            data = [data]
        dfs.append(pd.DataFrame(data))
    if not dfs:
        raise FileNotFoundError("No sentiment data found.")
    return pd.concat(dfs, ignore_index=True)


def load_market_data():
    """Load market prices JSON as DataFrame."""
    if not os.path.exists(MARKET_FILE):
        raise FileNotFoundError(f"Market file not found: {MARKET_FILE}")
    with open(MARKET_FILE, "r", encoding="utf-8") as f:
        market_data = json.load(f)

    rows = []
    for ticker, info in market_data.items():
        rows.append({
            "ticker": ticker,
            "price": info["price"],
            "timestamp": info["timestamp"]
        })
    return pd.DataFrame(rows)


def encode_sentiment(df):
    """Encode sentiment (Positive/Neutral/Negative)."""
    le = LabelEncoder()
    df["sentiment_encoded"] = le.fit_transform(df["sentiment"])
    return df


def build_feature_dataset():
    """Merge sentiment + market prices into a feature dataset."""
    sentiment_df = load_sentiment_data()
    market_df = load_market_data()

    # Flatten sentiment tickers (each record may have multiple tickers)
    records = []
    for _, row in sentiment_df.iterrows():
        tickers = row.get("tickers", [])
        for t in tickers:
            records.append({
                "ticker": t,
                "sentiment": row.get("sentiment", "Neutral"),
                "source": row.get("source", ""),
                "published_at": row.get("published_at", "")
            })
    sentiment_flat = pd.DataFrame(records)

    if sentiment_flat.empty:
        raise ValueError("No sentiment-ticker mappings found.")

    # Encode sentiment
    sentiment_flat = encode_sentiment(sentiment_flat)

    # Aggregate by ticker → average sentiment
    agg_sentiment = sentiment_flat.groupby("ticker")["sentiment_encoded"].mean().reset_index()
    agg_sentiment.rename(columns={"sentiment_encoded": "avg_sentiment"}, inplace=True)

    # Merge with market prices
    feature_df = market_df.merge(agg_sentiment, on="ticker", how="left")

    # Fill missing sentiment with Neutral (1)
    feature_df["avg_sentiment"].fillna(1.0, inplace=True)

    return feature_df


if __name__ == "__main__":
    df = build_feature_dataset()
    os.makedirs("data/features", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Features saved to {OUTPUT_FILE}")
    print(df.head())
