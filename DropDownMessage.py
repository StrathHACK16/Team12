import Tkinter
from Tkinter import *
import pickle

class DropDownMessage:
    def __init__(self, collection):
        self.master = Tk()
        self.master.minsize(height = 250, width = 250)
        self.inputText = StringVar(self.master)

        self.currentBranch = StringVar(self.master)
        
        self.branchCol= collection
        self.OPTIONS = []
        
        self.build(self.branchCol)
    def build(self, collection):
        branchCol = collection
        for x in branchCol:
            self.OPTIONS.append(x)
        
        self.frame = Frame(self.master)

        self.label = Label(self.master, text = "Select Branch")
        self.label.pack(side = TOP)
        
        self.currentBranch.set(self.OPTIONS[0])
        branchselect = apply(OptionMenu, (self.frame, self.currentBranch) + tuple(self.OPTIONS))
        branchselect.pack(side = TOP)

        subButt = Button(self.master, text = "Submit Branch", command = self.submit)
        subButt.pack(side = BOTTOM)
        self.frame.pack()
        self.master.mainloop()
    def submit(self):
        with open("DropDownBranchText.pickle",'wb') as n:
            pickle.dump(self.currentBranch.get(),n)
        n.close()
        print(self.currentBranch.get())
        self.destroyBox()
    def destroyBox(self):
        self.master.destroy()
