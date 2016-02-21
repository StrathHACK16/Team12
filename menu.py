import subprocess
import pickle
from NotificationMessage import NotificationMessage
from EntryMessage import EntryMessage
from DropDownMessage import DropDownMessage

class inputMenu:
  def __init__(self,CurrentRepo,ArduinoComm):
    self.input=input
    self.CurrentRepo=CurrentRepo
    self.Checkout=CurrentRepo.listofBranches
    self.ArduinoComm=ArduinoComm
    self.mainMenu=True
    self.MenuList=["Commit","Push","Pull","New Branch","Merge","Checkout","Log","Status"]
    self.index=0
    self.submenuIndex=0
    self.Checkout=False
    self.Confirm="Yes           No"


  def menuNavigate(self,input):
    if(input==0): #setting up
      self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "000")

    if(input==1): #right
      if(not self.mainMenu and (self.index==1 or self.index==2 or self.index==5)):
        self.index=0
        self.mainMenu=True
        self.Checkout=False
        self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
     
    elif(input==2): #up
      if(self.mainMenu):
        self.index+=len(self.MenuList)-1
        self.index%=len(self.MenuList)
        self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
      elif(self.Checkout):
        self.submenuIndex += len(self.CurrentRepo.listofBranches) - 1
        self.submenuIndex %= len(self.CurrentRepo.listofBranches)
        self.ArduinoComm.SendData("Checkout which branch?", self.CurrentRepo.listofBranches[self.submenuIndex], "221")
    elif(input==3): #down
      if(self.mainMenu):
        self.index+=1
        self.index%=len(self.MenuList)
        self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
      elif(self.Checkout):
        self.submenuIndex += 1
        self.submenuIndex %= len(self.CurrentRepo.listofBranches)
        self.ArduinoComm.SendData("Checkout which branch?", self.CurrentRepo.listofBranches[self.submenuIndex], "221")
    elif(input==4): #left = yes
      if(not self.mainMenu): # we're in the submenu
        if (self.index==1): # push
          #execute push
          self.ArduinoComm.SendData("","","223") # Flash while processing
          cmd = ["git", "push","-u","origin",self.CurrentRepo.listofBranches[0]]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()

          self.index=0
          self.mainMenu=True
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
        if (self.index==2): # pull
          #execute pull
          self.ArduinoComm.SendData("","","223") # Flash while processing
          cmd = ["git", "pull"]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()

          self.index=0
          self.mainMenu=True
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
        if (self.index==5): # checkout
          #execute checkout
          cmd = ["git", "checkout", self.CurrentRepo.listofBranches[self.submenuIndex]]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()


          temp = self.CurrentRepo.listofBranches[self.submenuIndex]
          self.CurrentRepo.listofBranches[self.submenuIndex] = self.CurrentRepo.listofBranches[0]
          self.CurrentRepo.listofBranches[0] = temp
          self.index=0
          self.mainMenu=True
          self.Checkout=False
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")

    elif(input==5): #select
      if (self.mainMenu):
        if self.index==0:
          #print("Paul")
          #COMMIT THING GO HERE
          #call enter message Gui
          cmd=["git", "diff"]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()
          cmd=["git", "status", "-s"]
          soutput = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          soutput = soutput.stdout.read()
          if output != "" or soutput.startswith("A "):
            self.ArduinoComm.SendData("","","221") # red led on
            EntryMessage("Enter commit message:")
            with open("EntryText.pickle",'r') as a:
              test=pickle.load(a)
            a.close()
            cmd = ["git", "commit", "-a", "-m", test]
            output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            output = output.stdout.read()
            self.ArduinoComm.SendData("","","220") #red led off
        elif(self.index==1): # PULL
          self.mainMenu=False
          self.ArduinoComm.SendData("Push?", self.Confirm, "221")
        elif(self.index==2): # PULL
          self.mainMenu=False          
          self.ArduinoComm.SendData("Pull?", self.Confirm, "221")
        elif(self.index==3):
          #BRANCH me baby
          #call enter messsage Gui
          self.ArduinoComm.SendData("","","221") # red led on
          EntryMessage("Enter new branch name:")
          with open("EntryText.pickle",'r') as b:
            test=pickle.load(b)
          b.close()
          cmd = ["git", "branch", test]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()
          self.CurrentRepo.listofBranches = self.CurrentRepo.listofBranches + [test]
          self.ArduinoComm.SendData("","","220") # red led off
        elif(self.index==4):
          #MERGE here
          #call drop down entry Gui
          self.ArduinoComm.SendData("","","221") # red led on
          DropDownMessage(self.CurrentRepo.listofBranches)
          with open("DropDownBranchText.pickle",'r') as c:
            test=pickle.load(c)
          c.close()

          cmd = ["git", "merge", test]

          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()

          self.CurrentRepo.listofBranches.remove(test)
          self.ArduinoComm.SendData("","","220") # red led off

        elif(self.index==5): # CHECKOUT
          self.mainMenu=False
          self.Checkout=True
          self.submenuIndex=0
          self.ArduinoComm.SendData("Checkout which branch?", self.CurrentRepo.listofBranches[self.submenuIndex],"221")
        elif(self.index==6): # LOG
          cmd = ["git", "log", "--oneline"]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()
          NotificationMessage(output)
          self.index = 0
          self.mainMenu =True
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
        elif(self.index==7): # STATUS
          cmd = ["git", "status"]
          output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
          output = output.stdout.read()
          NotificationMessage(output)
          self.index = 0
          self.mainMenu =True
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
      elif(self.Checkout):
        if(self.submenuIndex==self.CurrentRepo.branch): # we're already in this branch
          self.mainMenu=True
          self.Checkout=False
          self.index=0
          self.ArduinoComm.SendData(self.branchString(), self.MenuList[self.index], "220")
        else: # confirm whether to checkout branch
          self.ArduinoComm.SendData("Checkout " + self.CurrentRepo.listofBranches[self.submenuIndex] + "?", self.Confirm, "221")

  
  def branchString(self):
      return self.CurrentRepo.repoName + ":" + self.CurrentRepo.listofBranches[self.CurrentRepo.branch]
