from urllib.request import build_opener
from bs4 import BeautifulSoup
from settings import settings

settings = settings()

def fetchSoup(url):
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
        while True:
            try:
                dispatchSoup = fetchSoup(self.rootUrl).find_all('a', href=True)
                lastDispatchId = settings.fetchDispatchId()
                returnArray = []
                for link in dispatchSoup:
                    url = link['href']
                    if '?dis=' in url and int(link.text) > lastDispatchId:
                        returnArray.append(link.text)
                returnArray.sort()
                return returnArray
            except:
                pass

    def fetchDispatchDetails(self, dispatchId):
        while True:
            try:
                url = self.rootUrl + ('?dis=%s' % (dispatchId))
                dispatchSoup = fetchSoup(url).find_all('tr')
                returnStr = ""
                for tr in dispatchSoup:
                    th = tr.th
                    if th is not None:
                        if 'Details' in th.text:
                            returnStr = tr.td.text
                return returnStr
            except:
                pass
