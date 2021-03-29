#necassary dirs stored dir
import os
import gzip
import shutil
import hashlib
import rudi_defaults

hasher = lambda x: hashlib.sha256(x.encode()).hexdigest()
SEPARATOR = ":::"

class File:
    def __init__(self,file):
        self.fileType = file[file.index(".")+1:]
        self.path = file
        self.starterpath = file[:len(file) - len(os.path.basename(file))]
        self.file = os.path.basename(file)
        try:
            self.length = os.path.getsize(self.path)
        except FileNotFoundError:
            pass
        self.name = file[:file.index(".")]
        self.local()
        self.fileDir = self.name
        if ".gz" in file:
            self.oldFile = file[:len(file)-3]
            self.fileType = self.oldFile[self.oldFile.index(".")+1:]
        else:
            self.oldFile =""

    def shard(self):
        self.local(True)
        j = 0
        os.chdir(rudi_defaults.stored_dir)
        hashed = hasher(self.path)
        if not os.path.exists(hashed):
            os.mkdir(hashed)
        filesize = os.path.getsize(self.path)
        f = open(self.path,"rb")
        os.chdir(hashed)
        for i in range(filesize,0, -16536):
            num = len(str(j))
            j = (5-num) * "0" + str(j)
            name = self.fileType+":::"+hashed+":::"+str(j)+".bin"
            file = open(name,"wb")
            file.write(f.read(16536))
            file.close()
            j = int(j)+1
        return os.getcwd()

    def local(self, stored=False):
        if stored:
            os.chdir(rudi_defaults.stored_dir)
        else:
            os.chdir(self.starterpath)

    def changeDir(self,newloc):
        shutil.move(self.path,newloc+"/"+self.file)

    def compress(self):
        with open(self.path, 'rb') as f_in:
            #defines the new compressed files name
            newfilename = self.path + ".gz"
            #creates new compressed file to write too
            with gzip.open(newfilename, "wb") as f_out:
                #adds contents of bin file to compressed file, removes bin from directory and resets directory for next file
                shutil.copyfileobj(f_in, f_out)
                os.remove(self.path)
        return newfilename

    def deflate(self):
        name=self.file
        name=self.oldFile
        new = open(name,"wb")
        with gzip.open(self.file, "rb") as f:
            file_content = f.read()
        new.write(file_content)
        os.remove(self.file)
        new.close()
        return name

    def toFile(self, buffer=16536,r = True):
        if r:
            mode = "rb"
        else:
            mode = "wb"
        with open(self.path, mode) as f:
            return f.read(buffer)

def build(shardLoc):
    name = shardLoc[shardLoc.rindex("/")+1:]
    dirPath = shardLoc
    os.chdir(dirPath)
    files= os.listdir()
    files = sorted(files)
    define = files[1]
    define = define.split(SEPARATOR)
    fileType = define[0]
    name = define[1]
    newname = f"{name}.{fileType}"
    newfile = open(newname,"wb")

    for file in files:
        k = open(file,"rb")
        newfile.write(k.read())
        os.remove(file)
    newfile.close()
    new = File(f"{dirPath}/{newname}")
    new.changeDir(rudi_defaults.download)
    return rudi_defaults.download+new.file

def deflate(file):
    name=file[:file.rindex('.')]
    new = open(name,"wb")
    with gzip.open(file, "rb") as f:
        file_content = f.read()
    new.write(file_content)
    os.remove(file)
    new.close()
    return name
def rename(old, name):
    dir_=old.replace(os.path.basename(old),'')
    oldname=old.replace(dir_,'')
    type=oldname.split('.')[1]
    new=f"{dir_}/{name}"
    os.chdir(dir_)
    os.rename(old,new)

if __name__=="__main__":
    pass
