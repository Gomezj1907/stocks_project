import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json


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

    ftse_100.head()


    # Append .L to all tickers
    ftse_100['Ticker'] = ftse_100['Ticker'] + '.L'
    tickers = ftse_100["Ticker"].tolist()    
    return tickers

if __name__ == "__main__":
    tickers = scrape_ftse_100()
    update_json({"United Kingdom": {"FTSE 100": tickers}})
    print(f"✅ FTSE 100 tickers updated in JSON.")