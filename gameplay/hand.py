import random

from gameplay.card import Card
from gameplay.enums import Suit


class Hand(object):
    def __init__(self, hand):
        self.cards = {
            suit: [] for suit in Suit
        }

        self.played_cards = {
            suit: [] for suit in Suit
        }

        for card in hand:
            self.cards[card.suit].append(card)

        for suit, val in self.cards.items():
            val.sort(key=lambda x: x.number, reverse=True)

    def get_count(self, suit):
        return len(self.cards[suit])

    def get_random(self, suits=None) -> Card:
        if suits is None:
            suits = list(Suit)

        combined_cards = []

        for suit in suits:
            combined_cards.extend(self.cards[suit])

        return random.choice(combined_cards)

    def play_card(self, card: Card):
        assert(card in self.cards[card.suit])

        self.cards[card.suit].remove(card)
        self.played_cards[card.suit].append(card)