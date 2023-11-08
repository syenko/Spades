from gameplay.card import Card
from gameplay.constants import Suit


def str_value_to_num_value(value: str) -> int:
    cards_in_order = "23456789tjqka"
    return cards_in_order.index(value.lower())


def str_to_cards_list(card_str: str) -> list[Card]:
    cards = [
        Card(Suit(int(card_str[i])), str_value_to_num_value(card_str[i + 1])) for i in range(0,len(card_str) - 2, 2)
    ]
    return cards

test_str = "1J24262Q2A3438050608090T0K1317191T1Q1K27293335373903141522282J2K32363J040J0Q0A1216181A23252T3T3Q3K3A0207"

for card in str_to_cards_list(test_str):
    print(card)