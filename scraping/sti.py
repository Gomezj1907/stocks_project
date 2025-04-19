import requests as r 
from bs4 import BeautifulSoup 
import pandas as pd
from utils.json_writer import update_json
import re
def scrape_sti():
        
    """
    Scrapes the Straits Times Index (STI) from Wikipedia and returns the list of tickers.

    Returns
    -------
    list
        A list of tickers for the STI constituents.

    """
    
    url = "https://en.wikipedia.org/wiki/Straits_Times_Index"
    response = r.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all('table', {'class': 'wikitable'})
    components_table = None
    for table in tables:
        caption = table.find('caption')
        if caption and 'List of STI constituents' in caption.text:
            components_table = table
            break
        
        
    rows = components_table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            data.append([td.text.strip() for td in cols])

    STI = pd.DataFrame(data, columns=headers)

    STI.head()

    STI.rename(columns={'Stock symbol': 'Ticker'}, inplace=True)
    
    # Limpieza de caracteres invisibles y espacios
    STI['Ticker'] = STI['Ticker'].apply(lambda x: re.sub(r'\s+', '', x.replace('SGX:', '')))    

    STI.head()
    STI['Ticker'] = STI['Ticker'] + '.SI'

    tickers = STI["Ticker"].tolist()
    
    return tickers

if __name__ == "__main__":
    tickers = scrape_sti()
    update_json({"Singapore": {"STI": tickers}})
    print(f"✅ STI tickers updated in JSON.")