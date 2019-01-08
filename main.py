import sched
import time

from tweetLogic import tweetLogic

s = sched.scheduler(time.time, time.sleep)
_tweetLogic = tweetLogic()

def doATweet(sc):
    sentTweet = _tweetLogic.sendNext()
    secs = 900 if sentTweet else 300
    s.enter(secs, 1, doATweet, (sc,))

s.enter(5, 1, doATweet, (s,))
s.run()