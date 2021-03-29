import socket
import os
import sys
import time
import random
from numba import jit

SEPARATOR = "<SEPARATOR>"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()


def connect(addr=host, test=False, bound=20):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(5025, 5025+bound):
        try:
            s.connect((addr, i))
            if test:
                s.close()
            return True
        except (ConnectionRefusedError, BrokenPipeError, OSError):
            if i == 5025+bound:
                return False
            continue


"""path =rudi_giu.getFile()[0]
k = open(path,"rb")"""


def request_file_path(name, ip):
    name = os.path.basename((name))
    connect(ip)
    out = str(f"RQST{SEPARATOR}{name}{SEPARATOR}")
    s.send(cmdAlter(out))


def connect_test(ips, test=False, set=0):
    if test:
        for i in range(set):
            key = random.randint(0, len(ips)-set)
            ips[key] = ""
        return ips

    if type(ips) == str:
        ips = ips.split(",")
    for pos, ip in enumerate(ips):
        if not connect(ip, test=True):
            ips[pos] = ""
    return ips


def commands(cmd, path="", ip=""):
    if cmd == "file":
        define_file(path, ip)
    if cmd == "rqst":
        request_file_path(path, ip)
    if cmd == "update":
        define_file(path, ip, update=True)
    if cmd == "del":
        send_del(path, ip)


def send_del(file, ip):
    file = os.path.basename(file)
    if connect(ip):
        out = f"DEL{SEPARATOR}{file}{SEPARATOR}"
        out = cmdAlter(out)
        s.sendall(out)


def cmdAlter(cmd):
    size = len(cmd)
    size = 200-size
    if size > 0:
        cmd += " "*size
        return (cmd.encode("utf-8"))


def send_mult(cur_dir, ip, exclude=[], update=False):
    for i in cur_dir:
        if i in exclude:
            continue
        if not update:
            commands("file", path=i, ip=ip)
        else:
            commands("update", path=i, ip=ip)
        s.close()


def send_mult_dict(ip_dict, exclude=[]):
    fail = []
    for set_ in ip_dict.items():
        ip = set_[0]
        files = set_[1]
        try:
            send_mult(files, ip, exclude)
        except BrokenPipeError:
            fail.append(ip)
    return fail


def define_file(path, ip, buffer=16536, update=False):
    time.sleep(.5)
    if connect(ip):
        name = os.path.basename(path)
        if not update:
            out = str(f"FILE{SEPARATOR}{name}{SEPARATOR}{buffer}")
        if update:
            out = str(f"UPDATE{SEPARATOR}{name}{SEPARATOR}{buffer}")
        s.send(cmdAlter(out))
        time.sleep(.3)
        with open(path, "rb") as f:
            sendfile(f, buffer)
        s.close()
    time.sleep(.5)


@jit(forceobj=True)
def sendfile(k, buffer):
    while True:
        read = k.read(buffer)
        if not read:
            break
        s.sendall(read)
    s.close()


if __name__ == "__main__":

    file = "/Users/calebsirak/Downloads/463-Article Text-2446-1-10-20130328.pdf"
    ip = "192.168.1.211"
    define_file(file, ip)
