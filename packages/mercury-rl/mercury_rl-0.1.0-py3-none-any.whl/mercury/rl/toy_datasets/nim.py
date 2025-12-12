"""
This code generates the Minari dataset: Mercury/toy_datasets/nim_v1

You can adjust the following parameters (global constants):

  - RAND_SEED: Seed for random number generation to ensure reproducibility.
  - NUM_EPISODES: Number of game episodes to simulate and record.

You should only change the game constants and increase VERSION if you want to create a different dataset.

CHANGELOG:
  - VERSION	= 1: NUM_STACKS = 4, MAX_STONES = 10	# Generated 1000 episodes. (Wins: 423, Truncations: 213)
"""

import os

import numpy as np

from mercury.rl import RLDataset

RAND_SEED		= 2001
NUM_EPISODES	= 1000

NUM_STACKS		= 4
MAX_STONES		= 10

PLAYER_LEVEL	= [0.3, 0.5, 1.0]	# 30% of random players, 20% of "finishers", 50% of perfect players
RAND_UNCHECKED	= 0.25				# 20% of the random moves are not checked for validity

VERSION			= 1					# Generated 1000 episodes. (Wins: 423, Truncations: 213)


def new_board():
	while True:
		a = np.random.randint(0, MAX_STONES + 1, size = NUM_STACKS)
		if sum(a != 0) > 1:
			return a


def random_player(obs, no_error = False):
	rnd = np.random.random()
	if rnd < RAND_UNCHECKED and not no_error:
		i = np.random.randint(0, NUM_STACKS)
		v = np.random.randint(1, MAX_STONES + 1)

		return i, v

	ii = np.where(obs > 0)
	i  = np.random.choice(ii[0])
	v  = np.random.randint(1, obs[i] + 1)

	return i, v


def finishing_player(obs):
	ones = sum(obs == 1)
	more = np.where(obs > 1)[0]

	if len(more) > 2:
		i = np.random.choice(more)
		v = np.random.randint(1, obs[i] + 1)

		return i, v								# Too complicated, play a legal random move

	if len(more) == 2:
		i = more[0]
		j = more[1]
		if obs[i] == obs[j]:
			if ones % 2 == 0:					# You lost
				return random_player(obs, True)
			else:								# You win
				i = np.random.choice(np.where(obs == 1)[0])
				return i, 1

		if obs[i] > obs[j]:
			i, j = j, i

		if ones % 2 == 1:						# Too hard for the finishing player (may be winnable like 4, 2, 1 or not like 3, 2, 1)
			return random_player(obs, True)

		return j, obs[j] - obs[i] 				# You win

	if len(more) == 1:
		if ones % 2 == 0:
			return more[0], obs[more[0]] - 1	# You win leaving an odd number of ones
		else:
			return more[0], obs[more[0]]		# You win leaving an odd number of ones

	i = np.random.choice(np.where(obs == 1)[0])
	return i, 1									# You only have a possible move (winning if you leave an even number of ones)


def perfect_player(obs):
	x = 0
	for s in obs.tolist():
		x ^= int(s)

	if x == 0:
		return random_player(obs, True)			# You lost ... against a perfect player.

	ones = sum(obs == 1)
	more = np.where(obs > 1)[0]

	if len(more) > 1:
		for i, n in enumerate(obs.tolist()):
			y = n ^ x
			if y < n:
				return i, n - y					# You win.

	if len(more) == 1:
		if ones % 2 == 0:
			return more[0], obs[more[0]] - 1	# You win leaving an odd number of ones
		else:
			return more[0], obs[more[0]]		# You win leaving an odd number of ones

	i = np.random.choice(np.where(obs == 1)[0])
	return i, 1									# You only have a possible move (and win, otherwise x would be 0)


def move(obs, action):
	next_obs = obs.copy()
	i, v = action

	if i < 0 or i >= NUM_STACKS or v < 1 or v > obs[i]:
		return obs, True

	next_obs[i] -= v

	return next_obs, False


def do_episode(fn):
	obs	   = new_board()
	rows   = []
	finish = 0
	reward = 0

	while True:
		rnd = np.random.random()
		if rnd < PLAYER_LEVEL[0]:
			action = random_player(obs)
		elif rnd < PLAYER_LEVEL[1]:
			action = finishing_player(obs)
		else:
			action = perfect_player(obs)

		next_obs, error = move(obs, action)
		pieces = sum(next_obs)
		if error or pieces < 2:
			finish = int(not error)
			reward = int(pieces == 1)
			rows.append((obs, action, reward, finish))
			break

		reward += 0.01
		rows.append((obs, action, reward, finish))

		next_action = finishing_player(next_obs)
		obs, error	= move(next_obs, next_action)

		assert not error

	rows.append((next_obs, None, None, None))

	col_names = ['obs_%i' % (i + 1) for i in range(NUM_STACKS)] + ['action_stack', 'action_num', 'reward', 'finished']

	with open(fn, 'w') as f:
		f.write(','.join(col_names) + '\n')

		for obs, act, rew, fin in rows:
			o = ','.join(str(i) for i in obs)

			if act is not None:
				a = '%i,%i' % act
			else:
				a = ','

			if rew is not None:
				r = str(rew)
			else:
				r = ''

			if fin is not None:
				g = str(fin)
			else:
				g = ''

			f.write('%s,%s,%s,%s\n' % (o, a, r, g))

	return reward, finish


def	create_nim_dataset():
	np.random.seed(RAND_SEED)

	path = '%s/episodes' % os.path.dirname(os.path.abspath(__file__))

	os.makedirs(path, exist_ok = True)

	path += '/nim_%04i.csv'

	data = []
	args = {'author': 'mercury-team @ BBVA',
		 	'author_email': 'mercury.group@bbva.com',
			'algorithm_name': 'Synthetic Nim games (See nim.py in mercury-RL repository.)'}

	win	  = 0
	trunc = 0

	for i in range(NUM_EPISODES):
		fn = path % (i + 1)

		reward, finish = do_episode(fn)

		win	  += reward
		trunc += int(finish == 0)

		data.append(fn)

	print('Generated %i episodes. (Wins: %i, Truncations: %i)' % (NUM_EPISODES, win, trunc))

	mb = RLDataset()

	minari = mb.build(name = 'Mercury/toy_datasets/nim-v%i' % VERSION, data = data, args = args)

	assert mb.audit_dataset(minari, verbose = True) == 0

	print('Dataset: %s was added to Minari datasets.' % minari.id)
	print('   path: %s' % str(minari.storage.data_path))
	print('   removing episodes: ...', end = '')

	for fn in data:
		os.remove(fn)

	print('Ok.')


if __name__ == '__main__':
	create_nim_dataset()
