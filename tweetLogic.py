from tweepy import TweepError
from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult

blotFetcher = fetch()
settings = settings()
tweet = tweet()

blockedTweets = ["created from mobile", "cfs"]
eventBlock = ["event", "evnt", "ref amb", "req cert"]

class tweetLogic:
    def __init__(self):
        self.dispatchIds = []

    def isTweetable(self, message):
        message = message.lower()
        hasBlockedTweets = [i for i, s in enumerate(blockedTweets) if s in message]
        hasEventTweets = [i for i, s in enumerate(eventBlock) if message.startswith(s)]
        return len(message) > 15 and not hasBlockedTweets and not hasEventTweets

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            self.dispatchIds = blotFetcher.fetchDispatchIds()
            settings.printWithStamp("Added %s new ids" % (len(self.dispatchIds)))

    def tweetStatus(self):
        result = TweetResult.NOTWEETS
        logMsg = "Nothing to tweet..."
        if len(self.dispatchIds) > 0:
            result = TweetResult.IGNORED
            idToTweet = self.dispatchIds.pop(0)
            dispatchMsg = blotFetcher.fetchDispatchDetails(idToTweet)
            if self.isTweetable(dispatchMsg):
                try:
                    tweetMsg = "%s\n%s" % (dispatchMsg, settings.getUrl(dis=idToTweet))
                    newTweet = tweet.sendStatus(tweetMsg)
                    newTweetUrl = "https://twitter.com/%s/status/%s" % (newTweet.user.screen_name, newTweet.id_str)
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

    def sendNext(self):
        self.updateIds()
        return self.tweetStatus()
