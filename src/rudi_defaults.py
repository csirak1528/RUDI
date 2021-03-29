import platform
import getpass
import os
import sys
import netifaces as ni

app_dir=os.getcwd()
sys_dir=os.getcwd()

system =platform.system()
sys_defaults = ""
if system == "Darwin":
    wireless="en0"
    download=f"/Users/{getpass.getuser()}/Downloads"
    outdir=f"/Users/{getpass.getuser()}/out"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    middir=f"/Users/{getpass.getuser()}/mid"
    if not os.path.exists(middir):
        os.mkdir(middir)

if system == "Linux":
    download=f"/home/{getpass.getuser()}/Downloads/"
    wireless="wlan0"
    outdir=f"/home/{getpass.getuser()}/out"

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    middir=f"/home/{getpass.getuser()}/mid"
    if not os.path.exists(middir):
        os.mkdir(middir)

packet_size = 16536
buffer_size =1024
#dir where binary files store
if system == "Linux":
    stored_dir =  "/home/"+getpass.getuser()+ "/stored"
    if not os.path.isdir(stored_dir):
        os.mkdir(stored_dir)

    file_save_dir =""
    if file_save_dir == "":
        file_save_dir ="/home/pi/Desktop/onRudi"
        if not os.path.isdir(file_save_dir):
            os.mkdir(file_save_dir)

if platform.system() == "Darwin":
    stored_dir =  "/Users/"+getpass.getuser()+ "/stored"
    if not os.path.isdir(stored_dir):
        os.mkdir(stored_dir)

    file_save_dir =""
    if file_save_dir == "":
        file_save_dir = "/Users/"+getpass.getuser()+"/Desktop/onRudi"
        if not os.path.isdir(file_save_dir):
            os.mkdir(file_save_dir)


if platform.system() =="Windows":
    pass


try:
    if sys.argv[1] == "-u":
        p = input("r:1-add\n  2-change\nr:")

        if p =="1":
            ip = input("r: ip-")
            k = input(f"Device name {i}:")
            if not k == "":
                names[k] = ip

        if p =="2":
            for i in iplist:
                k = input(f"Device name {i}:")
                if not k == "":
                    nameseth[k] = i

            for j in ethlist:
                k = input(f"Device name {j}:")
                if not k == "0":
                    nameswlan[k] = j
except IndexError:
    pass

dev_ip=ni.ifaddresses(wireless)[ni.AF_INET][0]['addr']
#file definition and command size
define_size = 200
user_choice =""
#files downloaded are saved
