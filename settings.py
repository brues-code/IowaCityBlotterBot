from pathlib import Path

class settings:
    def __init__(self):
        self.resultsFile = Path("lastDispatch.txt")

    def fetchDispatchId(self):
        returnId = ""
        if self.resultsFile.is_file():
            returnId = self.resultsFile.read_text()
        return returnId
    
    def saveDispatchId(self, dispatchId):
        self.resultsFile.write_text(dispatchId)
