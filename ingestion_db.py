import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename='logs/ingestion_db.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a')

engine = create_engine('sqlite:///inventory.db')

# Scripting: adding a function to keep track of new data. (in case of replace in companies we write append to update the continuous coming data)

def ingest_db(df, table_name, engine):
    #this function will ingest the dataframe into database table
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False, chunksize = 10000)

#as above we can see there is .ipnyb file which we can neglect or can also remove it

def load_rawData():
    #this function will load CSVs as dataframe and ingest into db 
    start = time.time()
    for i in os.listdir('data'):
        if '.csv' in i:
            df = pd.read_csv('data/' + i)
            logging.info(f'Ingesting {i} in DB')
            ingest_db(df, i[:-4], engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('----------Ingestion Complete----------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ == '__main__':
    load_rawData()
