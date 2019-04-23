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
    "MENTAL IMPAIRMENT",
    "TRAFFIC STOP",
    "MISSING/JUVENILE",
    "WELFARE CHECK"
]
zBlock: list = ["Z"]
blockedDispositions: list = ["EMPL ERROR ALARM", "UNK CAUSE ALARM"]


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
        oldDispatchIds = settings.fetchOldDispatchIds()
        dateStamp = settings.getDateStamp()
        url = settings.getListUrl(dateStamp)
        dispatchTable = fetchSoup(url).find('tbody')
        for tRow in dispatchTable:
            dispatchIdLink = tRow.find('a')
            if(dispatchIdLink != -1):
                dispatchId = dispatchIdLink.text
                if dispatchId not in oldDispatchIds:
                    tds = tRow.find_all('td')
                    activityCat = str(tds[2].text).strip()
                    activityDisposition = str(tds[3].text).strip()
                    hasDetails = tds.pop().text
                    if hasDetails == 'Y' and isTweetable(activityCat, activityDisposition):
                        returnArray.append(dispatchId)
        returnArray.sort()
        return returnArray

    def fetchDispatchDetails(self, id: str) -> str:
        url = settings.getDispatchUrl(id)
        return fetchSoup(url).find('dl')
        # return fetchSoup(url).find_all('dd').pop().text
