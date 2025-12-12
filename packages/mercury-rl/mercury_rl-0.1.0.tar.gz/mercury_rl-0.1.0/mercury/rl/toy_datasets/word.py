"""
This code generates the Minari dataset: Mercury/toy_datasets/word_v1

You can adjust the following parameters (global constants):

  - RAND_SEED: Seed for random number generation to ensure reproducibility.
  - NUM_EPISODES: Number of game episodes to simulate and record.

You should only change the game constants and VERSION if you want to create a different dataset.
"""

import os

import numpy as np

from mercury.rl import RLDataset

RAND_SEED		= 2001
NUM_EPISODES	= 250


VERSION			= 1


def do_episode(fn):
	with open(fn, 'w') as f:
		f.write('obs_a,obs_b,obs_c,action_guess,reward,finished\n')
		f.write('1,1,2,1,0.1,0\n')
		f.write('-12,100,1,3,0.2,1\n')
		f.write('2,150,3\n')


def create_word_dataset():
	np.random.seed(RAND_SEED)

	path = '%s/episodes' % os.path.dirname(os.path.abspath(__file__))

	os.makedirs(path, exist_ok = True)

	path += '/word_%04i.csv'

	data = []
	args = {'author': 'mercury-team @ BBVA',
		 	'author_email': 'mercury.group@bbva.com',
			'algorithm_name': 'Synthetic Word game (See word.py in mercury-RL repository.)'}

	for i in range(NUM_EPISODES):
		fn = path % (i + 1)

		do_episode(fn)

		data.append(fn)

	mb = RLDataset()
	minari = mb.build(name = 'Mercury/toy_datasets/word-v%i' % VERSION, data = data, args = args)

	assert mb.audit_dataset(minari, verbose = True) == 0

	print('Dataset: %s was added to Minari datasets.' % minari.id)
	print('   path: %s' % str(minari.storage.data_path))
	print('   removing episodes: ...', end = '')

	for fn in data:
		os.remove(fn)

	print('Ok.')


if __name__ == '__main__':
	create_word_dataset()
