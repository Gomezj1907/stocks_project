import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json
from data.connection import connect_db



def scrape_dow_jones():

    """
    Scrapes the Dow Jones Industrial Average from Wikipedia and returns the list of tickers.

    Returns
    -------
    list
        A list of tickers for the Dow Jones Industrial Average constituents.
    """
    
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    response = r.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    components_table = soup.find("table", {"id": "constituents"})

    rows = components_table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    headers.pop(0)

    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            data.append([td.text.strip() for td in cols])

    djia = pd.DataFrame(data, columns=headers)

    djia.head()

    djia.rename(columns={"Symbol": "Ticker"}, inplace=True)
    djia['name'] = djia['Company']
    djia['sector'] = djia['Industry']
    djia['country'] = 'United States'
    djia["source_index"] = "Dow Jones Industrial Average"

    return djia[['Ticker', 'name', 'sector', 'country', 'source_index']]

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
    df = scrape_dow_jones()
    con = connect_db()
    update_json({"United States1": {"Dow Jones": df['Ticker'].tolist()}})
    print("✅ Dow Jones tickers updated in JSON.")
    insert_metadata(df, con)
    con.colose()
    print("✅ Dow Jones metadata inserted into database.")