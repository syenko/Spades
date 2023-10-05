from abc import abstractmethod, ABC

from gameplay.card import Card
from gameplay.constants import MAX_NUM_CARDS


# Actions are different actions that a player can take (does *NOT* include player information)

class Action(ABC):  # Interface
    NUM_BID_ACTIONS = 14
    NUM_CARD_ACTIONS = MAX_NUM_CARDS

    @abstractmethod
    def get_id(self) -> int:
        pass

    @classmethod
    def get_num_actions(cls) -> int:
        return cls.NUM_BID_ACTIONS + cls.NUM_CARD_ACTIONS


class PlayCardAction(Action):
    def __init__(self, card: Card):
        self.card = card

    def get_id(self):
        return Action.NUM_BID_ACTIONS + self.card.get_id()

class BidAction(Action):
    def __init__(self, bid: int):
        self.bid = bid

    def get_id(self):
        return self.bid