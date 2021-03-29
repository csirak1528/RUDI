from tkinter import *
from tkinter import filedialog
import os
 
def getFile():
    path = filedialog.askopenfile(initialdir = "/Users/calebsirak",title = "Select file")
    file  = os.path.basename(path.name)
    fileType = file[file.index(".") +1:]
    return path.name,file,fileType

class RudiGui:
    def __init__(self,root):
        self.root = root
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("RUDI File System")
        self.sidebar = Frame(root, width=200, bg='white', height=self.height, borderwidth=10)
        self.sidebar.pack(expand=True, fill='both', side='left', anchor='nw')

        self.mainarea = Frame(root, bg='white', width=self.width - 200, height=self.height)
        self.mainarea.pack(expand=False, fill='both', side='right')

    def add_button():
        pass
    def sidebar():
        pass
    def header():
        pass
    def actions():
        pass
if __name__ == "__main__":
    root = Tk()
    k = RudiGui(root)
    root.mainloop()
