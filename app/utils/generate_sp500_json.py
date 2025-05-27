import pandas as pd
import json
import os

# Wikipedia 表格 URL（标准 S&P 500 股票列表）
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def fetch_sp500_stocks():
    tables = pd.read_html(WIKI_URL)
    sp500_table = tables[0]  # 第一张表是我们要的
    stocks = []

    for _, row in sp500_table.iterrows():
        stocks.append({
            "ticker": row["Symbol"],
            "name": row["Security"]
        })

    return stocks

def save_to_json(data, filename="static/sp500_list.json"):
    os.makedirs("static", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(data)} stocks to {filename}")

if __name__ == "__main__":
    sp500_list = fetch_sp500_stocks()
    save_to_json(sp500_list)
