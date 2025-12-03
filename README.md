# 📘 Inventory Manager - Command line Application 

Manage stock levels, record sales, and generate daily sales reports using a simple terminal-based Python application connected to Google Sheets.

# ⭐ Value 
Inventory Manager is a Python command-line application designed to maintain and update a live inventory dataset stored in Google Sheets.
It allows users to:

### View current inventory  

### Record product sales 

### Automatically update stock levels

### Store sales history in a linked Google Sheet

### Generate daily sales reports

### Display clean, easy-to-read tables in the terminal

This project demonstrates structured programming practices, data handling, algorithm implementation, and use of external APIs.

# Table of Contents

1. [Features](#features)  
2. [Technology Stack](#technology-stack)  
3. [Data Structure](#data-structure)  
4. [How to Set Up](#how-to-set-up)  
5. [How to Run](#how-to-run)  
6. [Testing](#testing)  
8. [Deployment](#deployment)  
9. [Credits](#credits)


# Features
##  View Inventory

### Displays your full inventory from Google Sheets in a formatted table using the tabulate library.

## Record a Sale (Update Stock)

- User enters SKU and quantity sold

- Application checks stock levels

- Updates stock in memory and Google Sheets

- Records the sale in the Sales worksheet

- Automatically timestamps the sale with today’s date

## Add New Products

Allows the user to add new stock items with:

- SKU

- Name

- Price

- Stock quantity

- Category

##  Daily Sales Reports

Generates a full report for a chosen date, including:

- SKU

- Quantity sold

- Unit price

- Total revenue per product

- Grand total for that day

Uses automatic currency cleaning to avoid formatting errors.

## Live Google Sheets Integration

Uses gspread and Google OAuth to automatically:

- Pull inventory data

- Push stock changes

- Append sales records


# Technology-stack 

| Component | Description| 
|---------|----------|
| Python3 | Core programming language    |      
| gspread | Google sheets intergration                         |   
| Google OAuth <br>(service account)  | Secure sheet access   |
| Tabulate        | pretty table layout      | 
| datetime | Automatic timestamping     | 
| Git & Github |  version controll and documentation         |
| Heroku/cloud deployment|Finale deployment target          |


# Data Structure 
### Inventory sheet(inventory) 
| Column| Example|Purpose |
|---------|----------|------|
| SKU| A001| Unique product ID|
| Name|Tv |  Product name|
| Stock| 12 | live quantity|
| price | 750 | Unit price|
| Category | Electronics |Sorting category | 



### Sales sheet (Sales)

| Column| Example|Purpose |
|---------|----------|------|
|    date |2025-07-01|  Auto generated date|
 SKU|  A001 |product sold 
|Quantity | 1 | units sold
| price| 219| price per unit 
|total|  1799.00| Auto calculated|
| Customer| optional | additional infomation|


# How to Set Up
### Install Dependencies
### pip install:
- Gspread
- Google-auth 
- Tabulate

### Add Credentials

### Create a folder named:

1. creds

2. Place your Google service account file here:

- creds/creds.json

3. Share Sheets with Service Account

Share your Google Sheet with this email (from your credentials file):

your-service-account@project.iam.gserviceaccount.com

4. Name Your Google Sheets Document

Your Google Sheet must be named:

- Inventory_Manager


With two worksheets:

1. Inventory

2. Sales


# How to Run
### python run.py


The menu will appear:

- [1] View Inventory
- [2] Record a Sale
- [3] Add a Product
- [4] Daily Sales Report
- [5] Exit

Use number keys to navigate the system.


# Testing
### manual testing was performed:

 - Input validation:

- Invalid SKUs

- Invalid quantities

- Negative numbers

- Empty strings

- Incorrect date input

##  Data integrity:

- Stock cannot go negative

- Sales always record correct totals

- Google Sheets successfully pushes/pulls updates

##  Error handling:

- API errors handled gracefully

- Value conversion protected with currency-cleaning function
- No errros returned from PEP8online.com 

# Deployment 
This project was deployed using code institue mock terminal for Heroku 

- Steps for deployment:
   - fork of clone the repository 
   - Create a new Heroku app
   - Set the buildpacks to **python** and **nodeJS** in that order 
   - Link the Heroku app to repository
   - click on deploy 

# Credits
- Project 3 template was created by code institue
- Google sheets api code was taken from love sandwhices project 