from typing import List, Tuple
import pandas as pd
import numpy as np
import tensorflow as tf
import random


class DataGenerator(tf.keras.utils.Sequence):

    def __init__(
        self,
        file_path: str,
        episode_col_id: str = "episode_id",
        order_col: str = "seq",
        state_cols: List[str] = None,
        action_col: str = "action",
        reward_col: str = "reward",
        batch_size: int = 64,
        shuffle: bool = False
    ):
        """
        Initializes a DataGenerator object.

        Args:
            file_path (str): The directory path where the data files are located.
            episode_col_id (str): The column ID for the episode.
            order_col (str): The column for the order.
            state_cols (List[str]): A list of column names for the state.
            action_col (str): The column for the action.
            reward_col (str): The column for the reward.
            batch_size (int, optional): The batch size. Defaults to 64. It corresponds to the number of episodes to extract.
            shuffle (bool, optional): Whether to shuffle the data. Defaults to False.
        """

        self.file_path = file_path
        self.batch_size = batch_size
        self.state_cols = state_cols
        self.action_col = action_col
        self.reward_col = reward_col
        self.episode_col_id = episode_col_id
        self.order_col = order_col
        self.shuffle = shuffle
        self.already_visited = []
        self.states_cols = state_cols if state_cols else ["state_1", "state_2"]

        self.episodes = self.__len__()

    def __len__(self) -> int:
        """
        Returns the number of batches per epoch.

        This method calculates the number of batches by dividing the total number of files
        in the dataset by the batch size. The result is rounded down to the nearest integer.

        Returns:
            int: The number of batches per epoch.
        """

        with open(self.file_path, "rb") as f:
            self.num_lines = sum(1 for _ in f)

        return int(np.floor(self.num_lines / self.batch_size))

    def get_batch(self):
        choices = list(set(range(1, self.num_lines + 1)) - set(self.already_visited))
        non_skip = random.sample(choices, self.batch_size)
        rows = [i for i in range(1, self.num_lines + 1) if i not in non_skip]
        skip = sorted(rows)

        df = pd.read_csv(self.file_path, skiprows=skip)

        self.already_visited.extend(non_skip)
        return df

    def __getitem__(self, index) -> Tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray
    ]:
        """
        Generate one batch of data.

        Args:
            index (int): The index of the batch.

        Returns:
            A 5-element tuple containing:
                    Episode IDs: numpy array of episode IDs. Shape = (episode lengths x n_episodes,)
                    Sequence: numpy array of sequence oder numbers. Shape = (episode lengths x n_episodes,)
                    States: numpy array of states. Shape = (episode lengths x n_episodes, n_states)
                    Actions: numpy array of actions. Shape = (episode lengths x n_episodes,)
                    Rewards: numpy array of rewards. Shape = (episode lengths x n_episodes,)
        """

        episode, sequence, states, actions, rewards = self.__data_generation()

        return episode, sequence, states, actions, rewards

    def __data_generation(self) -> Tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray
    ]:
        """
        Generates data samples.

        Returns:
            tuple: A tuple containing the episode, sequence, states, actions, and rewards arrays.
        """

        data = self.get_batch()

        episode = data[self.episode_col_id].values
        sequence = data[self.order_col].values
        states = data[self.state_cols].values
        actions = data[self.action_col].values
        rewards = data[self.reward_col].values

        return episode, sequence, states, actions, rewards
