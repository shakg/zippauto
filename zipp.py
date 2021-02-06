import os
import time
import shutil
from datetime import date
import threading
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def greetUser():
    print("======================================================")
    print("|                                                    |")
    print("|            Hello, welcome to zipp!                 |")
    print("|  You can set a directory to zip it in given times. |")
    print("|                                                    |")
    print("======================================================")

def askForDirectoryLocation():
    print("\n")
    locationToZip = input(">>> Which folder to zipp : ")
    return locationToZip

def validateLocation(location):
    if(os.path.exists(location)):
        return True
    print(">>> I did not find the file at {0} ".format(str(location)))
    return False

def zipFilesInDir(location):
    print(">>> Zipping the {0}".format(str(location)))
    retval = shutil.make_archive(os.sep.join([location,str(date.today())]), "zip", str(location))
    return retval

def googleDriveAuth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def showProgressBar():
    while True:
        print(".", end="")
        time.sleep(0.5)
        global stopProgressBar
        if stopProgressBar:
            break

def moveZipFile(createdZipFile,pathOfCopies):

    if(os.path.exists(pathOfCopies)):
        pass
    else:
        try:
            os.mkdir(pathOfCopies)
        except EnvironmentError as env:
            return str(env)
        else:
            pass
    try:
        shutil.copy(createdZipFile,pathOfCopies)
    except IOError as e:
        return str(e)
    except EnvironmentError as env:
        return str(env)
    else:
        return ""
    
def deleteOriginalFile(location):
    try:
        os.remove(location)
    except EnvironmentError:
        return 0
    else:
        return 1


pathOfCopies = os.sep.join(["D:","ZippAutoCopies"])
stopProgressBar = False
greetUser()
locationThatUserGave = askForDirectoryLocation()
isValid = validateLocation(location=locationThatUserGave)
if(isValid):
    threading.Thread(target=showProgressBar).start()
    result = zipFilesInDir(locationThatUserGave)
    if(result != None or result != ""):
        print("\n")
        print(">>> Your zip file ({0}) has been created.\n ".format(result))
        stopProgressBar = True
        moveZipFileResult = moveZipFile(result,pathOfCopies)
        if(len(moveZipFileResult)<=1):
            print(">>> Your zip file has been transfered to D:\\ZippAutoCopies")
            if(deleteOriginalFile(result)):
                print(">>> Your original zip file has been deleted from {0}".format(locationThatUserGave))
            else:
                print(">>> Something went wrong while deleting your original zip file. ")

        else:
            print(">>> Something went wrong while copying files.")

    print(">>> Authenticating to google.")
    drive = googleDriveAuth()
    
    print(">>> Authenticated..")
    print(">>> Uploading files to Google Drive.")

    threading.Thread(target=showProgressBar).start()
    for x in os.listdir(pathOfCopies):

        f = drive.CreateFile({'title': x}) 
        f.SetContentFile(os.path.join(pathOfCopies, x)) 
        f.Upload() 
        # Due to a known bug in pydrive if we  
        # don't empty the variable used to 
        # upload the files to Google Drive the 
        # file stays open in memory and causes a 
        # memory leak, therefore preventing its  
        # deletion 
        f = None
    
    stopProgressBar = True
    print(">>> Upload completed.")
    input()





