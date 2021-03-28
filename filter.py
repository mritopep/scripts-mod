import os
import xml.etree.ElementTree as ET
from datetime import date
from shutil import copyfile
import shutil

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
METADATA_ADNI=f'{PWD}/metadata/adni/'
METADATA_CANCER=f'{PWD}/metadata/cancer/'
DIVIDE=f'{PWD}/parts/'
PREPROCESSED=str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/preprocessed_data/")

def make_dir():
    dirs=[DOWNLOAD,EXTRACT,ADNI,CANCER,METADATA_ADNI,METADATA_CANCER,PREPROCESSED,DIVIDE]
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def get_metadata(dataset):
    xml_files={}
    for r, d, f in os.walk(METADATA_ADNI):
          for file in f:
              if file.endswith(".xml") and file.startswith("ADNI"):
                file_path=os.path.join(r, file)
                subId,seriesId,imageId,date = get_xml_data(file_path)
                id=f"S{seriesId}_I{imageId}"
                xml_files[id]={"subId":subId,"date":date}
    return xml_files

def get_xml_data(path):
    tree = ET.parse(path)
    root = tree.getroot()
    subId=root.find("./project/subject/subjectIdentifier").text
    seriesId=root.find("./project/subject/study/series/seriesIdentifier").text
    imageId=root.find("./project/subject/study/imagingProtocol/imageUID").text
    date=root.find("./project/subject/study/series/dateAcquired").text
    return [subId,seriesId,imageId,date]

metadata=get_metadata("ADNI")

def get_name(scan_path):
    if(scan_path.find("/PT/")!=-1):
        index=scan_path.find("/PT/")
    index=scan_path.find("/MR/")
    return scan_path[index+4:-4]+".xml"

def get_date(scan_path):
    name=get_name(scan_path)
    for k in metadata.keys():
        if(k in name):
            if(metadata[k]["subId"] in name):
                return metadata[k]["date"]

def get_diff(mri_date,pet_date):
    year,month,day=[int(i) for i in mri_date.split("-")]
    d0 = date(year,month,day)
    year,month,day=[int(i) for i in pet_date.split("-")]
    d1 = date(year,month,day)
    diff = abs(d1 - d0)
    return diff.days

def pair_scan_images(MR,PT):
    print("\nPAIR SCANS\n")
    pair_data=[]
    used_mri=[]

    for pet in PT:
        min_diff=2147483647
        cache_data={}
        for mri in MR:
            if(mri in used_mri):
                continue
            mri_date=get_date(mri)
            pet_date=get_date(pet)
            diff=get_diff(mri_date,pet_date)
            if(diff not in cache_data.keys()):
                cache_data[diff]={"mr":mri,"pt":pet}
            if(diff<min_diff):
                min_diff=diff
                used_mri.append(mri)
            if(cache_data[min_diff] not in pair_data):
                pair_data.append(cache_data[min_diff])
                #print(f'MRI: {cache_data[min_diff]["mr"]}\n\nPET: {cache_data[min_diff]["pt"]}\n\nDAYS: {min_diff}\n\n')

    return pair_data

def filter():
    make_dir()
    subject_ids=os.listdir(ADNI)
    pair_datas=[]
    for id in subject_ids:
        mri=[]
        pet=[]
        
        try:
            files = os.listdir(f"{ADNI}{id}/MR")
        except:
            continue

        for file in files:
            mri.append(f"{ADNI}{id}/MR/{file}")

        try:
            files = os.listdir(f"{ADNI}{id}/PT")
        except:
            continue

        for file in files:
            pet.append(f"{ADNI}{id}/PT/{file}")

        if(len(mri) == 0 or len(pet) == 0):
            shutil.rmtree(f"{ADNI}{id}")
            continue
        
        pair_data = pair_scan_images(mri,pet)
        pair_datas.extend(pair_data)

        print(f"Subject Id: {id}")
        print(f"PET NUM: {len(pet)}")
        print(f"MRI NUM: {len(mri)}")       
        print(f"PAIR DATA NUM: {len(pair_data)}")

        count=0
        for pair in pair_data:
            count+=1
            loc=f"{PREPROCESSED}{id}_{count}"
            if(os.path.isdir(loc)==False):
              try:  
                os.makedirs(loc) 
              except OSError as error:  
                  print(error) 
            copyfile(pair["mr"], loc+"/mri.nii")
            copyfile(pair["pt"], loc+"/pet.nii")

        shutil.rmtree(f"{ADNI}{id}")
        
    print(f"PAIR DATAS NUM: {len(pair_datas)}")


if __name__ == "__main__":
    filter()
