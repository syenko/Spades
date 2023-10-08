from abc import abstractmethod, ABC
from typing import Self

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

    @classmethod
    def get_action_from_id(cls, val: int) -> Self:
        if val < cls.NUM_BID_ACTIONS:
            return BidAction(val)
        val -= cls.NUM_BID_ACTIONS

        if val < cls.NUM_CARD_ACTIONS:
            return PlayCardAction.from_id(val)

class PlayCardAction(Action):
    def __init__(self, card: Card):
        self.card = card

    @classmethod
    def from_id(cls, val: int) -> Self:
        return cls(Card.from_id(val))

    def get_id(self):
        return Action.NUM_BID_ACTIONS + self.card.get_id()

class BidAction(Action):
    def __init__(self, bid: int):
        self.bid = bid

    def get_id(self):
        return self.bid