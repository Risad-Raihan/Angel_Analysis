import pyodbc
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# Step 3.1: Connect to SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=103.197.207.66,1433;'
    'DATABASE=APON;'
    'UID=apontech;'
    'PWD=Db@9345#'
)

# Step 3.2: Run the Query
query = """
SELECT 
  h.strWarehouseName AS Outlet,
  r.strItemCode AS "Item Code",
  r.strItemName AS "Item Name",
  i.strItemSubCategoryName AS "Item Sub Category",
  CASE
    WHEN  i.strItemSubCategoryName IN ('Baby Food', 'Baby Oral Care', 'Baby Shampoo', 'Baby Soap', 'Baby Powder', 'Baby Lotion', 'Baby Cream', 'Baby Oil', 'Baby Hair Oil', 'Baby Diapers') THEN 'Baby Essentials'
    WHEN  i.strItemSubCategoryName IN ('Bathroom Cleaner', 'Floor Cleaner', 'Glass Cleaner') THEN 'Cleaning Item'
    WHEN  i.strItemSubCategoryName IN ('Dal', 'Flour', 'Mustard Oil', 'Salt', 'Sugar', 'Chinigura Rice', 'Spices', 'Cooking Essentials', 'Condensed Milk', 'Whole Spice', 'Rice Bran Oil') THEN 'Commodities'
    WHEN  i.strItemSubCategoryName IN ('Milk Powder', 'UHT Milk', 'Ghee') THEN 'Dairy'
    WHEN  i.strItemSubCategoryName IN ('Egg', 'Fruits', 'Fish', 'Meat', 'Vegetables') THEN 'Perishable'
    WHEN  i.strItemSubCategoryName IN ('Rice') THEN 'Rice'
    WHEN  i.strItemSubCategoryName IN ('Tiffin Item -1', 'Tiffin Item -2', 'Noodles', 'Non-Fried Snack', 'Home-made Snacks', 'Family Pack', 'Combo Pack', 'Beverages', 'Water', 'Sweets', 'Soup', 'Soft Drink Powder', 'Breakfast', 'Shemai') THEN 'Snacks'
    WHEN  i.strItemSubCategoryName IN ('Soybean Oil') THEN 'Soybean Oil'
    WHEN  i.strItemSubCategoryName IN ('Bath Soap', 'Oral Care', 'Shampoo', 'Dish Wash', 'Face Cream', 'Hair Oil', 'Facewash', 'Body Spray', 'Body Powder', 'Handwash', 'Hair Remover', 'Personal Care', 'Petroleum Jelly', 'Body Wash', 'Shaving Item', 'Nail Polish', 'Body Lotion', 'Glycerin', 'Nail Polish Remover', 'Basket', 'Body Oil', 'Face wash') THEN 'Toiletries'
    ELSE 'Others'
  END AS 'Big Block',
  SUM(numQuantity) AS "Total Quantity",
  SUM(r.numDeliveryValue) AS "Total Sales Amount",
  r.numCOGS as Total_COGS
FROM 
  [APON].[pos].[tblPosDeliveryRow] r
JOIN 
  [APON].[pos].[tblPosDeliveryHeader] h ON h.intDeliveryId = r.intDeliveryId
JOIN
  [APON].[itm].[tblItem] i ON r.intItemId = i.intItemId
WHERE 
  h.isActive = 1 
  AND r.isActive = 1 
  AND h.dteDeliveryDate BETWEEN '2024-05-01' AND GETDATE()
GROUP BY 
  h.strWarehouseName,
  r.strItemCode, 
  r.strItemName, 
  i.strItemSubCategoryName,
  r.numCOGS
"""

# Read SQL query results into a DataFrame
df = pd.read_sql(query, conn)

# Close the SQL connection
conn.close()

# Set up Google Sheets credentials
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('axial-coyote-380606-df56768f3817.json', scopes=scopes)

# Authorize access to Google Sheets
gc = gspread.authorize(credentials)

# Open a Google Sheet by its key
gs = gc.open_by_key('1srUhOm0429oBjke4d9ja4f56jUPAxVSv3OI5h2Pc7Xo')

# Select a specific worksheet from the Google Sheet (optional)
# worksheet = gs.worksheet("Name of your worksheet")

# Export DataFrame to Google Sheet
set_with_dataframe(gs.sheet1, df)  # Write DataFrame to the default sheet in the Google Sheet

print("DataFrame successfully exported to Google Sheet!")
