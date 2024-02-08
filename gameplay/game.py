from gameplay.actions import Action, PlayCardAction, BidAction
from gameplay.card import Card
from gameplay.deck import Deck
from gameplay.constants import Suit, Phase, NUM_ROUNDS
from gameplay.moves import Move, PlayCardMove
from gameplay.player import Player
from gameplay.round import Round


class Game(object):

    def __init__(
            self,
            max_rounds: int,
            winning_score: int,
            starting_card_orders: list[list[Card]] = None,
            starting_players: list[int] = None,
            starting_scores: list[int] = None
    ):
        self.initial_scores = [0, 0] if starting_scores is None else starting_scores[:]
        self.card_orders = [] if starting_card_orders is None else starting_card_orders[:]
        self.starting_players = [] if starting_players is None else starting_players[:]

        self.deck: Deck = Deck()

        self.max_rounds = max_rounds
        self.winning_score = winning_score

        self.players: list[Player] = []
        self.starting_player_index = 0
        self.current_player_index = 0

        self.previous_rounds = []
        self.round_num = 0
        self.round: Round = Round(players=self.players, round_num=0)

        self.setup_next_round()

    def setup_next_round(self):
        # fixed order given
        if len(self.card_orders) > self.round_num:
            self.deck.set_fixed_order(self.card_orders[self.round_num])
        # otherwise, just shuffle
        else:
            self.deck.shuffle()

        self.players.clear()

        for i in range(1, 5):
            hand = self.deck.cards[(i - 1) * NUM_ROUNDS: i * NUM_ROUNDS]
            self.players.append(Player(hand, i - 1))

        starting_player = 0
        # set fixed starting player if there is one
        if len(self.starting_players) > self.round_num:
            starting_player = self.starting_players[self.round_num]

        self.round = Round(players=self.players, round_num=self.round_num, game_starting_player=starting_player)

        self.round_num += 1

    def reset(self):
        self.starting_player_index = 0
        self.current_player_index = 0
        self.previous_rounds = []
        self.round: Round = Round(players=self.players, round_num=0)

        self.setup_next_round()

    def get_total_score(self) -> list[int]:
        round_scores = self.round.get_scores()
        total_scores = round_scores[:]

        total_scores[0] += self.initial_scores[0]
        total_scores[1] += self.initial_scores[1]

        for round_ in self.previous_rounds:
            if round_ != self.round:
                round_scores = round_.get_scores()
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
            self.previous_rounds.append(self.round)

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
                    legal_actions = [BidAction(bid) for bid in range(0, NUM_ROUNDS)]
                # partner bid first
                else:
                    partner_bid = self.round.bids[current_player.position % 2]
                    max_bid = NUM_ROUNDS - partner_bid
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

