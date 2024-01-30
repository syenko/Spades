import torch
import torch.nn as nn

"""
Based on RLCard DQN implementation
https://github.com/datamllab/rlcard/blob/master/rlcard/agents/dqn_agent.py#L413

Fully connected neural net with ReLU activation functions
Input: State
Output: Actions
"""
class EstimatorNetwork(nn.Module):
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