from gameplay.actions import PlayCardAction, BidAction
from gameplay.constants import Suit, Phase, MAX_NUM_CARDS
from gameplay.player import Player
from gameplay.moves import PlayCardMove, Move, BidMove


class Round(object):
    def __init__(self, players: list[Player], round_num: int, game_starting_player: int = 0):
        self.round_num = round_num

        self.players = players

        self.current_player_id: int = 0

        self.phase: Phase = Phase.BIDDING

        self.leading_suit: Suit | None = None
        self.spades_broken = False

        self.num_cards_played: int = 0
        self.tricks_won: list[int] = [0, 0, 0, 0]  # tricks won per player
        self.bids: list[int] = [0, 0, 0, 0]  # tricks bid per player
        self.bid_move_log: list[BidMove] = []
        self.card_move_log: list[PlayCardMove] = []

        self.game_starting_player = game_starting_player

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
            self.tricks_won[winning_trick.player.position] += 1

            # reset position and leading suit
            self.current_player_id = winning_trick.player.position
            self.leading_suit = None
        else:
            self.current_player_id = (self.current_player_id + 1) % 4

    def bid(self, action: BidAction):
        current_player = self.get_current_player()
        self.bid_move_log.append(BidMove(action, current_player))
        current_player.bid = action.bid
        self.bids[current_player.position] += action.bid

        # increment player
        self.current_player_id = (self.current_player_id + 1) % 4

        # switching to playing once all bids are finished
        if len(self.bid_move_log) >= len(self.players):
            self.phase = Phase.PLAYING
            self.current_player_id = self.game_starting_player

    def get_trick_moves(self) -> list[PlayCardMove]:
        if self.num_cards_played > 0:
            num_trick_moves = self.num_cards_played % 4
            if num_trick_moves == 0:
                num_trick_moves = 4

            return self.card_move_log[-num_trick_moves:]

    def get_current_player(self) -> Player:
        return self.players[self.current_player_id]

    # returns for the appropriate score for a NON-NIL BID
    def __calculate_bid(self, made, bid):
        if made >= bid:
            return bid * 10 + (made - bid)
        else:
            return -bid * 10

    def get_scores(self) -> list[int]:
        scores = [0, 0]

        for team_num in range(2):
            # nil bid
            if self.bids[team_num] == 0 or self.bids[team_num + 2] == 0:
                for made, bid in zip(self.tricks_won[team_num: 4: 2], self.bids[team_num: 4: 2]):
                    # bid nil
                    if bid == 0:
                        if made == 0:
                            scores[team_num] += 100
                        else:
                            scores[team_num] += -100
                    else:
                        scores[team_num] += self.__calculate_bid(made, bid)

                pass
            # normal scoring
            else:
                made = sum(self.tricks_won[team_num: 4: 2])
                bid = sum(self.bids[team_num: 4: 2])
                scores[team_num] = self.__calculate_bid(made, bid)

        return scores

    def is_over(self) -> bool:
        return self.num_cards_played >= MAX_NUM_CARDS
