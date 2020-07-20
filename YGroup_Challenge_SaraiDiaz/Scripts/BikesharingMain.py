import BikesharingMontreal as montreal_bikes
import BikesharingToronto as toronto_bikes
import BikesharingDB as db
import CollisionsByCity as collisions
import pandas as pd
import os
import requests
from datetime import datetime

# #Setting variables
print ('Starting process at: ', datetime.now())
current_dir = os.getcwd()
montreal_dir = current_dir + '\Datasets\Montreal'
toronto_dir = current_dir + '\Datasets\Toronto'
db_connection = db.db_setup(current_dir)

#Downloading Montreal bikeshare data
print ('Downloading Montreal Data')
url = 'https://www.bixi.com/en/page-27'
data_without_parsing = montreal_bikes.get_html(url)
data_links = montreal_bikes.parse_html(data_without_parsing)
montreal_bikes.download_data(data_links,montreal_dir)
montreal_bikes.validation(montreal_dir,db_connection)

#Downloading Toronto bikeshare data
print ('Downloading Toronto Data')
download = toronto_bikes.consume_api()
toronto_bikes.get_data(download,toronto_dir)
toronto_bikes.get_stations(toronto_dir)
toronto_bikes.validation(toronto_dir,db_connection)

#Importing downloaded data into db
print ('Importing Montreal data into db')
db.db_import(db_connection,montreal_dir)
print ('Importing Toronto data into db')
db.db_import(db_connection,toronto_dir)

#Adding collisions data by city
print ('Adding collisions data by city')
collisions.toronto_collisions(db_connection,toronto_dir)
collisions.montreal_collisions(db_connection,montreal_dir)

#Adding db structures
idx_script = current_dir + '\Scripts\create_idx.sql'
agg_script = current_dir + '\Scripts\create_agg.sql'
validation_script = current_dir + '\Scripts\Validation'
print ('Adding indexes')
db.script_to_db(db_connection,idx_script)
print ('Adding agg table')
db.script_to_db(db_connection,agg_script)
print ('Adding validations')
db.script_to_db(db_connection,validation_script)

print ('Ending process at: ', datetime.now())
