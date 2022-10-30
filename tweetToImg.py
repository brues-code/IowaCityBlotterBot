import os
import imgkit
from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet

settings = settings()
fetcher = fetch()
tweet = tweet()

IMAGE_DIRECTORY = 'images/'
CSS_FILE = 'blotstyle.css'
IMAGE_OPTIONS = {
    'format': 'png',
    'crop-w': '478',
    'quiet': ''
}
if os.name == 'posix':
    IMAGE_OPTIONS['xvfb'] = ''

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
        return fileName

# dispatchId = "22169064"
# tweetSoup = fetcher.fetchDispatchDetails(dispatchId)
# tweetToImg = tweetToImg()

# fileName = tweetToImg.convertTweetToImage(dispatchId, tweetSoup)
# tweet.sendStatus(fileName=fileName)

#tweet.sendImageStatus(fileName)
