from data_analysis.utilities import str_to_cards_list, processing
from gameplay.actions import BidAction, PlayCardAction
from gameplay.game import Game

data = processing("data_analysis/660481.txt")
first_round = data['rounds'][0]

game = Game(1, 100000000,
            starting_card_orders=[first_round['cards']],
            starting_players=[first_round['tricks'][0]['start']])

for player in game.round.players:
    print(player.hand.cards)

bids = first_round['bids']
for bid in bids:
    game.step(BidAction(bid))

trick_cards = [x['cards'] for x in first_round['tricks']]

for trick in trick_cards:
    for card in trick:
        print("Player {} plays card {}".format(game.round.current_player_id, card))
        game.step(PlayCardAction(card))

print(game.get_total_score())
print(game.round.tricks_won)
print(game.round.bids)
