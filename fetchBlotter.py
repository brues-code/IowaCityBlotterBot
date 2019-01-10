from datetime import datetime, timedelta
from urllib.request import build_opener
from bs4 import BeautifulSoup
from settings import settings

settings = settings()

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
        while True:
            try:
                dispatchSoup = fetchSoup(url)
                dispatchTable = dispatchSoup.find('tbody', {"valign" : "top"})
                returnArray = []
                for tRow in dispatchTable:
                    hasNone = tRow.find('strong')
                    if hasNone and hasNone != -1:
                        dispatchId = int(tRow.find('a').text)
                        if dispatchId > lastDispatchId:
                            returnArray.append(dispatchId)
                returnArray.sort()
                return returnArray
            except:
                pass

    def fetchDispatchDetails(self, dispatchId):
        url = "%sdis=%s" % (self.rootUrl, dispatchId)
        while True:
            try:
                dispatchSoup = fetchSoup(url).find_all('tr')
                returnStr = ""
                for tr in dispatchSoup:
                    th = tr.th
                    if th and 'Details' in th.text:
                        returnStr = tr.td.text
                return returnStr
            except:
                pass
