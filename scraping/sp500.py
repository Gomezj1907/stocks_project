import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json
from data.connection import connect_db

def scrape_sp500():
    
    """
    Scrapes the S&P 500 from Wikipedia and returns the list of tickers.

    Returns
    -------
    list
        A list of tickers for the S&P 500 constituents.
    """
    
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = r.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    components_table = soup.find("table", {"id": "constituents"})

    rows = components_table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    #headers.pop(0)

    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            data.append([td.text.strip() for td in cols])

    sp500 = pd.DataFrame(data, columns=headers)

    sp500.head()

    sp500.rename(columns={"Symbol": "Ticker"}, inplace=True)
    sp500["Ticker"] = sp500["Ticker"].str.replace(".B", "-B")
    sp500["name"] = sp500["Security"]
    sp500["sector"] = sp500["GICS Sector"]
    sp500["country"] = "United States"
    sp500["source_index"] = "S&P500"
    
    
    return sp500[["Ticker", "name", "sector", "country", "source_index"]]

def insert_metadata(df, con):
    
    cursor = con.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
                       INSERT INTO tickers_metadata (ticker, name, sector, country, source_index)
                       VALUES (%s, %s, %s, %s, %s)
                       ON CONFLICT (ticker) DO NOTHING;
                       """, (row['Ticker'], row['name'], row['sector'], row['country'], row['source_index']))
    con.commit()
    cursor.close()
    
    
    
if __name__ == "__main__":
    df = scrape_sp500()
    update_json({"United States2": {"S&P500": df["Ticker"].tolist()}})
    print(f"✅ S&P500 tickers updated in JSON.")
    con = connect_db()
    insert_metadata(df, con)
    con.close()
    print(f"✅ S&P500 metadata inserted into database.")
