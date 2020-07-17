import pandas as pd
import sqlite3
import warnings
import os

def db_setup(data_dir):
    sqlite_dir = data_dir +'/SQLiteDatabaseBrowserPortable/Data'
    db_dir = sqlite_dir + '/bikesharing.db'
    warnings.filterwarnings("ignore") #to avoide warning messages
    db_connection = sqlite3.connect(db_dir)
    return db_connection

def db_import(db_connection,data_dir):
    files = os.listdir(data_dir)
    for file in files: 
        file_name = data_dir+'\\'+file
        csv_data = pd.read_csv(file_name,encoding='utf-8')
        csv_data.columns = csv_data.columns.str.replace(" ", "_")

        #Import to sqlite3
        if 'montreal' in data_dir.lower(): #checking if the data is about Montral or Toronto
            if 'stations' in file.lower(): #checking if Montreal data is about bikes or stations
                csv_data['source'] =  file[(file.find('_')+1):(file.find('.'))]
                csv_data.to_sql('montreal_stations', db_connection, if_exists = 'append', index = False)
            else:
                csv_data['start_date'] = pd.to_datetime(csv_data.start_date)
                csv_data['start_time'] = csv_data['start_date'].dt.strftime('%H')
                csv_data['day_of_week'] = csv_data['start_date'].dt.strftime('%A')
                csv_data.to_sql('montreal_bikes', db_connection, if_exists = 'append', index = False)
        else: #Toronto
            if 'stations' in file.lower():
                csv_data.to_sql('toronto_stations', db_connection, if_exists = 'append', index = False)
            else:
                csv_data.to_sql('toronto_bikes', db_connection, if_exists = 'append', index = False)
    return