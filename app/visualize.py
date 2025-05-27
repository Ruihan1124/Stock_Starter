import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

# 📈 股票价格图（仅历史）
def plot_price_trend(df, save_path):
    plt.figure(figsize=(10, 4))
    plt.plot(df["ds"], df["y"], label="Stock Price", color="blue")
    plt.title("Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# 📈 股票 + 预测图
def plot_price_trend_with_forecast(df, save_path, forecast_df):
    plt.figure(figsize=(10, 4))
    plt.plot(df["ds"], df["y"], label="Actual Price", color="blue")

    forecast_future = forecast_df.tail(7)
    plt.plot(forecast_future["ds"], forecast_future["yhat"],
             label="Forecast (7-day)", color="red", linestyle="--")

    plt.title("Stock Price + 7-Day Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# 🟦 新闻情绪散点图
def plot_sentiment_timeline(df, save_path):
    if "datetime" in df.columns:
        df = df.sort_values("datetime")
        x = df["datetime"]
    else:
        df["index"] = range(len(df))
        x = df["index"]

    plt.figure(figsize=(8, 4))
    plt.scatter(x, df["score"], c="blue", alpha=0.6)
    plt.title("Sentiment Score Over Headlines")
    plt.xlabel("Time")
    plt.ylabel("Score")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# 🥧 情绪分布饼图
def plot_sentiment_distribution(df, save_path):
    counts = df["sentiment"].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140)
    plt.title("Sentiment Distribution")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# 📅 加权情绪折线图（过去 7 天）
def plot_daily_weighted_sentiment(df, save_path):
    source_weights = {
        "Bloomberg": 1.2,
        "Reuters": 1.1,
        "MarketWatch": 0.9,
        "CNBC": 1.0
    }

    df["weight"] = df["source"].map(source_weights).fillna(1.0)
    df["weighted_score"] = df["score"] * df["weight"]
    df["date"] = df["datetime"].dt.date

    daily = df.groupby("date")["weighted_score"].mean().tail(7)
    daily = daily.clip(-1, 1)

    plt.figure(figsize=(9, 4))
    plt.plot(daily.index, daily.values, marker='o', color='green')
    plt.title("Daily Weighted Sentiment (Past 7 Days)")
    plt.xlabel("Date")
    plt.ylabel("Score [-1, 1]")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
