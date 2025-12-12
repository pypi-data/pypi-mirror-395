import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
# import tensorflow_probability as tfp
import numpy as np


class ImitationAgent:
    """
    The ImitationAgent class represents an agent that learns through imitation learning.

    Attributes:
        gamma (float): The discount factor for future rewards.
        lr (float): The learning rate for the optimizer.
        n_actions (int): The number of actions in the environment.
        deterministic (bool): Whether to use a deterministic policy.
        state_memory (list): The memory to store observed states.
        action_memory (list): The memory to store taken actions.
        reward_memory (list): The memory to store received rewards.
        policy (tf.keras.Model): The policy network used by the agent.

    Methods:
        __init__(self, learning_rate, gamma, num_states, n_actions, deterministic)
        choose_action(self, observation)
        store_transition(self, observation, action, reward)
        learn(self)
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        gamma: float = 0.99,
        num_states: int = 2,
        n_actions: int = 3,
        deterministic: bool = False
    ) -> None:
        """
        Initialize the ImitationLearning agent.

        Args:
            learning_rate (float): The learning rate for the optimizer. Default is 0.01.
            gamma (float): The discount factor for future rewards. Default is 0.99.
            num_states (int): The number of states in the environment. Default is 2.
            n_actions (int): The number of actions in the environment. Default is 3.
            deterministic (bool): Whether to use a deterministic policy. Default is False.

        Returns:
            None
        """
        self.gamma = gamma
        self.lr = learning_rate
        self.n_actions = n_actions
        self.deterministic = deterministic
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []

        self.policy = Sequential([
            Input(shape=(num_states,)),
            Dense(32, activation="relu"),
            Dense(32, activation="relu"),
            Dense(n_actions, activation="softmax")
        ])

        self.policy.compile(optimizer=Adam(learning_rate=self.lr))

    def choose_action(self, observation: np.ndarray) -> int:
        """
        Choose an action based on the given observation.

        Args:
            observation (array-like): The observation of the environment of shape [n_states,].

        Returns:
            int: The chosen action.
        """
        state = tf.convert_to_tensor([observation], dtype=tf.float32)
        probs = self.policy(state)
        if self.deterministic:
            # action_probs = tfp.distributions.Categorical(probs=probs) #  This was the original code
            action = tf.random.categorical(tf.math.log(probs), num_samples=1)
            action = tf.squeeze(action, axis=1).numpy()[0]
        else:
            action = tf.argmax(probs, axis=1).numpy()[0]
        return action

    def store_transition(
        self,
        observation: np.ndarray,
        action: int,
        reward: float
    ) -> None:
        """
        Stores a transition in the agent's memory.

        Args:
            observation (np.ndarray): The observation/state of the environment.
            action (int): The action taken by the agent.
            reward (float): The reward received from the environment.

        Returns:
            None
        """
        self.state_memory.append(observation)
        self.action_memory.append(action)
        self.reward_memory.append(reward)

    def learn(self):
        """
        Performs a learning step for the imitation learning agent.

        This function calculates the loss and updates the policy network based on the
        collected memories.

        Returns:
            None
        """
        actions = tf.convert_to_tensor(self.action_memory, dtype=tf.int32)
        states = tf.convert_to_tensor(self.state_memory, dtype=tf.float32)

        with tf.GradientTape() as tape:
            probs = self.policy(states)
            action_masks = tf.one_hot(actions, self.n_actions)
            log_probs = tf.math.log(probs)
            masked_log_probs = tf.reduce_sum(action_masks * log_probs, axis=-1)
            loss = -tf.reduce_mean(masked_log_probs)

        net_gradients = tape.gradient(loss, self.policy.trainable_variables)
        self.policy.optimizer.apply_gradients(zip(net_gradients, self.policy.trainable_variables))

        self.loss = loss
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
