from urllib.request import build_opener
from bs4 import BeautifulSoup
from settings import settings

settings = settings()

blockedCategories:list = ["MVA/PROPERTY DAMAGE ACCIDENT", "911 HANGUP", "SUICIDE/LAW", "TR/PARKING"]
zBlock:list = ["Z"]

def fetchSoup(url):
    settings.printWithStamp("Fetching " + url)
    text:str = build_opener().open(url).read().decode('utf-8')
    return BeautifulSoup( text, features='html.parser' )

class fetch:
    def __init__(self):
        pass

    def fetchDispatchIds(self) -> list:
        returnArray = []
        lastDispatchId = settings.fetchDispatchId()
        dateStamp = settings.getDateStamp()
        url = settings.getUrl(dateStamp)
        dispatchTable = fetchSoup(url).find('tbody', {"valign" : "top"})
        for tRow in dispatchTable:
            hasNote = tRow.find('strong')
            if hasNote and hasNote != -1:
                dispatchId = int(tRow.find('a').text)
                if dispatchId > lastDispatchId:
                    activityCat = str(tRow.find_all('td')[2].text).strip()
                    isBlockedCat = [i for i, s in enumerate(blockedCategories) if s in activityCat]
                    isZCat = [i for i, s in enumerate(zBlock) if activityCat.startswith(s)]
                    if not isBlockedCat and not isZCat:
                        returnArray.append(dispatchId)
        returnArray.sort()
        return returnArray
        

    def fetchDispatchDetails(self, id:int) -> str:
        url = settings.getUrl(dis=id)
        while True:
            try:
                return fetchSoup(url).find_all('td').pop().text
            except:
                pass
