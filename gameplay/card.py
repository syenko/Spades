from gameplay.constants import Suit

class Card(object):
    def __init__(self, suit: Suit, number: int):
        self.suit: Suit = suit
        self.number: int = number  # 2 - 14: 11 (Jack), 12 (Queen), 13 (King), 14 (Ace)

    def __repr__(self):
        return "{number} of {suit}".format(number=str(self.number), suit=self.suit.name.title())

    def get_id(self) -> int:
        return self.suit.value * 13 + (self.number-2)

