import tweepy
from settings import Settings

keys = Settings().get_settings()


class Tweet:
    def __init__(self):
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(
            keys['CONSUMER'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS'], keys['ACCESS_SECRET'])
        self.api: tweepy.API = tweepy.API(auth)

    def send_status(self, status="", file_name="") -> tweepy.models.Status:
        place_id = keys['PLACE_ID']
        media_ids = []
        if file_name != "":
            media = self.api.media_upload(file_name)
            media_ids.append(media.media_id)
        return self.api.update_status(status, place_id=place_id, media_ids=media_ids)
