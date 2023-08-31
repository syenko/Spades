from gameplay.card import Card


class Player(object):

    SUIT_ORDER = {
        "Diamonds": 0,
        "Clubs": 1,
        "Hearts": 2,
        "Spades": 3,
    }

    def __init__(self, hand):
        self.hand = hand
        self.tricks = 0;

    def helper(card: Card):
        suit = Player.SUIT_ORDER.get(card.suite)
        rank = card.number
        return (suit, rank)

    def hand_sort(self):
        self.hand.sort(key=Player.helper)