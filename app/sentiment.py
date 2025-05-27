from transformers import pipeline
import pandas as pd

def analyze_sentiment_titles(headlines: list):
    classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    results = classifier(headlines)
    df = pd.DataFrame({
        "headline": headlines,
        "sentiment": [r["label"] for r in results],
        "score": [r["score"] for r in results]
    })
    return df
