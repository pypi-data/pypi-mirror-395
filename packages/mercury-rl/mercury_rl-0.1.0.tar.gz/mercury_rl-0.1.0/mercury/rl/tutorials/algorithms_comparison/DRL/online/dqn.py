import torch 
from torch import nn
import torch.nn.functional as F

class DQN(nn.Module):
    """
    A simple Deep Q-Network (DQN) implementation.
    This network aims to approximate the Q-values for each action given a state input.

    Args:
        input_dim (int): The dimension of the input state.
        output_dim (int): The number of possible actions (output dimension).
        hidden_dim (int, optional): The number of neurons in the hidden layers. Default is 256.
    """

    def __init__(self, input_dim, output_dim, hidden_dim=256):
        super(DQN, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Forward pass through the network.
        Args:
            x (torch.Tensor): Input tensor representing the state. Dimensions: [batch_size, *].
        Returns:
            torch.Tensor: Output tensor containing Q-values for each action. Dimensions: [batch_size, output_dim].
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    

if __name__ == "__main__":
    # Example usage
    state_dim = 12
    action_dim = 4 # 4 Actions to draw probabilities from
    model = DQN(input_dim=state_dim, output_dim=action_dim)

    state = torch.randn(1, state_dim)  # Example state
    output = model(state)  # Forward pass
    print("Output Q-values:", output)
