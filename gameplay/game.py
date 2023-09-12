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
            self.hand = self.deck.cards[(i - 1) * 13: i * 13]
            self.players.append(Player(self.hand, i))

    def play_game(self):
        for i in range(13):
            print("=================== ROUND {} ===================".format(i))
            game.play_round()

        print("\n***************** Final Results *****************")
        for i, player in enumerate(self.players):
            print("Player {}: {}/{}".format(i, player.tricks_taken, player.bid))

        print("Team 1 scored {} ".format(self.get_score(self.players[::2])))
        print("Team 2 scored {} ".format(self.get_score(self.players[1::2])))

    def get_score(self, players):
        total_bid = 0
        total_made = 0

        for player in players:
            total_bid += player.bid
            total_made += player.tricks_taken

        if total_made >= total_bid:
            return total_bid * 10 + (total_made - total_bid)
        else:
            return -total_bid * 10

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