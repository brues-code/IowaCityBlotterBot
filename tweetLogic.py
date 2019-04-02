import re
from tweepy import TweepError
from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult

blotFetcher = fetch()
settings = settings()
tweet = tweet()

BLOCKED_TWEETS:list = ["created from mobile", "cfs", "mileage report:"]
EVENT_BLOCK:list = ["event", "evnt", "ref amb", "req cert", "front desk relief", "type of call changed"]
MIN_MESSAGE_LEN:int = 15

def isTweetable(message:str) -> bool:
    message = message.lower()
    hasBlockedTweets = [i for i, s in enumerate(BLOCKED_TWEETS) if s in message]
    hasEventTweets = [i for i, s in enumerate(EVENT_BLOCK) if message.startswith(s)]
    return len(message) >= MIN_MESSAGE_LEN and not hasBlockedTweets and not hasEventTweets

def formatTweet(message:str, idToTweet:int) -> str:
    msg = re.sub(r'\s\s+', '\n', message)
    url = settings.getUrl(dis=idToTweet)
    tweetMsg = "%s\n%s" % (msg, url)
    if len(tweetMsg) > 240:
        tweetMsg = "%s #%s" % (msg, idToTweet)
    return tweetMsg

class tweetLogic:
    def __init__(self):
        self.dispatchIds:list = []

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            self.dispatchIds = blotFetcher.fetchDispatchIds()
            settings.printWithStamp("Added %s new ids" % (len(self.dispatchIds)))

    def tweetStatus(self) -> TweetResult:
        result:TweetResult = TweetResult.NOTWEETS
        logMsg:str = "Nothing to tweet..."
        if len(self.dispatchIds) > 0:
            result = TweetResult.IGNORED
            idToTweet:int = self.dispatchIds.pop(0)
            dispatchMsg:str = blotFetcher.fetchDispatchDetails(idToTweet)
            if isTweetable(dispatchMsg):
                try:
                    tweetMsg:str = formatTweet(dispatchMsg, idToTweet)
                    newTweet = tweet.sendStatus(tweetMsg)
                    newTweetUrl:str = "https://twitter.com/%s/status/%s" % (newTweet.user.screen_name, newTweet.id_str)
                    logMsg = "%s\n%s" % (newTweetUrl, tweetMsg)
                    result = TweetResult.SENT
                except TweepError as e:
                    logMsg = "Twitter error #%s: '%s'" % (idToTweet, str(e))
                    if e.api_code != tweet.duplicateErrorCode:
                        result = TweetResult.ERROR
            else:
                logMsg = "Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg)
            if result != TweetResult.ERROR:
                settings.saveDispatchId(idToTweet)
        settings.printWithStamp(logMsg)
        return result

    def sendNext(self) -> TweetResult:
        self.updateIds()
        return self.tweetStatus()
