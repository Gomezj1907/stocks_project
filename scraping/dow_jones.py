import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json

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

    tickers = djia["Ticker"].tolist()

    return tickers


if __name__ == "__main__":
    tickers = scrape_dow_jones()
    update_json({"United States1": {"Dow Jones": tickers}})
    print(f"✅ Dow Jones tickers updated in JSON.")