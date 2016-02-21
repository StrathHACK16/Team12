import serial
import pickle
import subprocess
import os
from menu import inputMenu
from GUI_class import GUI
#import ProcessRun
#import
from ArduinoComms import ArduinoComms2
def main():
  ArduinoComm=ArduinoComms2("/dev/ttyACM2",9600)
  ArduinoComm.SendData('WeeGit v1.0','Setting up...','000')
  Git_Data=populateRepoList() #get list of repos from file. Git Data is a list of repo objects.
  #Display Setup Message on Arduino
  #list1=["one", "two"]
  #Git_Data=[Repository("test",list1,"test","test","test","test","testURL"),Repository("test",list1,"test","test","test","test","testURL")]
  GUI
  _Start=GUI(Git_Data)
  Git_Data=populateRepoList()

  index=getIndex() #Git_Data[index] is the repo we want.
  os.chdir(Git_Data[index].gitPath)
  Git_Data[index].listofBranches=getBranches(Git_Data[index].gitPath)
  #serializeData(Git_Data)
  MainLoop(ArduinoComm, Git_Data[index])

def serializeData(Git_Data):
    if(Git_Data is not None):
        with open("a-file.pickle",'wb') as f:
            pickle.dump(Git_Data,f)
        f.close()

def populateRepoList():
    with open("a-file.pickle",'r') as f:
        Git_Data=pickle.load(f)
    f.close()
    return Git_Data

def MainLoop(ArduinoComm, repo):
  CurrentRepo=repo
  menu=inputMenu(CurrentRepo, ArduinoComm)
  menu.menuNavigate(0)
  while(True):
    cmd=["git", "diff"]
    output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = output.stdout.read()
    cmd=["git", "status", "-s"]
    soutput = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    soutput = soutput.stdout.read()
    if output == "" and not soutput.startswith("A "):
      ArduinoComm.SendData("","","102")
    else:
      ArduinoComm.SendData("","","012")
    cmd=["git", "status"]
    output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = output.stdout.read()
    if output.startswith("HEAD detached"):
      ArduinoComm.SendData("","","032")
    input=ArduinoComm.ReadData()
    menu.menuNavigate(input)

    

def getIndex():
    with open("index",'r') as f:
        repo_index=pickle.load(f)
    f.close()
    return repo_index

def getBranches(path):
    cmd=["git", "branch"]
    output = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    branchRaw= output.stdout.read()
    branchRaw=branchRaw.split('\n')
    out=[]
    for s in branchRaw:
      s=s.strip()
      if s != "":
        if s[0] == '*':
          out = [s[2:]] + out
        else:
          out += [s]
    print(out)
    return out

class Repository:
  def __init__(self,repoName,listofBranches,username,password,sshKeyPath,gitPath,gitURL):
      print("init")
      self.repoName=repoName
      self.listofBranches=listofBranches
      self.branch=0
      self.username=username
      self.password=password
      self.sshKeyPath=sshKeyPath
      self.gitPath=gitPath
      self.gitURL=gitURL
if __name__ == "__main__":
  main()
