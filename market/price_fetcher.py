# market/price_fetcher.py
"""
Market Price Fetcher (Dynamic Tickers)
--------------------------------------
- Reads tickers from processed sentiment JSON files
- Fetches latest stock/crypto prices using Yahoo Finance (yfinance)
- Saves results into data/processed/market_prices.json to JSON


"""

import os
import json
from datetime import datetime
import yfinance as yf

# Paths for the data 
DATA_DIR = "data/processed"
PROCESSED_FILES = [
    os.path.join(DATA_DIR, "reddit_with_sentiment.json"),
    os.path.join(DATA_DIR, "news_with_sentiment.json")
]
OUTPUT_FILE = os.path.join(DATA_DIR, "market_prices.json")

def extract_tickers(files):
    """Extract unique tickers from processed JSON files."""
    tickers = set()
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"[WARN] File not found: {file_path}")
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            tickers.update(item.get("tickers", []))
    return list(tickers)

def fetch_prices(tickers):
    """Fetch latest prices from Yahoo Finance."""
    prices = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist["Close"].iloc[-1]
                prices[ticker] = {
                    "price": float(price),
                    "timestamp": datetime.utcnow().isoformat()
                }
                print(f"[INFO] {ticker}: {price}")
            else:
                print(f"[WARN] No data for {ticker}")
        except Exception as e:
            print(f"[ERROR] Could not fetch {ticker}: {e}")
    return prices

def save_prices(prices, output_path):
    """Save fetched prices to JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=2)
    print(f"[INFO] Saved prices to {output_path}")

if __name__ == "__main__":
    tickers = extract_tickers(PROCESSED_FILES)
    if not tickers:
        print("[WARN] No tickers found. Exiting.")
    else:
        prices = fetch_prices(tickers)
        save_prices(prices, OUTPUT_FILE)
