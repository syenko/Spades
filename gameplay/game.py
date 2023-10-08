from gameplay.actions import Action, PlayCardAction, BidAction
from gameplay.card import Card
from gameplay.deck import Deck
from gameplay.constants import Suit, Phase
from gameplay.moves import Move, PlayCardMove
from gameplay.player import Player
from gameplay.round import Round


class Game(object):

    def __init__(self, max_rounds: int, winning_score: int):
        self.deck: Deck = Deck()

        self.max_rounds = max_rounds
        self.winning_score = winning_score

        self.players: list[Player] = []
        self.starting_player_index = 0
        self.current_player_index = 0

        self.previous_rounds = []
        self.round: Round = Round(players=self.players, round_num=0)

        self.setup_next_round()

    def setup_next_round(self):
        self.deck.shuffle()
        self.players.clear()

        for i in range(1, 5):
            hand = self.deck.cards[(i - 1) * 13: i * 13]
            self.players.append(Player(hand, i))

        self.round: Round = Round(players=self.players, round_num=len(self.previous_rounds))

    def play_game(self):
        for i in range(13):
            print("=================== ROUND {} ===================".format(i))
            game.play_round()

        print("\n***************** Final Results *****************")
        for i, player in enumerate(self.players):
            print("Player {}: {}/{}".format(i, player.tricks_taken, player.bid))

        print("Team 1 scored {} ".format(self.get_score(self.players[::2])))
        print("Team 2 scored {} ".format(self.get_score(self.players[1::2])))

    def get_total_score(self) -> list[int]:
        round_scores = self.round.get_scores()
        total_scores = round_scores[:]
        for round in self.previous_rounds:
            round_scores = round.get_scores()
            total_scores[0] += round_scores[0]
            total_scores[1] += round_scores[1]

        return total_scores

    # takes an action, returns next player
    def step(self, action: Action) -> int:
        if isinstance(action, BidAction):
            self.round.bid(action)

        if isinstance(action, PlayCardAction):
            self.round.play_card(action)

        if self.round.is_over():
            self.previous_rounds.append(round)

        # TODO: consider what to return (state too??)

        return self.round.current_player_id

    # returns a list of actions the player can take given the particular state
    def get_legal_actions(self) -> list[Action]:
        legal_actions: list[Action] = []
        if not self.is_over():
            current_player = self.round.get_current_player()
            if self.round.phase == Phase.BIDDING:
                # bidding first
                if len(self.round.bid_move_log) < len(self.round.players) // 2:
                    legal_actions = [BidAction(bid) for bid in range(0, 13)]
                # partner bid first
                else:
                    partner_bid = self.round.bids[current_player.position % 2]
                    max_bid = 13 - partner_bid
                    min_bid = 4 - partner_bid
                    legal_actions = [BidAction(bid) for bid in range(min_bid, max_bid)]
                    legal_actions.append(BidAction(0)) # always allow going nil

            elif self.round.phase == Phase.PLAYING:
                leading_suit = self.round.leading_suit
                hand = current_player.hand.hand

                legal_cards: list[Card] = hand

                # there is an existing starting suit
                if leading_suit:
                    legal_cards = [card for card in hand if card.suit == leading_suit]
                # starting, but spades hasn't been broken yet
                elif not self.round.spades_broken:
                    legal_cards = [card for card in hand if card.suit != Suit.SPADES]

                if len(legal_cards) == 0:
                    legal_cards = hand

                legal_actions = [PlayCardAction(card) for card in legal_cards]
        return legal_actions

    def is_over(self) -> bool:
        return len(self.previous_rounds) > self.max_rounds or \
            max(self.round.get_scores()) > self.winning_score



game = Game()
game.play_game()