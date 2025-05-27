import requests
import re
from config import GEMINI_API_KEY

# Gemini Summary: for initial analysis
def generate_gemini_summary(ticker, df_price, df_forecast, df_sentiment):
    summary = f"""
You are an AI stock analysis assistant.

Stock: {ticker}

- Past 5-day Close Prices: {df_price['y'].tail(5).tolist()}
- 7-Day Forecasted Prices: {df_forecast['yhat'].tail(7).tolist()}
- First 5 News Sentiment Scores: {df_sentiment['score'].head(5).tolist()}

Based on the above, briefly suggest if a short-term investor should go long or short. Justify in 2–3 sentences.
"""
    return call_gemini(summary)

# Gemini Chat: for follow-up conversation
def generate_gemini_reply(user_msg):
    return call_gemini(user_msg)

# Clean up Gemini response formatting
def clean_gemini_response(text):
    # 替换重复的符号组合，如 ":*•"、"*•"、"**"
    text = re.sub(r"[:\*]*•", "•", text)            # 清理项目符号
    text = re.sub(r"\*\*", "", text)                # 去除粗体符号
    text = re.sub(r"\*", "", text)                  # 去除残留的单个星号
    text = re.sub(r"\n{3,}", "\n\n", text)           # 避免多个空行
    return text.strip()

# Unified Gemini API caller
def call_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        cleaned = clean_gemini_response(text)
        return cleaned

    except Exception as e:
        return f"❌ Gemini error: {str(e)}"

