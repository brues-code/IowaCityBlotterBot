import os
from datetime import datetime, timedelta

LOG_DIRECTORY = "logs/"
LAST_DISPATCH_FILE = "lastDispatch.txt"
SETTINGS_FILE = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/icgov/apps/police/activityLog.asp?'
DATE_STAMP_HOUR_DELAY = 5

class settings:
    def __init__(self):
        pass

    def fetchDispatchId(self) -> int:
        returnId = 0
        try:
            f=open(LAST_DISPATCH_FILE, "r")
            if f.readable():
                returnId = int(f.read())
            f.close()
        except:
            pass
        return returnId
    
    def saveDispatchId(self, dispatchId:int):
        f=open(LAST_DISPATCH_FILE, "w")
        if f.writable():
            f.write(str(dispatchId))
        f.close()

    def getSettings(self):
        f=open(SETTINGS_FILE, "r")
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
        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)
        f=open("%s%s.txt" % (LOG_DIRECTORY, self.getDateStamp()), "a")
        if f.writable():
            f.write(logMessage + "\n")
        f.close()

    def getDateStamp(self) -> str:
        return (datetime.now() - timedelta(hours = DATE_STAMP_HOUR_DELAY)).strftime('%m%d%Y')
