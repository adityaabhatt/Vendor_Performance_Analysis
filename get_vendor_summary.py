import sqlite3
import pandas as pd
import logging
import time
from ingestion_db import ingest_db

logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def create_vendor_summary(conn):
    '''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    summary_table = pd.read_sql_query("""WITH FreightSummary as(
    SELECT
        VendorNumber,
        SUM(Freight) as FreightCost
    FROM vendor_invoice
    GROUP BY VendorName
),

PurchaseSummary as (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price as ActualPrice,
        pp.Volume,
        SUM(p.Quantity) as TotalPurchaseQuantity,
        SUM(p.Dollars) as TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber,p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),
    
salesSummary as(
    SELECT
        VendorNo,
        Brand,
        SUM(SalesQuantity) as TotalSalesQuantity,
        SUM(SalesDollars) as TotalSalesDollars,
        SUM(SalesPrice) as TotalSalesPrice,
        SUM(ExciseTax) as TotalExciseTax
    FROM sales
    GROUP BY VendorNO, Brand
)

SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
    
FROM PurchaseSummary ps
LEFT JOIN 
salesSummary ss
    ON ps.VendorNumber = ss.VendorNO
    AND ps.Brand = ss.Brand
LEFT JOIN
FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""", conn)
    
return summary_table

def clean_data(df):
    '''this function will clean the data'''
    #change datatype to float
    df['Volume'] = df['Volume'].astype('float')
    
    #filling missing value with 0
    df.fillna(0, inplace=True)
    
    #removing spaces from categorical columns(white space)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    
    #creating new columns for better analysis
    summary_table['GrossProfit'] = summary_table['TotalSalesDollars'] - summary_table['TotalPurchaseDollars']
    summary_table['ProfitMargin'] = (summary_table['GrossProfit'] / summary_table['TotalSalesDollars'])*100
    summary_table['StockTurnover'] = summary_table['TotalSalesQuantity'] / summary_table['TotalPurchaseQuantity']
    summary_table['SalestoPurchaseRatio'] = summary_table['TotalSalesDollars'] / summary_table['TotalPurchaseDollars']
    
    return df
  
if __name__ == '__main__':
    #creating database connection
    conn = sqlite3.connect('inventory.db')
    
    logging.info('Creating vendor summary tale.....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())
    
    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())
    
    logging.info('Ingesting data......')
    ingest_db(clean_df, 'summary_table', conn)
    logging.info('Completed')
    
    
    
    
    
    
    