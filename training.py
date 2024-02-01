from rl.memory import Memory
from rl.memory import Transition

UPDATE_FREQ: int = 5 # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10 # update target network every x rounds
NUM_ROUNDS: int = 10000
MIN_EXP: int = 1000 # min number of observations in memory to start training
BATCH_SIZE = 10

mem = Memory(memory_size=10000, batch_size=BATCH_SIZE)

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
    loss_val = 0

    sample = mem.sample()

    obs: Transition
    for obs in sample:
        # TODO: implement psuedocode
        # get list of q_vals from network at current time
        # get specific q_val for the action

        # if done
            # reward = given reward
        # else
            # get list of q_vals from TARGET network at time + 1
            # get best action based on those values
            # determine next q_value (max of action values returned from TARGET network)

            # reward = reward + scalar * next q-value (future rewards play a little role)

        # add reward to get target_value
        pass
    # compute total loss (returned Q-value for the action compared to calculated Q value)

    # calculate average loss
    mean_loss_val = loss_val / BATCH_SIZE

    # TODO: update model with loss (use optimizer -> backwards propagation)


for episode in range(10000):
    # collect data
    play_phase()

    # learning phase
    if mem.size() > MIN_EXP:
        if episode % UPDATE_FREQ == 0:
            learn_phase()

        # update target network
        if episode % T_UPDATE_FREQ == 0:
            # TODO: update target network (copy weights)
            pass

    pass