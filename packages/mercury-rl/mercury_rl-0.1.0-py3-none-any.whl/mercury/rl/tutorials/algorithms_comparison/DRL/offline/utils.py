from collections import deque
import random
import torch
import minari

# own modules
from models import MinariObsEncoder


class ObservationProcessor:
    """
    Process observations from the Minari dataset.
    Converts mission strings to one-hot encoded tensors, and processes image and direction data.
    This is useful for preparing observations for reinforcement learning algorithms.
    """
    def __init__(self, mission_vocab: list[str], device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.mission_vocab = sorted(mission_vocab)
        self.mission2idx = {m: i for i, m in enumerate(self.mission_vocab)}
        self.vocab_size = len(self.mission_vocab)

    def __call__(self, observation: dict):
        # Mission index (no one-hot)
        mission_raw = observation["mission"]
        mission_str = mission_raw.decode("utf-8") if isinstance(mission_raw, bytes) else str(mission_raw)
        idx = self.mission2idx[mission_str]
        mission_tensor = torch.tensor(idx, device=self.device)

        # Image tensor
        image_tensor = torch.tensor(observation["image"], device=self.device)

        # Direction tensor
        direction_tensor = torch.tensor(observation["direction"], device=self.device)

        return {
            "mission": mission_tensor,
            "image": image_tensor,
            "direction": direction_tensor
        }


class ReplayMemory:
    """
    Replay memory buffer to store experiences from a Minari dataset for offline reinforcement learning.
    """

    def __init__(self, capacity, seed=None, encoder_output_dim=16):
        """
        Initialize the replay memory.

        Args:
            capacity (int): Maximum number of experiences to store.
            seed (int, optional): Random seed for reproducibility.
            encoder_output_dim (int): Dimension of final encoded state from MinariObsEncoder.
        """
        self.memory = deque(maxlen=capacity)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._encoder = None
        self._obs_processor = None
        self._mission_vocab_initialized = False
        self.encoder_output_dim = encoder_output_dim

        if seed is not None:
            random.seed(seed)

    def _initialize_processors(self, dataset_id):
        """
        Internal method to initialize the observation processor and encoder.

        Args:
            dataset_id (str): Dataset identifier to extract mission and direction vocabularies.
        """
        mission_vocab = get_unique_missions(dataset_id)
        direction_vocab = get_unique_directions(dataset_id)
        direction_vocab_size = len(direction_vocab)

        self._obs_processor = ObservationProcessor(mission_vocab, device=self.device)

        self._encoder = MinariObsEncoder(
            mission_dim=len(mission_vocab),
            direction_dim=direction_vocab_size,
            output_dim=self.encoder_output_dim  # embedding reducido
        ).to(self.device)

        self._mission_vocab_initialized = True

    @torch.no_grad()
    def load_minari_dataset(self, dataset):
        """
        Load experiences from a Minari dataset into the memory.

        Args:
            dataset (MinariExperienceReplay): The Minari dataset to load experiences from.
        """
        for episode in dataset.iterate_episodes():
            obs = episode.observations
            actions = episode.actions
            rewards = episode.rewards
            terminals = episode.terminations

            for i in range(len(actions)):
                if hasattr(obs, 'keys'):
                    if not self._mission_vocab_initialized:
                        self._initialize_processors(dataset._dataset_id)

                    raw_state = {k: obs[k][i] for k in obs.keys()}
                    raw_next_state = {k: obs[k][i + 1] for k in obs.keys()} if i + 1 < len(obs['image']) else None

                    processed_state = self._obs_processor(raw_state)
                    processed_next_state = self._obs_processor(raw_next_state) if raw_next_state else None

                    state = self._encoder(processed_state)
                    next_state = self._encoder(processed_next_state) if processed_next_state else None

                else:  # embedded observation
                    state = torch.tensor(obs[i], device=self.device, dtype=torch.float32)
                    next_state = torch.tensor(obs[i + 1], device=self.device,  dtype=torch.float32) if i + 1 < len(obs) else None

                action = torch.tensor(actions[i], device=self.device, dtype=torch.float32)
                reward = torch.tensor(rewards[i], device=self.device, dtype=torch.float32)
                done = torch.tensor(terminals[i], device=self.device, dtype=torch.float32)
                self.push((state, action, reward, next_state, done))

    def push(self, experience):
        """
        Add a new experience to the memory.

        Args:
            experience (tuple): A tuple containing (state, action, reward, next_state, done).
        """
        self.memory.append(experience)

    def sample(self, batch_size):
        """
        Sample a random batch of experiences from the memory.

        Args:
            batch_size (int): Number of experiences to sample.

        Returns:
            list: A list of sampled experiences.
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """
        Get the current size of the memory.

        Returns:
            int: The number of experiences stored in the memory.
        """
        return len(self.memory)

    def compute_reward_mean(self):
        """
        Compute the mean of rewards in memory.

        Returns:
            torch.Tensor: Mean reward.
        """
        rewards = [r.item() for (_, _, r, _, _) in self.memory]
        return torch.tensor(rewards).mean().to(self.device)

    def compute_reward_std(self):
        """
        Compute the standard deviation of rewards in memory.

        Returns:
            torch.Tensor: Std of rewards.
        """
        rewards = [r.item() for (_, _, r, _, _) in self.memory]
        return torch.tensor(rewards).std().to(self.device)

    @property
    def obs_dim(self):
        """
        Get the observation dimensionality produced by the encoder.

        Returns:
            int: Dimension of encoded state vectors.
        """
        return self.encoder_output_dim


"""
Minari utility functions
"""
def get_all_missions(dataset_id):
    """
    Retrieve all missions (including duplicates) from a Minari dataset.

    Args:
        dataset_id (str): The ID of the Minari dataset.

    Returns:
        list: A list of mission strings.
    """
    dataset = minari.load_dataset(dataset_id)
    missions = []

    for episode in dataset.iterate_episodes():
        mission_raw = episode.observations["mission"]
        if isinstance(mission_raw, list) or hasattr(mission_raw, "__len__"):
            for m in mission_raw:
                missions.append(m.decode("utf-8") if isinstance(m, bytes) else str(m))
        else:
            missions.append(mission_raw.decode("utf-8") if isinstance(mission_raw, bytes) else str(mission_raw))

    return missions


def get_unique_missions(dataset_id: str) -> list[str]:
    """
    Get unique missions from a Minari dataset.
    Args:
        dataset_id (str): The ID of the Minari dataset.
    Returns:
        list: A list of unique missions.
    """
    all_missions = get_all_missions(dataset_id)
    return list(set(all_missions))


def get_unique_directions(dataset_id: str) -> list[int]:
    """
    Get unique direction values from a Minari dataset.

    Args:
        dataset_id (str): The ID of the Minari dataset.

    Returns:
        list: A list of unique integer directions (e.g., [0,1,2,3]).
    """
    dataset = minari.load_dataset(dataset_id)
    directions = []

    for episode in dataset.iterate_episodes():
        dir_raw = episode.observations["direction"]
        if hasattr(dir_raw, "__len__"):
            directions.extend(dir_raw)
        else:
            directions.append(dir_raw)

    return sorted(set(int(d) for d in directions))


if __name__ == "__main__":
    # Example usage
    dataset_id = "minigrid/BabyAI-OneRoomS12/optimal-fullobs-v0"
    memory = ReplayMemory(capacity=1000, seed=42, encoder_output_dim=16)
    dataset = minari.load_dataset(dataset_id, download=True)

    memory.load_minari_dataset(dataset)

    batch = memory.sample(32)
    for state, action, reward, next_state, done in batch:
        print(f"State: {state.shape}, Action: {action}, Reward: {reward}, Next State: {next_state.shape if next_state is not None else None}, Done: {done}")
