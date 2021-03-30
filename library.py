import os
import pickle

def store_data(name,data,path):
    with open(path, 'wb') as f:
        pickle.dump(data, f) 

def get_data(name,path):
    with open(path, 'rb') as f:
        return pickle.load(f) 

def make_dir(dirs):
    for dir in dirs:
        try:
            os.makedirs(dir)  
        except:
            pass

def remove_dir(dirs):
    for dir in dirs:
        try:
            os.removedirs(dir)  
        except:
            pass

