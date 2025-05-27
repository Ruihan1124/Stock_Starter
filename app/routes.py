import json
from flask import Blueprint, render_template, request, jsonify
from app.etl.stock_etl import run_stock_etl
from app.etl.news_etl import run_news_etl
from app.utils.symbol_lookup import lookup_ticker_by_name
from app.gemini import generate_gemini_summary, generate_gemini_reply

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        company = request.form.get("company")
        ticker = lookup_ticker_by_name(company) or company.upper()

        df_price, df_forecast = run_stock_etl(ticker)
        df_sentiment = run_news_etl(ticker)

        gemini_response = generate_gemini_summary(ticker, df_price, df_forecast, df_sentiment)

        return render_template("result.html", ticker=ticker, analysis=gemini_response)

    # ✅ 后端加载 sp500_list.json 用于 index.html 渲染
    with open("static/sp500_list.json", "r", encoding="utf-8") as f:
        sp500_list = json.load(f)

    return render_template("index.html", sp500_list=sp500_list)


@main.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"response": "Please enter a question."})
    reply = generate_gemini_reply(user_msg)
    return jsonify({"response": reply})


