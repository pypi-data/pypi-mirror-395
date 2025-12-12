import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import gymnasium as gym
import numpy as np
import pygame
from gymnasium.wrappers import FlattenObservation

from .vsss_base_env import BaseVSSSEnv
from .modules.OUNoise import OrnsteinUhlenbeckNoise
from .modules.render_vsss import RenderVSSS
from .modules.env_description import ObservationSystem

sys.dont_write_bytecode = True

M2P = 400


class VSSSGymEnv(BaseVSSSEnv, gym.Env):
    """Custom Gymnasium Environment for Very Small Size Soccer (VSSS).
    Provides a standardized Gymnasium interface for reinforcement learning.

    This environment simulates a VSSS match, allowing AI agents to control
    robots and interact with a ball within a defined field.
    """
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(
        self,
        render_mode: Optional[str] = None,
        scenario: str = "formation",
        num_agent_robots: int = 1,
        num_adversary_robots: int = 0,
        color_team: str = "blue",
        truncated_time: int = 600,
    ):
        """Initializes the VSSSGymEnv environment.

        Args:
            render_mode: The rendering mode. Can be "human" for display or "rgb_array" for returning RGB images.
            scenario: The game scenario to use ("formation" or "full_random").
            num_agent_robots: The number of agent robots in the simulation.
            num_adversary_robots: The number of adversary robots in the simulation.
            color_team: The color of the agent team ("blue" or "yellow").
        """
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window_size = np.asarray([1.70, 1.30]) * M2P

        self.window = None
        self.clock = None

        # Initialize base environment
        BaseVSSSEnv.__init__(
            self,
            render_mode=render_mode,
            scenario=scenario,
            num_agent_robots=num_agent_robots,
            num_adversary_robots=num_adversary_robots,
            color_team=color_team,
            truncated_time=truncated_time,
        )

        # Initialize gymnasium.Env
        gym.Env.__init__(self)

        # VSSSGymEnv specific components
        self.render_vsss = RenderVSSS()
        self.observation_system = ObservationSystem(self.simulator)

        # num_agent_robots is handled by BaseEnv
        # num_adversary_robots is handled by BaseEnv

        # Initialize positions using BaseEnv method
        self._init_positions()

        # Determine number of controllable robots from config
        agent_movement_types = self.movement_configs['agent_movement_types']
        self.action_robots = agent_movement_types.count('action')

        # Ornstein-Uhlenbeck noise for adversary robots
        self.ou_noise_vw_adversary: List[Tuple[OrnsteinUhlenbeckNoise, OrnsteinUhlenbeckNoise]] = [
            (OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise())
            for _ in range(num_adversary_robots)
        ]
        # Ornstein-Uhlenbeck noise for non-controlled agent robots
        self.ou_noise_vw_agent: List[Tuple[OrnsteinUhlenbeckNoise, OrnsteinUhlenbeckNoise]] = [
            (OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise())
            for _ in range(num_agent_robots - self.action_robots)
        ] if num_agent_robots > self.action_robots else []

        # Initialize simulator to calculate feature size dynamically
        self._reset_simulator()
        
        # Calculate num_features dynamically by running a sample observation
        sample_obs = self.observation_system.agent_observation(0)
        num_features = len(sample_obs)
            
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(self.action_robots, 2), dtype=np.float32
        )
        self.observation_space = gym.spaces.Tuple(
            tuple(
                gym.spaces.Box(low=-np.inf, high=np.inf, shape=(num_features,), dtype=np.float32)
                for _ in range(self.action_robots)
            )
        )

    def _init_positions(self) -> None:
        """Initialize ball and robot positions using BaseEnv game setup."""
        # Use BaseEnv's position initialization
        super()._init_positions()

        # Split robot positions for agent and adversary
        self.robots_agent = self.robots_pose[:self.num_agent_robots]
        self.robots_adversary = self.robots_pose[self.num_agent_robots:] if self.num_adversary_robots > 0 else []

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[Any, Dict[Any, Any]]:
        """Resets the environment to an initial state.

        Args:
            seed: An optional seed for the random number generator.

        Returns:
            A tuple containing the initial observation and an info dictionary.
        """
        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)

        self.simulator.world.ClearForces()
        self._init_positions()

        # Use BaseEnv's simulator reset method
        self._reset_simulator()

        observation = self._get_obs()
        info = {}

        # Reset reward system time
        self.reward_system.reset()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action: np.ndarray, adversary_actions: Optional[np.ndarray] = None) -> Tuple[tuple, float, bool, bool, Dict[Any, Any]]:
        """Performs one step in the environment using the given action.

        Args:
            action: The action to be taken by the agent(s).
            adversary_actions: Optional action array for adversary robots.

        Returns:
            A tuple containing the observation, reward, terminated flag, truncated flag, and info dictionary.
        """
        action_idx = 0
        ou_noise_idx = 0

        for idx in range(self.num_agent_robots):
            movement_type = self.movement_configs['agent_movement_types'][idx]
            if movement_type == 'action':
                # Control this robot with agent action
                act = action[action_idx]  # Unified action format
                action_idx += 1
            elif movement_type == 'ou':
                # Use Ornstein-Uhlenbeck noise
                v, w = (
                    self.ou_noise_vw_agent[ou_noise_idx][0].sample(),
                    self.ou_noise_vw_agent[ou_noise_idx][1].sample(),
                )
                act = np.array([v, w])
                ou_noise_idx += 1
            else:  # 'no_move'
                # No movement
                act = np.array([0.0, 0.0])

            self.simulator.agent_step(idx, act)

        for idx in range(self.num_adversary_robots):
            movement_type = self.movement_configs['adversary_movement_types'][idx]
            
            if movement_type == 'action':
                if adversary_actions is not None and idx < len(adversary_actions):
                    adversary_action = adversary_actions[idx]
                else:
                    adversary_action = np.array([0.0, 0.0])
            elif movement_type == 'ou':
                v, w = (
                    self.ou_noise_vw_adversary[idx][0].sample(),
                    self.ou_noise_vw_adversary[idx][1].sample(),
                )
                adversary_action = np.array([v, w])
            else:  # 'no_move'
                adversary_action = np.array([0.0, 0.0])
            
            self.simulator.adversary_step(idx, adversary_action)

        # Use BaseEnv's simulation step method
        self._step_simulation()

        observation = self._get_obs()

        # Use BaseEnv's reward system
        reward, terminated, truncated = self.get_reward()

        info = {}

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info

    def render(self) -> Optional[np.ndarray]:
        """Renders the environment.

        Returns:
            An RGB array if render_mode is "rgb_array", otherwise None.
        """
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self) -> Optional[np.ndarray]:
        """Renders a single frame of the environment."""
        return self._render_frame_common(
            self.render_vsss,
            self.simulator.robots_agent,
            self.simulator.robots_adversary,
            self.window_size
        )

    def _get_obs(self):
        """Retrieves the current observation of the environment.

        Returns:
            Tuple of observation arrays for all controllable robots.
        """
        return tuple(self.observation_system.agent_observation(idx) for idx in range(self.action_robots))

    def close(self):
        """Closes the Pygame window and quits Pygame."""
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


def _main():
    """Main function to run the VSSS environment for demonstration.

    This function initializes the environment, runs a few episodes,
    and demonstrates the basic usage of the VSSSGymEnv class.
    """
    env = FlattenObservation(
        VSSSGymEnv(
            render_mode="human",
            scenario="full_random",
            num_agent_robots=3,
            num_adversary_robots=3,
            color_team="yellow",
        )
    )
    obs, _, = env.reset()
    for _ in range(10):
        for _ in range(500):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            if terminated or truncated:
                env.reset()
        env.reset()
    env.close()


if __name__ == "__main__":
    _main()
