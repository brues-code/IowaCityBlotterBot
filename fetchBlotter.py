from urllib.request import build_opener
from bs4 import BeautifulSoup

IC_ROOT_URL = 'https://www.iowa-city.org/icgov/apps/police/activityLog.asp'


def fetchSoup(url):
    opener = build_opener()
    response = opener.open(url)
    data = response.read()
    text = data.decode('utf-8')
    soup = BeautifulSoup( text, features='html.parser' )
    return soup

class fetch:
    def __init__(self):
        pass

    def fetchDispatchIds(self):
        dispatchSoup = fetchSoup(IC_ROOT_URL).find_all('a', href=True)
        returnArray = []
        for link in dispatchSoup:
            url = link['href']
            if '?dis=' in url:
                returnArray.append(link.text)
        return returnArray

    def fetchDispatchDetails(self, dispatchId):
        url = IC_ROOT_URL + ('?dis=%s&date=' % (dispatchId))
        dispatchSoup = fetchSoup(url).find_all('tr')
        returnStr = ""
        for tr in dispatchSoup:
            th = tr.th
            if th is not None:
                if 'Details' in th.text:
                    returnStr = tr.td.text
        return returnStr
