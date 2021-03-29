import os
import rudi_send
import time
import rudi_defaults
import sys
from rudi_data import wlan_ips,wlan_ips_names, add_save_data,close
from rudi_threads import threader



def getcur_dir(dir=""):
    if dir:
        os.chdir(dir)
    cur_dir = os.listdir()
    for i,j in enumerate(cur_dir):
        if ".DS_" in j or "." not in j:
            cur_dir.pop(i)
    dir_ = os.getcwd()
    curdir = [dir_ +"/"+i for i in cur_dir]
    return cur_dir

def update_all(ips,out=[]):
    dir_=getcur_dir()
    for ip in ips:
        threader(update(dir_,ip,out))


def update(cur_dir,ip,out=[]):
    rudi_send.send_mult(cur_dir,ip,out,update=True)

ips=wlan_ips
try:
    names=wlan_ips_names
except:
    names={}
    for ip in wlan_ips:
        names[input(f"name? {ip}>")]=ip
if not len(wlan_ips) == len(names):
    temp_ip=wlan_ips[len(names):]
    for ip in temp_ip:
        names[input(f"name? {ip}>")]=ip
    add_save_data("wlan_ips_names",names)
    close()

if __name__ == "__main__":
    d_ip=rudi_defaults.dev_ip
    #if d_ip in ips:
        #ips.remove()
    try:
        if sys.argv[1]=='-a':
            update_all(ips)
    except IndexError:
        pass
    x=input(">>")
    sel_ip= False

    if x=="add":
        sel_ip=input('ip>')
    if sel_ip:
        update(getcur_dir(),sel_ip)
    if x:
        update(getcur_dir(),wlan_ips_names[x])
