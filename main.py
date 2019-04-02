from sched import scheduler
from time import sleep, time
from tweetLogic import tweetLogic

s = scheduler(time, sleep)
_tweetLogic = tweetLogic()


def doATweet(sc):
    secs = _tweetLogic.sendNext()
    s.enter(secs.value, 1, doATweet, (sc,))


s.enter(1, 1, doATweet, (s,))
s.run()
