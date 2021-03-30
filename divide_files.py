from zipfile import ZipFile
import os
import shutil
from distutils.dir_util import copy_tree

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/raw_data")

# file locations
DOWNLOAD=f'{PWD}/downloads/'
ADNI=f'{PWD}/data/adni/'
CANCER=f'{PWD}/data/cancer/'
EXTRACT=f'{PWD}/extracts/'
DIVIDE=f'{PWD}/parts/'
PREPROCESSED=str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","/preprocessed_data/")

def make_dir():
    dirs=[DOWNLOAD,EXTRACT,ADNI,CANCER,DIVIDE]
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths   

def divide(name,path,parts):
    divided_dirs=[]
    dirs=[]

    dir_list=os.listdir(path)
    num_dir=len(dir_list)
    div=int(num_dir/parts)

    for i in range(1,num_dir+1):
        if(i%div==0):
            dirs.append(dir_list[i-1])
            divided_dirs.append(dirs)
            dirs=[]
        else:
            dirs.append(dir_list[i-1])

    if(dirs not in divided_dirs and len(dirs) != 0):
        divided_dirs.append(dirs)

    print(divided_dirs)

    dir_count=file_count=0
    for divide in divided_dirs:
        dir_count+=1
        for folder in divide:
            file_count+=1
    
    print(f"dir count:{dir_count} file count: {file_count}")

    count=0

    for divide in divided_dirs:
        try:
            os.makedirs(f"{DIVIDE}{name}")
        except:
            pass
        divided_file_paths = []
        count+=1
        for folder in divide:
            dest_directory = f"{DIVIDE}{name}/{folder}"
            src_directory = f"{path}{folder}"   
            os.makedirs(dest_directory)       
            shutil.copyfile(f"{src_directory}/mri.nii",f"{dest_directory}/mri.nii")
            shutil.copyfile(f"{src_directory}/pet.nii",f"{dest_directory}/pet.nii")
        shutil.make_archive(f"{DIVIDE}{name}_{count}", 'zip', f"{DIVIDE}{name}")
        print(f"\n\nremoved !")
        shutil.rmtree(f"{DIVIDE}{name}")

if __name__ == "__main__":
    make_dir()
    divide("adni",PREPROCESSED,10)