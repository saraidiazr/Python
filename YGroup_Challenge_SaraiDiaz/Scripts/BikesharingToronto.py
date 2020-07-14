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
def get_data(links):
  #Setting up folder as repository for all the data related to Toronto
  current_dir = os.getcwd()
  file = 'csv.zip'
  folder = '\Datasets\Toronto' + '\\'
  dir = current_dir + folder + file
  if not os.path.exists(current_dir + '\Datasets\Toronto'):
    os.makedirs('Datasets\Toronto')

  #Getting links to download the data
  for link in links:
    #Downloading and extracting data in .zip files
    if str(link).endswith('.zip'):
      urllib.request.urlretrieve(link,dir)
      zip = zipfile.ZipFile(dir, 'r')
      zip.extractall(current_dir+folder)
      zip.close()
      os.remove(dir)

      #Moving downloaded data into Toronto folder
      root_dir = current_dir + folder
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