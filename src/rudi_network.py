from rudi_file import *
from time import sleep
from random import shuffle
from rudi_send import connect_test, send_mult_dict,commands
from rudi_defaults import middir,dev_ip,file_save_dir,dev_ip
from datetime import datetime
from rudi_rqst import *
from rudi_data import rating_data,direct_dirs,send_dirs,add_save_data,wlan_ips
from rudi_save import save_close
from math import sin,pi
import os

def rating_algorithm(ip,state,rating_data=rating_data):
    time=datetime.now().hour
    if not state:
        state =-1
    try:
        data=rating_data[ip]
    except KeyError:
        return False

    total_connections=data[0]
    rating=data[1]
    """
    -sin(total_connections*pi/100) = period of 100 connections where weight counter is reset
    -state is an addition or deduciton based on if the ip connected or disconneceted
    -rating increases the later the device is on
    """
    rating+=state*abs(sin((pi*(total_connections)/100)))*(time-11)**2
    rating_data[ip]=[total_connections,rating]
    add_save_data("rating_data",rating_data)

def distribute(f,ip_list):
    file=f
    if type(f)==str:
        f=File(f)

    shard_dir=f.shard()
    os.chdir(shard_dir)
    files=os.listdir()
    shuffle(files)
    ip_pos=0
    location_map={}
    for ip in ip_list:
        location_map[ip]=[]

    for shard in files:
        location_map[ip_list[ip_pos]].append(shard_dir+"/"+shard)
        ip_pos+=1
        if ip_pos >=len(ip_list):
            ip_pos=0

    direct_dir,send_dir=direct_map(location_map)
    name=hasher(f.path)
    send_dirs[name]=send_dir
    direct_dirs[name]=direct_dir
    add_save_data("send_dirs",send_dirs)
    add_save_data("direct_dirs",direct_dirs)
    os.remove(file)

def direct_map(location_map):
    ips=[]
    files=[]
    for ip_set in location_map.items():
        ips.append(ip_set[0])
        files.append(ip_set[1])
    direct_dir={}
    for ip in ips:
        direct_dir[ip]=[]
    for ip_pos,file_set in enumerate(files):
        out=[]
        for file in file_set:
            out.append([os.path.getsize(file),file])
        direct_dir[ips[ip_pos]]=out
    outfiles =[]
    name=os.path.basename(list(location_map.items())[0][1][0])
    name=name.split(":::")[1]
    if not os.path.exists(f"{middir}/{name}"):
        os.mkdir(f"{middir}/{name}")

    for item in location_map.items():
        ip=item[0]
        files=item[1]
        name=os.path.basename(files[0])
        name=name.split(":::")[1]
        ipname=str(ip)+":::"+name
        compress_file=middir+"/"+name+"/"+ipname+".bin"
        out_file = open(compress_file,'wb')
        for file in files:
            with open(file,"rb") as f:
                out_file.write(f.read())
                f.close()

        out_file.close()
        f=File(compress_file)
        compress_file=f.compress()
        outfiles.append(compress_file)
    send_dir = {}
    for ip,file in zip(ips, outfiles):
        send_dir[ip]=file
    for item in send_dir.items():
        commands("file",path=item[1],ip=item[0])
        os.remove(item[1])
    return direct_dir,send_dir

def network_request(direct_dir,send_dir):
    iplist=[ip[0] for ip in send_dir.items()]
    file=send_dir[iplist[0]]
    file=os.path.basename(file)
    name=file[file.index('.'):]
    ips=connect_test(iplist)
    live_devices_direct_dir_update={}
    for ip_info in direct_dir.items():
        ip=ip_info[0]
        file_info=ip_info[1]
        if ip in ips:
            live_devices_direct_dir_update[ip]=file_info
            request_file=send_dir[ip]
            request_file=request_file[request_file.rindex("/")+1:]
            rating_algorithm(ip,True)
            commands('rqst',path=request_file,ip=ip)
        else:
            send_dir[ip]=""
            send_dirs[name]=send_dir
            add_save_data("send_dirs", send_dir)
            rating_algorithm(ip,False)
    return live_devices_direct_dir_update, send_dir,file_save_dir

def getlen(dir_,num):
    num+=len(dir)
    return num

def rebuild(direct_dir,send_dir,file_loc):
    send_len=len(send_dir)

    for i in send_dir.values():
        if i=="":
            send_len-=1
    os.chdir(file_loc)
    files_temp=[]
    for i in send_dir.items():
        if i[1] =='':
            direct_dir[i[0]]=''
            continue
        files_temp.append(os.path.basename(i[1]))

    tot=0
    cur=os.listdir()

    while True:
        for i in files_temp:
            if i in cur:
                tot+=1
        if len(files_temp)==tot:
            break
        tot=0
        cur=os.listdir()
        sleep(1)

    lens=[0 for i in range(len(files_temp))]
    running=True

    while running:
        temp=lens
        for pos,file in enumerate(files_temp):
            if not lens[pos]==os.path.getsize(file):
                lens[pos]= os.path.getsize(file)
                break
        if temp==lens and lens[-1]>100:
            running=False

    running=True
    while running:
        for file in files_temp:
            try:
                if ".gz" in file and file in os.listdir():

                    deflate(file)
            except (EOFError):
                os.remove(file[:len(file)-3])
                sleep(1)

        for i in os.listdir():
            if ".gz" in i and i in files_temp:
                running=True
                break
            else:
                running=False
        if not running:
            break
        sleep(1)
        #include offload option
    base_files=[i[:len(i)-3] for i in files_temp]
    compress_files=[]
    for i in os.listdir():
        if i in base_files:
            compress_files.append(i)
    name=os.path.basename(list(direct_dir.items())[0][1][0][1])
    name=name.split(":::")[1]
    for i in compress_files:
        if name not in i:
            compress_files.remove(i)
    if '.DS_Store' in compress_files:
        compress_files.remove('.DS_Store')
    name = compress_files[0].split(":::")[1]
    shard_dir = list(direct_dir.items())[0][1][0][1]
    shard_dir=shard_dir[:shard_dir.rindex("/")]
    for file in compress_files:
        info = file.split(":::")
        ip=info[0]
        file_info=direct_dir[ip]
        if not file_info:
            continue
        readfile = open(file,"rb")

        for file_set in file_info:
            with open(file_set[1],"wb") as shard:
                shard.write(readfile.read(file_set[0]))
                shard.close()
        readfile.close()
        os.remove(file)
    return shard_dir

def clear_stored():
    os.chdir(file_save_dir)
    for file in os.listdir():
        os.remove(file)

def del_from_network(file):
    send_dir=send_dirs[hasher(file)]
    iplist=[ip[0] for ip in send_dir.items()]
    ips=connect_test(iplist)
    for ip in ips:
        commands("del",path=send_dir[ip],ip=ip)
    del direct_dirs[hasher(file)]
    del send_dirs[hasher(file)]

def boot():
    with open("requirements.txt","r") as f:
        for i in f.readlines():
            os.system(f"pip3 install {i}")
if __name__=="__main__":
    if dev_ip in wlan_ips:
        wlan_ips.pop(wlan_ips.index(dev_ip))
    ips=wlan_ips
    file="/home/pi/Downloads/1008-Article Text-4742-1-10-20131007.pdf"
    #distribute(file,ips)
    file_request(file)
    #del_from_network(file)
    #FIX TIMING ISSUE
    save_close()
