from math import floor

from gameplay.actions import BidAction
from gameplay.card import Card
from gameplay.deck import Deck
from gameplay.hand import Hand


# bidding for full game
def bid_full(hand) -> int:
    cards = hand
    bid = 0

    number_of_suits = [0, 0, 0, 0]  # DIAMONDS = 3 CLUBS = 2 HEARTS = 1 SPADES = 0

    for x in cards:
        number_of_suits[x.suit.value] += 1

    trumps = number_of_suits[0]  # checking voids + extra trumps for bid
    if trumps == 6:
        bid += 0.5
    elif trumps >= 7:
        bid += (trumps - 6)

    for i, x in enumerate(number_of_suits):
        if i == 0:
            pass
        else:
            if x == 0:
                bid += 1.5
            elif x == 1:
                bid += 1
            elif x == 2:
                bid += 0.5

    for x in cards:
        card_suit = x.suit.value
        card_number = x.number
        num_suits = number_of_suits[card_suit]
        if card_suit != 0:  # NonTrump
            if card_number == 14:  # NonTrump Ace
                if num_suits < 7:
                    bid += 1
                elif num_suits == 7 or num_suits == 8:
                    bid += 0.5
            elif card_number == 13:  # NonTrump King
                if num_suits == 1 or num_suits == 5:
                    bid += 0.25
                elif 4 >= num_suits >= 2:
                    bid += 0.75
            elif card_number == 12:  # NonTrump Queen
                if num_suits < 6:
                    bid += 0.25
        else:  # Trump
            if 11 <= card_number <= 14:  # only count J, Q, K, or A
                value = card_number + num_suits  # seeing how protected trump is
                if value >= 15:
                    bid += 1
                elif value >= 14:
                    bid += 0.75
                elif value >= 13:
                    bid += 0.25

    return floor(bid)


# bidding for simplified game
def bid_partial(hand: [Card]) -> int:
    cards = hand
    bid = 0

    number_of_suits = [0, 0, 0, 0]  # DIAMONDS = 3 CLUBS = 2 HEARTS = 1 SPADES = 0

    for x in cards:
        number_of_suits[x.suit.value] += 1

    trumps = number_of_suits[0]  # checking voids + extra trumps for bid
    if trumps == 3:
        bid += 0.5
    elif trumps >= 4:
        bid += (trumps - 3)

    for i, x in enumerate(number_of_suits):
        if i == 0:
            pass
        else:
            if x == 0:
                bid += 0.5

    for x in cards:
        card_suit = x.suit.value
        card_number = x.number
        num_suits = number_of_suits[card_suit]
        if card_suit != 0:  # NonTrump
            if card_number == 7:  # NonTrump Ace
                if num_suits < 3:
                    bid += 1
                elif num_suits == 3:
                    bid += 0.5
            elif card_number == 6:  # NonTrump King
                if num_suits == 2:
                    bid += 0.5
                elif num_suits == 1 or num_suits == 3:
                    bid += 0.25
        else:  # Trump
            if 6 <= card_number <= 7:  # only count 6, 7
                value = card_number + num_suits  # how protected Trump is
                if value >= 8:
                    bid += 1
                elif value >= 7:
                    bid += 0.5
    if floor(bid) == 0:
        return 1
    return floor(bid)


def bid_action_partial(hand: Hand) -> BidAction:
    return BidAction(bid_partial(hand.hand))

# deck = Deck()
# deck.shuffle()
#
# hand = []
#
# for x in deck.cards:
#     if x.number <= 7:
#         hand.append(x)
#     if len(hand) == 6:
#         break
#
# hand = deck.cards[0:13]
# print(hand)
# print(bid_partial(hand))
