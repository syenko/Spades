from gameplay.deck import Deck
from gameplay.player import Player

class Game(object):

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.players = []

        for i in range(1, 5):
            self.hand = self.deck.cards[(i-1)*13: i*13]
            self.players.append(Player(self.hand))


    def play_game(self):
        pass



game = Game()
for i in range(0, 13):
     print(game.players[0].hand[i])
print("-------")
game.players[0].hand_sort()
for i in range(0, 13):
     print(game.players[0].hand[i])
