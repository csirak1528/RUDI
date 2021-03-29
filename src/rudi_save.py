import rudi_file
from rudi_defaults import app_dir
import pickle
import os

def save_init(file_name=f"{app_dir}/dt.pickle"):
    global data
    try:
        file = open(file_name,"rb+")
        if os.path.getsize(file_name) ==0:
            data = {}
        else:
            data = pickle.load(file)
    except FileNotFoundError:
        file = open(file_name,"wb+")
        data = {}
    file.close()
    return file_name,data

def get_from_pk(i):
    global data
    try:
        return data[i]
    except KeyError:
        return False

def save_close(file_name=f"{app_dir}/dt.pickle"):
    global data
    file = open(file_name,'wb')
    file.truncate()
    pickle.dump(data, file)
    file.close()
    return True

if __name__ == "__main__":
    pass
