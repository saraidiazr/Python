import BikesharingMontreal as montreal_bikes
import BikesharingToronto as toronto_bikes
import BikesharingDB as db
import CollisionsByCity as collisions
import os
import pandas as pd

#Setting variables
print ('process started')
current_dir = os.getcwd()
montreal_dir = current_dir + '\Datasets\Montreal'
toronto_dir = current_dir + '\Datasets\Toronto'

#Downloading Montreal bikeshare data
print ('Downloading Montreal Data')
url = 'https://www.bixi.com/en/page-27'
data_without_parsing = montreal_bikes.get_html(url)
data_links = montreal_bikes.parse_html(data_without_parsing)
montreal_bikes.download_data(data_links)

#Downloading Toronto bikeshare data
print ('Downloading Toronto Data')
download = toronto_bikes.consume_api()
toronto_bikes.get_data(download)
toronto_bikes.get_stations(toronto_dir)

#Importing downloaded data into database
print ('Importing downloaded data into database')
db_connection = db.db_setup()
db.db_import(db_connection,montreal_dir)
db.db_import(db_connection,toronto_dir)

#Add collisions data by city
print ('Add collisions data by city')
collisions.toronto_collisions(db_connection,toronto_dir)
collisions.montreal_collisions(db_connection,montreal_dir)

print ('process ended')
