from datetime import datetime, timedelta
from urllib.request import build_opener
from bs4 import BeautifulSoup
from settings import settings

settings = settings()

blockedCategories = ["MVA/PROPERTY DAMAGE ACCIDENT", "911 HANGUP", "SUICIDE/LAW"]
zBlock = ["Z"]

def fetchSoup(url):
    settings.printWithStamp("Fetching " + url)
    opener = build_opener()
    response = opener.open(url)
    data = response.read()
    text = data.decode('utf-8')
    soup = BeautifulSoup( text, features='html.parser' )
    return soup

class fetch:
    def __init__(self):
        self.rootUrl = settings.getRootUrl()

    def fetchDispatchIds(self):
        lastDispatchId = settings.fetchDispatchId()
        six_hour_ago_date_time = datetime.now() - timedelta(hours = 6)
        st = six_hour_ago_date_time.strftime('%m%d%Y')
        url = "%sdate=%s" % (self.rootUrl, st)
        returnArray = []
        dispatchSoup = fetchSoup(url)
        dispatchTable = dispatchSoup.find('tbody', {"valign" : "top"})
        for tRow in dispatchTable:
            hasNone = tRow.find('strong')
            if hasNone and hasNone != -1:
                dispatchId = int(tRow.find('a').text)
                activityCat = str(tRow.find_all('td')[2].text).strip()
                noBlockedCats = len([i for i, s in enumerate(blockedCategories) if s in activityCat]) == 0
                hasNoZCat = len([i for i, s in enumerate(zBlock) if activityCat.startswith(s)]) == 0
                if dispatchId > lastDispatchId and noBlockedCats and hasNoZCat:
                    returnArray.append(dispatchId)
        returnArray.sort()
        return returnArray
        

    def fetchDispatchDetails(self, dispatchId):
        url = "%sdis=%s" % (self.rootUrl, dispatchId)
        while True:
            try:
                return fetchSoup(url).find_all('td').pop().text
            except:
                pass
