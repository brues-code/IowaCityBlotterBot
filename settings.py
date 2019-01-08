from pathlib import Path

class settings:
    def __init__(self):
        self.resultsFile = Path("lastDispatch.txt")
        self.settingsFile = Path("settings.txt")
        self.IC_ROOT_URL = 'https://www.iowa-city.org/icgov/apps/police/activityLog.asp'

    def fetchDispatchId(self):
        returnId = 0
        if self.resultsFile.is_file():
            returnId = int(self.resultsFile.read_text())
        return returnId
    
    def saveDispatchId(self, dispatchId):
        self.resultsFile.write_text(dispatchId)

    def getSettings(self):
        if self.resultsFile.is_file():
            return eval(self.settingsFile.read_text())

    def getRootUrl(self):
        return self.IC_ROOT_URL