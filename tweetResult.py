from enum import Enum
class TweetResult(Enum):
    NOTWEETS = 1
    IGNORED = 2
    SENT = 3
    TWITTER_ERROR = 4