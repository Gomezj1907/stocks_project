import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json
from data.connection import connect_db

def scrape_ftse_100():
    
    """
    Scrapes the FTSE 100 index from Wikipedia and returns the list of tickers.

    The function fetches the HTML content of the FTSE 100 Wikipedia page and
    parses it to extract stock tickers. It identifies list items containing 
    tickers with the pattern 'EPS' followed by numbers, cleans them, and 
    appends '.L' to each ticker to indicate the London Stock Exchange.

    Returns
    -------
    list
        A list of tickers for the FTSE 100 constituents.
    """
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    response = r.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    components_table = soup.find("table", {"id": "constituents"})

    rows = components_table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            data.append([td.text.strip() for td in cols])

    ftse_100 = pd.DataFrame(data, columns=headers)

    # Clean and format
    
    ftse_100['Ticker'] = ftse_100['Ticker'] + '.L'
    ftse_100['name'] = ftse_100['Company']
    ftse_100['sector'] = ftse_100['FTSE industry classification benchmark sector[28]']
    ftse_100["country"] = "United Kingdom"
    ftse_100["source_index"] = "FTSE 100"

    return ftse_100[["Ticker", "name", "sector", "country", "source_index"]]

    
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
    df = scrape_ftse_100()
    con = connect_db()
    update_json({"United Kingdom": {"FTSE 100": df['Ticker'].tolist()}})
    print(f"✅ FTSE 100 tickers updated in JSON.")
    insert_metadata(df, con)
    con.close()
    print(f"✅ FTSE 100 metadata inserted into database.")
    
    
