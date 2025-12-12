import warnings

import numpy as np

from minari.data_collector import EpisodeBuffer
from minari import create_dataset_from_buffers, delete_dataset, load_dataset
from gymnasium.spaces import Box


from .episodes import Episodes


class RLDataset:
	"""
	This class creates, audits and implements some utilities to manage **episodic** datasets used in RL models.
	The whole system (RLDataset, ModelCreator and OfflineTrainer) constitutes the core of an offline RL framework.
	You can create datasets from any source (CSV files, Pandas DataFrames, Numpy arrays, Spark DataFrames, etc.)
	with a well-defined episodic structure and the datasets become Minari datasets, but using just a subset of all
	the possible Minari options since Minari supports online environments and more complex data and metadata structures.
	Validating that your episodic datasets conform to the standard is what the `audit_dataset()` method does.

	Arguments:
	----------
		id: (optional) An optional minari dataset id (string). In case it is given to the constructor, the class behaves as a
	lazy loader for that dataset. The dataset is only loaded when the `data` property is accessed for the first time. When the `build()`
	method is used to create a new dataset, the `id` and `data` properties are those of the last built dataset.


	Episodic datasets reference
	===========================

	Minari Dataset Overview
	-----------------------

	A Minari dataset is a standardized offline reinforcement learning (RL) dataset
	format developed by the Farama Foundation (the maintainers of Gymnasium, Minari, etc.).
	Its purpose is to make RL datasets easy to share, reproduce, and consume across
	different research projects and pipelines.

	Basic Terminology:
	------------------

	  - state: The true, complete description of the environment at a given point in time. May or may not be the same as an observation.
	  - observation: The information an agent receives about the environment at a given timestep. (What the agent has access to.)
	  - action: A decision made by the agent that affects the environment.
	  - reward: A scalar feedback signal indicating the immediate value of an action taken as defined by the environment designer.
	  - timestep: A single step (state, action) -> (next state, reward) transition. The agent takes an action based on the observation and
	receives a reward and signals indicating whether the episode ended. Possibly a next observation if the episode is not finished.
	  - episode: A sequence of timesteps from the initial that represents a complete interaction with the environment until termination or
	truncation. The initial state may be deterministic (always the same like an initial chess board) or stochastic.
	  - episode end: An episode ends when the environment says so. That may be either by termination (e.g. winning or losing a game) or
	truncation (e.g. reaching a time limit). The Last timestep of an episode has a reward which depends on the environment design, it
	could be a game won (+1) not seen before but that may be different across different datasets. The last timestep corresponds to the last
	action. There is the same number of actions, reward, termination, truncation as timesteps in an episode, but there is an additional
	observation. We can think of the last action as the decision that led to the episode to finish and the additional observation as
	the result of it.

	Constituents of a Minari Dataset
	--------------------------------

	A Minari dataset is more than just raw trajectories: it comes with structure and APIs to make offline RL research reproducible.

	How to Load a Dataset:
	----------------------

		>>> import minari
		>>> data = minari.load_dataset('D4RL/door/human-v2')

	This call returns a `MinariDataset` object that provides direct access to the dataset's contents and metadata.

	Main Constituents:
	------------------

	1. **Episodes and Timesteps**

		- `data` behaves like a sequence of episodes.
		- You can iterate through episodes:

			>>> episode = data[0]   # first episode

		- An `episode` object has five fundamental properties:

		* `episode.observations`: A numpy array of observations of shape (T+1, *obs_shape).
		* `episode.actions`: A numpy array of actions of shape (T, *action_shape).
		* `episode.rewards`: A numpy array of rewards of shape (T,) (double).
		* `episode.terminations`: A numpy array of boolean flags, possibly True at the last timestep (if not, truncations must be True).
		* `episode.truncations`: A numpy array of boolean flags, possibly True at the last timestep (if not, terminations must be True).

		- An `episode` also has two extra properties:

		* `episode.id`: The index of the episode in the dataset.
		* `episode.infos`: (optional) Dictionaries with auxiliary information defined by the designer.

	2. **Dataset Metadata**

		- The dataset also includes the following properties related to how the data should be interpreted:

		* `data.total_episodes`: Total number of episodes in the dataset.
		* `data.total_steps`: Total number of timesteps across all episodes.
		* `data.observation_space`: A gymnasium.spaces.box.Box with the range definition for the observations. Among other things,
			`data.observation_space.low` is a numpy array with the minimum value for each dimension and `data.observation_space.high`
			the maximum value.
		* `data.action_space`: A gymnasium.spaces.box.Box with the range definition for the actions. (See above for observations.)

	   - The dataset has additional metadata fields including:

		* `data.id`: The specific dataset name (typically `namespace`/`dataset_name`-v`version`) (e.g., 'D4RL/door/human-v2').
		* `data.spec.namespace`: Part of the id. (e.g., 'D4RL/door')
		* `data.spec.dataset_name`: Part of the id. (e.g., 'human')
		* `data.spec.version`: Part of the id. (e.g., '2')
		* `data.spec.env_spec`: (optional) The environment spec which is an EnvSpec that contains a dictionary specified by the designer.
		* `data.spec.data_path`: The path to the data on the local computer. (Where Minari stores what can see with `minari list local`.)
	"""

	def __init__(self, id = None):
		self._id	 = id
		self._data	 = None
		self._issues = None


	@property
	def id(self):
		"""
		The id of the Minari dataset being managed.
		"""
		return self._id


	@property
	def data(self):
		"""
		The Minari dataset being managed.
		"""
		if self._data is None and self._id is not None:
			self._data = load_dataset(self._id)

		return self._data


	@property
	def issues(self):
		"""
		Issues found during the last audit. None if no issues found.
		"""
		return self._issues


	def audit_dataset(self, data, verbose = False):
		"""
		Audits a Minari dataset to check if it conforms to the expected structure for episodic datasets.

		Args:
			data (minari.Dataset): The Minari dataset (an object returned by minari.load_dataset() call) to audit.
			verbose (bool): If True, prints detailed information about any issues found.

		Returns:
			(int): An integer score being 0 if no issues found, the number of issues if the audit could be completed, or the negative
				number of issues until the audit was aborted due to critical problems.
		"""

		self._issues = None
		abort = False

		if hasattr(data, 'total_episodes'):
			T = data.total_episodes
			if T <= 0:
				abort = True
				self._report('data.total_episodes <= 0', abort)
		else:
			abort = True
			self._report('data.total_episodes not found', abort)

		TN  = None
		TTN = 0
		if hasattr(data, 'total_steps'):
			TN = data.total_steps
		else:
			abort = True
			self._report('data.total_steps not found', abort)

		obs_min = None
		if hasattr(data, 'observation_space') and hasattr(data.observation_space, 'low'):
			obs_min = data.observation_space.low
		else:
			self._report('data.observation_space.low not found', abort)

		obs_max = None
		if hasattr(data, 'observation_space') and hasattr(data.observation_space, 'high'):
			obs_max = data.observation_space.high
		else:
			self._report('data.observation_space.high not found', abort)

		act_min = None
		if hasattr(data, 'action_space') and hasattr(data.action_space, 'low'):
			act_min = data.action_space.low
		else:
			self._report('data.action_space.low not found', abort)

		act_max = None
		if hasattr(data, 'action_space') and hasattr(data.action_space, 'high'):
			act_max = data.action_space.high
		else:
			self._report('data.action_space.high not found', abort)

		id = None
		if hasattr(data, 'id'):
			id = data.id
		else:
			self._report('data.id not found', abort)

		namespace = None
		if hasattr(data, 'spec') and hasattr(data.spec, 'namespace'):
			namespace = data.spec.namespace
		else:
			self._report('data.spec.namespace not found', abort)

		dataset_name = None
		if hasattr(data, 'spec') and hasattr(data.spec, 'dataset_name'):
			dataset_name = data.spec.dataset_name
		else:
			self._report('data.spec.dataset_name not found', abort)

		version = None
		if hasattr(data, 'spec') and hasattr(data.spec, 'version'):
			version = data.spec.version
		else:
			self._report('data.spec.version not found', abort)

		env_spec = None
		if hasattr(data, 'spec') and hasattr(data.spec, 'env_spec'):
			env_spec = data.spec.env_spec

		data_path = None
		if hasattr(data, 'spec') and hasattr(data.spec, 'data_path'):
			data_path = data.spec.data_path

			if type(data_path) is not str:
				self._report('data.spec.data_path is not a string', abort)
		else:
			self._report('data.spec.data_path not found', abort)


		if not abort:
			if id != '%s/%s-v%s' % (namespace, dataset_name, str(version)):
				self._report('data.id != namespace/dataset_name-version', abort)

			if env_spec is not None and 'EnvSpec' not in str(type(env_spec)):
				self._report('data.spec.env_spec is not a gymnasium.envs.registration.EnvSpec', abort)

			for i in range(T):
				episode = data[i]

				if not hasattr(episode, 'id'):
					self._report('episode.id not found for episode %d' % i, abort)
					continue

				if episode.id != i:
					self._report('episode.id != episode index for episode %d' % i, abort)

				if not hasattr(episode, 'observations'):
					self._report('episode.observations not found for episode %d' % i, abort)
					continue

				observations = episode.observations
				N = observations.shape[0] - 1

				if obs_min is not None:
					if (observations.shape[1:] != obs_min.shape):
						self._report('observations has different shape as observation_space.low for episode %d' % i, abort)

				if obs_max is not None:
					if (observations.shape[1:] != obs_max.shape):
						self._report('observations has different shape as observation_space.high for episode %d' % i, abort)

				if not hasattr(episode, 'actions'):
					self._report('episode.actions not found for episode %d' % i, abort)
					continue

				actions = episode.actions
				if actions.shape[0] != N:
					self._report('episode.actions has different length as observations - 1 for episode %d' % i, abort)

				if act_min is not None:
					if (actions.shape[1:] != act_min.shape):
						self._report('actions has different shape as action_space.low for episode %d' % i, abort)

				if act_max is not None:
					if (actions.shape[1:] != act_max.shape):
						self._report('actions has different shape as action_space.high for episode %d' % i, abort)

				if not hasattr(episode, 'rewards'):
					self._report('episode.rewards not found for episode %d' % i, abort)
					continue

				rewards = episode.rewards
				if rewards.shape[0] != N:
					self._report('episode.rewards has different length as observations - 1 for episode %d' % i, abort)

				if (rewards.dtype != 'float64' and rewards.dtype != 'float32') or len(rewards.shape) != 1:
					self._report('episode.rewards is not a 1D array of float for episode %d' % i, abort)

				if not hasattr(episode, 'terminations'):
					self._report('episode.terminations not found for episode %d' % i, abort)
					continue

				terminations = episode.terminations
				if terminations.shape[0] != N:
					self._report('episode.terminations has different length as observations - 1 for episode %d' % i, abort)

				if terminations.dtype != 'bool' or len(terminations.shape) != 1:
					self._report('episode.terminations is not a 1D array of bool for episode %d' % i, abort)

				if not hasattr(episode, 'truncations'):
					self._report('episode.truncations not found for episode %d' % i, abort)
					continue

				truncations = episode.truncations
				if truncations.shape[0] != N:
					self._report('episode.truncations has different length as observations - 1 for episode %d' % i, abort)

				if truncations.dtype != 'bool' or len(truncations.shape) != 1:
					self._report('episode.truncations is not a 1D array of bool for episode %d' % i, abort)

				if truncations[:-1].any() or terminations[:-1].any():
					self._report('truncations or terminations has True before the last for episode %d' % i, abort)

				if not (truncations[-1] or terminations[-1]):
					self._report('truncations and terminations are both False at the last timestep for episode %d' % i, abort)

				TTN += N

			if TN is not None and TN != TTN:
				self._report('data.total_steps != sum of episode lengths', abort)

		issues = 0 if self._issues is None else len(self._issues)

		if verbose:
			if issues == 0:
				print('RLDataset.audit_dataset(): No issues found.\n')
			else:
				print('RLDataset.audit_dataset(): %d issues found:\n' % issues)
				for issue in self._issues:
					print('  - %s' % issue)
				print('')

		if abort:
			issues = -issues

		return issues


	def build(self, name, data, args = None):
		"""
		Build a Minari dataset from raw data.

		Args:
			name (str): The name of the dataset to create, in the form 'namespace/dataset_name-vX' where X is the version number.
			data (): A single dataset or a list of datasets. Each dataset can be:
				- A pandas DataFrame
				- A numpy array
				- A Spark DataFrame
				- A string path to a CSV file
				- A dictionary with:
					- 'path' (mandatory): path to the CSV file
					- 'sep' (optional): separator used in the CSV file (default is ',')
					- 'names' (optional): list of column names to use when reading the CSV file. When this is given, the CSV file is read
					  without a header row.
			args (dict): A dictionary with additional arguments required for interpreting episode structure and adding metadata.
				There is a default shown here. The mandatory keys are:
				- 'episodes': Either the name of a column that contains episode IDs or None. In the latter case, the dataset must be a list
				  of datasets where each dataset corresponds to a single episode. (Default: None)
				- 'completion': (optional) A regex string that returns 0 or 1 when applied to the dataset name. If the episode is complete,
				  a final termination will be autogenerated, else a final truncation will be autogenerated. (Default: Not defined)
				- 'observations': Either a regex string to match column names or a list of column names that correspond to the observation.
				(Default: '^obs.*$')
				- 'actions': Either a regex string to match column names or a list of column names that correspond to the action.
				(Default: '^action.*$')
				- 'reward': The column name that corresponds to the reward. (Default: 'reward')
				- 'termination': The column name that corresponds to the termination. It should be None when 'completion' is given.
				(Default: 'finished')
				- 'truncation': The column name that corresponds to the truncation. It should be None when 'completion' is given. It can
				also be None when it is just complementary to 'termination'. In that case, the last timestep of each episode will be either
				a termination or a truncation depending on the value of 'termination'. (Default: None)
				- 'obs_space': (optional) A gymnasium.spaces.box.Box defining the observation space. If not given, it will be inferred
				from the data. (Default: Not defined)
				- 'act_space': (optional) A gymnasium.spaces.box.Box defining the action space. If not given, it will be inferred from
				the data. (Default: Not defined)
				- 'author': (optional) The author of the dataset. (Default: 'mercury-rl')
				- 'author_email': (optional) The email of the author. (Default: Not defined)
				- 'code_permalink': (optional) A URL to the code that generated the dataset. (Default: Not defined)
				- 'algorithm_name': (optional) The name of the algorithm used to generate the dataset. (Default: Not defined)
		"""

		dd = Episodes(data, args)

		author = 'mercury-rl' if 'author' not in args else args['author']
		author_email = None if 'author_email' not in args else args['author_email']
		code_permalink = None if 'code_permalink' not in args else args['code_permalink']
		algorithm_name = None if 'algorithm_name' not in args else args['algorithm_name']

		try: delete_dataset(name)
		except FileNotFoundError: pass

		with warnings.catch_warnings():
			warnings.simplefilter('ignore')

			data = create_dataset_from_buffers(
				dataset_id        = name,
				buffer            = dd.episodes,
				observation_space = dd.obs_space,
				action_space      = dd.act_space,
				author            = author,
				author_email      = author_email,
				code_permalink    = code_permalink,
				algorithm_name    = algorithm_name)

		return data


	def modify_rewards(self, new_data, src_data, args):
		"""
		Jira issue: DEMERCURY-35 """
		pass


	def as_supervised(self, fn, data, args):
		"""
		Jira issue: DEMERCURY-36 """
		pass


	def _report(self, message, abort):
		"""
		An internal method to simplify the output of `audit_dataset()`.

		Args:
			message: The message to append to issues.
			abort: A boolean indicating whether the audit should be aborted to avoid excessive repetition of the same error or testing
				not being possible due to unexpected type of data.
		"""
		if self._issues is None:
			self._issues = []

		n = len(self._issues)
		message = '%4d - %s' % (n + 1, message)

		if abort:
			message = '%s | Audit aborted!! ' % message

		self._issues.append(message)


	def _build_hello_world_dataset(self, id):
		"""
		Builds a simple "Hello World" Minari dataset with two episodes in a one-dimensional observation and action space.
		"""

		# Episode 0
		obs0 = np.array([[0.0], [1.0], [2.0]])          # (T+1, obs_dim)
		act0 = np.array([[0.1], [0.2]])                 # (T, act_dim)
		rew0 = np.array([1.0, 1.0], dtype = np.float32)
		trm0 = np.array([False, True])
		trn0 = np.array([False, False])

		epi0 = EpisodeBuffer(id = 0, observations = obs0, actions = act0, rewards = rew0, terminations = trm0, truncations = trn0)

		# Episode 1
		obs1 = np.array([[5.0], [6.0]])                 # (T+1, obs_dim)
		act1 = np.array([[0.5]])                        # (T, act_dim)
		rew1 = np.array([2.0], dtype = np.float32)
		trm1 = np.array([True])
		trn1 = np.array([False])

		epi1 = EpisodeBuffer(id = 1, observations = obs1, actions = act1, rewards = rew1, terminations = trm1, truncations = trn1)

		episodes = [epi0, epi1]

		# Explicit spaces: shape must match single timestep slice
		obs_space = Box(low = -np.inf, high = np.inf, shape = obs0.shape[1:], dtype = np.float32)
		act_space = Box(low = -np.inf, high = np.inf, shape = act0.shape[1:], dtype = np.float32)

		try: delete_dataset(id)
		except FileNotFoundError: pass

		with warnings.catch_warnings():
			warnings.simplefilter('ignore')

			data = create_dataset_from_buffers(
				dataset_id        = id,
				buffer            = episodes,
				observation_space = obs_space,
				action_space      = act_space,
				author            = 'mercury-team @ BBVA')

		return data
