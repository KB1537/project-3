"""
Inventory Management CLI with Google Sheets Sync
------------------------------------------------
Features:
- Pull inventory from Google Sheets
- Update stock and auto-record sales
- Auto-calculate total price: qty * unit price
- Push updated stock + sales back to Google Sheets
"""

"""
Google Sheets Structure:
Sheet1: Inventory → SKU | Name | Quantity | Price
Sheet2: Sales     → Date | SKU | Qty Sold | Price | Customer
"""

import os
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials



# ---------------- GOOGLE SHEETS CONNECTION ---------------- #

SCOPE=[
 "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"

]

CREDS=Credentials.from_service_account_file('creds/creds.json')
SCOPED_CREDS=CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)


# Open Google Sheet
SHEET=GSPREAD_CLIENT.open('Inventory_Manager')
INVENTORY_WS = SHEET.worksheet("Inventory")
SALES_WS = SHEET.worksheet("Sales")



# ---------------------------------------------------------- #
#                      LOAD INVENTORY                        #
# ---------------------------------------------------------- #

def load_inventory():
    """
    Load inventory into a list of dicts from Google Sheets.
    Columns: SKU, Name, Stock, Price, Category
    """
    data = INVENTORY_WS.get_all_values()[1:]  # skips header row
    inventory = []

    for row in data:
        if len(row) < 5:
            continue

        inventory.append({
            "sku": row[0],
            "name": row[1],
            "stock": int(row[2]),
            "price": float(row[3]),
            "category": row[4]
        })

    print(f"✓ Loaded {len(inventory)} items from Google Sheets.")
    return inventory

# ---------------------------------------------------------- #
#                    SAVE INVENTORY BACK                     #
# ---------------------------------------------------------- #

def save_inventory(inventory):
    """
    Save the inventory list back to Google Sheets.
    Overwrites sheet contents except header.
    """
    rows = [[item["sku"], item["name"], item["stock"], item["price"], item["category"]]
            for item in inventory]

    INVENTORY_WS.update('A2', rows)
    print("✓ Inventory synced to Google Sheets.")