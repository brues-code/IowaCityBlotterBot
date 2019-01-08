import sched
import time
from tweetLogic import tweetLogic
from tweetResult import TweetResult

s = sched.scheduler(time.time, time.sleep)
_tweetLogic = tweetLogic()

def doATweet(sc):
    sentTweet = _tweetLogic.sendNext()
    secs = 900
    if sentTweet == TweetResult.NOTWEETS:
        secs = 300
    elif sentTweet == TweetResult.IGNORED or sentTweet == TweetResult.TWITTER_ERROR:
        secs = 5
    s.enter(secs, 1, doATweet, (sc,))

s.enter(5, 1, doATweet, (s,))
s.run()
