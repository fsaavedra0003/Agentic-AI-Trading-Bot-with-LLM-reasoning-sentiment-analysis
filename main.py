#Import json library
import json
from sentiment.llm_analyzer import analyze_dataset

if __name__ == "__main__":
    # Load raw Reddit posts
    with open("data/raw/reddit_posts.json", "r", encoding="utf-8") as f:
        reddit_posts = json.load(f)

    # Load raw News articles
    with open("data/raw/news.json", "r", encoding="utf-8") as f:
        news_articles = json.load(f)

    # Analyze Reddit posts with LLM
    reddit_with_sentiment = analyze_dataset(reddit_posts, text_fields=("title", "body"))

    # Analyze News articles with LLM
    news_with_sentiment = analyze_dataset(news_articles, text_fields=("title", "description"))

    # Save to processed folder
    with open("data/processed/reddit_with_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(reddit_with_sentiment, f, indent=2, ensure_ascii=False)

    with open("data/processed/news_with_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(news_with_sentiment, f, indent=2, ensure_ascii=False)

    print("[INFO] Sentiment analysis complete and saved.")
