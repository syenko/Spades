
class Observation(object):
    def __init__(self, position, trick_cards_played, total_cards_played, suit, bids, spades_broken):
        self.position = position
        self.trick_cards_played = trick_cards_played
        self.total_cards_played = total_cards_played
        self.suit = suit
        self.bids = bids
        self.spades_broken = spades_broken
