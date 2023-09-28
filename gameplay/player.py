from gameplay.card import Card
from gameplay.hand import Hand
from gameplay.observation import Observation
from gameplay.enums import Suit
import random


class Player(object):

    def __init__(self, hand, position):
        self.hand = Hand(hand)
        self.position = position
        self.tricks_taken = 0
        self.bid = 0

    def is_valid_move(self, observation: Observation, card: Card) -> bool:
        if observation.suit is None:
            return observation.spades_broken or card.suit != Suit.SPADES
        else:
            if self.hand.get_count(observation.suit) > 0:
                return observation.suit == card.suit
            else:
                return True

    def get_card_to_play(self, observation: Observation) -> Card:
        # TODO: Refactor to work with game.get_legal_actions
        if observation.suit is None:
            if not observation.spades_broken:
                card = self.hand.get_random(suits=[Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS])
                # TODO: account for case when can *only* play spades
            else:
                card = self.hand.get_random()
        else:
            if self.hand.get_count(observation.suit) > 0:
                card = self.hand.get_random(suits=[observation.suit])
            else:
                card = self.hand.get_random()

        print(card)

        assert (self.is_valid_move(observation, card))

        return card

    def play_card(self, card: Card):
        self.hand.play_card(card)

    def __str__(self):
        return ['N', 'E', 'S', 'W'][self.position]
