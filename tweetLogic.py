import re
from tweepy import TweepyException
from enums import TweetResult
from fetchBlotter import Fetch
from settings import Settings
from tweetBlot import Tweet
from tweetToImg import TweetToImg

blotFetcher = Fetch()
settings = Settings()
tweet = Tweet()
tweetToImg = TweetToImg()

BLOCKED_TWEETS = ["created from mobile", "cfs", "mileage report:"]
EVENT_BLOCK = ["event", "evnt", "ref amb",
               "req cert", "front desk relief", "type of call changed", "scheduled for:"]
MIN_MESSAGE_LEN = 10
MAX_TWEET_LEN = 240


def is_tweetable(message: str) -> bool:
    message = message.lower()
    has_blocked_tweets = [i for i, s in enumerate(BLOCKED_TWEETS) if s in message]
    has_event_tweets = [i for i, s in enumerate(EVENT_BLOCK) if message.startswith(s)]
    return len(message) >= MIN_MESSAGE_LEN and not has_blocked_tweets and not has_event_tweets


def format_tweet(message: str, id_to_tweet: str) -> str:
    msg = re.sub(r'\s\s+', '\n', message)
    tweet_msg = "%s\n#%s" % (msg, id_to_tweet)
    if len(tweet_msg) > MAX_TWEET_LEN:
        newMsgLen = MAX_TWEET_LEN - (4 + len(str(id_to_tweet)))
        msg = (msg[:newMsgLen] + '..') if len(msg) > newMsgLen else msg
        tweet_msg = "%s #%s" % (msg, id_to_tweet)
    return tweet_msg


def format_tweet_url(new_tweet) -> str:
    return "https://twitter.com/%s/status/%s" % (new_tweet.user.screen_name, new_tweet.id_str)


def process_tweet(idToTweet) -> TweetResult:
    dispatch_soup = blotFetcher.fetch_dispatch_details(idToTweet)
    if dispatch_soup:
        dispatch_msg = dispatch_soup.find_all('dd').pop().text.strip()
        if is_tweetable(dispatch_msg):
            try:
                tweet_msg = format_tweet(dispatch_msg, idToTweet)
                image_file_path = ""
                #if tweet_msg == "":
                    # image_file_path = TweetToImg.convert_tweet_to_image(idToTweet, dispatch_soup)
                new_tweet = tweet.send_status(tweet_msg, image_file_path)
                new_tweet_url = format_tweet_url(new_tweet)
                settings.print_with_stamp("%s\n%s" % (new_tweet_url, tweet_msg))
                return TweetResult.SENT
            except TweepyException as e:
                settings.print_with_stamp("Twitter error #%s: '%s'" % (idToTweet, str(e)))
                return TweetResult.ERROR
        else:
            settings.print_with_stamp("Didn't tweet #%s: '%s'" % (idToTweet, dispatch_msg))
    return TweetResult.IGNORED


class TweetLogic:
    def __init__(self):
        self.dispatchIds = []

    def update_ids(self):
        if len(self.dispatchIds) == 0:
            self.dispatchIds = blotFetcher.fetch_dispatch_ids()
            settings.print_with_stamp("Added %s new ids" % (len(self.dispatchIds)))

    def tweet_status(self) -> TweetResult:
        result: TweetResult = TweetResult.NO_TWEETS
        if len(self.dispatchIds) > 0:
            id_to_tweet = self.dispatchIds[0]
            result = process_tweet(id_to_tweet)
            self.dispatchIds.pop(0)
            settings.save_dispatch_id(id_to_tweet)
        else:
            settings.print_with_stamp("Nothing to tweet...")
        return result

    def send_next(self) -> TweetResult:
        self.update_ids()
        return self.tweet_status()
