from gameplay.deck import Deck
from gameplay.enums import Suit
from gameplay.observation import Observation
from gameplay.player import Player

class Game(object):

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.players = []
        self.starting_player_index = 0
        self.current_player_index = 0

        self.cards_played = []
        self.bids = []

        self.spades_broken = False

        for i in range(1, 5):
            self.hand = self.deck.cards[(i-1)*13: i*13]
            self.players.append(Player(self.hand, i))

    def play_game(self):
        for i in range(13):
            print("=================== ROUND {} ===================".format(i))
            game.play_round()

    def play_round(self):
        tricks_played = []
        suit = None

        for i in range(len(self.players)):
            self.current_player_index = (self.starting_player_index + i) % 4
            card_played = self.players[self.current_player_index].play(
                Observation(i, tricks_played, self.cards_played, suit, self.bids, self.spades_broken)
            )

            if suit is None:
                suit = card_played.suit

            if card_played.suit == Suit.SPADES:
                self.spades_broken = True

            self.cards_played.append(card_played)
            tricks_played.append({
                "card": card_played,
                "player": self.players[self.current_player_index]
            })

        # sort tricks to get the winner
        tricks_played.sort(key=lambda x: (
            2 if x["card"].suit == Suit.SPADES else
            1 if x["card"].suit == suit else
            0,
            x["card"].number
        ), reverse=True)

        winning_trick = tricks_played[0]

        winning_trick["player"].tricks_taken += 1
        self.starting_player_index = winning_trick["player"].position

        print("Winning Trick: {}".format(tricks_played[0]["card"]))


game = Game()
game.play_game()
# for i in range(0, 13):
#      print(game.players[0].hand[i])
# print("-------")
# game.players[0].hand_sort()
# for i in range(0, 13):
#      print(game.players[0].hand[i])
