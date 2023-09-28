from gameplay.actions import PlayCardAction
from gameplay.player import Player


# Moves are Actions that a player *HAS* taken

class Move:  # Interface
    pass


class PlayCardMove(Move):
    def __init__(self, action: PlayCardAction, player: Player):
        self.action = action
        self.card = action.card
        self.player = player
