import tweepy
from settings import settings

keys = settings().getSettings()

class tweet:
    def __init__(self):
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(keys['CONSUMER'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS'], keys['ACCESS_SECRET'])
        self.api: tweepy.API = tweepy.API(auth)
        self.duplicateErrorCode: int = 187

    def sendStatus(self, status:str) -> tweepy.Status:
        placeId = keys['PLACE_ID']
        return self.api.update_status(status, place_id=placeId)
