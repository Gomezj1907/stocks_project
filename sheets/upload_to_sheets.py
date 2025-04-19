import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)



def publish_to_gsheets(df, sheet_tab):

    # Autenticación
    """
    Publishes a DataFrame to a specified Google Sheets worksheet.

    This function takes a Pandas DataFrame and uploads it to a specified
    worksheet in a Google Sheets document. If the worksheet does not exist,
    it will create a new one with default dimensions.

    :param df: The Pandas DataFrame to be published to the Google Sheets.
    :param sheet_tab: The name of the worksheet tab where the DataFrame should be published.
    """

    gc = gs.authorize(credentials)

# Abrir la hoja
     
    spreadsheet = gc.open_by_key("1KgFj0UpYmvfmxD0d2l44YMP_CBwzpQWKcVl_pG98Ch0")
    try:
        worksheet = spreadsheet.worksheet(sheet_tab)  # Cambia esto al nombre de la hoja
        set_with_dataframe(worksheet, df)

        
    except gs.exceptions.WorksheetNotFound:
        # dimensiones arbitrarias; ajústalas si necesitas más filas/columnas
        worksheet = spreadsheet.add_worksheet(title=sheet_tab, rows="1000", cols="20")
        
        set_with_dataframe(worksheet, df)



if __name__ == "__main__":
    pass