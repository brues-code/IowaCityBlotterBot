from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult
from tweepy import TweepError

blotFetcher = fetch()
settings = settings()
tweet = tweet()

blockedTweets = ["created from mobile", "cfs"]
eventBlock = ["event", "evnt"]

class tweetLogic:
    def __init__(self):
        self.dispatchIds = []
        self.lastDispatchId = settings.fetchDispatchId()

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            newIds = blotFetcher.fetchDispatchIds()
            self.dispatchIds = newIds
        else:
            newDispatchIds = blotFetcher.fetchDispatchIds()
            for id in newDispatchIds:
                if id not in self.dispatchIds and int(id) > self.lastDispatchId:
                    print("Added dispatchId: " + id)
                    self.dispatchIds.append(id)
                    self.dispatchIds.sort()

    def tweetStatus(self):
        result:TweetResult = TweetResult.NOTWEETS
        if len(self.dispatchIds) > 0:
            idToTweet = int(self.dispatchIds.pop(0))
            dispatchMsg = blotFetcher.fetchDispatchDetails(idToTweet)
            blockedTweetsLen = len([i for i, s in enumerate(blockedTweets) if s in dispatchMsg.lower()])
            eventFilter = len([i for i, s in enumerate(eventBlock) if dispatchMsg.lower().startswith(s)])
            if len(dispatchMsg) > 2 and idToTweet > self.lastDispatchId and blockedTweetsLen == 0 and eventFilter == 0:
                try:
                    dispatchUrl = "%s?dis=%s" % (settings.getRootUrl(), idToTweet)
                    tweetMsg = "%s\n%s" % (dispatchMsg, dispatchUrl)
                    tweet.sendStatus(tweetMsg)
                    print("Sent #%s: '%s'" % (idToTweet, tweetMsg))
                    result = TweetResult.SENT
                except TweepError as e:
                    print("Twitter error #%s: '%s'" % (idToTweet, str(e)))
                    result = TweetResult.TWITTER_ERROR
            else:
                print("Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg))
                result = TweetResult.IGNORED
            settings.saveDispatchId(idToTweet)
            self.lastDispatchId = idToTweet
        else:
            print("Nothing to tweet...")
        return result

    def sendNext(self):
        self.updateIds()
        return self.tweetStatus()
