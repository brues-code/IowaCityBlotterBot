import re
from tweepy import TweepyException
from enums import TweetResult
from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetToImg import tweetToImg

blotFetcher = fetch()
settings = settings()
tweet = tweet()
tweetToImg = tweetToImg()

BLOCKED_TWEETS = ["created from mobile", "cfs", "mileage report:"]
EVENT_BLOCK = ["event", "evnt", "ref amb",
               "req cert", "front desk relief", "type of call changed", "scheduled for:"]
MIN_MESSAGE_LEN = 10
MAX_TWEET_LEN = 240


def isTweetable(message: str) -> bool:
    message = message.lower()
    hasBlockedTweets = [i for i, s in enumerate(BLOCKED_TWEETS) if s in message]
    hasEventTweets = [i for i, s in enumerate(EVENT_BLOCK) if message.startswith(s)]
    return len(message) >= MIN_MESSAGE_LEN and not hasBlockedTweets and not hasEventTweets


def formatTweet(message: str, idToTweet: str) -> str:
    msg = re.sub(r'\s\s+', '\n', message)
    tweetMsg = "%s\n#%s" % (msg, idToTweet)
    if len(tweetMsg) > MAX_TWEET_LEN:
        return ""
    return tweetMsg

def formatTweetUrl(newTweet) -> str:
    return "https://twitter.com/%s/status/%s" % (newTweet.user.screen_name, newTweet.id_str)

def processTweet(idToTweet) -> TweetResult:
    dispatchSoup = blotFetcher.fetchDispatchDetails(idToTweet)
    if dispatchSoup:
        dispatchMsg = dispatchSoup.find_all('dd').pop().text.strip()
        if isTweetable(dispatchMsg):
            try:
                tweetMsg = formatTweet(dispatchMsg, idToTweet)
                imageFilePath = ""
                if tweetMsg == "":
                    imageFilePath = tweetToImg.convertTweetToImage(idToTweet, dispatchSoup)
                newTweet = tweet.sendStatus(tweetMsg, imageFilePath)
                newTweetUrl = formatTweetUrl(newTweet)
                settings.printWithStamp("%s\n%s" % (newTweetUrl, tweetMsg))
                return TweetResult.SENT
            except TweepyException as e:
                settings.printWithStamp("Twitter error #%s: '%s'" % (idToTweet, str(e)))
                return TweetResult.ERROR
        else:
            settings.printWithStamp("Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg))
    return TweetResult.IGNORED

class tweetLogic:
    def __init__(self):
        self.dispatchIds = []

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            self.dispatchIds = blotFetcher.fetchDispatchIds()
            settings.printWithStamp("Added %s new ids" % (len(self.dispatchIds)))

    def tweetStatus(self) -> TweetResult:
        result: TweetResult = TweetResult.NOTWEETS
        if len(self.dispatchIds) > 0:
            idToTweet = self.dispatchIds[0]
            result = processTweet(idToTweet)
            self.dispatchIds.pop(0)
            settings.saveDispatchId(idToTweet)
        else:
            settings.printWithStamp("Nothing to tweet...")
        return result

    def sendNext(self) -> TweetResult:
        self.updateIds()
        return self.tweetStatus()
