import os

import numpy as np


RAND_SEED		= 2001
NUM_STEPS		= 10000

NUM_STACKS		= 4
MAX_STONES		= 10



def new_board():
	while True:
		a = np.random.randint(0, MAX_STONES + 1, size = NUM_STACKS)
		if sum(a != 0) > 1:
			return a


def random_player(obs):
	ii = np.where(obs > 0)
	i  = np.random.choice(ii[0])
	v  = np.random.randint(1, obs[i] + 1)

	return i, v


def perfect_player(obs):
	x = 0
	for s in obs.tolist():
		x ^= int(s)

	assert x != 0

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


def move(obs, action):
	next_obs = obs.copy()
	i, v = action

	assert i >= 0 and i < NUM_STACKS and v > 0 and v <= obs[i]

	next_obs[i] -= v

	return next_obs, False


def do_dataset(fn):

	col_names = ['obs_%i' % (i + 1) for i in range(NUM_STACKS)] + ['action_stack', 'action_num']

	with open(fn, 'w') as f:
		f.write(','.join(col_names) + '\n')

		n	  = 0
		games = 0
		error = False
		step  = 0
		while step < NUM_STEPS:
			if n == 0:
				obs = new_board()
				games += 1
			else:
				obs, error = move(obs, opponent_action)

			assert not error

			x = 0
			for s in obs.tolist():
				x ^= int(s)

			if x == 0:
				n = 0
				continue

			action = perfect_player(obs)

			o = ','.join(str(i) for i in obs)
			a = '%i,%i' % action

			f.write('%s,%s\n' % (o, a))

			step += 1

			obs, error = move(obs, action)

			n += 1

			assert not error

			if sum(obs) == 1:
				n = 0
			else:
				opponent_action = random_player(obs)

	return games


def create_nim_supervised_dataset(only_if_not_exists = True):
	np.random.seed(RAND_SEED)

	path = '%s/supervised' % os.path.dirname(os.path.abspath(__file__))

	os.makedirs(path, exist_ok = True)
	fn = '%s/nim_%d_%d_%d.csv' % (path, NUM_STACKS, MAX_STONES, NUM_STEPS)

	if only_if_not_exists and os.path.exists(fn):
		print('File %s already exists, not regenerating.' % fn)

		return fn

	num_games = do_dataset(fn)

	print('Generated %i games, %i steps in file %s' % (num_games, NUM_STEPS, fn))

	print('Ok.')

	return fn


if __name__ == '__main__':
	create_nim_supervised_dataset()
