import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from utils.json_writer import update_json

def scrape_nikkei():
    
    """
    Scrapes the Nikkei 225 index from Wikipedia and returns the list of tickers.

    The function fetches the HTML content of the Nikkei 225 Wikipedia page and
    parses it to extract stock tickers. It identifies list items containing 
    tickers with the pattern 'TYO:' followed by numbers, cleans them, and 
    appends '.T' to each ticker to indicate the Tokyo Stock Exchange.

    Returns
    -------
    list
        A list of tickers for the Nikkei 225 constituents.
    """
     # URL de la página 

    url = 'https://en.wikipedia.org/wiki/Nikkei_225' 

    # Obtener HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tickers = []
    list_items = soup.find_all('li')

    for item in list_items:
        # Look for text containing TYO: followed by numbers
        if item.text and 'TYO:' in item.text:
            # Extract the ticker pattern (TYO: followed by digits)
            match = re.search(r'TYO:\s*(\d+)', item.text)
            if match:
                ticker = match.group(0)  # This gets "TYO: XXXX"
                tickers.append(ticker.replace(' ', ''))  # Remove spaces

    # Convert to DataFrame
    nikkei = pd.DataFrame(tickers, columns=['Ticker'])
    nikkei['Ticker'] = nikkei['Ticker'].str.replace('TYO:', '')

    nikkei['Ticker'] = nikkei['Ticker']+'.T'
    
    tickers = nikkei["Ticker"].tolist()
    return tickers


if __name__ == "__main__":
    tickers = scrape_nikkei()
    update_json({"Japan": {"Nikkei": tickers}})
    print(f"✅ Nikkei tickers updated in JSON.")