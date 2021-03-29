from threading import Thread

def threader(func):
    t1=Thread(target=func)
    t1.start()
    