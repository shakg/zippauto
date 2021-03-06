import os
from os.path import isfile
import shutil
from datetime import date
from oauth2client.clientsecrets import Error
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging
import gui

def askForDirectoryLocation():
    print("\n")
    locationToZip = input(">>> Which folder to zipp : ")
    return locationToZip

def validateLocation(location):
    if(os.path.exists(location)):
        return True
    logging.error(">>> Cannot locate file at %s ", str(location))
    return False

def zipFilesInDir(location):
    logging.info(">>> Zipping the %s ", str(location))
    retval = shutil.make_archive(os.sep.join([location,str(date.today())]), "zip", str(location))
    return retval

def googleDriveAuth(secrets_file):
    gauth = GoogleAuth()
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = secrets_file
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
                    logging.info("<<< File deleted. => %s ",x)
                else:
                    logging.warning("<<< Cannot delete file. => %s",x)

            except:
                logging.error(">>> Cannot delete file. => %s",x)
            else:
                pass
    except:
        logging.error(">>> There was a problem while listing the files in folder.")
        return False
    else:
        return True


def deleteFile(location):
    try:
        os.remove(location)
    except EnvironmentError as ee:
        logging.error("<<< Delete file error. =====> %s",ee)
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

def check_if_settings_files_exists():
    if(os.path.exists("zipplocation.txt") == False):
        return False
    if(os.path.exists("backuplocation.txt") == False):
        return False
    return True

## Logger Settings
logDestination = os.sep.join(["D:","ZippAutoCopies","zippauto.log"])

logging.basicConfig(filename=logDestination, level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
secrets_file = os.sep.join(["D:","CODE","zippauto","client_secrets.json"])

## End of Logger Settings

if(check_if_settings_files_exists()):
    pass
else:
    gui.main()

pathOfCopies_Array = []

f = open("zipplocation.txt", "r")
locationToZipp = f.read()

f = open("backuplocation.txt", "r")
pathOfCopies_Array.append(f.read())

result = zipFilesInDir(locationToZipp)
if(result != None or result != ""):
    print("\n")
    logging.info(">>> Zip file (%s) has been created. ", result)
    moveZipFileResult = moveZipFile(result,pathOfCopies_Array)
    if(moveZipFileResult != "There is an error while creating the folder!"):
        logging.info(">>> Zip file has been transfered to %s ",moveZipFileResult)
        if(deleteFile(result)):
            logging.info(">>> Original zip file has been deleted from %s",locationToZipp)
        else:
            logging.error(">>> Something went wrong while deleting original zip file. ")
        
        #Auth to google and upload files.
        logging.info(">>> Authenticating to google.")
        drive = googleDriveAuth(secrets_file)
        logging.info(">>> Authenticated..")
        logging.info(">>> Uploading files to Google Drive.")
        
        if(uploadFileToDrive(moveZipFileResult,drive)):
            logging.info(">>> Upload completed.")
            logging.info(">>> Deleting uploaded files from %s",locationToZipp)
            if(deleteFolder(locationToZipp)):
                logging.info(">>> Delete completed.")
            else:
                logging.warning(">>> Cannot delete file.")
        else:
            logging.warning(">>> There was a problem while uploading the file.")

    else:
        logging.warning(">>> Something went wrong while copying files.")

    




