"""
Memory for Experience Replay

Stores previous states / actions
"""
import random

class Memory:
    def __init__(self, memory_size, batch_size):
        """
        :param memory_size: Max number of experiences to be stored
        :param batch_size: Size of each batch
        """
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.memory = []

    def sample(self, k=-1):
        if k == -1:
            k = self.batch_size
        sample = random.sample(self.memory, k)

        # TODO: return the sample in some usable form (maybe want to split by stuff)
        return sample

    def save(self, state, action, reward, prev_state):
        if len(self.memory) == self.memory_size:
            self.memory.pop(0)

        self.memory.append((state, action, reward, prev_state))

    def size(self):
        return len(self.memory)