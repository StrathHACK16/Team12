import Tkinter
from Tkinter import *
import pickle

class EntryMessage:
    def __init__(self, lblText):
        self.master = Tk()
        self.master.title("WeeGit v1.0")
        self.inputText = StringVar(self.master)

        self.labelText = StringVar(self.master)
        self.labelText.set(lblText)
        
        self.build()
    def build(self):

        self.frame = Frame(self.master)

        self.label = Label(self.master, textvariable = self.labelText)
        
        self.label.pack()
        
        self.entrybox = Entry(self.master, textvariable = self.inputText)
        self.entrybox.focus_set()
        self.entrybox.pack()
            
        subButt = Button(self.master, text = "Submit Text", command = self.submit)
        subButt.pack()
        self.frame.pack()
        self.master.bind("<Return>", self.submit)
        self.master.mainloop()
    def submit(self,event):
        with open("EntryText.pickle",'wb') as n:
            pickle.dump(self.inputText.get(),n)
        n.close()
        self.destroyBox()
    def destroyBox(self):
        self.master.destroy()