import os
from datetime import date
from shutil import copyfile
import shutil
import pickle
import gzip

#import
from set_data import get_data as get_file_data
from library import make_dir,get_data,store_data,remove_dir

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
METADATA_ADNI=f'{PWD}/metadata/adni/'
METADATA_CANCER=f'{PWD}/metadata/cancer/'
PREPROCESSED=str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/preprocessed_data")

# Temp
SKULL_STRIP=f'{PWD}/temp/skull_strip/'
IMG_REG=f'{PWD}/temp/img_reg/'
DENOISE=f'{PWD}/temp/denoise/'
PETPVC=f'{PWD}/temp/petpvc/'
BAIS_COR=f'{PWD}/temp/bias_cor/'
TEMP_OUTPUT=f'{PWD}/temp/output/'


# globals
sub_scan={}

def image_registration(mri_image,pet_image):
    os.system(f"image_reg.py {mri_image} {pet_image}")

def intensity_normalization(input_image,output_image):
    os.system(f"denoise -i {input_image}  -o {output_image}")

def skull_strip(input_image):
    os.system(f"skull_strip.py -i {input_image} -o output {SKULL_STRIP}")

def bias_correction(input_image,output_image):
    os.system(f"bais_field_correction.py {input_image} {output_image}")

def petpvc(input_image,output_image):
    os.system(f"petpvc -i {input_image} -o {output_image}")

def preprocess(key):
    scan=sub_scan[key]
    make_dir([SKULL_STRIP,IMG_REG,DENOISE,PETPVC,BAIS_COR,TEMP_OUTPUT,f"{PREPROCESSED}/{key}"])
    mri_path=scan['mri.nii']
    pet_path=scan['pet.nii']
    print(mri_path,"\n",pet_path,)
    image_registration(mri_path,pet_path)
    preprocess_mri(mri_path)
    preprocess_pet(pet_path)
    copyfile(f"{TEMP_OUTPUT}mri.nii",f"{PREPROCESSED}/{key}/mri.nii")
    copyfile(f"{TEMP_OUTPUT}pet.nii",f"{PREPROCESSED}/{key}/pet.nii")
    remove_dir([SKULL_STRIP,IMG_REG,DENOISE,PETPVC,BAIS_COR,TEMP_OUTPUT])

def upzip_gz(input_gz,output):
    with gzip.open(input_gz, 'rb') as f_in:
        with open(output, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def preprocess_mri(mri_path):
    intensity_normalization(mri_path,f"{DENOISE}mri.nii")
    skull_strip(f"{DENOISE}mri.nii")
    upzip_gz(f"{SKULL_STRIP}mri_masked.nii.gz",f"{SKULL_STRIP}mri_sk.nii")
    bias_correction(f"{SKULL_STRIP}mri_sk.nii",f"{TEMP_OUTPUT}mri.nii")
    
def preprocess_pet(pet_path):
    skull_strip(pet_path[:-4] + "_registered.nii")
    upzip_gz(f"{SKULL_STRIP}pet_masked.nii.gz",f"{SKULL_STRIP}pet_sk.nii")
    petpvc(f"{SKULL_STRIP}pet_sk.nii",f"{TEMP_OUTPUT}pet.nii")

def get_folder_name(path):
  return path.split("/")[-2]

def driver(extracted_paths):
    for i in extracted_paths:
      folder = get_folder_name(i['path'])
      if(folder not in sub_scan.keys()):
        sub_scan[folder]={}
        sub_scan[folder].update({i['name']:i['path']})
      else:
        sub_scan[folder].update({i['name']:i['path']})
    for k,v in sub_scan.items():
      print(k,v)
    store_data("dic",sub_scan)
    for k in sub_scan:
        preprocess(k)

# if __name__ == "__main__":
#     # driver()
    