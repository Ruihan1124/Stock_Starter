import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import FINNHUB_API_KEY
from app.sentiment import analyze_sentiment_titles
from app.visualize import plot_sentiment_distribution, plot_sentiment_timeline
from app.visualize import plot_daily_weighted_sentiment
import logging
logging.basicConfig(filename='etl.log', level=logging.INFO)

# Extract
def extract_news_data(ticker: str):
    print(f"[E] Extracting news for {ticker}...")
    end = datetime.today()
    start = end - timedelta(days=7)
    url = (
        f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={start.date()}&to={end.date()}&token={FINNHUB_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    print(f"[E] Fetched {len(data)} articles.")
    return data

# Transform
def transform_news_data(news_json):
    print("[T] Transforming news data...")
    # 提取 headline + source + datetime
    rows = []
    for item in news_json:
        if "headline" in item and "source" in item and "datetime" in item:
            rows.append({
                "headline": item["headline"],
                "source": item["source"],
                "datetime": pd.to_datetime(item["datetime"], unit="s")
            })

    df_raw = pd.DataFrame(rows)

    # 分析情绪
    df_sentiment = analyze_sentiment_titles(df_raw["headline"].tolist())

    # 合并情绪结果与原始 source, datetime
    df = pd.concat([df_raw.reset_index(drop=True), df_sentiment], axis=1)

    df["date"] = datetime.today().date()
    print(f"[T] Transformed {df.shape[0]} headlines with sentiment labels.")
    return df

# Load
def load_news_data(news_json, df_sentiment, ticker: str):
    os.makedirs("data/news_data/raw", exist_ok=True)
    os.makedirs("data/news_data/processed", exist_ok=True)

    with open(f"data/news_data/raw/{ticker}_news_raw.json", "w", encoding="utf-8") as f:
        json.dump(news_json, f, indent=2)

    df_sentiment.to_csv(f"data/news_data/processed/{ticker}_sentiment.csv", index=False)
    print("[L] News ETL completed and data saved.")

    # 可视化图表保存
    os.makedirs("app/static", exist_ok=True)
    plot_sentiment_timeline(df_sentiment, f"app/static/{ticker}_sentiment_line.png")
    plot_sentiment_distribution(df_sentiment, f"app/static/{ticker}_sentiment_pie.png")
    plot_daily_weighted_sentiment(df_sentiment, f"app/static/{ticker}_daily_sentiment.png")  # 👈 添加这一行



def run_news_etl(ticker: str):
    raw_news = extract_news_data(ticker)
    sentiment_df = transform_news_data(raw_news)
    load_news_data(raw_news, sentiment_df, ticker)
    logging.info(f"{ticker} news ETL completed.")
    return sentiment_df

