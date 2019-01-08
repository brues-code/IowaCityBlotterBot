from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult
from tweepy import TweepError

blotFetcher = fetch()
settings = settings()
tweet = tweet()

blockedTweets = ["Field Initiated Activity created from Mobile"]

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
                    self.dispatchIds.append(id)
                    self.dispatchIds.sort()

    def tweetStatus(self):
        result:TweetResult = TweetResult.NOTWEETS
        if len(self.dispatchIds) > 0:
            idToTweet = self.dispatchIds.pop(0)
            dispatchMsg = blotFetcher.fetchDispatchDetails(idToTweet)
            blockedTweetsLen = [i for i, s in enumerate(blockedTweets) if dispatchMsg in s]
            if len(dispatchMsg) > 0 and int(idToTweet) > self.lastDispatchId and len(blockedTweetsLen) == 0:
                try:
                    dispatchUrl = "%s?dis=%s" % (settings.getRootUrl(), idToTweet)
                    tweetMsg = "%s\n%s" % (dispatchMsg, dispatchUrl)
                    tweet.sendStatus(tweetMsg)
                    print("Tweeted #%s: '%s'" % (idToTweet, tweetMsg))
                    result = TweetResult.SENT
                except TweepError as e:
                    print("Twitter error #%s: '%s'" % (idToTweet, str(e)))
                    result = TweetResult.TWITTER_ERROR
            else:
                print("Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg))
                result = TweetResult.IGNORED
            settings.saveDispatchId(idToTweet)
            self.lastDispatchId = int(idToTweet)
        else:
            print("Nothing to tweet...")
        return result

    def sendNext(self):
        self.updateIds()
        return self.tweetStatus()
