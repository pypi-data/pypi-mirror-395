"""
train.py
This script sets up the training loop for a custom offline CQL training using TorchRL.
"""

#modules
import torch
from typing import Any, Dict, Tuple
from copy import deepcopy
from torch import nn
import minari
from torch.optim import Adam
import numpy as np
import torch.nn.functional as F

# own modules
from models import ActorCriticModel, Critic, GaussianActor, Scalar

# Hyperparameters
GAMMA = 0.99  # Discount factor
LEARNING_RATE = 0.001  # Learning rate
BATCH_SIZE = 64  # Batch size
MEMORY_SIZE = 10000  # Replay buffer size (not used in MinariDataLoader)
TARGET_UPDATE = 100  # Target network update frequency (handled by SoftUpdate)
NUM_EPOCHS = 50  # Number of training epochs
dataset_id = "minigrid/BabyAI-Pickup/optimal-fullobs-v0"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


from copy import deepcopy
from torch import nn
import torch
from typing import Dict, Any

class SACAgent:
    def __init__(
        self,
        actor: GaussianActor,
        critic: Critic,
        actor_optimizer: torch.optim.Optimizer,
        critic_optimizer: torch.optim.Optimizer,
        alpha_lr: float = 1e-4,
        gamma: float = 0.99,
        tau: float = 0.005,
        device: str = "cpu",
    ):
        self.device = device
        self.actor = actor
        self.critic = critic
        self.target_critic = deepcopy(critic)

        self.actor_optimizer = actor_optimizer
        self.critic_optimizer = critic_optimizer

        self.gamma = gamma
        self.tau = tau

        # Entropy temperature (alpha)
        self.target_entropy = -actor.action_dim
        self.log_alpha = torch.tensor([0.0], dtype=torch.float32, device=self.device, requires_grad=True)
        self.alpha_optimizer = torch.optim.Adam([self.log_alpha], lr=alpha_lr)
        self.alpha = self.log_alpha.exp().detach()

    def compute_alpha_loss(self, states):
        actions, log_probs = self.actor.get_action(states)
        loss = (-self.log_alpha * (log_probs + self.target_entropy)).mean()
        return loss

    def compute_actor_loss(self, states):
        actions, log_probs = self.actor.get_action(states)
        q_values = self.critic(states, actions)
        loss = (self.alpha * log_probs - q_values).mean()
        return loss, log_probs.mean().item()

    def compute_critic_loss(self, states, actions, rewards, next_states, dones):
        with torch.no_grad():
            next_actions, next_log_probs = self.actor.get_action(next_states)
            q_next = self.target_critic(next_states, next_actions)
            q_target = rewards + self.gamma * (1 - dones) * (q_next - self.alpha * next_log_probs)

        q_current = self.critic(states, actions)
        return nn.MSELoss()(q_current, q_target)

    def update(self, batch):
        states, actions, rewards, next_states, dones = [x.to(self.device) for x in batch]

        # Alpha update
        alpha_loss = self.compute_alpha_loss(states)
        self.alpha_optimizer.zero_grad()
        alpha_loss.backward()
        self.alpha_optimizer.step()
        self.alpha = self.log_alpha.exp().detach()

        # Actor update
        actor_loss, entropy = self.compute_actor_loss(states)
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Critic update
        critic_loss = self.compute_critic_loss(states, actions, rewards, next_states, dones)
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Soft update of target critic
        for target_param, param in zip(self.target_critic.parameters(), self.critic.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau) * target_param.data)

        return {
            "critic_loss": critic_loss.item(),
            "actor_loss": actor_loss.item(),
            "alpha_loss": alpha_loss.item(),
            "entropy": entropy,
            "alpha": self.alpha.item()
        }


class ContinuousCQLAgent:
    """Implements Conservative Q-Learning (CQL) with Soft Actor-Critic (SAC) for offline reinforcement learning.

    This class trains an actor-critic model using a fixed dataset, incorporating CQL regularization to prevent
    overestimation of Q-values and SAC's entropy regularization for exploration. It assumes precomputed state
    embeddings as input, delegating observation preprocessing to another class.

    Attributes:
        discount (float): Discount factor for future rewards.
        target_entropy (float): Target entropy for SAC policy.
        alpha_multiplier (float): Scaling factor for entropy coefficient.
        use_automatic_entropy_tuning (bool): Whether to automatically tune the entropy coefficient.
        soft_target_update_rate (float): Rate for soft target network updates.
        bc_steps (int): Number of steps for behavior cloning before switching to CQL loss.
        target_update_period (int): Frequency of target network updates.
        cql_n_actions (int): Number of actions sampled for CQL regularization.
        cql_importance_sample (bool): Whether to use importance sampling in CQL.
        cql_lagrange (bool): Whether to use Lagrange multipliers for CQL regularization.
        cql_target_action_gap (float): Target action gap for CQL regularization.
        cql_temp (float): Temperature for CQL logsumexp computation.
        cql_alpha (float): Weight for CQL regularization term.
        cql_max_target_backup (bool): Whether to use max target backup in CQL.
        cql_clip_diff_min (float): Minimum clipping value for CQL Q-difference.
        cql_clip_diff_max (float): Maximum clipping value for CQL Q-difference.
        _device (torch.device): Device for computation (e.g., CPU or GPU).
        total_it (int): Total training iterations performed.
        critic_1 (Critic): First Q-function critic.
        critic_2 (Critic): Second Q-function critic.
        target_critic_1 (Critic): Target network for critic_1.
        target_critic_2 (Critic): Target network for critic_2.
        actor (GaussianActor): Stochastic policy network.
        actor_optimizer (torch.optim.Optimizer): Optimizer for the actor.
        critic_1_optimizer (torch.optim.Optimizer): Optimizer for critic_1.
        critic_2_optimizer (torch.optim.Optimizer): Optimizer for critic_2.
        log_alpha (Scalar, optional): Learnable entropy coefficient for SAC.
        alpha_optimizer (torch.optim.Optimizer, optional): Optimizer for log_alpha.
        log_alpha_prime (Scalar): Learnable coefficient for CQL regularization.
        alpha_prime_optimizer (torch.optim.Optimizer): Optimizer for log_alpha_prime.
    """

    def __init__(
        self,
        critic_1: Critic,
        critic_1_optimizer: torch.optim.Optimizer,
        critic_2: Critic,
        critic_2_optimizer: torch.optim.Optimizer,
        actor: GaussianActor,
        actor_optimizer: torch.optim.Optimizer,
        target_entropy: float,
        discount: float = 0.99,
        alpha_multiplier: float = 1.0,
        use_automatic_entropy_tuning: bool = True,
        soft_target_update_rate: float = 5e-3,
        bc_steps: int = 100000,
        target_update_period: int = 1,
        cql_n_actions: int = 10,
        cql_importance_sample: bool = True,
        cql_lagrange: bool = False,
        cql_target_action_gap: float = -1.0,
        cql_temp: float = 1.0,
        cql_alpha: float = 5.0,
        cql_max_target_backup: bool = False,
        cql_clip_diff_min: float = -np.inf,
        cql_clip_diff_max: float = np.inf,
        device: str = "cpu",
    ):
        """Initialize the ContinuousCQL model.

        Args:
            critic_1 (Critic): First Q-function critic.
            critic_1_optimizer (torch.optim.Optimizer): Optimizer for critic_1.
            critic_2 (Critic): Second Q-function critic.
            critic_2_optimizer (torch.optim.Optimizer): Optimizer for critic_2.
            actor (GaussianActor): Stochastic policy network.
            actor_optimizer (torch.optim.Optimizer): Optimizer for the actor.
            target_entropy (float): Target entropy for SAC policy.
            discount (float, optional): Discount factor for future rewards. Defaults to 0.99.
            alpha_multiplier (float, optional): Scaling factor for entropy coefficient. Defaults to 1.0.
            use_automatic_entropy_tuning (bool, optional): Whether to tune entropy coefficient. Defaults to True.
            soft_target_update_rate (float, optional): Rate for target network updates. Defaults to 5e-3.
            bc_steps (int, optional): Steps for behavior cloning. Defaults to 100000.
            target_update_period (int, optional): Frequency of target updates. Defaults to 1.
            cql_n_actions (int, optional): Number of actions for CQL regularization. Defaults to 10.
            cql_importance_sample (bool, optional): Use importance sampling in CQL. Defaults to True.
            cql_lagrange (bool, optional): Use Lagrange multipliers for CQL. Defaults to False.
            cql_target_action_gap (float, optional): Target action gap for CQL. Defaults to -1.0.
            cql_temp (float, optional): Temperature for CQL logsumexp. Defaults to 1.0.
            cql_alpha (float, optional): Weight for CQL regularization. Defaults to 5.0.
            cql_max_target_backup (bool, optional): Use max target backup in CQL. Defaults to False.
            cql_clip_diff_min (float, optional): Minimum clipping for CQL Q-difference. Defaults to -inf.
            cql_clip_diff_max (float, optional): Maximum clipping for CQL Q-difference. Defaults to inf.
            device (str, optional): Computation device ('cpu' or 'cuda'). Defaults to 'cpu'.
        """
        super().__init__()

        # Initialize hyperparameters
        self.discount = discount
        self.target_entropy = target_entropy
        self.alpha_multiplier = alpha_multiplier
        self.use_automatic_entropy_tuning = use_automatic_entropy_tuning
        self.soft_target_update_rate = soft_target_update_rate
        self.bc_steps = bc_steps
        self.target_update_period = target_update_period
        self.cql_n_actions = cql_n_actions
        self.cql_importance_sample = cql_importance_sample
        self.cql_lagrange = cql_lagrange
        self.cql_target_action_gap = cql_target_action_gap
        self.cql_temp = cql_temp
        self.cql_alpha = cql_alpha
        self.cql_max_target_backup = cql_max_target_backup
        self.cql_clip_diff_min = cql_clip_diff_min
        self.cql_clip_diff_max = cql_clip_diff_max
        self._device = torch.device(device)

        # Initialize training counter
        self.total_it = 0

        # Initialize models and move to device
        self.critic_1 = critic_1.to(self._device)
        self.critic_2 = critic_2.to(self._device)
        self.target_critic_1 = deepcopy(critic_1).to(self._device)
        self.target_critic_2 = deepcopy(critic_2).to(self._device)
        self.actor = actor.to(self._device)

        # Initialize optimizers
        self.actor_optimizer = actor_optimizer
        self.critic_1_optimizer = critic_1_optimizer
        self.critic_2_optimizer = critic_2_optimizer

        # Initialize entropy coefficient for SAC
        if self.use_automatic_entropy_tuning:
            self.log_alpha = Scalar(0.0).to(self._device)
            self.alpha_optimizer = torch.optim.Adam(
                self.log_alpha.parameters(), lr=3e-4
            )
        else:
            self.log_alpha = None

        # Initialize CQL regularization coefficient
        self.log_alpha_prime = Scalar(1.0).to(self._device)
        self.alpha_prime_optimizer = torch.optim.Adam(
            self.log_alpha_prime.parameters(), lr=3e-4
        )

    def update_target_network(self, soft_target_update_rate: float):
        """Update target networks using soft updates.

        Args:
            soft_target_update_rate (float): Rate for updating target networks.
        """
        # Update critic_1 target
        for target_param, param in zip(self.target_critic_1.parameters(), self.critic_1.parameters()):
            target_param.data.copy_(
                target_param.data * (1.0 - soft_target_update_rate) + param.data * soft_target_update_rate
            )
        # Update critic_2 target
        for target_param, param in zip(self.target_critic_2.parameters(), self.critic_2.parameters()):
            target_param.data.copy_(
                target_param.data * (1.0 - soft_target_update_rate) + param.data * soft_target_update_rate
            )

    def _alpha_and_alpha_loss(self, state_embedding: torch.Tensor, log_pi: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute the entropy coefficient and its loss for SAC.

        Args:
            state_embedding (torch.Tensor): State embedding tensor of shape [batch_size, state_dim].
            log_pi (torch.Tensor): Log-probability of sampled actions of shape [batch_size, 1].

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Entropy coefficient (alpha) and its loss.
        """
        if self.use_automatic_entropy_tuning:
            alpha_loss = -(self.log_alpha.value * (log_pi + self.target_entropy).detach()).mean()
            alpha = self.log_alpha.value.exp() * self.alpha_multiplier
        else:
            alpha_loss = torch.tensor(0.0, device=self._device)
            alpha = torch.tensor(self.alpha_multiplier, device=self._device)
        return alpha, alpha_loss

    def _policy_loss(
        self,
        state_embedding: torch.Tensor,
        actions: torch.Tensor,
        new_actions: torch.Tensor,
        alpha: torch.Tensor,
        log_pi: torch.Tensor,
    ) -> torch.Tensor:
        """Compute the policy loss for the actor.

        During the initial bc_steps, uses behavior cloning loss. Afterward, uses SAC loss with entropy regularization.

        Args:
            state_embedding (torch.Tensor): State embedding tensor of shape [batch_size, state_dim].
            actions (torch.Tensor): Ground-truth actions from the dataset of shape [batch_size, action_dim].
            new_actions (torch.Tensor): Actions sampled from the policy of shape [batch_size, action_dim].
            alpha (torch.Tensor): Entropy coefficient scalar.
            log_pi (torch.Tensor): Log-probability of sampled actions of shape [batch_size, 1].

        Returns:
            torch.Tensor: Policy loss scalar.
        """
        if self.total_it <= self.bc_steps:
            # Behavior cloning loss
            _, log_probs = self.actor.get_action(state_embedding)
            policy_loss = (alpha * log_pi - log_probs).mean()
        else:
            # SAC loss: maximize Q-value minus entropy penalty
            q_new_actions = torch.min(
                self.critic_1(state_embedding, new_actions),
                self.critic_2(state_embedding, new_actions),
            )
            policy_loss = (alpha * log_pi - q_new_actions).mean()
        return policy_loss

    def _q_loss(
        self,
        state_embedding: torch.Tensor,
        actions: torch.Tensor,
        next_state_embedding: torch.Tensor,
        rewards: torch.Tensor,
        dones: torch.Tensor,
        alpha: torch.Tensor,
        log_dict: Dict,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute the Q-function loss with CQL regularization.

        Args:
            state_embedding (torch.Tensor): State embedding tensor of shape [batch_size, state_dim].
            actions (torch.Tensor): Actions from the dataset of shape [batch_size, action_dim].
            next_state_embedding (torch.Tensor): Next state embedding tensor of shape [batch_size, state_dim].
            rewards (torch.Tensor): Rewards from the dataset of shape [batch_size, 1].
            dones (torch.Tensor): Done flags from the dataset of shape [batch_size, 1].
            alpha (torch.Tensor): Entropy coefficient scalar.
            log_dict (Dict): Dictionary to store logging metrics.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Total Q-function loss and alpha_prime loss.
        """
        # Compute Q-value predictions
        q1_predicted = self.critic_1(state_embedding, actions)
        q2_predicted = self.critic_2(state_embedding, actions)

        # Compute target Q-values
        if self.cql_max_target_backup:
            new_next_actions, next_log_pi = self.actor.get_action(next_state_embedding)
            target_q_values = torch.min(
                self.target_critic_1(next_state_embedding, new_next_actions),
                self.target_critic_2(next_state_embedding, new_next_actions),
            )
        else:
            new_next_actions, next_log_pi = self.actor.get_action(next_state_embedding)
            target_q_values = torch.min(
                self.target_critic_1(next_state_embedding, new_next_actions),
                self.target_critic_2(next_state_embedding, new_next_actions),
            )

        # Include entropy in target Q-values
        target_q_values = target_q_values - alpha * next_log_pi
        td_target = rewards + (1.0 - dones) * self.discount * target_q_values.detach()
        qf1_loss = F.mse_loss(q1_predicted, td_target)
        qf2_loss = F.mse_loss(q2_predicted, td_target)

        # CQL regularization
        batch_size = actions.shape[0]
        action_dim = actions.shape[-1]
        cql_random_actions = actions.new_empty(
            (batch_size, self.cql_n_actions, action_dim), requires_grad=False
        ).uniform_(-1, 1)
        cql_current_actions, cql_current_log_pis = self.actor.get_action(state_embedding)
        cql_next_actions, cql_next_log_pis = self.actor.get_action(next_state_embedding)

        cql_q1_rand = self.critic_1(state_embedding, cql_random_actions)
        cql_q2_rand = self.critic_2(state_embedding, cql_random_actions)
        cql_q1_current_actions = self.critic_1(state_embedding, cql_current_actions)
        cql_q2_current_actions = self.critic_2(state_embedding, cql_current_actions)
        cql_q1_next_actions = self.critic_1(state_embedding, cql_next_actions)
        cql_q2_next_actions = self.critic_2(state_embedding, cql_next_actions)

        cql_cat_q1 = torch.cat(
            [cql_q1_rand, cql_q1_current_actions.unsqueeze(1), cql_q1_next_actions.unsqueeze(1)],
            dim=1,
        )
        cql_cat_q2 = torch.cat(
            [cql_q2_rand, cql_q2_current_actions.unsqueeze(1), cql_q2_next_actions.unsqueeze(1)],
            dim=1,
        )

        if self.cql_importance_sample:
            random_density = np.log(0.5 ** action_dim)
            cql_cat_q1 = torch.cat(
                [cql_q1_rand - random_density, cql_q1_next_actions.unsqueeze(1), cql_q1_current_actions.unsqueeze(1)],
                dim=1,
            )
            cql_cat_q2 = torch.cat(
                [cql_q2_rand - random_density, cql_q2_next_actions.unsqueeze(1), cql_q2_current_actions.unsqueeze(1)],
                dim=1,
            )

        cql_qf1_ood = torch.logsumexp(cql_cat_q1 / self.cql_temp, dim=1) * self.cql_temp
        cql_qf2_ood = torch.logsumexp(cql_cat_q2 / self.cql_temp, dim=1) * self.cql_temp

        cql_qf1_diff = torch.clamp(
            cql_qf1_ood - q1_predicted,
            self.cql_clip_diff_min,
            self.cql_clip_diff_max,
        ).mean()
        cql_qf2_diff = torch.clamp(
            cql_qf2_ood - q2_predicted,
            self.cql_clip_diff_min,
            self.cql_clip_diff_max,
        ).mean()

        if self.cql_lagrange:
            alpha_prime = torch.clamp(
                torch.exp(self.log_alpha_prime.value), min=0.0, max=1000000.0
            )
            cql_min_qf1_loss = alpha_prime * self.cql_alpha * (cql_qf1_diff - self.cql_target_action_gap)
            cql_min_qf2_loss = alpha_prime * self.cql_alpha * (cql_qf2_diff - self.cql_target_action_gap)
            alpha_prime_loss = (-cql_min_qf1_loss - cql_min_qf2_loss) * 0.5
        else:
            cql_min_qf1_loss = cql_qf1_diff * self.cql_alpha
            cql_min_qf2_loss = cql_qf2_diff * self.cql_alpha
            alpha_prime_loss = torch.tensor(0.0, device=self._device)

        qf_loss = qf1_loss + qf2_loss + cql_min_qf1_loss + cql_min_qf2_loss

        # Update logging dictionary
        log_dict.update(
            dict(
                qf1_loss=qf1_loss.item(),
                qf2_loss=qf2_loss.item(),
                alpha=alpha.item(),
                average_qf1=q1_predicted.mean().item(),
                average_qf2=q2_predicted.mean().item(),
                average_target_q=target_q_values.mean().item(),
                cql_min_qf1_loss=cql_min_qf1_loss.item(),
                cql_min_qf2_loss=cql_min_qf2_loss.item(),
                cql_qf1_diff=cql_qf1_diff.item(),
                cql_qf2_diff=cql_qf2_diff.item(),
            )
        )

        return qf_loss, alpha_prime_loss

    def train(self, batch: Tuple[torch.Tensor, ...]) -> Dict[str, float]:
        """Train the model on a batch of data.

        Args:
            batch (Tuple[torch.Tensor, ...]): Batch of data containing (state_embedding, actions, rewards,
                                              next_state_embedding, dones).

        Returns:
            Dict[str, float]: Dictionary of logging metrics.
        """
        # Unpack batch
        state_embedding, actions, rewards, next_state_embedding, dones = batch
        self.total_it += 1

        # Initialize logging dictionary
        log_dict = {}

        # Sample actions from policy
        new_actions, log_pi = self.actor.get_action(state_embedding)

        # Compute entropy coefficient and loss
        alpha, alpha_loss = self._alpha_and_alpha_loss(state_embedding, log_pi)

        # Compute policy loss
        policy_loss = self._policy_loss(
            state_embedding, actions, new_actions, alpha, log_pi
        )
        log_dict.update(
            dict(
                log_pi=log_pi.mean().item(),
                policy_loss=policy_loss.item(),
                alpha_loss=alpha_loss.item(),
                alpha=alpha.item(),
            )
        )

        # Compute Q-function and CQL loss
        qf_loss, alpha_prime_loss = self._q_loss(
            state_embedding, actions, next_state_embedding, rewards, dones, alpha, log_dict
        )

        # Update entropy coefficient
        if self.use_automatic_entropy_tuning:
            self.alpha_optimizer.zero_grad()
            alpha_loss.backward()
            self.alpha_optimizer.step()

        # Update actor
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()

        # Update critics
        self.critic_1_optimizer.zero_grad()
        self.critic_2_optimizer.zero_grad()
        qf_loss.backward()
        self.critic_1_optimizer.step()
        self.critic_2_optimizer.step()

        # Update CQL regularization coefficient
        if self.cql_lagrange:
            self.alpha_prime_optimizer.zero_grad()
            alpha_prime_loss.backward()
            self.alpha_prime_optimizer.step()

        # Update target networks
        if self.total_it % self.target_update_period == 0:
            self.update_target_network(self.soft_target_update_rate)

        return log_dict

    def state_dict(self) -> Dict[str, Any]:
        """Get the state dictionary of the model.

        Returns:
            Dict[str, Any]: State dictionary containing model and optimizer states.
        """
        state_dict = {
            "actor": self.actor.state_dict(),
            "critic1": self.critic_1.state_dict(),
            "critic2": self.critic_2.state_dict(),
            "critic1_target": self.target_critic_1.state_dict(),
            "critic2_target": self.target_critic_2.state_dict(),
            "critic_1_optimizer": self.critic_1_optimizer.state_dict(),
            "critic_2_optimizer": self.critic_2_optimizer.state_dict(),
            "actor_optim": self.actor_optimizer.state_dict(),
            "cql_log_alpha": self.log_alpha_prime.state_dict(),
            "cql_log_alpha_optim": self.alpha_prime_optimizer.state_dict(),
            "total_it": self.total_it,
        }
        if self.use_automatic_entropy_tuning:
            state_dict.update({
                "sac_log_alpha": self.log_alpha.state_dict(),
                "sac_log_alpha_optim": self.alpha_optimizer.state_dict(),
            })
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any]):
        """Load the state dictionary into the model.

        Args:
            state_dict (Dict[str, Any]): State dictionary to load.
        """
        self.actor.load_state_dict(state_dict["actor"])
        self.critic_1.load_state_dict(state_dict["critic1"])
        self.critic_2.load_state_dict(state_dict["critic2"])
        self.target_critic_1.load_state_dict(state_dict["critic1_target"])
        self.target_critic_2.load_state_dict(state_dict["critic2_target"])
        self.critic_1_optimizer.load_state_dict(state_dict["critic_1_optimizer"])
        self.critic_2_optimizer.load_state_dict(state_dict["critic_2_optimizer"])
        self.actor_optimizer.load_state_dict(state_dict["actor_optim"])
        self.log_alpha_prime.load_state_dict(state_dict["cql_log_alpha"])
        self.alpha_prime_optimizer.load_state_dict(state_dict["cql_log_alpha_optim"])
        if self.use_automatic_entropy_tuning:
            self.log_alpha.load_state_dict(state_dict["sac_log_alpha"])
            self.alpha_optimizer.load_state_dict(state_dict["sac_log_alpha_optim"])
        self.total_it = state_dict["total_it"]





if __name__ == "__main__":
    import torch
    import minari
    from utils import ReplayMemory
    from models import ActorCriticModel
    from train import OfflineRLTrainer  # Asumiendo que guardaste la clase ahí

    # --- 1. Load Minari dataset and memory ---
    dataset_id = "minigrid/BabyAI-OneRoomS12/optimal-fullobs-v0"
    dataset = minari.load_dataset(dataset_id)

    memory = ReplayMemory(capacity=10_000, seed=42)
    memory.load_minari_dataset(dataset)
    print(f"[INFO] Loaded dataset {dataset_id} with {len(memory.memory)} samples.")

    # --- 2. Infer dimensions from the first sample ---
    sample_state = next(iter(memory.memory))[0]  # state is already encoded
    state_dim = sample_state.shape[0]
    action_dim = dataset.action_space.n

    print(f"[INFO] State dim: {state_dim}, Action dim: {action_dim}")

    # --- 3. Create Actor-Critic model ---
    model = ActorCriticModel(
        state_dim=state_dim,
        action_dim=action_dim,
        actor_type='discrete'
    )

    # --- 4. Create offline trainer with uniform CQL ---
    trainer = OfflineRLTrainer(
        model=model,
        memory=memory,
        batch_size=64,
        gamma=0.99,
        lr=3e-4,
        cql_alpha=1.0,
        use_cql=True
    )

    # --- 5. Offline training loop ---
    print("[INFO] Starting training...")
    for epoch in range(1000):
        loss = trainer.train_step()
        print(f"Epoch {epoch:02d}: Loss = {loss:.4f}")