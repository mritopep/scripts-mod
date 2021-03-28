import os
import shutil
from shutil import move
from os import path
import time

#library
from set_data import get_data

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'

def get_id_and_mod(name):
  mod=""
  if(name.find('_P') !=-1):
    mod="PT"
    id_index=name.find('_P') 
  if(name.find('_M') !=-1):
    mod="MR"
    id_index=name.find('_M')
  sub_id=name[5:id_index]
  return [sub_id,mod]

def make_dir(file_data):
  sub_id,mod=get_id_and_mod(file_data["name"])
  loc=ADNI+sub_id+"/"+mod
  if(path.isdir(loc)==False):
    try:  
      os.makedirs(loc) 
    except OSError as error:  
        print(error) 
  move(file_data["path"], loc+"/"+file_data["name"])
  print(f"File Name: {file_data['name']}\n Loc: {loc}/{file_data['name']}")

def make_struct(name):
  files=get_data(name)
  print("MAKING STRUCTRE")
  for f in files:
      make_dir(f)
  shutil.rmtree(EXTRACT) 

if __name__ == "__main__":
  print(PWD)
  make_struct("adni_data")