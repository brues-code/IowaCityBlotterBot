import emoji
from tweepy import TweepError
from fetchBlotter import fetch
from settings import settings
from tweetBlot import tweet
from tweetResult import TweetResult

blotFetcher = fetch()
settings = settings()
tweet = tweet()

blockedTweets = ["created from mobile", "cfs"]
eventBlock = ["event", "evnt", "ref amb"]

def appendEmojis( inputStr ):
    splitStr = inputStr.split()
    emojiOutput = " "
    for word in splitStr:
        emojiStr = ":" + word.lower() + ":"
        if (emojiStr in emoji.EMOJI_ALIAS_UNICODE or emojiStr in emoji.EMOJI_UNICODE) and len(word) > 2:
            emojiOutput = emojiOutput + emojiStr
    return emoji.emojize(inputStr + emojiOutput, use_aliases=True)

class tweetLogic:
    def __init__(self):
        self.dispatchIds = []

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            self.dispatchIds = blotFetcher.fetchDispatchIds()
            settings.printWithStamp("Added %s new ids" % (len(self.dispatchIds)))

    def tweetStatus(self):
        result:TweetResult = TweetResult.NOTWEETS
        logMsg = "Nothing to tweet..."
        if len(self.dispatchIds) > 0:
            idToTweet = self.dispatchIds.pop(0)
            dispatchMsg = blotFetcher.fetchDispatchDetails(idToTweet)
            blockedTweetsLen = len([i for i, s in enumerate(blockedTweets) if s in dispatchMsg.lower()])
            eventFilter = len([i for i, s in enumerate(eventBlock) if dispatchMsg.lower().startswith(s)])
            if len(dispatchMsg) > 2 and blockedTweetsLen == 0 and eventFilter == 0:
                try:
                    tweetMsg = "%s\n%sdis=%s" % (dispatchMsg, settings.getRootUrl(), idToTweet)
                    #emojizedTweet = appendEmojis(tweetMsg)
                    newTweet = tweet.sendStatus(tweetMsg)
                    newTweetUrl = "https://twitter.com/%s/status/%s" % (newTweet.user.screen_name, newTweet.id_str)
                    logMsg = "%s\n%s" % (newTweetUrl, tweetMsg)
                    result = TweetResult.SENT
                except TweepError as e:
                    logMsg = "Twitter error #%s: '%s'" % (idToTweet, str(e))
                    result = TweetResult.TWITTER_ERROR
            else:
                logMsg = "Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg)
                result = TweetResult.IGNORED
            settings.saveDispatchId(idToTweet)
        settings.printWithStamp(logMsg)
        return result

    def sendNext(self):
        self.updateIds()
        return self.tweetStatus()
