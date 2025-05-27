from app.etl.stock_etl import run_stock_etl
from app.etl.news_etl import run_news_etl
from app.utils.symbol_lookup import lookup_ticker_by_name
from config import FINNHUB_API_KEY
import logging
logging.basicConfig(filename='etl.log', level=logging.INFO)


# === Manually enter company name or ticker ===
user_input = input("🔍 Enter company name or stock ticker (e.g., Tesla, AAPL): ").strip()

# === Try to look up ticker from company name ===
ticker = lookup_ticker_by_name(user_input)

# If not found, fallback: assume user input was already a ticker
if not ticker:
    print(f"⚠️ Couldn't find ticker for '{user_input}', treating it as ticker directly.")
    ticker = user_input.upper()

# debug
# print(f"\n✅ Running ETL for: {ticker}\n")

try:
    # Stock price ETL
    run_stock_etl(ticker)

    # News sentiment ETL
    run_news_etl(ticker)

    print(f"\n✅ ETL for {ticker} completed successfully.")
    logging.info(f"{ticker} full ETL completed successfully.")
except Exception as e:
    print(f"\n❌ ETL failed for {ticker}: {e}")

