"""
eval.py

This module is responsible for evaluating offline reinforcement learning algorithms
"""

# modules
import minari
import torch

# own modules
from utils import ObservationProcessor, get_unique_missions, get_unique_directions
from models import MinariObsEncoder

class ValueFunctionEstimator():
    """
    This class estimates the value function for reinforcement learning algorithms.
    Value function estimator is computed as the mean of the rewards in the replay memory.

    Hence, an actor can use this estimator to evaluate the expected return of a policy throughout episodes.
    """

    def __init__(self, dataset_name, actor=None, num_episodes=100):
        """
        Initialize the value function estimator.
        Args:
            agent: The agent for which the value function is being estimated.
            minari_dataset: The Minari dataset used for evaluation.
        """
        self.actor = actor
        self.minari_dataset = minari.load_dataset(dataset_name)
        self.DISCOUNT_FACTOR = 0.99
        self.rewards = []
        self.num_episodes = num_episodes  # Number of episodes to evaluate the actor
        

        # Initialize the observation processor and encoder
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        mission_vocab = get_unique_missions(dataset_name)
        direction_vocab = get_unique_directions(dataset_name)

        self.obs_processor = ObservationProcessor(mission_vocab, device=device)

        self.encoder = MinariObsEncoder(
            mission_dim=len(mission_vocab),
            direction_dim=len(direction_vocab)
        ).to(device)


    def get_value_estimate(self) -> float:
        """
        Calculate the discounted sum of rewards.
        Returns:
            float: The discounted sum of rewards.
        """

        if not self.rewards:
            return 0.0
        
        # Calculate the discounted sum of rewards
        # Using the formula: V(s) = sum(reward_t * (discount_factor ** t))
        # where t is the time step and reward_t is the reward at time t.
        # This is a simplified version assuming rewards are collected in order.
        # The rewards are assumed to be in chronological order.
        discounted_sum = 0.0
        future_reward = 0.0

        for reward in reversed(self.rewards):
            future_reward = reward + self.DISCOUNT_FACTOR * future_reward
            discounted_sum += future_reward

        return discounted_sum / len(self.rewards) 
    
    def random_agent_estimate(self):
        """
        Estimate the value function using a random agent.
        Returns:
            float: The estimated value function.
        """

        self.rewards = []  # Reset rewards for the new evaluation
        env = self.minari_dataset.recover_environment()

        for episode in range(self.num_episodes):
            obs, info = env.reset()
            done = False
            while not done:
                action = env.action_space.sample()  # Sample a random action
                obs, reward, done, truncated, info = env.step(action)
                self.rewards.append(reward)
        env.close()

        print(f"Random agent estimated value: {self.get_value_estimate()}")
        return self.get_value_estimate()
    
    def actor_agent_estimate(self):
        """
        Estimate the value function using the actor policy.
        Returns:
            float: The estimated value function.
        """

        self.rewards = []  # Reset rewards for the new evaluation
        env = self.minari_dataset.recover_environment()

        for episode in range(self.num_episodes):
            obs, info = env.reset()
            done = False

            while not done:
                # Process observation as in your training
                processed = self.obs_processor(obs)  # dict with image, mission, direction
                encoded = self.encoder(processed)    # tensor [D]
                action = self.actor(encoded.unsqueeze(0))  # actor expects batch
                action = action.squeeze(0).detach().cpu().numpy()

                obs, reward, done, truncated, info = env.step(action)
                self.rewards.append(reward)

        env.close()
        print(f"Actor agent estimated value: {self.get_value_estimate()}")
        return self.get_value_estimate()




if __name__ == "__main__":
    # Example usage

    minari_buffer = ReplayMemory(1000) # Replace with the actual Minari buffer path
    actor = torch.load("models/actor_model.pth")  # Load your trained actor model
    value_estimator = ValueFunctionEstimator("minigrid/BabyAI-OneRoomS12/optimal-fullobs-v0", minari_buffer, actor=actor)

    # Estimate value using a random agent
    value_estimate = value_estimator.random_agent_estimate()
