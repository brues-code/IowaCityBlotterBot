import ssl
import urllib.request
from bs4 import BeautifulSoup, Tag, ResultSet
from settings import settings

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

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
    "WELFARE CHECK",
    "PAPER SERVICE/WARRANT"
]
zBlock: list = ["Z", "TEST"]
blockedDispositions: list = ["EMPL ERROR ALARM", "UNK CAUSE ALARM"]

def fetchSoup(url):
    text = ""
    try:
        settings.printWithStamp("Fetching " + url)
        with urllib.request.urlopen(url, context=ctx) as response:
            text = response.read()
    except Exception as e:
        pass
    return BeautifulSoup(text, 'html.parser')

def isTweetable(activityCat, activityDisposition):
    isBlockedCat = [i for i, s in enumerate(
        blockedCategories) if s in activityCat]
    isZCat = [i for i, s in enumerate(zBlock) if activityCat.startswith(s)]
    isBlockedDisp = [i for i, s in enumerate(blockedDispositions) if s in activityDisposition]
    return not isBlockedCat and not isZCat and not isBlockedDisp

DISPATCH_HEADERS = ["dispatchId", "address", "activity", "disposition", "hasDetails"]
def rowToDispatchEntry(entry: ResultSet):
    dispatchEntry = dict() 
    for index,value in enumerate(entry):
        dispatchEntry[DISPATCH_HEADERS[index]] = str(value.text).strip()
    return dispatchEntry

class fetch:
    def __init__(self):
        pass

    def fetchDispatchIds(self) -> list:
        returnArray = []
        oldDispatchIds = settings.fetchOldDispatchIds()
        dateStamp = settings.getDateStamp()
        url = settings.getListUrl(dateStamp)
        dispatchTable = fetchSoup(url).find('tbody')
        if dispatchTable:
            for tRow in dispatchTable:
                if isinstance(tRow, Tag):
                    tds = tRow.find_all('td')
                    dispatchEntry = rowToDispatchEntry(tds)
                    if dispatchEntry['dispatchId'] not in oldDispatchIds:
                        if dispatchEntry['hasDetails'] == 'Y' and isTweetable(dispatchEntry['activity'], dispatchEntry['disposition']):
                            returnArray.append(dispatchEntry['dispatchId'])
        returnArray.sort()
        return returnArray

    def fetchDispatchDetails(self, id: str) -> str:
        url = settings.getDispatchUrl(id)
        return fetchSoup(url).find('dl')
        # return fetchSoup(url).find_all('dd').pop().text
