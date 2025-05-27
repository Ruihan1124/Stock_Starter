import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from config import ALPHA_VANTAGE_API_KEY
from app.visualize import plot_price_trend_with_forecast
import logging
logging.basicConfig(filename='etl.log', level=logging.INFO)
from app.forecast import forecast_stock
from app.visualize import plot_price_trend_with_forecast


# Extract from Alpha Vantage
def extract_stock_data(ticker: str):
    print(f"[E] Extracting stock data for {ticker} from Alpha Vantage...")
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={ALPHA_VANTAGE_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    # print("📦 Raw API response:", data)  # 保留调试信息

    if "Time Series (Daily)" not in data:
        raise ValueError(f"❌ Failed to fetch data for {ticker}: {data.get('Note') or data.get('Error Message') or data.get('Information') or 'Unknown Error'}")

    timeseries = data["Time Series (Daily)"]
    records = []
    for date_str, day_data in timeseries.items():
        records.append({
            "ds": pd.to_datetime(date_str),
            "y": float(day_data["4. close"])
        })

    df = pd.DataFrame(records)
    df = df.sort_values("ds").reset_index(drop=True)
    print(f"✅ Downloaded {len(df)} rows of stock data for {ticker}.")
    return df

# Transform
def transform_stock_data(df: pd.DataFrame):
    print("[T] Transforming stock data...")
    df = df.dropna()
    print(f"[T] Cleaned data has {len(df)} rows.")
    return df

# Load
def load_stock_data(df_raw, df_clean, ticker: str):
    os.makedirs("data/stock_data/raw", exist_ok=True)
    os.makedirs("data/stock_data/processed", exist_ok=True)

    df_raw.to_csv(f"data/stock_data/raw/{ticker}_raw.csv", index=False)
    df_clean.to_csv(f"data/stock_data/processed/{ticker}_clean.csv", index=False)
    print("[L] Stock ETL completed and data saved.")

    os.makedirs("app/static", exist_ok=True)

    # Forecast and plot
    forecast_df = forecast_stock(df_clean)
    plot_price_trend_with_forecast(df_clean, f"app/static/{ticker}_price_trend.png", forecast_df)

    return forecast_df  # ✅ 把预测结果也返回出去


def run_stock_etl(ticker: str):
    df_raw = extract_stock_data(ticker)
    df_clean = transform_stock_data(df_raw)
    forecast_df = load_stock_data(df_raw, df_clean, ticker)
    logging.info(f"{ticker} stock ETL completed.")
    return df_clean, forecast_df



