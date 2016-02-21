import Tkinter
from Tkinter import *
import tkMessageBox
class NotificationMessage:
    def __init__(self,message):
        self.master = Tk()
        self.master.title("WeeGit v1.0")
        self.mb = tkMessageBox.showinfo("Information Notice",message)
        self.build()
    def build(self):
        self.master.destroy()
    
