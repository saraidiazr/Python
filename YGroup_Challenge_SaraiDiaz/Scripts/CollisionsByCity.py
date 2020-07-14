import pandas as pd
import urllib.request
import requests
import sqlite3
import zipfile
import os


def montreal_collisions(db_connection,data_dir):
    url = "http://donnees.ville.montreal.qc.ca/dataset/cd722e22-376b-4b89-9bc2-7c7ab317ef6b/resource/05deae93-d9fc-4acb-9779-e0942b5e962f/download/accidents_2012_2018.zip"
    zip_name = data_dir + '/montral_collisions.zip'
    file_name = data_dir + '/accidents_2012_2018.csv'
    urllib.request.urlretrieve(url,zip_name)
    zip = zipfile.ZipFile(zip_name, 'r')
    zip.extractall(data_dir)
    zip.close()
    os.remove(zip_name)

    #Importing data into sqlite
    csv_data = pd.read_csv(file_name)
    csv_data.columns = csv_data.columns.str.replace(" ", "_")
    csv_data = csv_data[['DT_ACCDN' ,'CD_MUNCP' ,'RUE_ACCDN' ,'NB_MORTS' ,'HR_ACCDN' ,'NB_VICTIMES_TOTAL' ,'nb_bicyclette' ,'LOC_LONG' ,'LOC_LAT']]
    csv_data.rename(columns = {'DT_ACCDN':'date','CD_MUNCP':'cod_district','RUE_ACCDN':'street','NB_MORTS':'total_deaths','HR_ACCDN':'hour','NB_VICTIMES_TOTAL':'total_victims','nb_bicyclette':'total_bikes','LOC_LONG':'longitude','LOC_LAT':'latitude'}, inplace = True)
    csv_data.to_sql('montreal_collisions', db_connection, if_exists = 'append', index = False)
    return 


def toronto_collisions(db_connection,data_dir):
    url = "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Cyclists/FeatureServer/0/query?where=1%3D1&outFields=YEAR,DATE,TIME,HOUR,STREET1,STREET2,OFFSET,ROAD_CLASS,District,LATITUDE,LONGITUDE,LOCCOORD,TRAFFCTL,RDSFCOND,ACCLASS,IMPACTYPE,INVTYPE,INVAGE,INJURY,FATAL_NO,VEHTYPE,MANOEUVER,DRIVACT,DRIVCOND,CYCACT,CYCCOND,Neighbourhood,CYCLISTYPE,Hood_ID&outSR=4326&f=json"
    package = requests.get(url).json()
    data = package["features"]

    df = pd.DataFrame()
    for items in data:
        json_clean = items["attributes"]
        json_sample_loop = str(json_clean).replace(": ",":[").replace(", ","], ").replace("}", " ]}")
        current = pd.DataFrame(eval(str(json_sample_loop)))
        df = df.append(current)

    #Importing data into sqlite
    df.columns = map(str.lower, df.columns)
    df.to_sql('toronto_collisions', db_connection, if_exists = 'append', index = False)
    return 