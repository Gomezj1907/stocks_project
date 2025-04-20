✅ README.md

# 📈 Global Stock Index Tracker

This Python project tracks the performance of stocks across major global indices, fetching data from Yahoo Finance and publishing it to Google Sheets. The goal is to analyze top and bottom performers over time using a fully automated pipeline.

---

## 🌍 Tracked Indices

- 🇺🇸 Dow Jones Industrial Average (DJI)
- 🇺🇸 S&P 500
- 🇯🇵 Nikkei 225
- 🇸🇬 Straits Times Index (STI)
- 🇬🇧 FTSE 100
- 🇭🇰 Hang Seng Index (HSI)

---

## 🔧 Project Structure


```bash

├── main.py                       # Main script to scrape and publish
├── scraping/                    # Individual modules to scrape index tickers
│   ├── scrape_dow_jones.py
│   ├── scrape_sp500.py
│   └── ...
├── sheets/
│   └── upload_to_sheets.py      # Publishes dataframes to Google Sheets
├── services/
│   └── consult_yfinance.py          # Gets historical price data
├── utils/
│   └── json_writer.py        # code that updates tickers json
│   └── analysis.py        # Tools for calculating returns, rankings
├── data/
│   └── tickers_por_pais.json    # Contains index tickers by country
├── config/
│   └── credentials.json         # GSheets service credentials (ignored)
│   └── settings.py        # Include sheet key
├── .gitignore
├── README.md
└── requirements.txt             # Dependencies
```

⚙️ Setup

Clone the repo

    git clone https://github.com/YOUR_USERNAME/global-stock-tracker.git
    cd global-stock-tracker

Create and activate a virtual environment

    python -m venv stocks
    source stocks/bin/activate  # On Windows: stocks\Scripts\activate

Install dependencies

    pip install -r requirements.txt

Add your credentials

Place your Google Sheets API JSON in config/credentials.json.
🚀 Running the Pipeline

python main.py

This script will:

1. Scrape tickers from each index

2. Fetch historical stock prices (starting from 2024-04-03)

3. Publish prices to individual tabs in your connected Google Sheet

📊 Coming Soon

    analysis.py: Analyze top/bottom performers

    Scheduled automation with Power Automate / Task Scheduler

    Visual dashboards with Google Data Studio or Streamlit

🔒 Notes

Your credentials (credentials.json) are ignored by git via .gitignore

Be sure to share access to your GSheet with the service account email

🤝 License

MIT License.


---
