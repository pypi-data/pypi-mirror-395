import numpy as np
from typing import Optional, Tuple, Dict, Any
import pygame

from .vsss_base_env import BaseVSSSEnv
from .modules.OUNoise import OrnsteinUhlenbeckNoise
from .modules.render_vsss import RenderVSSS

class SimpleVSSSEnv(BaseVSSSEnv):
    """
    Simple VSSS Environment for traditional control algorithms.

    This environment provides a clean interface for testing PID controllers
    and other traditional control algorithms. All agent robots are controlled
    simultaneously through actions defined by the control algorithm.
    """

    def __init__(
        self,
        render_mode: str = "human",
        num_agent_robots: int = 1,
        num_adversary_robots: int = 0,
        color_team: str = "blue",
        scenario: str = "formation",
        truncated_time: int = 3600,
        **kwargs: Any
    ):
        """Initialize Simple Environment.

        Args:
            render_mode: Render mode ("human", "rgb_array", or None).
            num_agent_robots: The number of agent robots in the simulation.
            num_adversary_robots: The number of adversary robots in the simulation.
            color_team: The color of the agent team ("blue" or "yellow").
            scenario: Game scenario to use from config file.
            truncated_time: Maximum steps before truncation.
            **kwargs: Additional arguments passed to BaseEnv.
        """
        # Initialize base environment
        super().__init__(
            render_mode=render_mode,
            scenario=scenario,
            num_agent_robots=num_agent_robots,
            num_adversary_robots=num_adversary_robots,
            color_team=color_team,
            truncated_time=truncated_time,
            **kwargs
        )

        # Initialize render system
        self.window_size = np.asarray([1.70, 1.30]) * 400  # M2P = 400

        if self.render_mode in ["human", "rgb_array"]:
            self.renderer = RenderVSSS()

        self._init_positions()
        self._init_movement_controllers()
    
    def _init_positions(self) -> None:
        """Initialize the positions of the ball and robots."""
        # Use base class method
        super()._init_positions()

        # SimpleEnv specific setup
        self.robots_agent, self.robots_adversary = (
            self.robots_pose[: self.num_agent_robots],
            self.robots_pose[self.num_agent_robots :],
        )

    def _init_movement_controllers(self) -> None:
        """Initialize movement controllers based on JSON configuration."""
        # Initialize agent robot controllers
        self.agent_controllers = []
        for movement_type in self.movement_configs['agent_movement_types']:
            if movement_type == 'ou':
                self.agent_controllers.append((OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise()))
            else:  # 'action' or 'no_move'
                self.agent_controllers.append(None)

        # Initialize adversary robot controllers
        self.adversary_controllers = []
        for movement_type in self.movement_configs['adversary_movement_types']:
            if movement_type == 'ou':
                self.adversary_controllers.append((OrnsteinUhlenbeckNoise(), OrnsteinUhlenbeckNoise()))
            else:  # 'no_move'
                self.adversary_controllers.append(None)



    def reset(self, seed: Optional[int] = None) -> Tuple[Dict[str, np.ndarray], Dict]:
        """Reset the environment to initial state.

        Args:
            seed: Optional seed for random number generator.

        Returns:
            Tuple of (initial_observation, info_dict).
        """
        if seed is not None:
            np.random.seed(seed)

        self.simulator.world.ClearForces()
        self._init_positions()
        self._reset_simulator()

        # Automatic render in human mode after reset
        if self.render_mode == "human":
            self.render()

        return self._get_obs(), {}

    def step(self, action: np.ndarray, adversary_actions: Optional[np.ndarray] = None) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict]:
        """Perform one step in the environment.

        Args:
            action: Action array with shape (num_agent_robots, 2) containing [v, w] for each agent robot.
            adversary_actions: Optional action array for adversary robots.

        Returns:
            Tuple of (observation, reward, terminated, truncated, info).
        """
        # Apply actions to agent robots based on configuration
        for idx in range(self.num_agent_robots):
            movement_type = self.movement_configs['agent_movement_types'][idx]
            
            if movement_type == 'action':
                # Control this robot with agent action
                robot_action = action[idx] if len(action.shape) > 1 else action
            elif movement_type == 'ou':
                # Use Ornstein-Uhlenbeck noise
                v, w = self.agent_controllers[idx]
                robot_action = np.array([v.sample(), w.sample()])
            else:  # 'no_move'
                robot_action = np.array([0.0, 0.0])

            self.simulator.agent_step(idx, robot_action)

        # Apply actions to adversary robots
        for idx in range(self.num_adversary_robots):
            movement_type = self.movement_configs['adversary_movement_types'][idx]
            if movement_type == 'action':
                if adversary_actions is not None and idx < len(adversary_actions):
                    adversary_action = adversary_actions[idx]
                else:
                    adversary_action = np.array([0.0, 0.0])
            elif movement_type == 'ou':
                v, w = self.adversary_controllers[idx]
                adversary_action = np.array([v.sample(), w.sample()])
            else:  # 'no_move'
                adversary_action = np.array([0.0, 0.0])

            self.simulator.adversary_step(idx, adversary_action)

        # Advance simulation
        self._step_simulation()

        # Get new observation
        observation = self._get_obs()

        # Get reward and termination conditions
        reward, terminated, truncated = self.get_reward()

        # Automatic render in human mode
        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, {}

    def render(self, mode: Optional[str] = None) -> Optional[np.ndarray]:
        """Render the environment.

        Args:
            mode: Render mode ("human", "rgb_array", or None). If None, uses default render_mode.

        Returns:
            If mode is "rgb_array", returns numpy array of RGB image.
            If mode is "human", displays the environment and returns None.
        """
        if mode is None:
            mode = self.render_mode

        if mode is None or self.renderer is None:
            return

        if mode == "human":
            return self._render_frame(mode)
        elif mode == "rgb_array":
            return self._render_frame(mode)
        else:
            raise ValueError(f"Unsupported render mode: {mode}")

    def _render_frame(self, mode: Optional[str] = None) -> Optional[np.ndarray]:
        """Renders a single frame of the environment."""
        return self._render_frame_common(
            self.renderer,
            self.simulator.robots_agent,
            self.simulator.robots_adversary,
            self.window_size,
            mode
        )

    def _get_obs(self) -> Dict[str, np.ndarray]:
        """Get simplified observations with direct positions and orientations.

        Returns:
            Dictionary containing:
            - 'agent_robots': Array of [x, y, theta] for each agent robot
            - 'adversary_robots': Array of [x, y, theta] for each adversary robot
            - 'ball': Array of [x, y]
        """
        # Agent robots positions and orientations (direct values)
        agent_obs = []
        for robot in self.simulator.robots_agent:
            agent_obs.append([
                robot.position.x,
                robot.position.y,
                robot.angle
            ])

        # Adversary robots positions and orientations (direct values)
        adversary_obs = []
        for robot in self.simulator.robots_adversary:
            adversary_obs.append([
                robot.position.x,
                robot.position.y,
                robot.angle
            ])

        # Ball position (direct values)
        ball_obs = [
            self.simulator.ball_body.position.x,
            self.simulator.ball_body.position.y
        ]

        return {
            "agent_robots": np.array(agent_obs, dtype=np.float32),
            "adversary_robots": np.array(adversary_obs, dtype=np.float32),
            'ball': np.array(ball_obs, dtype=np.float32)
        }

    def close(self):
        """Close the environment and cleanup resources."""
        super().close()


