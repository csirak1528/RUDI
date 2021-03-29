from rudi_save import *

file,data=save_init()

vars_=['send_dirs',"wlan_ips","direct_dirs","rating_data",'eth_ips','queue','wlan_ips_names']

for var in vars_:
    try:
        globals()[var]=data[var]
    except KeyError:
        globals()[var]={}

def add_save_data(name,info,data_dict=data):
    data_dict[name]=info

def close(file_=file):
    save_close(file_)
