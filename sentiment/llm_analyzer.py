import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_text(text: str) -> dict:
    """
    Analyze financial sentiment and extract tickers from text using LLM.
    Returns a dict with sentiment + tickers.
    """
    prompt = f"""
    You are a financial sentiment and ticker analyzer.

    Task:
    1. Classify the sentiment of the following text as Positive, Negative, or Neutral.
    2. Extract any stock or crypto tickers (e.g., AAPL, TSLA, BTC-USD).
    3. If no tickers are found, return an empty list.

    Text: "{text}"

    Return ONLY valid JSON:
    {{
        "sentiment": "...",
        "tickers": ["..."]
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        result = json.loads(response["choices"][0]["message"]["content"].strip())
    except Exception:
        result = {"sentiment": "Neutral", "tickers": []}

    return result

def analyze_dataset(dataset: list, text_fields=("title", "body", "description", "content")) -> list:
    """
    Takes a list of JSON objects (Reddit or News articles),
    extracts text fields, and returns with sentiment + tickers attached.
    """
    results = []
    for item in dataset:
        combined_text = " ".join([item.get(field, "") for field in text_fields if item.get(field)])
        analysis = analyze_text(combined_text)
        item["sentiment"] = analysis["sentiment"]
        item["tickers"] = analysis["tickers"]
        results.append(item)
    return results
