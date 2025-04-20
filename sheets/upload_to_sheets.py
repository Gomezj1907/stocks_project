import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from config.settings import GSHEET_KEY

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)



def publish_to_gsheets(df, sheet_tab):
    
    """
    Publishes a DataFrame to a specified Google Sheets worksheet.
    If the sheet exists, it clears it before writing.
    If the sheet does not exist, it creates one.
    """
    gc = gs.authorize(credentials)
    spreadsheet = gc.open_by_key(GSHEET_KEY)  # cambia a tu variable si usas otra forma
    
    try:
        worksheet = spreadsheet.worksheet(sheet_tab)
        worksheet.clear()  # limpia todo antes de escribir
        print(f"📄 Sheet '{sheet_tab}' found and cleared.")
        
    except gs.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_tab, rows="1000", cols="20")
        print(f"🆕 Sheet '{sheet_tab}' created.")

    set_with_dataframe(worksheet, df)
    print(f"✅ Data published to Google Sheets tab '{sheet_tab}'")


if __name__ == "__main__":
    pass