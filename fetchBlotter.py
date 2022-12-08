import ssl
import urllib.request
from bs4 import BeautifulSoup, Tag, ResultSet
from settings import Settings

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

settings = Settings()

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


def fetch_soup(url):
    text = ""
    try:
        settings.print_with_stamp("Fetching " + url)
        with urllib.request.urlopen(url, context=ctx) as response:
            text = response.read()
    except Exception as e:
        pass
    return BeautifulSoup(text, 'html.parser')


def is_tweetable(activity_cat, activity_disposition):
    is_blocked_cat = [i for i, s in enumerate(
        blockedCategories) if s in activity_cat]
    is_z_cat = [i for i, s in enumerate(zBlock) if activity_cat.startswith(s)]
    is_blocked_disp = [i for i, s in enumerate(blockedDispositions) if s in activity_disposition]
    return not is_blocked_cat and not is_z_cat and not is_blocked_disp


DISPATCH_HEADERS = ["dispatchId", "address", "activity", "disposition", "hasDetails"]


def row_to_dispatch_entry(entry: ResultSet):
    dispatch_entry = dict()
    for index, value in enumerate(entry):
        dispatch_entry[DISPATCH_HEADERS[index]] = str(value.text).strip()
    return dispatch_entry


class Fetch:
    def __init__(self):
        pass

    def fetch_dispatch_ids(self) -> list:
        return_array = []
        old_dispatch_ids = settings.fetch_old_dispatch_ids()
        date_stamp = settings.get_date_stamp()
        url = settings.get_list_url(date_stamp)
        dispatch_table = fetch_soup(url).find('tbody')
        if dispatch_table:
            for tRow in dispatch_table:
                if isinstance(tRow, Tag):
                    tds = tRow.find_all('td')
                    dispatch_entry = row_to_dispatch_entry(tds)
                    if dispatch_entry['dispatchId'] not in old_dispatch_ids:
                        if dispatch_entry['hasDetails'] == 'Y' \
                                and is_tweetable(dispatch_entry['activity'], dispatch_entry['disposition']):
                            return_array.append(dispatch_entry['dispatchId'])
        return_array.sort()
        return return_array

    def fetch_dispatch_details(self, id: str) -> str:
        url = settings.get_dispatch_url(id)
        return fetch_soup(url).find('dl')
        # return fetchSoup(url).find_all('dd').pop().text
