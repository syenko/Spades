from typing import Any

from gameplay.card import Card
from gameplay.constants import Suit
from gameplay.moves import PlayCardMove


def winning_trick(trick_moves: list[PlayCardMove]):
    leading_suit = trick_moves[0].card.suit

    trick_moves.sort(key=lambda x: (
        2 if x.card.suit == Suit.SPADES else
        1 if x.card.suit == leading_suit else
        0,
        x.card.number
    ), reverse=True)

    return trick_moves[0].player.position, trick_moves[0].card
