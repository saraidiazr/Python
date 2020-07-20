import pandas as pd
import urllib3
import urllib.request
import requests
import zipfile
import shutil
import os

#Getting data from the API (code snippet from official website)
def consume_api():
  url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
  params = { "id": "7e876c24-177c-4605-9cef-e50dd74c617f"}
  package = requests.get(url, params = params).json()
  data = package["result"]['resources']
  df = pd.DataFrame(data)
  links = df['url'] #getting all links to download data
  return links

#Downloading data
def get_data(links,data_dir):
  #Setting up folder as repository for all the data related to Toronto
  file = 'csv.zip'
  dir = data_dir + '\\' + file
  if not os.path.exists(data_dir):
    os.makedirs(data_dir)

  #Getting links to download the data
  for link in links:
    #Downloading and extracting data in .zip files
    if str(link).endswith('.zip'):
      urllib.request.urlretrieve(link,dir)
      zip = zipfile.ZipFile(dir, 'r')
      zip.extractall(data_dir)
      zip.close()
      os.remove(dir)

      #Moving downloaded data into Toronto folder
      root_dir = data_dir + '\\'
      items = os.listdir(root_dir)
      for item in items: 
          if os.path.isdir(os.path.join(root_dir, item)): #filtering folders only
              subfolder = os.listdir(root_dir + item)
              for file in subfolder: #moving files in subfolders to root directory
                  file_name = root_dir+item+'\\'+file
                  shutil.move(file_name, root_dir)
                  if not((root_dir + file).endswith('.csv')): 
                    os.remove(root_dir + file)
              os.rmdir(root_dir + item)
  return

def get_stations(data_dir):
  file_name = data_dir + '/stations_2020.csv'
  url = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information'
  package = requests.get(url).json()
  stations = package["data"]['stations']

  #exporting to csv
  file_name = data_dir + '/stations_2020.csv'
  df = pd.DataFrame(stations) 
  df.to_csv(file_name, index = False, header=True)
  return

def validation(data_dir,db_connection):
  root_dir = data_dir + '\\'
  files = os.listdir(root_dir)
  df_validation = pd.DataFrame()
  for file in files: 
    file_name = root_dir+'\\'+file
    city = 'Toronto' 
    if '(' in file: #2017 files have a different format
      date = file[(file.find('(')+1):(file.find(')'))]
    else:
      date = file[(file.find('_')+1):(file.find('.'))]
      if len(date) > 4: #stations file only has the year in its name
        date = date[-4:] + ' ' + date[:2] #2018 files have a different format
    source_name = file
    df_file = pd.read_csv(file_name)
    source_count = len(df_file)
    df_file.drop_duplicates(keep=False,inplace=True)
    is_dedupe = 0 if source_count == len(df_file) else 1
    df = pd.DataFrame({'city': city, 'date': date, 'source_name': source_name, 'source_count':source_count, 'is_source_dedupe':is_dedupe},index=[0])
    df_validation = df_validation.append(df)
  df_validation.to_sql('validation_checks', db_connection, if_exists = 'append', index = False)
  return