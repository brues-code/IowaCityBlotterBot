import os
import imgkit
from fetchBlotter import Fetch
from settings import Settings
from tweetBlot import Tweet

settings = Settings()
fetcher = Fetch()
tweet = Tweet()

IMAGE_DIRECTORY = 'images/'
CSS_FILE = 'blotstyle.css'
IMAGE_OPTIONS = {
    'format': 'png',
    'crop-w': '478',
    'quiet': ''
}
if os.name == 'posix':
    IMAGE_OPTIONS['xvfb'] = ''


class TweetToImg:
    def __init__(self):
        pass

    def convert_tweet_to_image(self, dispatch_id, detail_list):
        img_directory = "%s%s" % (IMAGE_DIRECTORY, settings.get_date_directory())
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)

        for detail in detail_list.findAll(lambda tag: tag.string is None):
            detail.string = 'N/A'

        file_name = '%s%s.%s' % (img_directory, dispatch_id, IMAGE_OPTIONS['format'])
        imgkit.from_string(str(detail_list), file_name,
                           options=IMAGE_OPTIONS, css=CSS_FILE)
        return file_name

# dispatchId = "22169064"
# tweetSoup = fetcher.fetchDispatchDetails(dispatchId)
# tweetToImg = tweetToImg()

# fileName = tweetToImg.convertTweetToImage(dispatchId, tweetSoup)
# tweet.sendStatus(fileName=fileName)

#tweet.sendImageStatus(fileName)
