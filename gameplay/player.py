from gameplay.card import Card
from gameplay.hand import Hand
from gameplay.constants import Suit


class Player(object):

    def __init__(self, hand, position):
        self.hand = Hand(hand)
        self.position = position
        self.tricks_taken = 0
        self.bid = 0

    def play_card(self, card: Card):
        self.hand.play_card(card)

    def __str__(self):
        return ['N', 'E', 'S', 'W'][self.position]
