from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult
from tweepy import TweepError
from discordBot import BlotBot

blotFetcher = fetch()
settings = settings()
tweet = tweet()

blockedTweets = ["created from Mobile", "CFS", "EVENT 6", "EVENT 7", "EVNT"]

class tweetLogic:
    def __init__(self):
        self.dispatchIds = []
        self.lastDispatchId = settings.fetchDispatchId()
        self.keys = settings.getSettings()

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
            idToTweet = int(self.dispatchIds.pop(0))
            dispatchMsg = blotFetcher.fetchDispatchDetails(idToTweet)
            blockedTweetsLen = [i for i, s in enumerate(blockedTweets) if s in dispatchMsg]
            if len(dispatchMsg) > 2 and idToTweet > self.lastDispatchId and len(blockedTweetsLen) == 0:
                try:
                    dispatchUrl = "%s?dis=%s" % (settings.getRootUrl(), idToTweet)
                    tweetMsg = "%s\n%s" % (dispatchMsg, dispatchUrl)
                    tweet.sendStatus(tweetMsg)
                    discordClient = BlotBot(tweetMsg)
                    discordClient.run(self.keys['DISCORD_TOKEN'])
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
