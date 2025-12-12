"""
models.py
This is a custom implementation of a DQL model using PyTorch.
This model is designed to work with the Minari dataset and includes an observation encoder,
a policy network, and a value network.
"""

# modules
import torch
import torch.nn as nn
from torchrl.modules.tensordict_module.actors import ProbabilisticActor
from torchrl.modules.tensordict_module.common import SafeModule
from torchrl.modules.tensordict_module.actors import ValueOperator
from abc import abstractmethod
from typing import Any, Optional

# constants
LOG_STD_MAX = 2
LOG_STD_MIN = -5


class EmbeddingFuncion(torch.autograd.Function):
    """
    Class for the implementation of the forward and backward pass of
    the Embedding layer.
    """

    @staticmethod
    def forward(
        ctx: Any,
        inputs: torch.Tensor,
        weight: torch.Tensor,
        padding_idx: int,
    ) -> torch.Tensor:
        """
        This is the forward method of the Embedding layer.

        Args:
            ctx: context for saving elements for the backward.
            inputs: input tensor. Dimensions: [batch].

        Returns:
            outputs tensor. Dimensions: [batch, output dim].
        """

        # compute embeddings
        outputs: torch.Tensor = weight[inputs, :]

        # save tensors for the backward
        ctx.save_for_backward(inputs, weight, torch.tensor(padding_idx))

        return outputs

    @staticmethod
    def backward(  # type: ignore
        ctx: Any, grad_outputs: torch.Tensor
    ) -> tuple[None, torch.Tensor, None]:
        """
        This method is the backward of the Embedding layer.

        Args:
            ctx: context for loading elements from the forward.
            grad_output: outputs gradients. Dimensions:
                [batch, output dim].

        Returns:
            None value.
            inputs gradients. Dimensions: [batch].
            None value.
        """

        inputs, weight, padding_idx = ctx.saved_tensors
        batch = inputs.shape[0]
        grad_inputs = torch.zeros_like(weight)
        
        for b in range(batch): 
            
            word_idx = inputs[b]

            if word_idx != padding_idx:
                grad_inputs[word_idx] += grad_outputs[b]

        return None, grad_inputs, None



class Embedding(torch.nn.Module):
    """
    This is the class that represents the Embedding Layer.
    """

    padding_idx: int

    def __init__(
        self, num_embeddings: int, embedding_dim: int, padding_idx: Optional[int] = None
    ) -> None:
        """
        This method is the constructor of the Embedding layer.
        """

        # call super class constructor
        super().__init__()

        # define attributes
        self.weight: torch.nn.Parameter = torch.nn.Parameter(
            torch.empty(num_embeddings, embedding_dim)
        )

        # init parameters correctly
        self.reset_parameters()

        # set padding idx
        self.padding_idx = padding_idx if padding_idx is not None else -1

        self.fn = EmbeddingFuncion.apply

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """
        This is the forward pass for the class.

        Args:
            inputs: inputs tensor. Dimensions: [batch].

        Returns:
            outputs tensor. Dimensions: [batch, output dim].
        """

        return self.fn(inputs, self.weight, self.padding_idx)

    @torch.no_grad()
    def reset_parameters(self) -> None:
        torch.nn.init.normal_(self.weight)
import torch
import torch.nn as nn
import torch.nn.functional as F

import torch
import torch.nn as nn

import torch
import torch.nn as nn

import torch
import torch.nn as nn


class MinariObsEncoder(nn.Module):
    """
    Encodes a Minari observation into a compact embedding (e.g., 16D).
    Combines a CNN for image features with embeddings for direction and mission.
    """

    def __init__(self, direction_dim: int, mission_dim: int = 0, output_dim: int = 16):
        super().__init__()

        self.direction_dim = direction_dim
        self.mission_dim = mission_dim
        self.use_mission = mission_dim > 0
        self.output_dim = output_dim

        # CNN for image feature extraction
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Flatten()
        )
        self._cnn_output_dim = None  # Inferred on first forward

        # Smaller embedding dimensions
        self.dir_embed_dim = 4
        self.mission_embed_dim = 8

        self.direction_embedding = nn.Embedding(direction_dim, self.dir_embed_dim)

        if self.use_mission:
            self.mission_embedding = nn.Embedding(mission_dim, self.mission_embed_dim)

        self.encoder = None  # Lazy init MLP after knowing input size

    def forward(self, obs_td):
        device = next(self.parameters()).device

        # Process image
        image = obs_td['image']
        if image.ndim == 3 and image.shape[0] != 3:
            image = image.permute(2, 0, 1)  # [H, W, C] → [C, H, W]
        image = image.unsqueeze(0).float().to(device) / 255.0
        img_feat = self.cnn(image).squeeze(0)

        # Process direction
        direction = int(obs_td['direction'])
        dir_tensor = torch.tensor([direction], device=device).long()
        dir_feat = self.direction_embedding(dir_tensor).squeeze(0)

        # Optional mission
        if self.use_mission and 'mission' in obs_td:
            mission = int(obs_td['mission'])
            mission_tensor = torch.tensor([mission], device=device).long()
            mission_feat = self.mission_embedding(mission_tensor).squeeze(0)
            full_feat = torch.cat([img_feat, dir_feat, mission_feat], dim=-1)
        else:
            full_feat = torch.cat([img_feat, dir_feat], dim=-1)

        # Lazy initialize final projection
        if self._cnn_output_dim is None:
            self._cnn_output_dim = img_feat.shape[0]
            total_input_dim = self._cnn_output_dim + self.dir_embed_dim
            if self.use_mission:
                total_input_dim += self.mission_embed_dim

            # Autoencoder for dimensionality reduction
            self.encoder = nn.Sequential(
                nn.Linear(total_input_dim, 128),
                nn.ReLU(),
                nn.Linear(128, self.output_dim)
            ).to(device)

        return self.encoder(full_feat)


"""
AC Implementation
"""

class Actor(nn.Module):
    """
    Base class for the actor network in reinforcement learning.
    
    This class takes an state as input and outputs a probability distribution over action space.

    Args:
        state_dim (int): Dimension of the state space.
        action_dim (int): Dimension of the action space.
    """
    
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
    
    @abstractmethod
    def forward(self, obs):
        """
        Forward pass through the actor network.
        
        Args:
            obs (torch.Tensor): Input observation tensor of shape [B, state_dim].
        
        Returns:
            torch.Tensor: Output action tensor of shape [B, action_dim].
        """
        raise NotImplementedError("Forward method must be implemented in subclasses.")
    
class DiscreteActor(Actor): 
    """
    Discrete policy network (Actor) for discrete action spaces in offline RL.

    Given an input state, the actor outputs a probability distribution over actions.
    The action is sampled from this distribution.

    Args:
        state_dim (int): Dimension of the state space.
        action_dim (int): Dimension of the action space.
    """

    def __init__(self, state_dim, action_dim):
        super().__init__(state_dim, action_dim)

        self.net = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim)
        )

    def forward(self, obs):
        """
        Forward pass through the actor network.

        Args:
            obs (torch.Tensor): State input of shape [B, state_dim].

        Returns:
            torch.Tensor: Action probabilities of shape [B, action_dim].
        """
        return self.net(obs)  # Output logits for each action
    
    @torch.no_grad()  # Disable gradient computation for inference
    def get_action(self, obs):
        """
        Samples an action from the policy distribution.

        Args:
            obs (torch.Tensor): State input. Shape: [B, state_dim]

        Returns:
            action (torch.Tensor): Sampled action. Shape: [B, action_dim]
            log_prob (torch.Tensor): Log-probability of the sampled action. Shape: [B, 1]
        """
        logits = self(obs)
        action_probs = torch.softmax(logits, dim=-1)  # Convert logits to probabilities
        dist = torch.distributions.Categorical(action_probs)  # Create categorical distribution
        action = dist.sample()  #
        log_prob = dist.log_prob(action).unsqueeze(-1) 
        return action, log_prob  # Return action and log-probability

class Scalar(nn.Module):
    """
    A simple scalar module that outputs a constant value.
    
    This module is useful for learnable parameters such as entropy in SAC or regularization in CQL
    """
    
    def __init__(self, constant):
        super().__init__()
        self.constant = nn.Parameter(torch.tensor(constant, dtype=torch.float32))

    @property
    def value(self) -> nn.Parameter:
        """
        Returns the constant value of the scalar module.
        
        Returns:
            nn.Parameter: The constant value as a parameter.
        """
        return self.constant
    

class GaussianActor(Actor):
    """
    Gaussian policy network (Actor) for continuous action spaces in offline RL.

    Given an input state, the actor outputs the parameters of a Gaussian distribution
    (mean and standard deviation), applies a `tanh` squashing function, and rescales
    the action to match the environment's action space bounds.

    The sampling uses the reparameterization trick:  
        π(a|s) = tanh(N(mean, std)) × scale + bias

    Args:
        state_dim (int): Dimension of the state space.
        action_dim (int): Dimension of the action space.
    
    Reference:
    - CleanRL's SAC implementation:
      https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/sac_continuous_action.py
    """

    def __init__(self, state_dim, action_dim):
        super().__init__(state_dim, action_dim)

        self.net = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU()
        )

        self.fc_mean = nn.Linear(256, action_dim)
        self.fc_logstd = nn.Linear(256, action_dim)

        # Action rescaling
        self.register_buffer("action_scale", torch.ones(action_dim))
        self.register_buffer("action_bias", torch.zeros(action_dim))


    def forward(self, obs):
        """
        Forward pass through the actor network.

        Args:
            obs (torch.Tensor): State input of shape [B, state_dim].

        Returns:
            loc (torch.Tensor): Mean of the action distribution. Shape: [B, act_dim].
            log_std (torch.Tensor): Log std of the action distribution. Shape: [B, act_dim].
        """
        x = self.net(obs)
        loc = self.fc_mean(x) # compute mean of the action distribution
        log_std = torch.tanh(self.fc_logstd(x)) # compute log standard deviation; [-1, 1] range

        log_std = LOG_STD_MIN + 0.5 * (LOG_STD_MAX - LOG_STD_MIN) * (log_std + 1) # scale to [LOG_STD_MIN, LOG_STD_MAX]
        
        return loc, log_std

    @torch.no_grad()  
    def get_action(self, obs):
        """
        Samples an action using the reparameterization trick.

        Args:
            obs (torch.Tensor): State input. Shape: [B, state_dim]

        Returns:
            action (torch.Tensor): Sampled and scaled action.
            log_prob (torch.Tensor): Log-probability of the sampled action.
            mean (torch.Tensor): Mean of the distribution after squashing and scaling.
        """

        # Get normal distribution to sample actions 
        loc, log_std = self(obs)
        std = log_std.exp() 
        normal = torch.distributions.Normal(loc, std) # get Gaussian distribution

        # Use rsample() instead of sample() to enable backpropagation through the sampled actions (reparameterization trick)
        x_t = normal.rsample() 
        y_t = torch.tanh(x_t) 
        action = y_t * self.action_scale + self.action_bias # linear transformation to rescale the action

        # Compute log probability of the action
        log_prob = normal.log_prob(x_t)
        log_prob -= torch.log(self.action_scale * (1 - y_t.pow(2)) + 1e-6) # log probability of the squashed action (Jacobian of tanh)
        log_prob = log_prob.sum(dim=-1, keepdim=True)


        # The log-probability gives an idea of how likely the action is under the policy.
        
        return action, log_prob




class Critic(nn.Module):
    """
    Evaluates the value of state-action pairs using a neural network.
    Approximates the Q-value function for the given observation and action.
    

    Args:
        state_dim (int): The dimension of the state space.
        act_dim (int): The dimension of the action space.
    """
    def __init__(self, state_dim, act_dim, hidden_dim=256):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state_dim + act_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, obs, action):
        """
        Forward pass through the critic network.
        Args:
            obs (torch.Tensor): The input observation tensor.
            action (torch.Tensor): The input action tensor.
        Outputs:
            torch.Tensor: Estimated value for the state-action pair.
            Dimensions: [B, 1]
        """
        x = torch.cat([obs, action], dim=-1) 
        return self.net(x).clamp(min=-1e3, max=1e3)  # Clamp the output to avoid extreme values


class ActorCriticModel(nn.Module):
    """
    Actor-Critic model that combines both actor and critic networks.
    
    Args:
        state_dim (int): Dimension of the state space.
        action_dim (int): Dimension of the action space.
        actor_type (str): Type of actor network ('discrete' or 'continuous').
        hidden_dim (int): Dimension of the hidden layers in the networks.
    """
    
    def __init__(self, state_dim, action_dim, actor_type='continuous', hidden_dim=256):
        super().__init__()
        
        if actor_type == 'discrete':
            self.actor = DiscreteActor(state_dim, action_dim)
        elif actor_type == 'continuous':
            self.actor = GaussianActor(state_dim, action_dim)
        else:
            raise ValueError("actor_type must be either 'discrete' or 'continuous'")
        
        self.critic = Critic(state_dim, action_dim, hidden_dim)

    def forward(self, obs):
        """
        Forward pass through the actor-critic model.
        Args:
            obs (torch.Tensor): Input observation tensor of shape [B, state_dim].
        Returns:
            action (torch.Tensor): Sampled action tensor of shape [B, action_dim].
            log_prob (torch.Tensor): Log-probability of the sampled action.
            value (torch.Tensor): Estimated value for the state-action pair.
        """
        action, log_prob, _ = self.actor.get_action(obs)
        value = self.critic(obs, action)
        return action, log_prob, value
  
