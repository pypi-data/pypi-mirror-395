import torch
import torch.nn as nn
import torch.nn.functional as F


class NimPolicyArgMax(nn.Module):

	def __init__(self, obs_dim = 4, num_stacks = 4, num_classes = 10, hidden_dim = 64):
		super().__init__()

		# --- Shared Feature Extractor ---
		# A common set of layers to learn high-level features from the observation.
		self.fc1 = nn.Linear(obs_dim, hidden_dim)
		self.fc2 = nn.Linear(hidden_dim, hidden_dim)

		# --- Output Heads (Separate for each action component) ---

		# 1. Stack Head: Predicts which of the 4 stacks to remove from (0, 1, 2, 3)
		self.stack_head = nn.Linear(hidden_dim, num_stacks)

		# 2. Number Head: Predicts how many stones to remove (1 to 10)
		self.num_head = nn.Linear(hidden_dim, num_classes)


	def forward(self, x):
		# 1. Feature extraction
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))

		# 2. Get Logits
		stack_logits = self.stack_head(x)
		num_logits = self.num_head(x)

		# 3. Action Decoding (Argmax on logits)

		# Predicted stack index (0-3). Keep the dimension for concatenation.
		predicted_stack_index = torch.argmax(stack_logits, dim = 1, keepdim = True)

		# Predicted number index (0-9).
		predicted_num_index = torch.argmax(num_logits, dim = 1, keepdim = True)

		# Apply the +1 shift to get the final stone count (1-10)
		predicted_num_stones = predicted_num_index + 1

		# 4. Concatenate the integer actions to shape [batch_size, 2]
		actions = torch.cat([predicted_stack_index, predicted_num_stones], dim = 1)

		# Ensure the output is an integer type (LongTensor)
		return actions.long()


class NimSoftmax(nn.Module):

	def __init__(self, obs_dim = 4, num_stacks = 4, num_classes = 10, hidden_dim = 64):
		super().__init__()

		# --- Shared Feature Extractor ---
		# A common set of layers to learn high-level features from the observation.
		self.fc1 = nn.Linear(obs_dim, hidden_dim)
		self.fc2 = nn.Linear(hidden_dim, hidden_dim)

		# --- Output Heads (Separate for each action component) ---

		# 1. Stack Head: Predicts which of the 4 stacks to remove from (0, 1, 2, 3)
		self.stack_head = nn.Linear(hidden_dim, num_stacks)

		# 2. Number Head: Predicts how many stones to remove (1 to 10)
		self.num_head = nn.Linear(hidden_dim, num_classes)


	def forward(self, x):
		# 1. Feature extraction
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))

		# 2. Get Logits
		stack_logits = self.stack_head(x)
		num_logits	 = self.num_head(x)

		# 3. Action Decoding (Softmax on logits)
		stack_probs = F.softmax(stack_logits, dim = 1)
		num_probs	= F.softmax(num_logits, dim = 1)

		return torch.cat([stack_probs, num_probs], dim = 1)


def make_one_hot_targets(Y, num_stacks = 4, num_classes = 10):
	"""
	Convert the two action columns into concatenated one-hot vectors.

	Y: tensor of shape [batch_size, 2]
	   Y[:, 0] = stack index (0..num_stacks - 1)
	   Y[:, 1] = num stones (1..num_classes)
	"""
	Y_stack = F.one_hot(Y[:, 0].long(), num_classes = num_stacks)			# Stack is already zero-based
	Y_num	= F.one_hot((Y[:, 1] - 1).long(), num_classes = num_classes)	# Subtract 1 to make number of stones zero-based

	Y_cat = torch.cat([Y_stack, Y_num], dim = 1).float()

	return Y_cat


def training_loop(n_epochs, optimizer, model, loss_fn, train_loader):
	for epoch in range(1, n_epochs + 1):
		loss_train = 0.0
		for x, y_obs in train_loader:
			y_hat = model(x)
			loss  = loss_fn(y_obs, y_hat)

			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			loss_train += loss.item()

		print('Epoch: %2d, Training loss: %7.4f' % (epoch, loss_train/len(train_loader)))


class NimPolicy(nn.Module):

	def __init__(self, obs_dim = 4, num_stacks = 4, num_classes = 10, hidden_dim = 64):
		super().__init__()

		self.softmax_model = NimSoftmax(obs_dim, num_stacks, num_classes, hidden_dim)

		self.num_stacks  = num_stacks
		self.num_classes = num_classes


	def forward(self, x):
		# Get concatenated probabilities from NimSoftmax
		probs = self.softmax_model(x)

		if self.training:
			return probs

		# Split back into stack and num parts
		stack_probs = probs[:, :self.num_stacks]
		num_probs   = probs[:, self.num_stacks:]

		# Take argmax to get discrete predictions
		stack_index = torch.argmax(stack_probs, dim = 1, keepdim = True)
		num_index   = torch.argmax(num_probs, dim = 1, keepdim = True) + 1

		# Concatenate final integer predictions
		actions = torch.cat([stack_index, num_index], dim = 1)

		# Ensure the output is an integer type (LongTensor)
		return actions.long()


class RLModelCreator:

	def __init__(self):
		pass


	@property
	def minari_run_overview(self):
		"""
TorchRL Training on Minari Datasets
-----------------------------------

This step assumes we have a Minari dataset that passes the RLDataset.audit_dataset() that we have possibly created with RLDataset.
We want to use it to train a reinforcement learning (RL) model on it. This involves understanding three core concepts: **models**,
**policies**, and **replay buffers**.

Basic Terminology:
------------------

  - model: A parameterized function (usually a neural network) that maps inputs to outputs. In RL, a model is a combination of:
	a policy (π), a value function (V), or a Q-function (Q).
  - policy: A mapping from observations to actions. A policy can be:
	* deterministic: always produces the same action for a given observation.
	* stochastic: samples actions from a probability distribution conditioned on the observation.
  - Q-function: A function Q(s,a) estimating the expected return (cumulative discounted reward) of taking action a in state s and
  	following the policy thereafter.
  - value function: A function V(s) estimating the expected return from state s under a policy.
  - replay buffer: A storage system for transitions (s, a, r, s', done).
	In online RL it accumulates experiences as the agent interacts with the environment.
	In offline RL, it is filled once from a dataset (e.g. Minari) and then sampled from during training.
  - batch: A set of transitions sampled from the replay buffer to update the model parameters.

Where do Replay Buffers fit in the whole offline RL picture:
------------------------------------------------------------

In offline RL, the dataset is static: no new interactions are collected during training. Replay buffers provide the interface between
this fixed dataset (e.g. a Minari dataset) and the model optimization loop. They manage how transitions (s, a, r, s', done) are
stored, sampled, and delivered to the model during gradient updates.

TorchRL provides two main replay buffer types, serving different roles in the pipeline:

  * ReplayBuffer:
	- Flexible, Pythonic container for collecting or ingesting data.
	- Accepts transitions one by one or from iterables (e.g. MinariExperienceReplay).
	- Ideal for building or loading datasets incrementally (offline ingestion).
	- Uses generic storages (LazyTensorStorage, ListStorage) that grow dynamically.

  * TensorDictReplayBuffer:
	- High-performance, device-aware replay buffer optimized for batched tensors.
	- Requires data to be fully batched into a single TensorDict before loading.
	- Enables fast vectorized sampling and GPU storage for training efficiency.
	- Used once data are fixed and ready for repeated sampling during learning.

Workflow rationale (???)
  1. Load or create the Minari dataset.
  2. Stream its transitions into a ReplayBuffer — this step validates, filters, and formats transitions into TorchRL.
  3. Freeze the dataset into a TensorDictReplayBuffer for efficient, reproducible sampling during training.

This two-stage process separates *data ingestion* (flexible, one-pass) from *data consumption* (efficient, repeated access). In other
words: ReplayBuffer prepares the data; TensorDictReplayBuffer accelerates the training loop.


Training Workflow:
------------------

  1. **Loading a Dataset**
	- A Minari dataset contains episodes of transitions.
	- Each transition has observation, action, reward, next_observation, and termination/truncation flags.
	- We adapt this dataset into a TorchRL replay buffer.

  2. **Creating a Replay Buffer**
	- TorchRL provides replay buffer classes like `TensorDictReplayBuffer`.
	- The replay buffer allows random sampling of batches, which is crucial for stable training.
	- In offline RL, the replay buffer is entirely populated from Minari before training begins.

  3. **Defining a Model**
	- The model is typically a PyTorch neural network.
	- For discrete action spaces:
	  * The model outputs a vector of Q-values, one for each action.
	  * The policy can be derived by selecting the highest-Q action (`argmax`).
	- For continuous action spaces:
	  * The model may output parameters of a distribution over actions (e.g. mean and variance of a Gaussian).

	In both cases, **a separate critic (Q-function)** may be used to estimate the value of state-action pairs.
	This critic guides the learning of the policy network (actor) — especially in actor-critic methods such as SAC, TD3, and PPO.

  4. **Defining a Policy**
	- The policy is derived from the model:
	  * In DQN, the policy is "choose the action with the highest Q-value."
	  * In SAC, the policy samples actions from a learned probability distribution.
	- Policies can be wrapped with exploration strategies (e.g., epsilon-greedy in DQN).

  5. **Training Step**
	- Sample a batch from the replay buffer.
	- Compute the loss:
	  * Value-based methods (DQN, CQL): TD-error between predicted Q and target Q.
	  * Policy-based methods (SAC): maximize expected Q plus entropy regularization.
	- Backpropagate and update model parameters with an optimizer.

  6. **Evaluation**
	- After training, the learned policy can be tested in the original environment.
	- Evaluation involves running the policy without learning and measuring average returns.

Summary:
--------

Training a TorchRL model on a Minari dataset means:
  1. Load the dataset into a TorchRL replay buffer.
  2. Define the model (policy network, Q-network, etc.).
  3. Choose an offline RL algorithm (DQN, SAC, CQL, etc.).
  4. Train the model by sampling batches from the replay buffer.
  5. Evaluate the trained policy in the original environment.
"""
		return None


	def _run_poc_nim_workflow(self):
		# 1. We load a dataset
		import minari

		data = minari.load_dataset('Mercury/toy_datasets/nim-v1')

		obs_shape = data.observation_space.shape
		act_shape = data.action_space.shape

		# 2. We create the model we want to train

		# import torch
		# from torchrl.modules import MLP, QValueModule

		# q_net = MLP(in_features = obs_shape, out_features = act_shape, num_cells = [64, 64], activation_class = torch.nn.ReLU)

		# q_val = QValueModule(spec = action_spec, module = q_net, in_keys = [observation_key])

		print('Done.')
