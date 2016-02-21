from GUI_class import GUI

class Repository:
  repoName=""
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




def main():
  list=["test1","test2"]
  thing = Repository("test",list,"test","test","test","test","testURL")
  thing2 = Repository("test2",list,"test","test","test","test","testURL")
  test=[thing,thing2]
  testGUI=GUI(test)
  #HackingOffTheTrain ;) Giggedy?
if __name__ == "__main__":
  main()
