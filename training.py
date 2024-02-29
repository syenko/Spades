import torch

from rl.env import SpadesEnv
from rl.estimator import Estimator
from rl.memory import Memory
import numpy as np
import logging
from tqdm import tqdm
from matplotlib import pyplot as plt
from pathlib import Path
from datetime import datetime

logging.basicConfig(format='(%(levelname)s) %(message)s', level=logging.WARNING)

curtime = datetime.now()

PATH = f"data_analysis/training_data/{curtime.month}_{curtime.day}__{curtime.hour}_{curtime.minute}_{curtime.second}"

UPDATE_FREQ: int = 6  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 10000  # update target network every x rounds
NUM_ROUNDS: int = 1000000
BUFFER_SIZE: int = 50000  # max size of memory buffer
MIN_EXP: int = BUFFER_SIZE - 1  # min number of observations in memory to start training
BATCH_SIZE: int = 1000
HIDDEN_LAYERS: [int] = [256, 256, 256]
EPS_START: float = 1.0
EPS_END: float = 0.01
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
target = Estimator(
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
    This is the phase where the model interacts with the environment to get data for the replay buffer
    Here, the model IS NOT trained -> it's used to just

    Likely use e-greedy method
    :return:
    """
    global epsilon, state, action, legal_actions, next_state, reward, done, epsilon_decay_step

    # Update epsilon
    epsilon = epsilon * EPS_DECAY
    epsilon_decay_step += 1
    epsilons_log.append(epsilon)

    best_action: int
    # explore
    if np.random.rand() < epsilon:
        logging.debug(f"Agent explores")
        # choose random value
        probabilities = np.full(len(legal_actions), 1 / np.sum(legal_actions))
        # logging.debug(f"probabilities: {probabilities}")
        # logging.debug(f"legal actions: {legal_actions}")
        probabilities[np.logical_not(legal_actions)] = 0  # mask illegal actions (0 probability)
        # logging.debug(f"masked probabilities: {probabilities}")
        best_action = np.random.choice([x for x in range(0, len(legal_actions))], p=probabilities)
    # exploit
    else:
        logging.debug(f"Agent exploits")
        q_vals = qnet.predict_nograd(states=state, legal_actions=legal_actions)
        best_action: int = int(torch.argmax(q_vals).item())
        # logging.warning(f"best action: {best_action}, {q_vals}, {legal_actions}")
        assert (legal_actions[best_action] == 1)

    next_state, reward, terminated, truncated, legal_actions = env.step(best_action)

    # store transition (cur state, action, reward, next state)
    mem.save(state, action, reward, next_state, terminated, legal_actions)

    done = terminated

    return


def learn_phase():
    states, actions, rewards, next_states, dones, legal_actions = mem.sample()
    loss, batch_reward = qnet.update(
        states,
        actions,
        target.tar_get_rewards(next_states, legal_actions, rewards, dones)
    )
    # print(f"Loss is: {loss}")
    return loss, batch_reward


for episode in tqdm(range(NUM_ROUNDS)):
    logging.info(f"Episode #{episode} =================")

    if done:
        state, legal_actions = env.reset()
        done = False

    # collect data
    play_phase()

    # learning phase
    if mem.size() > MIN_EXP:
        if episode % UPDATE_FREQ == 0:
            batch_loss, batch_reward = learn_phase()
            loss.append([episode, batch_loss])
            reward_log.append([episode, batch_reward])

        # update target network
        if episode % T_UPDATE_FREQ == 0:
            logging.warning(f"Updated Target Net")
            target.copy_weights(qnet)

        if episode % 1000 == 0 and len(loss) > 1000:
            logging.warning(f"Average Loss: {sum(loss[-1000])/1000}")
            logging.warning(f"Average Reward: {sum(reward_log[-1000])/1000}")

    env.log_scores()

# save data
out = Path(f"{PATH}/info.txt")
out.parent.mkdir(exist_ok=True, parents=True)
out.write_text(f"""
UPDATE_FREQ: int = {UPDATE_FREQ}  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = {T_UPDATE_FREQ} # update target network every x rounds
NUM_ROUNDS: int = {NUM_ROUNDS} 
BUFFER_SIZE: int = {BUFFER_SIZE}  # max size of memory buffer
MIN_EXP: int = {MIN_EXP}  # min number of observations in memory to start training
BATCH_SIZE: int = {BATCH_SIZE}
HIDDEN_LAYERS: [int] = {HIDDEN_LAYERS}
EPS_START: float = {EPS_START} 
EPS_END: float = {EPS_END} 
EPS_DECAY = {EPS_DECAY}
LEARNING_RATE = {LEARNING_RATE}
""")
np.savetxt(f"{PATH}/loss_out.csv", np.asarray(loss), delimiter=",")
np.savetxt(f"{PATH}/reward_out.csv", np.asarray(reward_log), delimiter=",")

# plots
figure, axis = plt.subplots(3, 1, figsize=(5, 15))

axis[0].plot([x for x, y in loss], [y for x, y in loss])
axis[0].set_title("Loss")

axis[1].plot([x for x, y in reward_log], [y for x, y in reward_log])
axis[1].set_title("Reward")

axis[2].plot(epsilons_log)
axis[2].set_title("Epsilon")
plt.show()
