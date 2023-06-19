from enum import IntEnum

__all__ = ["Reaction"]


class Reaction(IntEnum):
    RECIPROCITY = 1
    FOLLOWER = 2
    USER = 3
    HATER = 4
    OTHER = 5
