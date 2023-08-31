from gameplay.card import Card
import random

class Deck(object):

    suites = ["Spades", "Hearts", "Diamonds", "Clubs"]

    def __init__(self):
        self.cards = []

        for i in range(0, 4):
            for j in range(2, 15):
                self.cards.append(Card(Deck.suites[i], j))

    def shuffle(self):
        random.shuffle(self.cards)