from enum import Enum


class Suit(Enum):
    DIAMONDS = 3
    CLUBS = 2
    HEARTS = 1
    SPADES = 0


class Phase(Enum):
    BIDDING = 0
    PLAYING = 1


MAX_NUM_CARDS = 52
