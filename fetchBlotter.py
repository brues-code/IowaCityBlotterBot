from urllib.request import build_opener
from bs4 import BeautifulSoup
from settings import settings

settings = settings()

blockedCategories: list = [
    "MVA/PROPERTY DAMAGE ACCIDENT",
    "911 HANGUP",
    "SUICIDE/LAW",
    "TR/PARKING",
    "ESCORT/RELAY",
    "ALARM/PANIC/HOLDUP",
    "MENTAL IMPAIRMENT"
]
zBlock: list = ["Z"]
blockedDispositions: list = ["EMPL ERROR ALARM"]


def fetchSoup(url):
    while True:
        try:
            settings.printWithStamp("Fetching " + url)
            text = build_opener().open(url).read().decode('utf-8')
            return BeautifulSoup(text, features='html.parser')
        except:
            pass


def isTweetable(activityCat, activityDisposition):
    isBlockedCat = [i for i, s in enumerate(
        blockedCategories) if s in activityCat]
    isZCat = [i for i, s in enumerate(zBlock) if activityCat.startswith(s)]
    isBlockedDisp = [i for i, s in enumerate(
        blockedDispositions) if s in activityDisposition]
    return not isBlockedCat and not isZCat and not isBlockedDisp


class fetch:
    def __init__(self):
        pass

    def fetchDispatchIds(self) -> list:
        returnArray = []
        lastDispatchId = settings.fetchDispatchId()
        dateStamp = settings.getDateStamp()
        url = settings.getUrl(dateStamp)
        dispatchTable = fetchSoup(url).find('tbody', {"valign": "top"})
        for tRow in dispatchTable:
            hasNote = tRow.find('strong')
            if hasNote and hasNote != -1:
                dispatchId = int(tRow.find('a').text)
                if dispatchId > lastDispatchId:
                    tds = tRow.find_all('td')
                    activityCat = str(tds[2].text).strip()
                    activityDisposition = str(tds[3].text).strip()
                    if isTweetable(activityCat, activityDisposition):
                        returnArray.append(dispatchId)
        returnArray.sort()
        return returnArray

    def fetchDispatchDetails(self, id: int) -> str:
        url = settings.getUrl(dis=id)
        return fetchSoup(url).find_all('td').pop().text
