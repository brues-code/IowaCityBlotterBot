from pathlib import Path

class settings:
    def __init__(self):
        self.resultsFile = Path("lastDispatch.txt")

    def fetchDispatchId(self):
        returnId = 0
        if self.resultsFile.is_file():
            returnId = int(self.resultsFile.read_text())
        return returnId
    
    def saveDispatchId(self, dispatchId):
        self.resultsFile.write_text(dispatchId)
