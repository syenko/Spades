"""
Memory for Experience Replay

Stores previous states / actions
"""
import random
from collections import namedtuple

import numpy as np

Transition = namedtuple('Transition', ['state', 'action', 'reward', 'next_state', 'done', 'legal_actions'])

class Memory:
    def __init__(self, memory_size, batch_size):
        """
        :param memory_size: Max number of experiences to be stored
        :param batch_size: Size of each batch
        """
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.memory: [Transition] = []

    def sample(self, k=-1):
        if k == -1:
            k = self.batch_size
        sample = random.sample(self.memory, k)

        # turns sample into arrays by type (array of all sampled states, all sampled actions, all sampled rewards, etc)
        by_type = [list(g) for g in zip(*sample)]

        return by_type

    def save(self, state, action, reward, next_state, done, legal_action):
        if len(self.memory) == self.memory_size:
            self.memory.pop(0)
        t = Transition(state, action, reward, next_state, done, legal_action)
        self.memory.append(t)

    def size(self):
        return len(self.memory)

# Testing memory
# mem = Memory(100, 10)
# for i in range(100):
#     mem.save(
#         random.randint(0, 10),
#         random.randint(10, 20),
#         random.randint(20, 30),
#         random.randint(30, 40),
#         random.randint(40, 50)
#     )
#
# print(mem.sample())