import tweepy
from settings import settings

keys = settings().getSettings()

class tweet:
    def __init__(self):
        auth = tweepy.OAuthHandler(keys['CONSUMER'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS'], keys['ACCESS_SECRET'])
        self.api = tweepy.API(auth)
    def sendStatus(self, status):
        self.api.update_status(status)
