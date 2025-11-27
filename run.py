"""
Inventory Management CLI with Google Sheets Sync
------------------------------------------------
Features:
- Pull inventory from Google Sheets
- Update stock and auto-record sales
- Auto-calculate total price: qty * unit price
- Push updated stock + sales back to Google Sheets
"""

import os
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials


SCOPE=[
 "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"

]

CREDS=Credentials.from_service_account_file('creds/creds.json')
SCOPED_CREDS=CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)
SHEET=GSPREAD_CLIENT.open('Inventory_Manager')


sales=SHEET.worksheet('Sales')

data=sales.get_all_values()

print(data)