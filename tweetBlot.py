import tweepy
from os import getenv
from dotenv import load_dotenv
load_dotenv()

CONSUMER_KEY = getenv("CONSUMER")
CONSUMER_SECRET_KEY = getenv("CONSUMER_SECRET")
ACCESS_KEY = getenv("ACCESS")
ACCESS_SECRET_KEY = getenv("ACCESS_SECRET")

class tweet:
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET_KEY)
        self.api = tweepy.API(auth)
    def sendStatus(self, status):
        self.api.update_status(status)