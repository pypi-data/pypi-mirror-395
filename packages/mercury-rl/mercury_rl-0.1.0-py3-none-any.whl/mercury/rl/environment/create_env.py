import numpy as np
from typing import List, Tuple
from .data_generator import DataGenerator


class ENV:
    """
    The ENV class represents an environment object that generates batches of data from a CSV file.

    Attributes:
        data_path (str): The path to the data file.
        state_cols (List[str]): A list of column names representing the state variables.
        action_col (str): The column name representing the action variable.
        reward_col (str): The column name representing the reward variable.
        episode_col_id (str): The column name representing the episode identifier.
        order_col (str): The column name representing the order of the data.
        batch_size (int): The batch size for generating data batches. It corresponds to the number of episodes to extract.

    Methods:
        __init__(self, data_path: str, states_cols: List[str], action_col: str, reward_col: str, episode_col_id: str, order_col: str, batch_size: int, shuffle: bool) -> None:
            Initializes the environment object.
        get_trajectories(self, batch_id: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
            Retrieves the trajectories for a given batch ID.
        generate_batches(self) -> None:
            Generates batches of data from a CSV file.
    """

    def __init__(
        self,
        data_path: str,
        state_cols: List[str] = None,
        action_col: str = "action",
        reward_col: str = "reward",
        episode_col_id: str = "episode_id",
        order_col: str = "seq",
        batch_size: int = 64,
        shuffle: bool = False
    ) -> None:
        """
        Initializes the environment object.

        Args:
            data_path (str): The path to the data file.
            state_cols (List[str]): A list of column names representing the state variables.
            action_col (str): The column name representing the action variable.
            reward_col (str): The column name representing the reward variable.
            episode_col_id (str): The column name representing the episode identifier.
            order_col (str): The column name representing the order of the data.
            batch_size (int): The batch size for generating data batches. It corresponds to the number of episodes to extract.
            shuffle (bool, optional): Whether to shuffle the data batches. Defaults to False.
        """
        self.env = None
        self.data_path = data_path
        self.action_col = action_col
        self.reward_col = reward_col
        self.episode_col_id = episode_col_id
        self.order_col = order_col
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.state_cols = state_cols if state_cols else ["state_1", "state_2"]

    def reset(self):
        self.env = DataGenerator(
            file_path=self.data_path,
            episode_col_id=self.episode_col_id,
            order_col=self.order_col,
            state_cols=self.state_cols,
            action_col=self.action_col,
            reward_col=self.reward_col,
            batch_size=self.batch_size,
            shuffle=self.shuffle
        )

    def get_replay(self, batch_id) -> Tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray
    ]:
        """
        Retrieves the trajectories for a given batch ID.

        Parameters:
        - batch_id (int):
            The ID of the batch for which to retrieve the trajectories.
            The batch size corresponds to the number of episodes.

        Returns:
            A 5-element tuple containing:
                    Episode IDs: numpy array of episode IDs. Shape = (episode lengths x n_episodes)
                    Sequence: numpy array of sequence order numbers. Shape = (episode lengths x n_episodes)
                    States: numpy array of states. Shape = (episode lengths x n_episodes, n_states)
                    Actions: numpy array of actions. Shape = (episode lengths x n_episodes)
                    Rewards: numpy array of rewards. Shape = (episode lengths x n_episodes)
        """
        return self.env[batch_id]
