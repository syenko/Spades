from rl.env import SpadesEnv
from rl.estimator import Estimator
from rl.memory import Memory
import numpy as np

UPDATE_FREQ: int = 5  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10  # update target network every x rounds
NUM_ROUNDS: int = 10000
MIN_EXP: int = 1000  # min number of observations in memory to start training
BATCH_SIZE: int = 10
HIDDEN_LAYERS: [int] = [128, 128, 128]
EPS_START: float = 1.0
EPS_END: float = 0.1
EPS_DECAY = 0.1

env = SpadesEnv()
mem = Memory(memory_size=10000, batch_size=BATCH_SIZE)
qnet = Estimator(
    state_shape_size=env.get_state_shape_size(),
    num_actions=env.get_num_actions(),
    hidden_layers=HIDDEN_LAYERS
)
target = Estimator(
    state_shape_size=env.get_state_shape_size(),
    num_actions=env.get_num_actions(),
    hidden_layers=HIDDEN_LAYERS
)
epsilon: int = EPS_START
epsilon_decay_step = 0
state: [int] = []
action: int = 0
reward: int = 0
next_state: [int] = []
done: bool = False
legal_actions: [bool] = []

def play_phase():
    """
    This is the phase where the model interacts with the environment to get data for the replay buffer
    Here, the model IS NOT trained -> it's used to just

    Likely use e-greedy method
    :return:
    """
    global epsilon, state, action, legal_actions

    # Update epsilon
    epsilon = EPS_END + (EPS_START - EPS_END) * np.exp(epsilon_decay_step * -EPS_DECAY)

    # TODO: implement psuedocode
    best_action: int
    # explore
    if np.random.rand() < epsilon:
        # choose random value
        probabilities = np.full(len(legal_actions), 1 / np.sum(legal_actions))
        probabilities[np.logical_not(legal_actions)] = 0  # mask illegal actions (0 probability)
        best_action = np.random.choice([x for x in range(0, len(legal_actions))], p=probabilities)
    # exploit
    else:
        q_vals = qnet.predict_nograd(states=state)
        best_action: int = np.argmax(q_vals)[0]

    next_state, reward, terminated, truncated, legal_actions = env.step(best_action)

    # store transition (cur state, action, reward, next state)
    mem.save(state, action, reward, next_state, terminated)

    return

def learn_phase():
    states, actions, rewards, next_states, dones = mem.sample()
    loss = qnet.update(
        states,
        actions,
        target.tar_get_rewards(next_states, rewards, dones)
    )
    print(f"Loss is: {loss}")

for episode in range(10000):

    state, legal_actions = env.reset()

    while not done:
        # collect data
        play_phase()

        # learning phase
        if mem.size() > MIN_EXP:
            if episode % UPDATE_FREQ == 0:
                learn_phase()

            # update target network
            if episode % T_UPDATE_FREQ == 0:
                target.copy_weights(qnet)