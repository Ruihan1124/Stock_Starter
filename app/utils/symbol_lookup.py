import requests
from config import FINNHUB_API_KEY

def lookup_ticker_by_name(company_name: str):
    url = f"https://finnhub.io/api/v1/search?q={company_name}&token={FINNHUB_API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    if "result" not in data or len(data["result"]) == 0:
        print(f"❌ No ticker found for '{company_name}'")
        return None

    best_match = data["result"][0]
    print(f"🔍 Found: {best_match['description']} ({best_match['symbol']})")
    return best_match["symbol"]
