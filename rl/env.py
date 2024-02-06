import gymnasium as gym
import numpy as np

from gameplay.actions import Action
from gameplay.constants import Phase, MAX_NUM_CARDS
from gameplay.game import Game


class SpadesEnv(gym.Env):

    def __init__(self, max_rounds=10, winning_score=500):
        self.game = Game(max_rounds, winning_score)
        pass

    # returns (observation, reward, terminated, truncated, info: list of legalactions)
    def step(self, action: int) -> tuple[list[int], int, bool, bool, list[int]]:
        self.game.step(Action.get_action_from_id(action))

        state = self.extract_state()
        observation: list[int] = state['obs']
        legal_actions: list[int] = state['legal_actions']

        return observation, 0, self.game.is_over(), False, legal_actions

    # returns (observation, info: list of legal actions)
    def reset(self, seed=None, options=None) -> tuple[list[int], list[int]]:
        self.game.reset()

        state = self.extract_state()
        observation: list[int] = state['obs']
        legal_actions: list[int] = state['legal_actions']

        return observation, legal_actions

    def close(self):
        pass

    # returns the state in numerical form
    def extract_state(self) -> dict:
        extracted_state = {}

        cur_round = self.game.round
        cur_player = self.game.round.get_current_player()

        # bidding phase?
        is_bidding_rep = np.array([1] if cur_round.phase == Phase.BIDDING else [0])

        # current bids
        bids_rep = np.array(cur_round.bids)

        # which cards are in my hand
        cards_in_hand_rep = np.zeros(MAX_NUM_CARDS)
        for card in cur_player.hand.cards:
            cards_in_hand_rep[card.get_id()] = 1

        # which cards have been played and by whom
        cards_played_rep = np.zeros(MAX_NUM_CARDS * 4)
        for move in cur_round.card_move_log:
            cards_played_rep[move.card.get_id() + move.player.position * MAX_NUM_CARDS] = 1

        # which cards have been played in this trick and by whom
        trick_cards_played_rep = np.zeros(MAX_NUM_CARDS * 4)
        for move in cur_round.get_trick_moves():
            trick_cards_played_rep[move.card.get_id() + move.player.position * MAX_NUM_CARDS] = 1

        # number of tricks taken by each player
        tricks_taken_rep = np.zeros(4)
        for player in cur_round.players:
            tricks_taken_rep[player.position] = player.tricks_taken

        spades_broken_rep = np.array([1] if cur_round.spades_broken else [0])
        round_number_rep = np.array([self.game.round])

        rep = []
        rep.append(is_bidding_rep)
        rep.append(bids_rep)
        rep.append(cards_in_hand_rep)
        rep.append(cards_played_rep)
        rep.append(trick_cards_played_rep)
        rep.append(tricks_taken_rep)
        rep.append(spades_broken_rep)
        rep.append(round_number_rep)

        obs = np.concatenate(rep)

        legal_actions = np.zeros(Action.get_num_actions())
        for action in self.game.get_legal_actions():
            legal_actions[action.get_id()] = 1

        extracted_state['obs'] = obs
        extracted_state['legal_actions'] = legal_actions

        return extracted_state

    def get_state_shape_size(self) -> int:
        size = 0
        size += 1  # is bidding (1 if bidding, 0 if not)
        size += 4  # other player's bids (not 1 hot)

        size += MAX_NUM_CARDS  # cards in hand (1 if in hand, 0 if not in hand)
        # size += 3 * MAX_NUM_CARDS  # cards in all hands (if perfect information)

        size += 4 * MAX_NUM_CARDS  # cards played (including cards currently in play)
        size += 4 * MAX_NUM_CARDS  # cards played in the current trick

        size += 4  # tricks taken (not 1 hot)

        size += 1  # spades broken (1 if yes, 0 if no)
        size += 1  # round number (not 1 hot)
        # TODO: implement
        return size

    def get_num_actions(self):
        return Action.get_num_actions()

    def get_reward(self) -> int:
        # TODO: Implement
        return 0
