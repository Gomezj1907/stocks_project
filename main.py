import pandas as pd
import json
from datetime import datetime
from scraping import scrape_dow_jones
from scraping import scrape_sp500
from scraping import scrape_ftse_100
from scraping import scrape_hanseng
from scraping import scrape_nikkei
from scraping import scrape_sti

from services import fetch_prices

from sheets.upload_to_sheets import publish_to_gsheets

def main():
    print("🚀 Starting scraping process...")

    # Llamadas a las funciones de scraping
    scrape_dow_jones()
    scrape_sp500()
    scrape_nikkei()
    scrape_sti()
    scrape_ftse_100()
    scrape_hanseng()

    print("✅ All index tickers successfully scraped and saved to JSON.")
    
    #-- Load tickers---#
    with open('data/tickers_por_pais.json', 'r') as f:
        tickers_data = json.load(f)
    
    #Date ranges
    start_date = '2025-04-03'
    end_date = datetime.today().strftime("%Y-%m-%d")
    
    # Iterate over the different datas 
    for country, indexes in tickers_data.items():
        for index_name, tickers in indexes.items():
            print(f"\n🔍 Fetching data for: {index_name} in {country}")
            
            try:
                prices_df = fetch_prices(tickers, start_date, end_date)
                
                # Convertir índice de fecha en columna explícita
                if isinstance(prices_df.index, pd.DatetimeIndex):
                    prices_df = prices_df.reset_index()
                
                prices_df.rename(columns={'index': 'Date'}, inplace=True)
                
                safe_index_name = index_name.replace(" ", "_")
                safe_country_name = country.replace(" ", "_")
                sheet_tab = f"{safe_country_name}_{safe_index_name}"
                
                # publish to gsheets
                publish_to_gsheets(prices_df, sheet_tab)
                print(f"✅ Data published to Google Sheets in tab '{sheet_tab}'")


            except Exception as e:
                print(f"⚠️ Error fetching/publishing data for {index_name} in {country}: {e}")
                
        print("\n✅ All data successfully exported to gsheets.") 
                

if __name__ == "__main__":
    main()
