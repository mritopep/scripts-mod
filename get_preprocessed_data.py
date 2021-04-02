# imports
import requests
import zipfile
import os
import shutil
import time
import gzip

# library files
from get_link import get_files
from library import make_dir,get_data,store_data,remove_dir
from preprocess import driver

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
METADATA_ADNI=f'{PWD}/metadata/adni/'
METADATA_CANCER=f'{PWD}/metadata/cancer/'
PREPROCESSED=str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/preprocessed_data")

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def extract(source,destination):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        files = zip_ref.infolist()
        for file in files:
            try:
                zip_ref.extract(file,path=destination)
            except:
                print(f"Bad File: {file.filename}")

def download_data(files):
    downloaded_files=[]
    print("\n DOWNLOADING FILES \n")
    for fs in files:
        file_id=fs['id']
        file_path=DOWNLOAD+fs['name']
        file_name=fs['name']
        print(f'Name:{file_name}\nPath: {file_path}')
        download_file_from_google_drive(file_id, file_path)
        downloaded_files.append({"name":file_name,"path":file_path})   
    return downloaded_files

def extract_files(downloaded_files): 
    print("\n EXTRACTING FILES \n")
    extract_paths=[]
    for file in downloaded_files:
      extract_path=EXTRACT+file['name'][:-4]
      extract(file['path'],extract_path)
      extract_paths.append(extract_path)
    return extract_paths

def get_nii_files(extracted_paths):
    print("\n SELECTING SCANS FILES \n")
    nii_files=[]
    for extract_path in extracted_paths:
      for r, d, f in os.walk(extract_path):
          for file in f:
              if file.endswith(".nii"):
                file_name=file
                file_path=os.path.join(r, file)
                nii_files.append({"name":file_name,"path":file_path})
    return nii_files

def get_data(name):
    make_dir([DOWNLOAD,EXTRACT,ADNI,CANCER,METADATA_ADNI,METADATA_CANCER,PREPROCESSED])
    nii_files=[]
    files=get_files(name)[:2]
    print(files)
    for file in files:
      downloaded_files=download_data([file])
      extracted_paths=extract_files(downloaded_files)
      extracted_files=get_nii_files(extracted_paths)
      print(f"\n\nREMOVE: {downloaded_files[0]['path']}\n")
      os.remove(downloaded_files[0]['path'])

      driver(extracted_files)

      name = file.replace("filtered","preprocessed")[:-4]
      shutil.make_archive(name, 'zip', PREPROCESSED)
      print(f"\n\nremoved !")
      shutil.rmtree(PREPROCESSED)

      make_dir([PREPROCESSED])
    return extracted_paths

if __name__ == "__main__":
    print(PWD)
    get_data("filtered_adni")