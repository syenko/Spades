from gameplay.constants import Suit

class Card(object):
    def __init__(self, suit: Suit, number: int):
        self.suit: Suit = suit
        self.number: int = number

    def __repr__(self):
        return "{number} of {suit}".format(number=str(self.number), suit=self.suit.name.title())
