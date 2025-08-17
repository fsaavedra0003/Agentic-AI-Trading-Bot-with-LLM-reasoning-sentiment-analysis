import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of a single text with LLM."""
    prompt = f"""
    Classify the financial sentiment of the following text:
    - Positive
    - Neutral
    - Negative

    Text: "{text}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response["choices"][0]["message"]["content"].strip()

def analyze_dataset(dataset: list, text_fields=("title", "body")) -> list:
    """
    Takes a list of JSON objects (Reddit or News articles),
    extracts text fields, and returns with sentiment attached.
    """
    results = []
    for item in dataset:
        combined_text = " ".join([item.get(field, "") for field in text_fields if item.get(field)])
        sentiment = analyze_sentiment(combined_text)
        item["sentiment"] = sentiment
        results.append(item)
    return results
