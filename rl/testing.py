import torch
import numpy as np
from tqdm import tqdm

from rl.env import SpadesEnv
from rl.estimator import Estimator
from rl.memory import Memory

# Constants -----
UPDATE_FREQ: int = 1  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10000  # update target network every x rounds
NUM_ROUNDS: int = 1000000
BUFFER_SIZE: int = 50000  # max size of memory buffer
MIN_EXP: int = BUFFER_SIZE - 1  # min number of observations in memory to start training
BATCH_SIZE: int = 256
HIDDEN_LAYERS: [int] = [256, 256, 256]
EPS_START: float = 1.0
EPS_END: float = 0.001
EPS_DECAY = (EPS_END/EPS_START)**(1/NUM_ROUNDS)
LEARNING_RATE = 0.001

env = SpadesEnv()
mem = Memory(memory_size=BUFFER_SIZE, batch_size=BATCH_SIZE)
qnet = Estimator(
    state_shape_size=env.get_state_shape_size(),
    num_actions=env.get_num_actions(),
    hidden_layers=HIDDEN_LAYERS,
    learning_rate=LEARNING_RATE
)

loss = []
reward_log = []

epsilon: int = EPS_START
epsilon_decay_step = 0
state: [int] = []
action: int = 0
reward: int = 0
next_state: [int] = []
done: bool = True
legal_actions: [bool] = []

epsilons_log = []

def play_phase():
    """
    Sample from env
    :return:
    """
    global epsilon, state, action, legal_actions, next_state, reward, done, epsilon_decay_step

    best_action: int
    # explore
    # choose random value
    probabilities = np.full(len(legal_actions), 1 / np.sum(legal_actions))
    probabilities[np.logical_not(legal_actions)] = 0  # mask illegal actions (0 probability)
    best_action = np.random.choice([x for x in range(0, len(legal_actions))], p=probabilities)

    next_state, reward, terminated, truncated, legal_actions = env.step(best_action)

    # store transition (cur state, action, reward, next state)
    mem.save(state, action, reward, next_state, terminated, legal_actions)

    done = terminated


for episode in tqdm(range(NUM_ROUNDS)):
    if done:
        state, legal_actions = env.reset()
        done = False

    # collect data
    play_phase()

batch = [mem.sample(10)]

print(batch)

assert_vars_change(
    model=qnet.qnet,
    optim=qnet.optimizer,
    loss_fn=qnet.loss,
    batch=batch
)
