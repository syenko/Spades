import torch
import torch.nn as nn


class Estimator:
    def __init__(
            self,
            state_shape_size: int,
            num_actions: int,
            hidden_layers: [int],
            learning_rate: int,
            discount_factor: float
    ):
        self.qnet = EstimatorNetwork(state_shape_size, num_actions, hidden_layers)

        self.optimizer = torch.optim.Adam(self.qnet.parameters(), learning_rate)
        self.loss = torch.nn.MSELoss(reduction='sum')
        self.discount_factor = discount_factor

    def predict_nograd(self, states):
        """
        Used to generate target values and for prediction
        Calculates q-values WITHOUT training

        :param states: Batch of states
        :return: q-value for specific state or STATES
        """
        with torch.no_grad():
            return self.qnet(states)

    def tar_get_rewards(self, next_states, rewards: [int], done: [bool]):
        """
        Used for target network to calculate rewards for a batch of states

        :param next_states: a list of states
        :param rewards: a list of rewards
        :param done: a boolean list of whether each state finished
        :return: rewards adjusted by network's prediction
        """

        next_q_values = self.predict_nograd(next_states).max()

        # if there is no next state, set all extra predictions from the model to zero
        # reward is just the final reward (don't predict future rewards, because there ARE no future rewards)
        next_q_values[done] = 0

        final_rewards = rewards + self.discount_factor * next_q_values

        return final_rewards

    def update(self, states, actions, rewards):
        """
        Updates the q-network (used for normal q-network)

        :param states: (s) a batch of states
        :param actions: (a) a batch of actions
        :param rewards: (y) a batch rewards calculated from BOTH the given rewards and target network outputs
        :return:
        """
        self.optimizer.zero_grad()  # zeroes the gradient

        self.qnet.train()  # sets up network for training (not really necessary but helpful)

        # for each state, calculate the q-vals
        # returns an array with dimensions [batch_size][num_actions]
        q_vals = self.qnet.forward(states)

        # convert general q_vals (all q-values for ALL actions) to Q-value for SPECIFIC action
        # good explanation of what torch.gather does:
        #   https://stackoverflow.com/questions/50999977/what-does-the-gather-function-do-in-pytorch-in-layman-terms
        # dimension = -1 means LAST dimension (because 1st dimension would be the batches)
        Q = torch.gather(q_vals, dim=-1, index=actions)

        # calculate loss
        batch_loss = self.loss(Q, rewards)

        # update model
        batch_loss.backward()
        self.optimizer.step()

        # sets up network for evaluation (not really necessary but probably safer)
        self.qnet.eval()

        # returns loss as a float
        return batch_loss.item()


class EstimatorNetwork(nn.Module):
    """
    Based on RLCard DQN implementation
    https://github.com/datamllab/rlcard/blob/master/rlcard/agents/dqn_agent.py#L413

    Fully connected neural net with ReLU activation functions
    Input: State
    Output: Actions
    """
    def __init__(self, state_shape_size: int, num_actions: int, hidden_layers: [int]):
        """
        :param state_shape_size: state shape size
        :param num_actions: number of actions
        :param hidden_layers: size of each of the hidden layers
        """
        self.state_shape_size = state_shape_size
        self.num_actions = num_actions
        self.hidden_layers = hidden_layers

        nodes_per_layer = [self.state_shape] + hidden_layers

        network = []
        for i in range(len(nodes_per_layer) - 1):
            network.append(nn.Linear(nodes_per_layer[i], nodes_per_layer[i + 1]))
            network.append(nn.ReLU())

        network.append(nn.Linear(nodes_per_layer[-1], num_actions))

        self.model = nn.Sequential(*network)

    def forward(self, x):
        """
        Passes an input tensor through the net

        :param x: the input tensor
        :return: output of the model
        """
        return self.model(x)
