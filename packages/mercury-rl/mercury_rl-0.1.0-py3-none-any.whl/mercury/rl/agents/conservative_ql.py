import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.losses import MSE
from tensorflow.keras.optimizers import Adam

import numpy as np
import random


class ConservativeDQLAgent:
    """
    A class representing a Conservative Deep Q-Learning Agent.

    Look at: https://arxiv.org/abs/2006.04779

    Attributes:
        MEMORY_SIZE (int): The maximum size of the agent's memory.
        GAMMA (float): The discount factor for future rewards.
        CQL_ALPHA (float): The coefficient for the conservative Q-learning loss.
        EPSILON (float): The exploration rate.
        NUM_STEPS_FOR_UPDATE (int): The number of steps before updating the target network.
        lr (float): The learning rate for the optimizer.
        n_actions (int): The number of actions in the environment.
        deterministic (bool): Whether to choose actions deterministically.
        states_memory (list): A list to store the states in the agent's memory.
        actions_memory (list): A list to store the actions in the agent's memory.
        next_states_memory (list): A list to store the next states in the agent's memory.
        rewards_memory (list): A list to store the rewards in the agent's memory.
        dones_memory (list): A list to store the done flags in the agent's memory.
        num_states (int): The number of states in the environment.
        num_actions (int): The number of actions in the environment.
        q_network (tf.keras.Sequential): The Q-network used by the agent.
        target_q_network (tf.keras.Sequential): The target Q-network used by the agent.
        optimizer (tf.keras.optimizers.Adam): The optimizer used for training the Q-network.
        loss (tf.Tensor): The computed loss during the learning step.

    Methods:
        __init__(self, learning_rate, gamma, epsilon, num_states, n_actions, deterministic):
            Initializes the ConservativeDQLAgent.

        choose_action(self, observation):
            Chooses an action based on the observation.

        store_transition(self, state, action, next_state, reward, done):
            Stores a transition in the agent's memory.

        compute_loss(self):
            Computes the loss for training the agent.

        learn(self):
            Performs a learning step for the agent.
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        num_states: int = 2,
        n_actions: int = 3,
        deterministic: bool = False
    ) -> None:
        """
        Initializes the ConservativeDQLAgent.

        Args:
            learning_rate (float): The learning rate for the optimizer. Default is 0.01.
            gamma (float): The discount factor for future rewards. Default is 0.99.
            epsilon (float): The exploration rate. Default is 1.0.
            num_states (int): The number of states in the environment. Default is 2.
            n_actions (int): The number of actions in the environment. Default is 3.
            deterministic (bool): Whether to choose actions deterministically. Default is False.
        """
        # Initialize hyperparameters
        self.MEMORY_SIZE = 100_000
        self.GAMMA = gamma
        self.CQL_ALPHA = 1.0
        self.EPSILON = epsilon
        self.NUM_STEPS_FOR_UPDATE = 4

        # Initialize learning parameters
        self.lr = learning_rate
        self.n_actions = n_actions
        self.deterministic = deterministic

        # Initialize memory
        self.states_memory = []
        self.actions_memory = []
        self.next_states_memory = []
        self.rewards_memory = []
        self.dones_memory = []

        # Initialize state and action space dimensions
        self.num_states = num_states
        self.num_actions = n_actions

        # Initialize Q-network and target Q-network
        self.q_network = Sequential([
            Input(shape=(self.num_states,)),
            Dense(64, activation="relu"),
            Dense(64, activation="relu"),
            Dense(self.num_actions, activation="linear")
        ])

        self.target_q_network = Sequential([
            Input(shape=(self.num_states,)),
            Dense(64, activation="relu"),
            Dense(64, activation="relu"),
            Dense(self.num_actions, activation="linear")
        ])

        self.target_q_network.set_weights(self.q_network.get_weights())

        # Initialize optimizer
        self.optimizer = Adam(learning_rate=self.lr)

    def choose_action(self, observation: np.ndarray) -> int:
        """
        Chooses an action based on the observation.

        Args:
            observation: The current observation/state.

        Returns:
            The chosen action.
        """
        state = tf.convert_to_tensor([observation], dtype=tf.float32)
        q_values = self.q_network(state)
        if self.deterministic:
            action = np.argmax(q_values.numpy()[0])
        else:
            if np.random.uniform(0, 1) < self.EPSILON:
                action = random.choice(np.arange(self.num_actions))
            else:
                action = np.argmax(q_values.numpy()[0])
        return action

    def store_transition(
            self,
            state: np.ndarray,
            action: int,
            next_state: np.ndarray,
            reward: float,
            done: bool) -> None:
        """
        Stores a transition in the agent's memory.

        Args:
            state (np.ndarray): The current state.
            action (int): The chosen action.
            next_state (np.ndarray): The next state.
            reward (float): The reward received.
            done (bool): Whether the episode is done or not.
        """
        self.states_memory.append(state)
        self.actions_memory.append(action)
        self.next_states_memory.append(next_state)
        self.rewards_memory.append(reward)
        self.dones_memory.append(done)

    def compute_loss(self) -> float:
        """
        Computes the loss for training the agent.

        Returns:
            The computed loss.
        """
        states = tf.convert_to_tensor(self.states_memory, dtype=tf.float32)
        actions = tf.convert_to_tensor(self.actions_memory, dtype=tf.int32)
        rewards = tf.convert_to_tensor(self.rewards_memory, dtype=tf.float32)
        next_states = tf.convert_to_tensor(self.next_states_memory, dtype=tf.float32)
        done_vals = tf.convert_to_tensor(np.array(self.dones_memory).astype(np.uint8), dtype=tf.float32)

        max_qsa = tf.reduce_max(self.q_network(next_states), axis=1)

        y_targets = rewards + (self.GAMMA * max_qsa * (1 - done_vals))
        q_values = self.q_network(states)

        q_values_mu = tf.gather_nd(
            q_values,
            tf.stack([tf.range(q_values.shape[0]), tf.cast(actions, tf.int32)], axis=1)
        )

        q_logsumexp = tf.math.reduce_logsumexp(q_values, axis=-1)
        loss = self.CQL_ALPHA * tf.reduce_mean(q_logsumexp - q_values_mu) + 0.5 * MSE(q_values_mu, y_targets)

        return loss

    def learn(self) -> None:
        """
        Performs a learning step for the agent.
        """
        with tf.GradientTape() as tape:
            loss = self.compute_loss()

        gradients = tape.gradient(loss, self.q_network.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.q_network.trainable_variables))

        TAU = 1e-3
        for target_weights, q_network_weights in zip(self.target_q_network.weights, self.q_network.weights):
            target_weights.assign(TAU * q_network_weights + (1.0 - TAU) * target_weights)

        self.loss = loss
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
