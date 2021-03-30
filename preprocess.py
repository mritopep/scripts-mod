import os
from datetime import date
from shutil import copyfile
import shutil
import pickle

#import
from set_data import get_data as get_file_data

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
METADATA_ADNI=f'{PWD}/metadata/adni/'
METADATA_CANCER=f'{PWD}/metadata/cancer/'
SKULL_STRIP=f'{PWD}/temp/skull_strip/output'
PREPROCESSED=str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/preprocessed_data")
OUTPUT=f'{PWD}/data/output/'

def store_data(name,data):
    with open(f'{OUTPUT}{name}', 'wb') as f:
        pickle.dump(data, f) 

def get_data(name):
    with open(f'{OUTPUT}{name}', 'rb') as f:
        return pickle.load(f) 

def make_dir():
    dirs=[DOWNLOAD,EXTRACT,ADNI,CANCER,METADATA_ADNI,METADATA_CANCER,SKULL_STRIP,PREPROCESSED,OUTPUT]
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def remove_dir():
    dirs=[SKULL_STRIP]
    for dir in dirs:
        try:
            os.removedirs(dir)  
        except:
            pass

def image_registration(pet_image,mri_image):
    os.system(f"image_reg.py {mri_image} {pet_image}")

def intensity_normalization(input_image,output_image):
    os.system(f"denoise -i {input_image}  -o {output_image}")

def skull_strip(input_image,output_image):
    os.system(f"skull_strip.py -i {input_image} -o output {SKULL_STRIP}")

def bias_correction(input_image,output_image):
    os.system(f"bais_field_correction.py {input_image} {output_image}")

def petpvc(input_image,output_image):
    os.system(f"petpvc -i {input_image} -o {output_image}")

# def make_dir(file_data):
#   sub_id,mod=get_id_and_mod(file_data["name"])
#   loc=ADNI+sub_id+"/"+mod
#   if(path.isdir(loc)==False):
#     try:  
#       os.makedirs(loc) 
#     except OSError as error:  
#         print(error) 
#   move(file_data["path"], loc+"/"+file_data["name"])
#   print(f"File Name: {file_data['name']}\n Loc: {loc}/{file_data['name']}")

def preprocess(name):
    make_dir()
    files=get_file_data(name)
    store_data("nii",files)
    # print("MAKING STRUCTRE")
    # for f in files:
    #     make_dir(f)
    # shutil.rmtree(EXTRACT) 
    

    # remove_dir()

if __name__ == "__main__":
    # preprocess("preprocessed_adni")
    data=get_data("nii")
    print(data)