from rl.env import SpadesEnv
from rl.estimator import Estimator
from rl.memory import Memory

UPDATE_FREQ: int = 5  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10  # update target network every x rounds
NUM_ROUNDS: int = 10000
MIN_EXP: int = 1000  # min number of observations in memory to start training
BATCH_SIZE = 10
HIDDEN_LAYERS = [128, 128, 128]

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

def play_phase():
    """
    This is the phase where the model interacts with the environment to get data for the replay buffer
    Here, the model IS NOT trained -> it's used to just

    Likely use e-greedy method
    :return:
    """

    # TODO: implement psuedocode
    # Update epsilon
    # if random < epsilon
        # calculate q-values for state by passing in state to net
        # choose action based on BEST Q value
    # else
        # choose random value

    # store transition (cur state, action, reward, next state)

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
    # collect data
    play_phase()

    # learning phase
    if mem.size() > MIN_EXP:
        if episode % UPDATE_FREQ == 0:
            learn_phase()

        # update target network
        if episode % T_UPDATE_FREQ == 0:
            target.copy_weights(qnet)