import sys
import os
import platform
from datetime import datetime


def start(file):
    currFile=""
    path=os.getcwd()
    fileTime=creation_date(file)
    fileTime=datetime.fromtimestamp(fileTime)
    fileTime2=str(fileTime).replace(" ","_")[:19]
    #print fileTime
    #print fileTime2
    command="python "+path+"/ddUrmet.py "+path+"/"+file
    os.system(command)
    for sfile in os.listdir(path+"/"):
        if sfile.endswith(".pre"):
           currFile=sfile
    if currFile != "":
       renFile=currFile[:16]
       os.system("mv "+path+"/"+currFile+" "+path+"/"+renFile+"-"+fileTime2+".hack")
       valueFile=open(path+"/"+renFile+".value", 'a')
       #print valueFile.read()
       valueFile.write(str(fileTime)+"\r\n")
       valueFile.close()
    os.system("rm "+path+"/"+file)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


if __name__ == '__main__':
    if not os.path.exists(sys.argv[1]):
        print >> (sys.stderr, "The file doesn't exist.")
        sys.exit(1)
    start(sys.argv[1])
