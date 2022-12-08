from enum import IntEnum


class TweetResult(IntEnum):
    IGNORED = 5
    ERROR = 6
    NO_TWEETS = 600
    SENT = 900
