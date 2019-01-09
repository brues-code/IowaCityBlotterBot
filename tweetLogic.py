import datetime
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

def printWithStamp( inputStr ):
    st = datetime.datetime.now().strftime('%H:%M:%S')
    outputStr = "[%s]: %s" % (st, inputStr)
    print(outputStr)


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
        self.lastDispatchId = settings.fetchDispatchId()

    def updateIds(self):
        if len(self.dispatchIds) == 0:
            newIds = blotFetcher.fetchDispatchIds()
            printWithStamp("Added %s new ids" % (len(newIds)))
            self.dispatchIds = newIds

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
                    #emojizedStr = appendEmojis(dispatchMsg)
                    tweetMsg = "%s\n%s" % (dispatchMsg, dispatchUrl)
                    newTweet = tweet.sendStatus(tweetMsg)
                    newTweetUrl = "https://twitter.com/%s/status/%s" % (newTweet.user.screen_name, newTweet.id_str)
                    printWithStamp("%s\n%s" % (newTweetUrl, tweetMsg))
                    result = TweetResult.SENT
                except TweepError as e:
                    printWithStamp("Twitter error #%s: '%s'" % (idToTweet, str(e)))
                    result = TweetResult.TWITTER_ERROR
            else:
                printWithStamp("Didn't tweet #%s: '%s'" % (idToTweet, dispatchMsg))
                result = TweetResult.IGNORED
            settings.saveDispatchId(idToTweet)
            self.lastDispatchId = idToTweet
        else:
            printWithStamp("Nothing to tweet...")
        return result

    def sendNext(self):
        self.updateIds()
        return self.tweetStatus()
