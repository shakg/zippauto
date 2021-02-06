import os
from os.path import isfile
import time
import shutil
from datetime import date
import threading
from oauth2client.clientsecrets import Error
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
    if(thereIsCredentialsFile()):
        gauth.LoadCredentialsFile("credentials.txt")
    else:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("credentials.txt")
    drive = GoogleDrive(gauth)
    return drive

def thereIsCredentialsFile():
    if(os.path.isfile(os.sep.join([os.path.abspath(os.getcwd()),"credentials.txt"]))):
        return True
    else:
        return False
    
def showProgressBar():
    while True:
        print(".", end="")
        time.sleep(0.5)
        global stopProgressBar
        if stopProgressBar:
            break

def createFolderToCopyIfNotExists(pathOfCopies):

    if(os.path.exists(pathOfCopies)):
        return True
    else:
        try:
            os.mkdir(pathOfCopies)
        except EnvironmentError:
            return False
        else:
            return True

def copyZippedFile(createdZipFile,pathOfCopies):
    try:
        shutil.copy(createdZipFile,pathOfCopies)
    except IOError:
        return False
    except EnvironmentError:
        return False
    else:   
        return True

def moveZipFile(createdZipFile,pathOfCopies_Array):

    for x in range(0,len(pathOfCopies_Array)):
        if(createFolderToCopyIfNotExists(pathOfCopies_Array[x])):
            if(copyZippedFile(createdZipFile, pathOfCopies_Array[x])):
                return pathOfCopies_Array[x]
        else:
            if(x==(len(pathOfCopies_Array)-1)):
                return "There is an error while creating the folder!"
            else:
                pass

def deleteFolder(location):
    try:
        for x in os.listdir(location):
            try:
                if(deleteFile(os.sep.join([location,x]))):
                    print("<<< File deleted. => {0}".format(x))
                else:
                    print("<<< Cannot delete file. => {0}".format(x))

            except:
                print(">>> Cannot delete file. => {0}".format(x))
            else:
                pass
    except:
        print(">>> There was a problem while listing the files in folder.")
        return False
    else:
        return True


def deleteFile(location):
    try:
        os.remove(location)
    except EnvironmentError as ee:
        print("$$$$$ Delete file error. =====> {0}".format(ee))
        return 0
    else:
        return 1

def uploadFileToDrive(pathOfCopies,drive):
    try:
        for x in os.listdir(pathOfCopies):
            f = drive.CreateFile({'title': x}) 
            f.SetContentFile(os.path.join(pathOfCopies, x)) 
            f.Upload() 
            f = None
    except Error:
        return False
    else:
        return True

pathOfCopies_Array = []

pathOfCopies_First = os.sep.join(["D:","ZippAutoCopies"])
pathOfCopies_Array.append(pathOfCopies_First)

pathOfCopies_Alternative = os.sep.join(["C:","ZippAutoCopies"])
pathOfCopies_Array.append(pathOfCopies_Alternative)

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
        moveZipFileResult = moveZipFile(result,pathOfCopies_Array)
        if(moveZipFileResult != "There is an error while creating the folder!"):
            print(">>> Your zip file has been transfered to {0}".format(moveZipFileResult))
            if(deleteFile(result)):
                print(">>> Your original zip file has been deleted from {0}".format(locationThatUserGave))
            else:
                print(">>> Something went wrong while deleting your original zip file. ")
            
            #Auth to google and upload files.
            print(">>> Authenticating to google.")
            drive = googleDriveAuth()
            print(">>> Authenticated..")
            print(">>> Uploading files to Google Drive.")
            
            if(uploadFileToDrive(moveZipFileResult,drive)):
                print(">>> Upload completed.")
                print(">>> Deleting uploaded files from {0}".format(locationThatUserGave))
                if(deleteFolder(locationThatUserGave)):
                    print(">>> Delete completed.")
                else:
                    print(">>> Cannot delete file.")
            else:
                print(">>> There was a problem while uploading your file.")

        else:
            print(">>> Something went wrong while copying files.")

    




