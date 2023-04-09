import requests
import json
import glob
import os
import sys
import tkinter

def isHostedFileDifferent(url, file):
    with open(file, "r") as f:
        local = f.read()
        hostedRes = requests.get(url)
        hosted = hostedRes.text
        if hostedRes.status_code == 404:
            print("File not found on GitHub")
            return False
        elif hosted != local:
            return True
        else:
            return False
        
def updateFile(url, file):
    hosted = requests.get(url).text
    with open(file, "w") as f:
        f.write(hosted)
        
def getProjectFiles():
    files = glob.glob("*.*")
    return files

def creatFileLists():
    projectName = os.path.basename(os.getcwd())
    files = []
    for file in getProjectFiles():
        url = "https://raw.githubusercontent.com/TheEpicFace007/{projectName}/main/{file}".format(projectName=projectName, file=file)
        files.append((url, file))
    return files

def updateAllFiles(updateGui: tkinter.BaseWidget):
    files = creatFileLists()
    for i, (url, file) in enumerate(files):
        if not isHostedFileDifferent(url, file):
            status = f"({i}/{len(files)} Updating {file}..."
            updateGui.event_generate("<<UpdateProgress>>", when="tail", arg={"status": status})
            print(status)
    
if __name__ == '__main__':
    creatFileLists()
    