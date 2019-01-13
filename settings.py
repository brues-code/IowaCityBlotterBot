from datetime import datetime

resultsFile = "lastDispatch.txt"
settingsFile = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/icgov/apps/police/activityLog.asp?'

class settings:
    def __init__(self):
        pass

    def fetchDispatchId(self):
        returnId = 0
        try:
            f=open(resultsFile, "r")
            if f.readable():
                returnId = int(f.read())
            f.close()
        except:
            pass
        return returnId
    
    def saveDispatchId(self, dispatchId):
        f=open(resultsFile, "w")
        if f.writable():
            f.write(str(dispatchId))
        f.close()

    def getSettings(self):
        f=open(settingsFile, "r")
        if f.readable():
            return eval(f.read())
        f.close()

    def getUrl(self, date=None, dis=None):
        dateStr = "date=%s&" % (date) if date else ""
        disStr = "dis=%s" % (dis) if dis else ""
        return IC_ROOT_URL + dateStr + disStr

    def printWithStamp(self, inputStr):
        st = datetime.now().strftime('%H:%M:%S')
        outputStr = "[%s]: %s" % (st, inputStr)
        print(outputStr)
