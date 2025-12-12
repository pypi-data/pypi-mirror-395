from collections import deque
import random
 
class ReplayMemory:
    """
    Replay memory buffer to store experiences for DQN.
    This class implements a simple FIFO queue (deque) to store experiences and sample them for training.
    Reference:
        https://github.com/johnnycode8/dqn_pytorch
    """

    def __init__(self, capacity, seed=None):
        self.memory = deque(maxlen=capacity)

        # Set the random seed for reproducibility
        if seed is not None:
            random.seed(seed)

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