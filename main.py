from tweetLogic import tweetLogic
import sched, time

s = sched.scheduler(time.time, time.sleep)
_tweetLogic = tweetLogic()

def doATweet(sc):
    _tweetLogic.sendNext()
    s.enter(60, 1, doATweet, (sc,))


s.enter(5, 1, doATweet, (s,))
s.run()