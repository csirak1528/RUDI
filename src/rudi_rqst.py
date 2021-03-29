import hashlib
from rudi_network import network_request,rebuild
from rudi_data import direct_dirs,send_dirs
from rudi_defaults import middir,file_save_dir
from rudi_send import commands
from rudi_file import build,hasher,rename
import os
hasher  = lambda x: hashlib.sha256(x.encode()).hexdigest()

def searchDir(path, term):
    terms = []
    for i in os.listdir(path):
        if term in i:
            terms.append(i)
    if terms:
        return terms
    else:
        return False

def r_request(file,addr,dir_=file_save_dir):
    os.chdir(file_save_dir)
    contents=os.listdir()
    if file in contents:
        commands('file',path=f"{dir_}/{file}",ip=addr)
        return True
    else:
        return False


def file_request(file):
    name = hasher(file)
    try:
        file_info=direct_dirs[name]
        send_info=send_dirs[name]
    except KeyError:
        return False
    update_direct_dir,send_dir,file_dir=network_request(file_info,send_info)
    os.chdir(middir)
    if name in os.listdir():
        dir_=rebuild(update_direct_dir,send_dir,file_dir)
        oldname=build(dir_)
        rename(oldname,os.path.basename(file))
    return True
