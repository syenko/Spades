from rl.memory import Memory

UPDATE_FREQ: int = 5 # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10 # update target network every x rounds
NUM_ROUNDS: int = 10000
MIN_MEMORY: int = 0 # min number of observations in memory to start training
BATCH_SIZE = 10

mem = Memory(memory_size=10000, batch_size=BATCH_SIZE)


for episode in range(10000):
    # collect data



    # learning phase
    if mem.size() > MIN_MEMORY and episode % UPDATE_FREQ == 0:
        loss_val = 0

        sample = mem.sample()

        for obs in sample:
            # TODO: fill in psuedocode
            # get list of q_vals from network at current time
            # get specific q_val for the action

            # get list of q_vals from TARGET network at time + 1
            # get best action based on those values
            # determine next q_value

            # add reward to get target_value

            # computer loss
            pass

        mean_loss_val = loss_val / BATCH_SIZE
        # TODO: update model with loss

    # update target network
    if episode % T_UPDATE_FREQ == 0:
        # TODO: update target network (copy weights)
        pass

    pass
