from enum import Enum


class Suit(Enum):
    DIAMONDS = 0
    CLUBS = 1
    HEARTS = 2
    SPADES = 3


class Phase(Enum):
    BIDDING = 0
    PLAYING = 1


MAX_NUM_CARDS = 52
