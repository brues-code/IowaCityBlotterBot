import tweepy
from settings import settings

keys = settings().getSettings()


class tweet:
    def __init__(self):
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(
            keys['CONSUMER'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS'], keys['ACCESS_SECRET'])
        self.api: tweepy.API = tweepy.API(auth)

    def sendStatus(self, status="", fileName="") -> tweepy.models.Status:
        placeId = keys['PLACE_ID']
        media_ids = []
        if fileName != "":
            media = self.api.media_upload(fileName)
            media_ids.append(media.media_id)
        return self.api.update_status(status, place_id=placeId, media_ids=media_ids)
