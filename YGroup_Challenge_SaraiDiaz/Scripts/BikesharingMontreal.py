from bs4 import BeautifulSoup
import urllib3
import urllib.request
import zipfile
import shutil
import os
import pandas as pd 

#Getting html info
def get_html(url):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #to avoid message popup
  requests = urllib3.PoolManager()
  request = requests.request('GET', url)
  info_without_parsing = request.data
  return info_without_parsing

#Parsing html info
def parse_html(info_without_parsing):
  info_parsed = BeautifulSoup(info_without_parsing, 'lxml')
  info_parsed_filtered = info_parsed.find_all(class_="document-csv col-md-2 col-sm-4 col-xs-12")

  links = []
  for items in info_parsed_filtered:
    links.append(items.get('href'))
  return links

#Downloading info
def download_data(data_links,data_dir):
  #Setting up folder as repository for all the data related to Montreal
  file = 'csv.zip' 
  dir = data_dir + '\\' + file
  if not os.path.exists(data_dir):
      os.makedirs(data_dir)

  #Downloading and extracting data in .zip files
  for link in data_links:
      urllib.request.urlretrieve(link,dir)
      zip = zipfile.ZipFile(dir, 'r')
      zip.extractall(data_dir)
      zip.close()
      os.remove(dir)

  #Moving downloaded data into Montreal folder
  root_dir = data_dir + '\\'
  items = os.listdir(root_dir)
  for item in items: 
      if os.path.isdir(os.path.join(root_dir, item)): #filtering folders only
          subfolder = os.listdir(root_dir + item)
          for file in subfolder: #moving files in subfolders to Montreal folder
              file_name = root_dir+item+'\\'+file
              shutil.move(file_name, root_dir)
          os.rmdir(root_dir + item)
  return

def validation(data_dir,db_connection):
  root_dir = data_dir + '\\'
  files = os.listdir(root_dir)
  df_validation = pd.DataFrame()
  for file in files: 
    file_name = root_dir+'\\'+file
    city = 'Montreal'
    date = file[(file.find('_')+1):(file.find('.'))]
    source_name = file
    df_file = pd.read_csv(file_name)
    source_count = len(df_file)
    df_file.drop_duplicates(keep=False,inplace=True)
    is_dedupe = 0 if source_count == len(df_file) else 1
    df = pd.DataFrame({'city': city, 'date': date, 'source_name': source_name, 'source_count':source_count,'is_source_dedupe':is_dedupe},index=[0])
    df_validation = df_validation.append(df)
  df_validation.to_sql('validation_checks', db_connection, if_exists = 'append', index = False)
  return