import pickle 
from internetdownloadmanager import Downloader
from os import listdir
from os.path import isfile, join

DOWNLOAD="/home/antony/Code/Medical Image Syntesis/presentation/raw_data/cancer_zip"

downloader = Downloader(worker=25,part_size=1000000)

def get_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def download(url,dest):
    downloader.download(url=url,path=dest)
    print(dest)

def get_data(name):
    with open(f'/home/antony/Code/Medical Image Syntesis/presentation/output/{name}', 'rb') as f:
        return pickle.load(f) 

def main():
    patients_data = get_data("patient-data")
    patients_data = patients_data[:1]
    count=0
    files=get_files(DOWNLOAD)
    for patient in patients_data:
        count+=1
        print(f"File Number: {count} out of 1131")
        name=f"CAN_{patient['modality']}_{patient['id'][18:]}_{count}.zip"
        file_path=DOWNLOAD+"/"+name
        print(F"NAME: {name}\nPATH:{file_path}")
        if(name not in files):    
            url=f'https://services.cancerimagingarchive.net/services/v4/TCIA/query/getImage?SeriesInstanceUID={patient["series_id"]}'
            download(url,file_path)
    

if __name__ == "__main__":
    main()