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
from tabulate import tabulate 



# ----------------------------------------------------------#
#                  GOOGLE SHEETS CONNECTION                 #
# ----------------------------------------------------------#

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




# ----------------------------------------------------------#
#                  HELPER FUNCTIONS                         #
# ----------------------------------------------------------#

def clean_price(value):
    """
    Remove currency symbols and commas so the value can convert to a float.
    Example: '£3,150.00' → 3150.00
    """
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = (
        value.replace("£", "")
        .replace("$", "")
        .replace(",", "")
        .strip()
    )
    return float(cleaned)


def validate_quantity(qty):
    if qty <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return qty


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Invalid date. Use YYYY-MM-DD.")



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


# ---------------------------------------------------------- #
#                     RECORD SALES DATA                      #
# ---------------------------------------------------------- #

def record_sale(sku, qty_sold, price, customer="Walk-in"):
    """
    Append a sale to the Sales sheet.
    Automatically calculates Total Price.
    """
    date = datetime.now().strftime("%Y-%m-%d")
    total_price = qty_sold * price

    SALES_WS.append_row([
        date, sku, qty_sold, price, total_price, customer
    ])

    print(f"✓ Sale recorded: £{total_price:.2f}")


# ---------------------------------------------------------- #
#                 DAILY SALES REPORT FUNCTION                #
# ---------------------------------------------------------- #

def total_sales_for_date():
    """
    Ask the user for a date (YYYY-MM-DD), then show all sales for that day.
    Displays SKU, Qty, Price, Total Price, Customer and daily revenue total.
    """

    date_input = input("Enter date (YYYY-MM-DD):\n ").strip()

    # Validate date format
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    # Read every row from the Sales sheet (skip header)
    sales_data = SALES_WS.get_all_values()[1:]

    print(f"\n--- SALES REPORT FOR {date_input} ---")

    total_revenue = 0
    found = False

    for row in sales_data:
        sale_date = row[0]

        if sale_date == date_input:
            found = True
            sku = row[1]
            qty = row[2]
            price = row[3]
            total = row[4]
            customer = row[5] if len(row) > 5 else "Unknown"

            print(
                f"SKU: {sku} | Qty: {qty} | Price: £{price} | "
                f"Total: £{total} | Customer: {customer}"
            )

            total_revenue += clean_price(total)

    if not found:
        print("No sales recorded for this date.")
    else:
        print(f"\nTOTAL REVENUE FOR {date_input}: £{total_revenue:.2f}")


# ---------------------------------------------------------- #
#                      INVENTORY ACTIONS                     #
# ---------------------------------------------------------- #

def view_inventory(inventory):
    headers = ["SKU", "Name", "Stock", "Price (£)", "Category"]
    table = []

    for item in inventory:
        table.append([
            item['sku'],
            item['name'],
            item['stock'],
            f"{item['price']:.2f}",
            item['category']
        ])

    print("\n--- INVENTORY ---")
    print(tabulate(table, headers=headers, tablefmt="grid"))


def find_item(inventory, sku):
    for item in inventory:
        if item["sku"].lower() == sku.lower():
            return item
    return None


def update_stock(inventory):
    """
    Reduce stock, record as a sale, then push updates to Google Sheets.
    """
    sku = input("Enter SKU:\n ").strip()
    item = find_item(inventory, sku)

    if not item:
        print("❌ SKU not found.")
        return

    try:
        qty = int(input("Quantity sold:\n "))
    except ValueError:
        print("❌ Invalid quantity.")
        return

    if qty > item["stock"]:
        print("❌ Not enough stock!")
        return



    
    # Reduce local stock
    item["stock"] -= qty
    print(f"✓ New stock level: {item['stock']}")

    # Record sale in Google Sheets
    record_sale(item["sku"], qty, item["price"])

    # Push updated inventory back to Sheets
    save_inventory(inventory)


# ---------------------------------------------------------- #
#                        MENU SYSTEM                         #
# ---------------------------------------------------------- #

def main():
    inventory = load_inventory()

    while True:
        print("\n--- MAIN MENU ---")
        print("1. View Inventory")
        print("2. Record Sale (Update Stock)")
        print("3. Reload Data From Google Sheets")
        print("4. Total Sales for a Date")  
        print("5. Exit")                    

        option = input("Choose an option:\n ")

        if option == "1":
            view_inventory(inventory)
        elif option == "2":
            update_stock(inventory)
        elif option == "3":
            inventory = load_inventory()
        elif option == "4":
            total_sales_for_date()
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid selection.")


# ---------------------------------------------------------- #
#                           RUN                              #
# ---------------------------------------------------------- #

if __name__ == "__main__":
    main()