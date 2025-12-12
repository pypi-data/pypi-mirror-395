import torch
import gymnasium
from dqn import DQN
from utils import ReplayMemory
from abc import ABC, abstractmethod
import random
import matplotlib.pyplot as plt
from torch import optim, nn
import flappy_bird_gymnasium  
import matplotlib

class Agent(ABC):
    """
    Base class for reinforcement learning agents.
    Provides a reusable run method for interacting with environments.
    """

    def __init__(self, env_name):
        self.env_name = env_name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    @abstractmethod
    def select_action(self, state):
        """
        Select an action given the current state.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def on_step(self, state, action, reward, next_state, done, is_training):
        """
        This method essentially handles the logic of what to do after taking an action.
        It can be used to update the agent's memory, perform learning steps, etc.
        """
        pass

    def run(self, num_episodes=100, is_training=True, render=False):
        """
        Run the agent in the specified environment.
        """
        env = gymnasium.make(self.env_name, render_mode='human' if render else None)
        ep_rewards = []

        for episode in range(num_episodes):
            state, _ = env.reset()
            state = torch.tensor(state, dtype=torch.float32, device=self.device)
            done = False
            ep_reward = 0.0

            while not done:
                action = self.select_action(state)
                next_state, reward, done, _, _ = env.step(action)
                next_state_tensor = torch.tensor(next_state, dtype=torch.float32, device=self.device)
                ep_reward += reward

                self.on_step(state, action, reward, next_state_tensor, done, is_training)
                state = next_state_tensor

            ep_rewards.append(ep_reward)
            print(f"Episode {episode + 1} finished with reward: {ep_reward}")

        env.close()
        print("All episodes finished.")
        return ep_rewards


class RandomAgent(Agent):
    """
    A simple random agent for reinforcement learning tasks.
    """

    def __init__(self, env_name='CartPole-v1'):
        super().__init__(env_name)
        self.memory = ReplayMemory(capacity=10000)

    def select_action(self, state):
        """
        Select a random action from the environment's action space.
        Args:
            state: The current state of the environment (not used in random action selection).
        Returns:
            action: A random action sampled from the environment's action space.
        """

        # Create the environment to sample an action
        env = gymnasium.make(self.env_name)
        action = env.action_space.sample()
        env.close()
        return action

    def on_step(self, state, action, reward, next_state, done, is_training):
        if is_training:
            self.memory.push((state, action, reward, next_state, done)) # Store the transition in memory




class DQNAgent(Agent):
    """
    A Deep Q-Network (DQN) agent for reinforcement learning tasks.
    This agent uses a neural network to approximate the Q-values for each action given a state input.

    Reference:
        https://github.com/johnnycode8/dqn_pytorch
    """


    def __init__(self, env_name='CartPole-v1', hidden_dim=256):
        """
        Initialize the DQN agent with the specified environment and hidden layer dimensions.
        Args:
            env_name (str): The name of the environment to use.
            hidden_dim (int): The number of neurons in the hidden layers of the DQN model.
        """
        
        super().__init__(env_name)
        self.env = gymnasium.make(env_name)
        self.model = DQN(input_dim=self.env.observation_space.shape[0],
                         output_dim=self.env.action_space.n,
                         hidden_dim=hidden_dim).to(self.device) # DQN model initialization
        self.target_model = DQN(input_dim=self.env.observation_space.shape[0],
                                output_dim=self.env.action_space.n,
                                hidden_dim=hidden_dim).to(self.device) # Target DQN model initialization
        
        self.loss_nn = nn.MSELoss()  # Loss function for DQN
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.memory = ReplayMemory(capacity=10000)
        self.epsilon = 1.0
        self.epsilon_min = 0 # a minimum epsilon value to ensure exploration
        self.epsilon_decay = 0.995
        self.batch_size = 64
        self.gamma = 0.99
        self.sync_target_steps = 1000
        self.epsilon_history = []
        self.step_count = 0

    def select_action(self, state):
        """
        Select an action based on the current state using an epsilon-greedy strategy.
        It is a balance between exploration (random actions) and exploitation (using the model to select the best action).
        Use epsilon decay in order to reduce the exploration over time as the agent learns.

        Args:
            state (torch.Tensor): The current state of the environment.
        Returns:
            int: The selected action.
        """
        if random.random() < self.epsilon:
            return self.env.action_space.sample() #-> Exploration: select a random action
        
        with torch.no_grad():
            q_values = self.model(state.unsqueeze(0))
            return q_values.argmax().item() # -> Exploitation: select the action with the highest Q-value

    def on_step(self, state, action, reward, next_state, done, is_training):
        """
        This method is used to handle the logic after taking an action.
        It updates the agent's memory, performs learning steps, and manages the epsilon-greedy exploration strategy.
        """
        if is_training:
            self.memory.push((state, action, reward, next_state, done)) # Store the transition in memory
            self.step_count += 1

            if len(self.memory) > self.batch_size:
                # Start training when there are enough transitions to sample a batch
                batch = self.memory.sample(self.batch_size)
                self.optimize(batch) # update parameters using the sampled batch

            if self.step_count % self.sync_target_steps == 0:
                # Sync target model with the current model after a certain number of steps

                self.target_model.load_state_dict(self.model.state_dict())
                
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            self.epsilon_history.append(self.epsilon)


    def optimize(self, batch):
        """
        Optimize the DQN model using a batch of transitions sampled from the replay memory.
        Updates parameters of the model based on the Bellman equation.

        This method computes the loss between the predicted Q-values and the expected Q-values,
        and performs a gradient descent step to minimize this loss.

        In order to prevent instability, it uses a target network to compute the expected Q-values.


        Args:
            batch (list): A list of tuples containing (state, action, reward, next_state, done).
        """
        
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.stack(states)
        next_states = torch.stack(next_states)
        actions = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float, device=self.device)
        dones = torch.tensor(dones, dtype=torch.float, device=self.device)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze() # this is model's Q(s,a) predictions for all actions in the batch using the model
        # dimensions: [batch_size]

        with torch.no_grad():
            # This computes the expected Q values using the target network
            
            next_q_values = self.target_model(next_states).max(1)[0] # Get the maximum Q value for the next states
            expected_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        # Compute loss as predicted Q values vs expected Q values 
        loss = self.loss_nn(q_values, expected_q_values)
        self.optimizer.zero_grad() 
        loss.backward()
        self.optimizer.step() # update the model parameters


if __name__ == "__main__":
    agent = DQNAgent(env_name="CartPole-v1", hidden_dim=512)
    rewards = agent.run(num_episodes=1000, is_training=True, render=False)
    print("Rewards per episode:", rewards)
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Rewards per Episode')
    plt.savefig("rewards.png")