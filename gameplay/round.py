from typing import List

from gameplay.actions import PlayCardAction
from gameplay.card import Card
from gameplay.enums import Suit, Phase
from gameplay.player import Player
from gameplay.moves import PlayCardMove, Move


class Round(object):
    def __init__(self, players: List[Player], round_num: int):
        self.round_num = round_num

        self.players = players

        self.current_player_id: int = 0

        self.phase: Phase = Phase.PLAYING  # TODO: Actually change this at some point

        self.leading_suit: Suit | None = None
        self.spades_broken = False

        self.num_cards_played: int = 0
        self.tricks_won: List[int] = [0, 0]  # tricks won on each side
        self.move_log: List[Move] = []

    def play_card(self, action: PlayCardAction):
        current_player = self.get_current_player()
        self.move_log.append(PlayCardMove(action, current_player))
        current_player.play_card(action.card)
        self.num_cards_played += 1

        if action.card.suit == Suit.SPADES:
            self.spades_broken = True

        trick_moves: List[PlayCardMove] = self.get_trick_moves()

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

    def get_trick_moves(self) -> List[PlayCardMove]:
        if self.num_cards_played > 0:
            num_trick_moves = self.num_cards_played % 4
            if num_trick_moves == 0:
                num_trick_moves = 4

            return self.move_log[-num_trick_moves:]

    def get_current_player(self):
        return self.players[self.current_player_id]