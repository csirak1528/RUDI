import socket
import rudi_user
from sys import exit
from rudi_rqst import *
import rudi_send
import netifaces as ni
import rudi_update
import rudi_defaults
import time
import os
import rudi_data


def get_ip(form):
    return ni.ifaddresses(form)[ni.AF_INET][0]['addr']


SEPARATOR = "<SEPARATOR>"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def binder(type, queue=5):
    for i in range(5025, 5045):
        try:
            s.bind((get_ip(type), i))
            s.listen(queue)
            break
        except OSError:
            continue


def fileScan(filename, buffer, update=False):
    if update:
        name = f"{rudi_defaults.app_dir}/{filename}"
    else:
        name = f"{rudi_defaults.file_save_dir}/{filename}"
    with open(name, "wb") as f:
        while True:
            k = clientsocket.recv(buffer)
            if not k:
                break
            f.write(k)
        f.close()


def remove_from_device(file):
    os.chdir(file_save_dir)
    if file in os.listdir():
        try:
            os.remove(file_save_dir+"/"+file)
        except FileNotFoundError:
            pass


main = "/home/pi/Desktop/RUDI"
wlan = rudi_data.wlan_ips


dev_ip = get_ip(rudi_defaults.wireless)
binder(rudi_defaults.wireless)
while True:
    try:
        clientsocket, address = s.accept()
        print(f'{address}')
    except KeyboardInterrupt:
        exit()

    cmd = clientsocket.recv(200)
    time.sleep(.3)
    cmd = cmd.decode("utf-8")
    cmd = cmd.split(SEPARATOR)

    if cmd[0] == "FILE":
        # FILE defined as 0 - command 1 - file name - 2 - read buffer
        fileScan(cmd[1], int(cmd[2]))
    if cmd[0] == "RQST":
        # RQST defined as 0 - command 1 - file name - 2 - read buffer
        r_request(cmd[1], address[0])
    if cmd[0] == "UPDATE":
        fileScan(cmd[1], int(cmd[2]), True)
    if cmd[0] == "DEL":
        remove_from_device(cmd[1])
