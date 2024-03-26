from gameplay import gameutilities

MAX_REWARD = 50

def reward_function(game, modelindex):
    cards_played = game.round.get_trick_moves()
    partnerindex = (modelindex + 2) % 4
    trickstaken = game.round.tricks_won[modelindex] + game.round.tricks_won[partnerindex]
    bid = game.round.bids[modelindex] + game.round.bids[partnerindex]
    winning_player, winning_card = gameutilities.winning_trick(cards_played)

    rewardtotal = 0

    if game.round.is_over():  # if game is over
        if trickstaken < bid:  # if you got set
            rewardtotal -= 50
        elif trickstaken == bid:  # if you made perfect
            rewardtotal += 10

        total_score = game.get_total_score()
        # won
        if total_score[modelindex % 2] > total_score[(modelindex + 1) % 2]:
            rewardtotal += 50
        # loss
        if total_score[modelindex % 2] < total_score[(modelindex + 1) % 2]:
            rewardtotal -= 50

    if winning_player == modelindex or winning_player == partnerindex:  # if winner is you or partner
        if trickstaken > bid:  # if overtrick
            rewardtotal -= 5
        else:
            rewardtotal += 5
    else: # if you didn't win
        if trickstaken < bid:  # need more tricks
            rewardtotal -= 5
        else: # don't need more tricks
            rewardtotal += 5

    return rewardtotal / MAX_REWARD
