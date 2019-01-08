import sched
import time

from tweetLogic import tweetLogic

s = sched.scheduler(time.time, time.sleep)
_tweetLogic = tweetLogic()

def doATweet(sc):
    sentTweet = False
    while sentTweet == False:
        sentTweet = _tweetLogic.sendNext()
    s.enter(300, 1, doATweet, (sc,))

s.enter(5, 1, doATweet, (s,))
s.run()