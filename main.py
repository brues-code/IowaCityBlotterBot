from sched import scheduler
from time import sleep, time
from tweetLogic import tweetLogic
from tweetResult import TweetResult

s = scheduler(time, sleep)
_tweetLogic = tweetLogic()

def doATweet(sc):
    secs = _tweetLogic.sendNext()
    s.enter(secs.value, 1, doATweet, (sc,))

s.enter(5, 1, doATweet, (s,))
s.run()
