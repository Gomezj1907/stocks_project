import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json
import re


def scrape_hanseng():
    
    """
    Scrapes the Hang Seng Index from Wikipedia and returns the list of tickers.

    The function fetches the HTML content of the Hang Seng Index Wikipedia page and
    parses it to extract stock tickers. It identifies list items containing 
    tickers with the pattern 'SEHK:' followed by numbers, cleans them, and 
    appends '.HK' to each ticker to indicate the Hong Kong Stock Exchange.

    Returns
    -------
    list
        A list of tickers for the Hang Seng Index constituents.
    """
    
    url = "https://en.wikipedia.org/wiki/Hang_Seng_Index"
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

    hanseng = pd.DataFrame(data, columns=headers)

    hanseng.head()

    # Limpieza de caracteres invisibles y espacios
    hanseng['Ticker'] = hanseng['Ticker'].apply(lambda x: re.sub(r'\s+', '', x.replace('SEHK:', '')))    
    hanseng.head()

    hanseng['Ticker'] = hanseng['Ticker']+'.HK'
    # Add preceding 0 to complete 4 digits before .HK
    hanseng['Ticker'] = hanseng['Ticker'].apply(lambda x: x.zfill(7))
    
  
    tickers = hanseng["Ticker"].tolist() 
    return tickers


if __name__ == "__main__":
    tickers = scrape_hanseng()
    update_json({"Hong Kong": {"Hang Seng": tickers}})
    print(f"✅ Hang Seng tickers updated in JSON.")