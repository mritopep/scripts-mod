import requests
import pickle
from os import listdir
from os.path import isfile, join

patients_data=[]
timeout=10

def get_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def store_data(name,data):
    with open(f'/home/antony/Code/Medical Image Syntesis/presentation/output/{name}', 'wb') as f:
        pickle.dump(data, f) 

def get_data(name):
    with open(f'/home/antony/Code/Medical Image Syntesis/presentation/output/{name}', 'rb') as f:
        return pickle.load(f) 

def get_patients():
    with open('/home/antony/Code/Medical Image Syntesis/presentation/output/common-patient', 'rb') as file:
        patients=pickle.load(file)
        return patients

def get_series(patient):
    result = requests.get(f'https://services.cancerimagingarchive.net/services/v4/TCIA/query/getSeries?Collection=ACRIN-FMISO-Brain&PatientID={patient}&format=json')
    data = result.json()
    return data

def correct_mri_scan(desc):
    description=desc.lower()
    if(description.find("t1")!=-1):
        if(description.find("sag")==-1 and description.find("cor")==-1):
            return True

def main():
    patients_data=[]
    patients = get_patients()
    patients = patients[:1]

    for patient in patients:
        print(f"{patient} DATA")
        patient_series=get_series(patient)
        for series in patient_series:
                if(series["Modality"]=="MR" and correct_mri_scan(series["SeriesDescription"]) or series["Modality"]=="PT"):
                    patient_data={}
                    patient_data['id']=series["PatientID"]
                    patient_data['series_desc']=series["SeriesDescription"]
                    patient_data['modality']=series["Modality"]
                    patient_data['series_id']=series["SeriesInstanceUID"]
                    patient_data['study_id']=series["StudyInstanceUID"]
                    patients_data.append(patient_data)
                    print(f'''
                    id:{patient_data['id']}\n
                    series_desc:{patient_data['series_desc']}\n
                    modality:{patient_data['modality']}\n
                    series_id:{patient_data['series_id']}\n
                    study_id:{patient_data['study_id']}\n\n
                    ''')

    pet=0
    mr=0
    for patient in patients_data:
        if(patient['modality']=="MR"):
            mr+=1
        elif(patient['modality']=="PT"):
            pet+=1
    print(f"MRI COUNT: {mr}\nPET COUNT: {pet}\nTOTAL COUNT: {pet+mr}")

    store_data("patient-data",patients_data)


if __name__ == "__main__":
    main()
























