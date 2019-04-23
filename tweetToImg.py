import os
import imgkit
from fetchBlotter import fetchSoup
from settings import settings

settings = settings()

IMAGE_DIRECTORY = 'images/'
CSS_FILE = 'blotstyle.css'
IMAGE_OPTIONS = {
    'format': 'png',
    'crop-w': '470',
    'quiet': '',
    'xvfb': ''
}

class tweetToImg:
    def __init__(self):
        pass

    def convertTweetToImage(self, dispatchId, detailList):
        imgDirectory = "%s%s" % (IMAGE_DIRECTORY, settings.getDateDirectory())
        if not os.path.exists(imgDirectory):
            os.makedirs(imgDirectory)

        for detail in detailList.findAll(lambda tag: tag.string is None):
            detail.string = 'N/A'

        fileName = '%s%s.%s' % (imgDirectory, dispatchId, IMAGE_OPTIONS['format'])
        imgkit.from_string(str(detailList), fileName,
                           options=IMAGE_OPTIONS, css=CSS_FILE)
