from gameplay.card import Card
from gameplay.constants import Suit

def str_value_to_num_value(value: str) -> int:
    cards_in_order = "23456789tjqka"
    return cards_in_order.index(value.lower()) + 2


def str_to_cards_list(card_str: str) -> list[Card]:
    cards = [
        Card(Suit(int(card_str[i])), str_value_to_num_value(card_str[i + 1])) for i in range(0, len(card_str), 2)
    ]
    return cards

def processing(filename):
    file = open(filename)

    lines = [x.strip() for x in file]

    info = lines[0]
    mode = int(info[5])
    variation = int(info[17])

    numrounds = int((len(lines) - 2)/17)

    rounds = []

    for i in range(numrounds):
        tricks = []
        for j in range(13):
            line = lines[4+j+i*17]
            start = int(line[0])
            cardsplayed = str_to_cards_list(line[2:])
            dict = {
                "start": start,
                "cards": cardsplayed
            }
            tricks.append(dict)

        hand = str_to_cards_list(lines[2 + i * 17][6:])
        bidstring = lines[3 + i * 17][5:]
        bid = [int(x) for x in bidstring.split(",")]
        trickstakenstring = lines[(i+1) * 17][7:]
        trickstaken = [int(x) for x in trickstakenstring.split(",")]
        scorestring = lines[(i+1) * 17 + 1][6:]
        score = [int(x) for x in scorestring.split(",")]

        dict = {
            "cards": hand,
            "bids": bid,
            "tricks": tricks,
            "trickstaken": trickstaken,
            "score": score
        }
        rounds.append(dict)

    dict = {
        "mode": mode,
        "variation": variation,
        "rounds": rounds
    }

    # print(dict)
    return dict

