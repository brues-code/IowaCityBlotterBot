from sched import scheduler
from time import sleep, time
from tweetLogic import TweetLogic

s = scheduler(time, sleep)
_tweetLogic = TweetLogic()


def do_a_tweet(sc):
    secs = _tweetLogic.send_next()
    s.enter(secs.value, 1, do_a_tweet, (sc,))


s.enter(1, 1, do_a_tweet, (s,))
s.run()
