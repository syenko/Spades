from gameplay import bidding
from gameplay.actions import PlayCardAction, BidAction
from gameplay.game import Game
from gameplay.playing import Playing
from gameplay.reward import reward_function

game = Game(6, 500)

players = game.players
playing = [Playing(game, players[0]), Playing(game, players[1]), Playing(game, players[2]), Playing(game, players[3])]

for i in range(4):
    game.step(BidAction(bidding.bid_partial(players[i].hand.hand)))
    print("Player: " + str(i) + " Bid: " + str(bidding.bid_partial(players[i].hand.hand)))

modelindex = 0  # hardcoded
bid = bidding.bid_partial(players[modelindex].hand.hand) + bidding.bid_partial(players[(modelindex+2)%4].hand.hand) # hardcoding model bid
totalreward = 0

player = 0
eventotal = 0
oddtotal = 0
for i in range(6):
    print("ROUND NUMBER: " + str(i))
    print("STARTING PLAYER: " + str(player))
    for j in range(4):
        move = playing[player].play()
        print(move)
        # print(players[player].hand.cards)
        player = game.step(PlayCardAction(move))
    for j in range(4):
        playing[j].update()

    if player % 2 == 0:
        eventotal += 1
    else:
        oddtotal += 1

    totalreward += reward_function(game, modelindex)
    print("REWARD: " + str(totalreward))

    print("TOTAL SCORES: EVEN " + str(eventotal) + ", ODD " + str(oddtotal))
