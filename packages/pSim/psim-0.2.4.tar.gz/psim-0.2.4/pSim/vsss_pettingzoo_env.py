"""
VSSSPettingZooEnv - PettingZoo Multi-Agent Environment for Very Small Size Soccer

This environment extends BaseEnv to provide PettingZoo ParallelEnv interface
for multi-agent deep reinforcement learning (MADRL).
"""

import sys
import os
from typing import Any, Dict, List, Optional, Tuple
from copy import copy
import functools

import numpy as np
import pygame
import gymnasium as gym

from pettingzoo import ParallelEnv
from pettingzoo.test import parallel_api_test

from .vsss_base_env import BaseVSSSEnv
from .modules.OUNoise import OrnsteinUhlenbeckNoise
from .modules.render_vsss import RenderVSSS
from .modules.env_description import ObservationSystem

sys.dont_write_bytecode = True

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.append(cwd)

M2P = 400


class VSSSPettingZooEnv(BaseVSSSEnv, ParallelEnv):
    """PettingZoo environment for Very Small Size Soccer (VSSS).

    This environment provides a multi-agent interface compatible with PettingZoo
    for training multiple agents simultaneously using MADRL algorithms.
    """

    metadata = {
        "name": "VSSS_pettingzoo_v0",
        "render_modes": ["human", "rgb_array"],
        "render_fps": 60
    }

    def __init__(
        self,
        render_mode: Optional[str] = None,
        scenario: str = "formation",
        num_agent_robots: int = 1,
        num_adversary_robots: int = 0,
        color_team: str = "blue",
        truncated_time: int = 600,
    ):
        """Initialize VSSSPettingZooEnv.

        Args:
            render_mode: Rendering mode ("human", "rgb_array", or None)
            scenario: Game scenario to use ("formation" or "full_random")
            num_agent_robots: Number of agent robots
            num_adversary_robots: Number of adversary robots
            color_team: Color of agent team ("blue" or "yellow")
        """
        # Initialize BaseEnv
        BaseVSSSEnv.__init__(
            self,
            render_mode=render_mode,
            scenario=scenario,
            num_agent_robots=num_agent_robots,
            num_adversary_robots=num_adversary_robots,
            color_team=color_team,
            truncated_time=truncated_time,
        )

        # Initialize PettingZoo ParallelEnv
        ParallelEnv.__init__(self)
        
        self.render_vsss = RenderVSSS()
        self.observation_system = ObservationSystem(self.simulator)

        # PettingZoo specific setup
        self.n_agents = num_agent_robots

        # Agent naming following PettingZoo conventions
        self.possible_agents = [f"agent_{i}" for i in range(self.num_agent_robots)]
        self.possible_adversaries = [f"adversary_{i}" for i in range(self.num_adversary_robots)]

        # Initialize simulator to calculate feature size dynamically
        self._init_positions()
        self._reset_simulator()

        # Calculate num_features dynamically by running a sample observation
        sample_obs = self.observation_system.agent_observation(0)
        self.num_features = len(sample_obs)

        # Ornstein-Uhlenbeck noise for adversary robots
        self.ou_noise_vw_adversary = [
            (OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise())
            for _ in range(num_adversary_robots)
        ]
        
        # Ornstein-Uhlenbeck noise for agent robots (if any are configured as 'ou')
        self.ou_noise_vw_agent = [
            (OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise())
            for _ in range(num_agent_robots)
        ]

        # Initialize rendering components
        self.window_size = np.array([1.70, 1.30]) * M2P
        self.window = None
        self.clock = None

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        """Get observation space for a specific agent."""
        return gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.num_features,), dtype=np.float32
        )

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        """Get action space for a specific agent."""
        return gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

    def _init_positions(self) -> None:
        """Initialize ball and robot positions using BaseEnv game setup."""
        # Use BaseEnv's position initialization
        super()._init_positions()

        # Split robot positions for agent and adversary (consistent with other environments)
        self.robots_agent = self.robots_pose[:self.num_agent_robots]
        self.robots_adversary = self.robots_pose[self.num_agent_robots:] if self.num_adversary_robots > 0 else []



    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> tuple:
        """Reset environment to initial state.

        Args:
            seed: Random seed for reproducibility
            options: Additional reset options (unused)

        Returns:
            Tuple of (observations, infos)
        """
        # Set agents list
        self.agents = copy(self.possible_agents)

        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)

        # Reset simulator using BaseEnv methods
        self._init_positions()
        self._reset_simulator()

        # Get initial observations
        observations = self._get_obs()
        infos = {agent: {} for agent in self.agents}

        # Reset reward system
        self.reward_system.reset()

        if self.render_mode == "human":
            self._render_frame()

        return observations, infos

    def step(self, actions: Dict[str, np.ndarray], adversary_actions: Optional[np.ndarray] = None) -> tuple:
        """Execute one simulation step.

        Args:
            actions: Dictionary mapping agent names to actions
            adversary_actions: Optional action array for adversary robots.

        Returns:
            Tuple of (observations, rewards, terminations, truncations, infos)
        """
        # Execute agent actions
        for idx in range(self.num_agent_robots):
            agent_name = self.possible_agents[idx]
            movement_type = self.movement_configs['agent_movement_types'][idx]
            
            if movement_type == 'action':
                if agent_name in actions:
                    action = actions[agent_name]
                else:
                    action = np.array([0.0, 0.0])
            elif movement_type == 'ou':
                v, w = (
                    self.ou_noise_vw_agent[idx][0].sample(),
                    self.ou_noise_vw_agent[idx][1].sample(),
                )
                action = np.array([v, w])
            else:  # 'no_move'
                action = np.array([0.0, 0.0])
                
            self.simulator.agent_step(idx, action)

        # Execute adversary robot actions
        for idx in range(len(self.robots_adversary)):
            movement_type = self.movement_configs['adversary_movement_types'][idx]
            
            if movement_type == 'action':
                if adversary_actions is not None and idx < len(adversary_actions):
                    action = adversary_actions[idx]
                else:
                    action = np.array([0.0, 0.0])
            elif movement_type == 'ou':
                v, w = (
                    self.ou_noise_vw_adversary[idx][0].sample(),
                    self.ou_noise_vw_adversary[idx][1].sample(),
                )
                action = np.array([v, w])
            else:  # 'no_move'
                action = np.array([0.0, 0.0])
            
            self.simulator.adversary_step(idx, action)

        # Step simulation
        self._step_simulation()

        # Get observations
        observations = self._get_obs()

        # Calculate rewards and termination conditions using BaseEnv
        base_reward, base_terminated, base_truncated = self.get_reward()

        # Apply to all agents (same reward/termination for all in this implementation)
        rewards, terminations, truncations = {}, {}, {}
        for agent in self.agents:
            rewards[agent] = base_reward
            terminations[agent] = base_terminated
            truncations[agent] = base_truncated

        # Update info dictionary
        infos = {agent: {} for agent in self.agents}

        # Remove terminated/truncated agents
        self.agents = [agent for agent in self.agents if not terminations[agent]]
        self.agents = [agent for agent in self.agents if not truncations[agent]]

        if self.render_mode == "human":
            self._render_frame()

        return observations, rewards, terminations, truncations, infos

    def render(self) -> Optional[np.ndarray]:
        """Render the environment.

        Returns:
            RGB array if render_mode is "rgb_array", otherwise None.
        """
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self) -> Optional[np.ndarray]:
        """Render a single frame of the environment."""
        return self._render_frame_common(
            self.render_vsss,
            self.simulator.robots_agent,
            self.simulator.robots_adversary,
            self.window_size
        )

        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def _get_obs(self) -> Dict[str, np.ndarray]:
        """Get observations for all active agents."""
        observations = {
            agent: self.observation_system.agent_observation(i)
            for i, agent in enumerate(self.possible_agents)
        }
        return observations


def main():
    """Test function for VSSSPettingZooEnv."""
    env = VSSSPettingZooEnv(
        render_mode="human",
        scenario="full_random",
        num_agent_robots=1,
        num_adversary_robots=0,
        color_team="blue"
    )

    # Run PettingZoo API test
    parallel_api_test(env)

    print("VSSSPettingZooEnv test completed successfully")


if __name__ == "__main__":
    main()