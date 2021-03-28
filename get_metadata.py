import os
import shutil
from os import path
from os import listdir
from os.path import isfile, join

#library
from set_data import download_data,extract_files
from get_link import get_files

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
METADATA_ADNI=f'{PWD}/metadata/adni/'
METADATA_CANCER=f'{PWD}/metadata/cancer/'

def make_dir():
    dirs=[DOWNLOAD,EXTRACT,ADNI,CANCER,METADATA_ADNI,METADATA_CANCER]
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def get_xml_files(extracted_paths):
    print("\n GETTING XML FILE\n")
    xml_files=[]
    for extract_path in extracted_paths:
      for r, d, f in os.walk(extract_path):
          for file in f:
              if file.endswith(".xml") and file.startswith("ADNI"):
                file_name=file
                file_path=os.path.join(r, file)
                xml_files.append({"name":file_name,"path":file_path})
                print(f'Name:{file_name}\nPath: {file_path}')
    return xml_files

def copy_metadata(files):
    for file in files:
        shutil.copyfile(file["path"], METADATA_ADNI+file["name"])
        os.remove(file["path"])

def get_metadata(name):
    make_dir()
    files=get_files(name)
    for file in files:
      downloaded_files=download_data([file])
      extracted_paths=extract_files(downloaded_files)
      print(f"\n\nRemoving {downloaded_files[0]['path']}\n")
      # shutil.rmtree(downloaded_files[0]["path"], ignore_errors=True)
      os.remove(downloaded_files[0]['path'])
      xml_files=get_xml_files(extracted_paths)
      copy_metadata(xml_files)

if __name__ == "__main__":
    get_metadata("adni_metadata")
    


























