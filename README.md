# 📈 Stock Starter - Sentiment & Forecast Dashboard

Stock Starter is a Flask-based interactive web app that allows users to explore any S\&P 500 stock through real-time sentiment analysis and short-term price forecasting.

This tool is ideal for retail investors, students, or anyone who wants a quick and visual overview of market trends—powered by FinBERT, Gemini AI, and Prophet.

---

## 🔍 Features

* 🔎 Type or select any S\&P 500 stock
* 📰 Run FinBERT-based news sentiment analysis
* 📈 Forecast stock prices with Prophet (7-day horizon)
* 🧠 Gemini AI answers questions about trends, risks, and suggestions
* 📊 Interactive visuals: price trends, sentiment timeline, distribution

---

## 🛠️ Technologies Used

* **Flask** – backend web framework
* **FinBERT** – sentiment analysis on financial news
* **Google Gemini API** – conversational and summary response
* **Alpha Vantage** – historical stock data (price)
* **Prophet** – stock trend forecasting
* **Matplotlib** – chart generation

---

## 🔁 ETL Flow Diagram

```mermaid
flowchart TD
    A[Input: Stock Ticker] --> B[Extract Stock Data --> from Alpha Vantage]
    A --> C[Extract News Data --> from Finnhub]
    B --> D[Clean & Save Stock Data]
    C --> E[Perform Sentiment Analysis --> using FinBERT]
    D --> F[Forecast Stock Price --> using Prophet]
    E --> G[Generate Sentiment Scores]
    F --> H[Plot Forecast Charts]
    G --> I[Summarize Insights with Gemini]


---

## 🚀 How to Run Locally
```

### 1. Clone the Repository

```bash
git clone https://github.com/Ruihan1124/Stock_Starter.git
cd stock-starter
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Set Your API Keys in `config.py`

```python
GEMINI_API_KEY = "your_google_gemini_api_key"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_api_key"
FINNHUB_API_KEY = "your_finnhub_api_key"
```

### 4. Generate S\&P 500 List

```bash
python app/utils/generate_sp500_json.py
```

### 5. Run the Flask App

```bash
python run.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
Stock-Starter/
├── app/
│   ├── etl/                          # ETL modules: extract-transform-load logic
│   │   ├── __init__.py              # Makes etl a Python package
│   │   ├── news_etl.py              # Extracts financial news & runs FinBERT sentiment
│   │   ├── stock_etl.py             # Fetches stock data & runs Prophet forecast
│   │
│   ├── utils/                        # Utility scripts
│   │   ├── generate_sp500_json.py   # Crawls Wikipedia to create sp500_list.json
│   │   ├── symbol_lookup.py         # Fuzzy mapping of company name → ticker
│   │
│   ├── gemini.py                     # Handles Gemini summary & follow-up Q&A
│   ├── routes.py                     # Flask route handlers (index, result, chat)
│
│   ├── Static/                       # Generated visualizations (note: capital 'S')
│   │   ├── *.png                    # Price trend, sentiment line, pie, etc.
│
├── static/                           # Lowercase: for Flask static files
│   ├── sp500_list.json              # Dropdown list of S&P 500 stocks
│
├── templates/                        # Jinja2 HTML templates
│   ├── index.html                   # Homepage: search + dropdown
│   ├── result.html                  # Results page: plots + Gemini chat
│
├── data/                             # Saved CSVs from ETL pipeline
│   ├── stock_data/
│   │   ├── raw/                     # Original price data (CSV)
│   │   ├── processed/              # Cleaned price data (used by Prophet)
│   ├── news_data/
│       ├── raw/                     # Raw scraped news
│       ├── processed/              # Sentiment-scored news

├── config.py                         # Stores API keys (Gemini, Alpha Vantage)
├── run.py                            # Entry point to launch Flask app
├── test_etl.py                       # Optional: test script for ETL modules
├── etl.log                           # Logs ETL pipeline output
├── .env                              # (Optional) environment variables (not committed)
├── .gitignore                        # Ignore logs, data, virtualenv, secrets, etc.
├── requirements.txt                  # List of Python dependencies
├── README.md                         # This file

```

---

## 🌐 Future Plans

* ✅ Gemini Q\&A support for stock trends and risks
* [ ] Deploy on Render / Vercel
* [ ] Add OAuth2 login + analysis history
* [ ] Allow multiple stocks & sector filtering
* [ ] Daily auto-refresh of sentiment scores


---

## ⚠️ Disclaimer & License

This project is licensed under the MIT License for its code and structure.

However, it makes use of third-party APIs and models:

- **Alpha Vantage** for stock prices (educational use only)
- **Google Gemini** for LLM summarization (subject to Google Cloud ToS)
- **FinBERT** for sentiment analysis (open model with citation)

Please ensure your usage complies with the respective providers' terms if deploying or redistributing.

---

## 🧠 Author

Built by \[Ruihan] — for educational and demo purposes. Contributions welcome!
