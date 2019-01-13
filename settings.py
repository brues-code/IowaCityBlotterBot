import os
from datetime import datetime, timedelta

logDirectory = "logs/"
resultsFile = "lastDispatch.txt"
settingsFile = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/icgov/apps/police/activityLog.asp?'

class settings:
    def __init__(self):
        pass

    def fetchDispatchId(self) -> int:
        returnId = 0
        try:
            f=open(resultsFile, "r")
            if f.readable():
                returnId = int(f.read())
            f.close()
        except:
            pass
        return returnId
    
    def saveDispatchId(self, dispatchId:int):
        f=open(resultsFile, "w")
        if f.writable():
            f.write(str(dispatchId))
        f.close()

    def getSettings(self):
        f=open(settingsFile, "r")
        if f.readable():
            return eval(f.read())
        f.close()

    def getUrl(self, date:str="", dis:str="") -> str:
        if date:
            date = "date=%s&" % (date)
        if dis:
            dis = "dis=%s" % (dis)
        return IC_ROOT_URL + date + dis

    def printWithStamp(self, inputStr:str):
        st:str = datetime.now().strftime('%H:%M:%S')
        outputStr:str = "[%s]: %s" % (st, inputStr)
        self.addToLog(outputStr)
        print(outputStr)

    def addToLog(self, logMessage:str):
        if not os.path.exists(logDirectory):
            os.makedirs(logDirectory)
        f=open("%s%s.txt" % (logDirectory, self.getDateStamp()), "a")
        if f.writable():
            f.write(logMessage + "\n")
        f.close()

    def getDateStamp(self) -> str:
        return (datetime.now() - timedelta(hours = 6)).strftime('%m%d%Y')
