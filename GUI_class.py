
#import GUI framework
import Tkinter
from Tkinter import *
import pickle
class GUI:
    def __init__(self,listOfRepos):

    #create new window
        self.top = Tk()
        self.top.title("WeeGit v1.0")
        #Boolean
        self.ConfirmPressed=False
    #create frame within window
        self.frame = Frame(self.top)

    #create lines for frame
        self.l1 = Frame(self.frame)
        self.l2 = Frame(self.frame)
        self.l3 = Frame(self.frame)
        self.l4 = Frame(self.frame)
        self.l5 = Frame(self.frame)
        self.l6 = Frame(self.frame)

    #build variables for GUI
        self.currentrepo = StringVar(self.top)
        self.username = StringVar(self.top)
        self.password = StringVar(self.top)
        self.sshpath = StringVar(self.top)
        self.gitpath = StringVar(self.top)
        self.url = StringVar(self.top)

    #set entry boxes to variable values
        self.userentry = Entry(self.l2, textvariable = self.username)
        self.passentry = Entry(self.l3, show = "*", textvariable = self.password)
        self.sshpathentry = Entry(self.l4, textvariable = self.sshpath)
        self.gitpathentry = Entry(self.l5, textvariable = self.gitpath)
        self.urlentry = Entry(self.l6, textvariable = self.url)

    #set global variables
        self.RepoCol= listOfRepos
        self.currentRepoIndex = 0
        self.OPTIONS = []
        self.update()
        self.Window1(self.RepoCol)

    #update button function which adds the current repo's other values
    def update(self):
        i = 0
        for x in self.OPTIONS:
            if (self.currentrepo.get() == self.OPTIONS[i]):
                self.currentRepoIndex = i
            i = i + 1

        self.userentry.delete(0, 4192)
        self.passentry.delete(0, 4192)
        self.sshpathentry.delete(0, 4192)
        self.gitpathentry.delete(0, 4192)
        self.urlentry.delete(0, 4192)

        self.userentry.insert(0,self.RepoCol[self.currentRepoIndex].username)
        self.passentry.insert(0,self.RepoCol[self.currentRepoIndex].password)
        self.sshpathentry.insert(0,self.RepoCol[self.currentRepoIndex].sshKeyPath)
        self.gitpathentry.insert(0,self.RepoCol[self.currentRepoIndex].gitPath)
        self.urlentry.insert(0,self.RepoCol[self.currentRepoIndex].gitURL)

    #confirm button, superfluous
    def confirm(self):

        self.RepoCol[self.currentRepoIndex].username=self.userentry.get()
        self.RepoCol[self.currentRepoIndex].password=self.passentry.get()
        self.RepoCol[self.currentRepoIndex].sshKeyPath=self.sshpathentry.get()
        self.RepoCol[self.currentRepoIndex].gitPath=self.gitpathentry.get()
        self.RepoCol[self.currentRepoIndex].gitURL=self.urlentry.get()
        #print( self.RepoCol[self.currentRepoIndex].gitPath)
        with open("a-file.pickle",'wb') as f:
            pickle.dump(self.RepoCol,f)
        f.close()
        with open("index",'wb') as s:
            pickle.dump(self.currentRepoIndex,s)
        s.close()
        self.destroyEVERYTHING()
    def returnRepo(self):
        return self.RepoCol[self.currentRepoIndex],self.currentRepoIndex

    def destroyEVERYTHING(self):
        self.top.destroy() #>=)
    #builds the window
    def Window1(self,collection):
        RepoCol = collection
        #add to options
        for x in RepoCol:
            self.OPTIONS.append(x.repoName)


        #build title
        title = Label(self.top, text = "Select Repo\n\n")

        #build Labels
        repolabel = Label(self.l1, text = "Choose Repo\n")
        repolabel.pack(side = LEFT)

        userlabel = Label(self.l2, text = "Username\n")
        userlabel.pack( side = LEFT)

        passlabel = Label(self.l3, text = "Password\n")
        passlabel.pack( side = LEFT)

        sshpathlabel = Label(self.l4, text = "SSH Key Path\n")
        sshpathlabel.pack( side = LEFT)

        gitpathlabel = Label(self.l5, text = "Git Local Path\n")
        gitpathlabel.pack( side = LEFT)

        urllabel = Label(self.l6, text = "Remote URL\n")
        urllabel.pack(side = LEFT)

        #build repoList with options
        self.currentrepo.set(self.OPTIONS[0])
        repoentry = apply(OptionMenu, (self.l1, self.currentrepo) + tuple(self.OPTIONS))
        repoentry.pack(side = RIGHT)


        #build entry boxes
        self.userentry.pack(side = RIGHT)
        self.passentry.pack(side = RIGHT)
        self.sshpathentry.pack(side = RIGHT)
        self.gitpathentry.pack(side = RIGHT)
        self.urlentry.pack(side = RIGHT)

        #pack lines
        self.l1.pack()
        self.l2.pack()
        self.l3.pack()
        self.l4.pack()
        self.l5.pack()
        self.l6.pack()

        title.pack(side = TOP)
        self.frame.pack(side = LEFT)

        #build buttons
        updateButt = Button(self.top, text = "Update", command = self.update)
        updateButt.pack(side = BOTTOM)
        confirmButt = Button(self.top, text =  "Confirm", command = self.confirm)
        confirmButt.pack(side = BOTTOM)

        self.top.mainloop()
