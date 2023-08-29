from gameplay.deck import Deck
from gameplay.player import Player

class Game(object):
    def __init__(self):
        deck = Deck()
        players = [Player(), Player(), Player(), Player()]