from gameplay.card import Card


# Actions are different actions that a player can take (does *NOT* include player information)

class Action:  # Interface
    pass


class PlayCardAction(Action):
    def __init__(self, card: Card):
        self.card = card
