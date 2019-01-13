from datetime import datetime

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
        print(outputStr)
