from gameplay.actions import PlayCardAction, BidAction
from gameplay.player import Player


# Moves are Actions that a player *HAS* taken

class Move:  # Interface
    pass


class PlayCardMove(Move):
    def __init__(self, action: PlayCardAction, player: Player):
        self.action = action
        self.card = action.card
        self.player = player


class BidMove(Move):
    def __init__(self, action: BidAction, player: Player):
        self.action = action
        self.bid = action.bid
        self.player = player