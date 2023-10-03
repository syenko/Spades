from gameplay.actions import PlayCardAction, BidAction
from gameplay.constants import Suit, Phase, MAX_NUM_CARDS
from gameplay.player import Player
from gameplay.moves import PlayCardMove, Move, BidMove


class Round(object):
    def __init__(self, players: list[Player], round_num: int):
        self.round_num = round_num

        self.players = players

        self.current_player_id: int = 0

        self.phase: Phase = Phase.BIDDING

        self.leading_suit: Suit | None = None
        self.spades_broken = False

        self.num_cards_played: int = 0
        self.tricks_won: list[int] = [0, 0]  # tricks won on each side
        self.tricks_bid: list[int] = [0, 0]  # tricks bid on each side
        self.bid_move_log: list[BidMove] = []
        self.card_move_log: list[PlayCardMove] = []

    def play_card(self, action: PlayCardAction):
        current_player = self.get_current_player()
        self.card_move_log.append(PlayCardMove(action, current_player))
        current_player.play_card(action.card)
        self.num_cards_played += 1

        if action.card.suit == Suit.SPADES:
            self.spades_broken = True

        trick_moves: list[PlayCardMove] = self.get_trick_moves()

        # on first card
        if len(trick_moves) == 1:
            self.leading_suit = trick_moves[0].card.suit

        # on round end
        if len(trick_moves) == 4:
            # sort tricks to get the winner
            trick_moves.sort(key=lambda x: (
                2 if x.card.suit == Suit.SPADES else
                1 if x.card.suit == self.leading_suit else
                0,
                x.card.number
            ), reverse=True)

            winning_trick = trick_moves[0]
            winning_trick.player.tricks_taken += 1
            self.tricks_won[winning_trick.player.position % 2] += 1

            # reset position and leading suit
            self.current_player_id = winning_trick.player.position
            self.leading_suit = None
        else:
            self.current_player_id = (self.current_player_id + 1) % 4

    def bid(self, action: BidAction):
        current_player = self.get_current_player()
        self.bid_move_log.append(BidMove(action, current_player))
        current_player.bid = action.bid
        self.tricks_bid[current_player.position % 2] += 1

        if len(self.bid_move_log) >= len(self.players):
            self.phase = Phase.BIDDING

    def get_trick_moves(self) -> list[PlayCardMove]:
        if self.num_cards_played > 0:
            num_trick_moves = self.num_cards_played % 4
            if num_trick_moves == 0:
                num_trick_moves = 4

            return self.card_move_log[-num_trick_moves:]

    def get_current_player(self) -> Player:
        return self.players[self.current_player_id]

    def get_scores(self) -> list[int]:
        scores = []
        for made, bid in zip(self.tricks_won, self.tricks_bid):
            if made >= bid:
                scores.append(bid * 10 + (made - bid))
            else:
                scores.append(-bid * 10)

        return scores

    def is_over(self) -> bool:
        return self.num_cards_played >= MAX_NUM_CARDS
