from gameplay.card import Card
import random

from gameplay.constants import Suit, NUM_ROUNDS


class Deck(object):
    def __init__(self):
        self.cards: list[Card] = []

        for suit in Suit:
            for j in range(2, NUM_ROUNDS + 2):
                self.cards.append(Card(suit, j))

    def shuffle(self):
        random.shuffle(self.cards)

    def set_fixed_order(self, cards: list[Card]):
        self.cards = cards