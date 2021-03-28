import requests
import pickle
from os import listdir
from os.path import isfile, join
import os

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

METADATA_CANCER=f'{PWD}/metadata/cancer/'

def get_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def make_dir():
    dirs=[METADATA_CANCER]
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def get_metadata(url):
    result = requests.get(url)
    data = result.json()
    return data[0]
    
def get_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def load_metadata(name):
    with open(f'{METADATA_CANCER}{name}', 'rb') as f:
        return pickle.load(f) 

def store_metadata(name,data):
    with open(f'{METADATA_CANCER}{name}', 'wb') as f:
        pickle.dump(data, f) 
        
def get_data(name):
    with open(f'/home/antony/Code/Medical Image Syntesis/presentation/output/{name}', 'rb') as f:
        return pickle.load(f) 
        
def main():
    make_dir()
    patients_data = get_data("patient-data")
    patients_data = patients_data[:1]
    count=0
    files=get_files(METADATA_CANCER)
    missed_names=[]
    for patient in patients_data:
    	count+=1
    	print(f"File Number: {count} out of 1131")
    	name=f"CAN_META_{patient['modality']}_{patient['id'][18:]}_{count}"
    	print(F"Name: {name}")
    	if(name in files):
    		continue
    	url=f'https://services.cancerimagingarchive.net/services/v4/TCIA/query/getSeries?SeriesInstanceUID={patient["series_id"]}&format=json/metadata'
    	data=get_metadata(url)
    	try:
    		print(F"Date: {data['SeriesDate']}")
    		store_metadata(name,data)
    		print(f"File stored: {METADATA_CANCER}{name}")
    	except:
    		missed_names.append(name)
    store_metadata("missed_names",missed_names) 

    
if __name__ == "__main__":
    main()
