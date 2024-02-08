from gameplay import gameutilities
from gameplay.constants import Suit


class Playing(object):

    # FOR REDUCED GAME: 2, 3, 4, 5, 6, 7

    DIAMONDS = 3
    CLUBS = 2
    HEARTS = 1
    SPADES = 0

    def __init__(self, game, player):
        self.game = game
        self.hand = player.hand
        self.position = player.position
        self.partner = (self.position + 2) % 4
        self.boss = {Suit.SPADES: [2, 3, 4, 5, 6, 7], Suit.HEARTS: [2, 3, 4, 5, 6, 7],
                     Suit.CLUBS: [2, 3, 4, 5, 6, 7], Suit.DIAMONDS: [2, 3, 4, 5, 6, 7]}

    def play(self):
        cards_played = self.game.round.get_trick_moves()

        length = len(cards_played) % 4  # to get position
        if length == 0:
            return self.play_first()
        elif length == 1:
            return self.play_second(cards_played)
        elif length == 2:
            return self.play_third(cards_played)
        else:
            return self.play_fourth(cards_played)

    def spades_winning(self, winner, possibilities, suit):
        if len(possibilities) == 0:  # I'm void
            if len(self.hand.cards[Suit.SPADES]) == 0:
                return self.hand.cards[self.worst_suit()][-1]
            elif self.hand.cards[Suit.SPADES][0].number > winner.number:
                for x in range(len(self.hand.cards[Suit.SPADES]), -1, -1):
                    if self.hand.cards[Suit.SPADES][x-1].number > winner.number:
                        return self.hand.cards[Suit.SPADES][x-1]
            return self.hand.cards[self.worst_suit()][-1]  # plays worst card
        return possibilities[-1]
    def play_first(self):
        suit = self.worst_suit()  # determine what suit to play
        possibilities = self.hand.cards[suit]  # get possible cards
        if possibilities[0].number == self.boss[suit][-1]:
            return possibilities[0]
        return possibilities[-1]

    def play_second(self, cards_played):
        suit = cards_played[0].card.suit
        possibilities = self.hand.cards[suit]  # get possible cards
        if len(possibilities) == 0:  # you're void
            if len(self.hand.cards[Suit.SPADES]) != 0:  # if ur not void spades
                return self.hand.cards[Suit.SPADES][-1]  # trump
            return self.hand.cards[self.worst_suit()][-1]  # plays worst card
        if possibilities[0].number == self.boss[suit][-1]:
            return possibilities[0]
        return possibilities[-1]

    def play_third(self, cards_played):
        suit = cards_played[0].card.suit
        winning_player, winning_card = gameutilities.winning_trick(cards_played)
        possibilities = self.hand.cards[suit]  # get possible cards

        if winning_player == self.partner:  # partner is winning
            if winning_card.number != self.boss[suit][-1]:  # if their card isn't the boss:
                if len(possibilities) == 0:  # i'm void
                    if len(self.hand.cards[Suit.SPADES]) != 0:
                        if winning_card.suit != Suit.SPADES:
                            return self.hand.cards[Suit.SPADES][-1]
                    return self.hand.cards[self.worst_suit()][-1]  # plays worst card
                if self.boss[suit][-1] == possibilities[0].number and self.boss[suit][-2] != winning_card.number:  # if i have boss and it doesn't cover partner
                    return possibilities[0]
                return possibilities[-1]  # play worst card
            if len(possibilities) == 0:
                return self.hand.cards[self.worst_suit()][-1]  # plays worst card
            return possibilities[-1]

        else: # partner not winning
            if winning_card.suit == Suit.SPADES:
                return self.spades_winning(winning_card, possibilities, suit)
            if len(possibilities) == 0:  # i'm void
                if len(self.hand.cards[Suit.SPADES]) != 0:
                    return self.hand.cards[Suit.SPADES][-1]
                return self.hand.cards[self.worst_suit()][-1]  # plays worst card
            if possibilities[0].number > winning_card.number:  # if i have a better card
                return possibilities[0]  # play it
            return possibilities[-1]  # play worst card

    def play_fourth(self, cards_played):
        suit = cards_played[0].card.suit
        winning_player, winning_card = gameutilities.winning_trick(cards_played)
        possibilities = self.hand.cards[suit]  # get possible cards

        if winning_player == self.partner:  # partner is winning
            if len(possibilities) == 0:
                return self.hand.cards[self.worst_suit()][-1]  # plays worst card
            return possibilities[-1]
        else:
            if len(possibilities) == 0:  # you're void
                if winning_card.suit == Suit.SPADES:
                    return self.spades_winning(winning_card, possibilities, suit)
                else:
                    if len(self.hand.cards[Suit.SPADES]) != 0:
                        return self.hand.cards[Suit.SPADES][-1]
                    return self.hand.cards[self.worst_suit()][-1]  # plays worst card
            else:
                if winning_card.suit == Suit.SPADES:
                    return possibilities[-1]
                if possibilities[0].number > winning_card.number:  # if you have highest card:
                    for x in range(len(self.hand.cards[suit]), -1, -1):
                        if self.hand.cards[suit][x - 1].number > winning_card.number:
                            return self.hand.cards[suit][x - 1]
                return possibilities[-1]  # plays worst card

    def update(self):
        cards_played = self.game.round.get_trick_moves()
        for move in cards_played:
            if move.card.suit == Suit.SPADES:
                self.boss[Suit.SPADES].remove(move.card.number)
            elif move.card.suit == Suit.DIAMONDS:
                self.boss[Suit.DIAMONDS].remove(move.card.number)
            elif move.card.suit == Suit.CLUBS:
                self.boss[Suit.CLUBS].remove(move.card.number)
            else:
                self.boss[Suit.HEARTS].remove(move.card.number)

    def worst_suit(self):  # returns weakest suit in 0, 1, 2, 3
        hearts = self.hand.cards[Suit.HEARTS]
        clubs = self.hand.cards[Suit.CLUBS]
        diamonds = self.hand.cards[Suit.DIAMONDS]
        if len(hearts) == len(clubs) == len(diamonds) == 0:  # if no other cards, play Spades
            return Suit.SPADES
        heartrank = -len(hearts)
        clubrank = -len(clubs)
        diamondrank = -len(diamonds)

        if heartrank != 0:
            if hearts[-1].number == 6:
                if len(hearts) == 1:
                    heartrank -= 10
                else:
                    heartrank -= 5
            elif hearts[-1].number == 7:
                if len(hearts) == 1:
                    heartrank -= 5
                else:
                    heartrank -= 2
        else:
            heartrank = -20

        if clubrank != 0:
            if clubs[-1].number == 6:
                if len(clubs) == 1:
                    clubrank -= 10
                else:
                    clubrank -= 5
            elif clubs[-1].number == 7:
                if len(clubs) == 1:
                    clubrank -= 5
                else:
                    clubrank -= 2
        else:
            clubrank = -20

        if diamondrank != 0:
            if diamonds[-1].number == 6:
                if len(clubs) == 1:
                    clubrank -= 10
                else:
                    clubrank -= 5
            elif diamonds[-1].number == 7:
                if len(diamonds) == 1:
                    diamondrank -= 5
                else:
                    diamondrank -= 2
        else:
            diamondrank = -20

        if heartrank >= clubrank and heartrank >= diamondrank:
            return Suit.HEARTS
        elif clubrank >= heartrank and clubrank >= diamondrank:
            return Suit.CLUBS
        else:
            return Suit.DIAMONDS
