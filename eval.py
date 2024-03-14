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

FOLDER = "3_7__20_29_10"
MODEL_PATH = f"data_analysis/training_data/{FOLDER}"
PATH = f"data_analysis/training_data/{FOLDER}/random"

UPDATE_FREQ: int = 1  # update every x rounds (need to test what works best)
T_UPDATE_FREQ: int = UPDATE_FREQ * 100000  # update target network every x rounds
NUM_ROUNDS: int = 600000
BUFFER_SIZE: int = 25000  # max size of memory buffer
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
ep_reward: int = 0
next_state: [int] = []
done: bool = True
legal_actions: [bool] = []

epsilons_log = []

num_games = 0
games_won = 0
scores_log = []

def play_phase():
    """
    This is the phase where the model interacts with the environment to get data for the replay buffer
    Here, the model IS NOT trained -> it's used to just

    Likely use e-greedy method
    :return:
    """
    global epsilon, state, action, legal_actions, next_state, reward, ep_reward, done, epsilon_decay_step

    logging.debug(f"Agent exploits")
    q_vals = qnet.predict_nograd(states=state, legal_actions=legal_actions)
    best_action: int = int(torch.argmax(q_vals).item())
    # logging.warning(f"best action: {best_action}, {q_vals}, {legal_actions}")
    assert (legal_actions[best_action] == 1)

    next_state, reward, terminated, truncated, legal_actions = env.step(best_action)

    done = terminated
    ep_reward += reward

    return

def play_random():
    global epsilon, state, action, legal_actions, next_state, reward, ep_reward, done, epsilon_decay_step

    logging.debug(f"Agent explores")
    probabilities = np.full(len(legal_actions), 1 / np.sum(legal_actions))
    probabilities[np.logical_not(legal_actions)] = 0  # mask illegal actions (0 probability)
    best_action = np.random.choice([x for x in range(0, len(legal_actions))], p=probabilities)

    next_state, reward, terminated, truncated, legal_actions = env.step(best_action)

    done = terminated
    ep_reward += reward

qnet.load_weights(f"{MODEL_PATH}/checkpoint.pt")

for episode in tqdm(range(NUM_ROUNDS)):
    logging.info(f"Episode #{episode} =================")

    if done:
        env.log_scores()
        scores = env.get_scores()
        scores_log.append([episode, scores[0], scores[1]])
        if scores[0] > scores[1]:
            games_won += 1
        num_games += 1
        reward_log.append([episode, ep_reward])
        ep_reward = 0
        state, legal_actions = env.reset()
        done = False

    # collect data
    play_random()


# save data
out = Path(f"{PATH}/stats.txt")
out.parent.mkdir(exist_ok=True, parents=True)
out.write_text(f"""
NUM_GAMES: {num_games}, 
GAMES_WON: {games_won},
""")
np.savetxt(f"{PATH}/eval_reward_out.csv", np.asarray(reward_log), delimiter=",")
np.savetxt(f"{PATH}/scores.csv", np.asarray(scores_log), delimiter=",")

# plots
figure, axis = plt.subplots(3, 1, figsize=(5, 15))

axis[0].plot([x for x, y in loss], [y for x, y in loss])
axis[0].set_title("Loss")

axis[1].plot([x for x, y in reward_log], [y for x, y in reward_log])
axis[1].set_title("Reward")

axis[2].plot(epsilons_log)
axis[2].set_title("Epsilon")
plt.show()
