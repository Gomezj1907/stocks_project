import pandas as pd
import yfinance as yf
import json
import os

def fetch_prices(tickers, start_date, end_date):
    """
    Fetches closing prices for a list of tickers over a given date range and returns a DataFrame.

    Parameters
    ----------
    tickers : list
        List of stock tickers to fetch prices for.
    start_date : str
        Start date of the time range. Format: 'YYYY-MM-DD'
    end_date : str
        End date of the time range. Format: 'YYYY-MM-DD'

    Returns
    -------
    pd.DataFrame
        DataFrame with dates as index and tickers as columns.
    """
    data = pd.DataFrame()

    for ticker in tickers:
        try:
            print(f"⏳ Downloading: {ticker}")
            ticker_data = yf.download(ticker, start=start_date, end=end_date)
            data[ticker] = ticker_data['Close']
        except Exception as e:
            print(f"⚠️ Could not download {ticker}: {e}")

    return data


if __name__ == '__main__':
    from datetime import datetime

    # Leer tickers desde el archivo JSON
    with open('data/tickers_por_pais.json', 'r') as f:
        tickers = json.load(f)

    # Seleccionar una muestra: Dow Jones (USA)
    sample_tickers = tickers["United States1"]["Dow Jones"][:5]  # Usa el nombre correcto aquí
    start_date = '2024-01-01'
    end_date = datetime.today().strftime("%Y-%m-%d")

    print(f"\n🔍 Fetching data for: {sample_tickers}")
    df = fetch_prices(sample_tickers, start_date, end_date)

    print("\n✅ Preview of the resulting DataFrame:")
    print(df)
