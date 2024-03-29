from typing import Self

from gameplay.constants import Suit, NUM_ROUNDS


class Card(object):
    def __init__(self, suit: Suit, number: int):
        self.suit: Suit = suit
        self.number: int = number  # 2 - 14: 11 (Jack), 12 (Queen), 13 (King), 14 (Ace)

    def __repr__(self):
        return "{number} of {suit}".format(number=str(self.number), suit=self.suit.name.title())

    def __eq__(self, other: Self):
        return self.number == other.number \
            and self.suit == other.suit

    def get_id(self) -> int:
        return self.suit.value * NUM_ROUNDS + (self.number-2)

    @classmethod
    def from_id(cls, val: int) -> Self:
        number: int = val % NUM_ROUNDS + 2
        suit: Suit = Suit(val // NUM_ROUNDS)
        return cls(suit, number)