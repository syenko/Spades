from gameplay import gameutilities


def reward(game, modelindex):
    cards_played = game.round.get_trick_moves()
    partnerindex = (modelindex + 2) % 4
    trickstaken = game.round.tricks_won[modelindex] + game.round.tricks_won[partnerindex]
    bid = game.round.bids[modelindex] + game.round.bids[partnerindex]
    winning_player, winning_card = gameutilities.winning_trick(cards_played)

    rewardtotal = 0

    if game.round.is_over(): # if game is over
        if trickstaken < bid: # if you got set
            rewardtotal -= 500
        elif trickstaken == bid: # if you made perfect
            rewardtotal += 10

    if winning_player == modelindex or winning_player == partnerindex: # if winner is you or partner
        if trickstaken > bid: # if overtrick
            rewardtotal -= 5
        else:
            rewardtotal += 5

    return rewardtotal
