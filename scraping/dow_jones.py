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


    data = []
    for row in rows[1:]:
        company_cell = row.find('th')
        cols = row.find_all('td')
        
        if company_cell and cols:
            row_data = [company_cell.text.strip()] + [td.text.strip() for td in cols]
            data.append(row_data)

    djia = pd.DataFrame(data, columns=headers)

    djia.head()

    djia.rename(columns={"Symbol": "Ticker"}, inplace=True)
    djia['name'] = djia['Company']
    djia['sector'] = djia['Industry']
    djia['country'] = 'United States'
    djia["source_index"] = "Dow Jones Industrial Average"

    return djia[['Ticker', 'name', 'sector', 'country', 'source_index']]

def insert_metadata(df, con):
        
    """
    Inserts metadata from a DataFrame into the tickers_metadata table in the database.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing metadata with columns: 'Ticker', 'name', 'sector', 'country', 'source_index'.
    con : psycopg2.extensions.connection
        Connection object to the PostgreSQL database.

    Notes
    -----
    - This function uses a SQL INSERT statement with ON CONFLICT to avoid inserting duplicate tickers.
    - The database connection is committed after all rows are inserted.
    - The cursor is closed after the operation is complete.
    """

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
    con.close()
    print("✅ Dow Jones metadata inserted into database.")