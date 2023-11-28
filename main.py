from data_analysis.utilities import str_to_cards_list, processing, two_lists_are_equal
from gameplay.actions import BidAction, PlayCardAction
from gameplay.game import Game
from os import listdir
from os.path import isfile, join
import logging

# SETUP
TEST_FILES = ['660671.txt', '660511.txt', '660672.txt', '660607.txt', '660570.txt', '660594.txt', '660596.txt', '660587.txt', '660552.txt', '660481.txt', '660668.txt', '660523.txt', '660731.txt', '660524.txt'] # ["660607.txt"]

num_files_tested = 0
num_files_correct = 0

def test_file(filename: str) -> bool:
    global num_files_tested
    global num_files_correct
    logging.info("********* Testing file {} *********".format(filename))
    logging.debug("========= SETUP VALUES =========")
    data = processing("data_analysis/data/{}".format(filename))

    logging.debug(data['variation'])

    # wrong mode or variation
    if data['mode'] != 0 or data['variation'] != 0:
        logging.info("Wrong mode / variation")
        return True

    first_round = data['rounds'][0]

    game = Game(1, 100000000,
                starting_card_orders=[first_round['cards']],
                starting_players=[first_round['tricks'][0]['start']])

    for player in game.round.players:
        logging.debug(player.hand.cards)

    bids = first_round['bids']
    for bid in bids:
        game.step(BidAction(bid))

    trick_cards = [x['cards'] for x in first_round['tricks']]

    for i, trick in enumerate(trick_cards):
        logging.debug("---------- Round {} ----------".format(i))
        for card in trick:
            logging.debug("Player {} plays card {}".format(game.round.current_player_id, card))
            game.step(PlayCardAction(card))

        logging.debug("Trick winner: Player {}".format(game.round.current_player_id))

    logging.info("========= RESULTS =========")
    logging.info("Simulated score: " + str(game.get_total_score()))
    logging.info("Data score: " + str(first_round['score']))
    logging.info("Simulated tricks won: " + str(game.round.tricks_won))
    logging.info("Data tricks won: " + str(first_round['trickstaken']))

    num_files_tested += 1
    if two_lists_are_equal(game.get_total_score(), first_round['score']):
    # if two_lists_are_equal(game.round.tricks_won, first_round['trickstaken']):
        num_files_correct += 1
        return True
    else:
        return False

logging.basicConfig(level=logging.INFO, format='%(message)s')

if len(TEST_FILES) == 0:
    onlyfiles = [f for f in listdir("data_analysis/data") if isfile(join("data_analysis/data", f))]
else:
    onlyfiles = TEST_FILES

incorrect_files = []

for f in onlyfiles:
    if not test_file(f):
        incorrect_files.append(f)

print("Number of files tested: {}".format(num_files_tested))
print("Number of files where the identical scores matched the result scores: {}".format(num_files_correct))

print(incorrect_files)