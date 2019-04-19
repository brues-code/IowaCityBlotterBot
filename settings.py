import os
from datetime import datetime, timedelta

LOG_DIRECTORY = "logs/"
LAST_DISPATCH_FILE = "lastDispatch.txt"
SETTINGS_FILE = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/IcgovApps/police/'
DATE_STAMP_HOUR_DELAY = 5


class settings:
    def __init__(self):
        pass

    def fetchDispatchId(self) -> int:
        returnId = 0
        try:
            f = open(LAST_DISPATCH_FILE, "r")
            if f.readable():
                returnId = int(f.read())
            f.close()
        except:
            pass
        return returnId

    def saveDispatchId(self, dispatchId: int):
        f = open(LAST_DISPATCH_FILE, "w")
        if f.writable():
            f.write(str(dispatchId))
        f.close()

    def getSettings(self):
        f = open(SETTINGS_FILE, "r")
        if f.readable():
            return eval(f.read())
        f.close()

    def getListUrl(self, date: str) -> str:
        return "%sActivityLog?activityDate=%s" % (IC_ROOT_URL, date)

    def getDispatchUrl(self, dispatchId: str) -> str:
        return "%sDetails?dispatchNumber=%s" % (IC_ROOT_URL, dispatchId)

    def printWithStamp(self, inputStr: str):
        st: str = datetime.now().strftime('%H:%M:%S')
        outputStr: str = "[%s]: %s" % (st, inputStr)
        self.addToLog(outputStr)
        print(outputStr)

    def addToLog(self, logMessage: str):
        logDirectory = self.getLogDirectory()
        if not os.path.exists(logDirectory):
            os.makedirs(logDirectory)
        today = self.getDate().day
        if(today < 10):
            today = "0%s" % (today)
        f = open("%s%s.txt" % (logDirectory, today), "a")
        if f.writable():
            f.write(logMessage + "\n")
        f.close()

    def getDate(self) -> datetime:
        return (datetime.now() - timedelta(hours=DATE_STAMP_HOUR_DELAY))

    def getDateStamp(self) -> str:
        return self.getDate().strftime('%m/%d/%Y')

    def getLogDirectory(self) -> str:
        date = self.getDate()
        month = date.month
        if(month < 10):
            month = "0%s" % (month)
        return '%s%s/%s/' % (LOG_DIRECTORY, date.year, month)
