"""
BaseVSSSEnv - Abstract Base Class for pSim VSSS Environments

Defines the core interface and common functionality for all pSim VSSS environments.
This abstract base class ensures consistency across SimpleVSSSEnv, VSSSGymEnv, and VSSSPettingZooEnv.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from .modules.game_setup import GameSetup
from .modules.env_description import RewardSystem
from .modules.simulator import Simulator


class BaseVSSSEnv(ABC):
    """
    Abstract base class for all pSim VSSS environments.

    This class defines the core interface and shared functionality that must be
    implemented by all VSSS environment types (SimpleVSSSEnv, VSSSGymEnv, VSSSPettingZooEnv).

    Core Components:
    - Simulator: Physics simulation (Box2D)
    - ConfigManager: Configuration file management
    - GameSetup: Initial robot/ball positioning
    - RewardSystem: Reward calculation and episode management

    Subclasses must implement:
    - step(): Execute one simulation step
    - reset(): Reset environment to initial state
    - render(): Display/return visual representation
    """

    def __init__(
        self,
        render_mode: str = "human",
        scenario: str = "formation",
        num_agent_robots: int = 1,
        num_adversary_robots: int = 0,
        color_team: str = "blue",
        truncated_time: int = 3600,
        **kwargs: Any
    ):
        """Initialize base environment components.

        Args:
            render_mode: Rendering mode ("human", "rgb_array", or None)
            scenario: Scenario name from configuration
            num_agent_robots: Number of agent robots
            num_adversary_robots: Number of adversary robots
            color_team: Team color ("blue" or "yellow")
            truncated_time: Maximum episode length
            **kwargs: Additional arguments for subclasses
        """
        # Store core parameters
        self.render_mode = render_mode
        self.scenario = scenario
        self.num_agent_robots = num_agent_robots
        self.num_adversary_robots = num_adversary_robots
        self.truncated_time = truncated_time

        # Team colors with standard naming
        self.agent_color, self.adversary_color = (
            ("blue", "yellow") if color_team == "blue" else ("yellow", "blue")
        )

        # Initialize core components
        self.game_setup = GameSetup()
        self.simulator = Simulator()
        self.reward_system = RewardSystem(self.simulator, truncated_time=truncated_time)

        # Environment state
        self.ball_pos: np.ndarray = np.zeros(2)
        self.ball_velocity: np.ndarray = np.zeros(2)
        self.robots_pose: List[List[float]] = []
        self.movement_configs: Dict[str, Any] = {}

        # Rendering components (initialized by subclasses)
        self.renderer = None
        self.window = None
        self.clock = None

    @abstractmethod
    def step(self, action: Any) -> Tuple[Any, ...]:
        """Execute one simulation step.

        Args:
            action: Action(s) to execute. Format depends on subclass.

        Returns:
            Tuple containing (observation, reward, terminated, truncated, info).
            Specific formats depend on subclass (single vs multi-agent).
        """
        pass

    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> Tuple[Any, Dict]:
        """Reset environment to initial state.

        Args:
            seed: Random seed for reproducibility

        Returns:
            Tuple of (initial_observation, info_dict).
            Formats depend on subclass.
        """
        pass

    @abstractmethod
    def render(self, mode: Optional[str] = None) -> Optional[np.ndarray]:
        """Render the environment.

        Args:
            mode: Render mode override. If None, uses self.render_mode.

        Returns:
            RGB array if mode="rgb_array", None if mode="human".
        """
        pass

    def close(self) -> None:
        """Clean up environment resources.

        This method should be called when done with the environment
        to properly clean up rendering resources.
        """
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()
            self.window = None

    # Common utility methods for subclasses

    def _init_positions(self) -> None:
        """Initialize ball and robot positions from configuration."""
        (self.ball_pos, self.ball_velocity,
         self.robots_pose, self.movement_configs) = self.game_setup.get_initial_state(
            self.scenario, self.num_agent_robots, self.num_adversary_robots
        )

        # Set ball velocity in simulator
        self.simulator.vx, self.simulator.vy = self.ball_velocity

    def set_ball_velocity(self, vx: float, vy: float) -> None:
        """Set the velocity of the ball directly.

        Args:
            vx: Velocity in x direction
            vy: Velocity in y direction
        """
        self.simulator.ball_body.linearVelocity = (vx, vy)

    def _reset_simulator(self) -> None:
        """Reset physics simulator with current positions."""
        robots_agent = self.robots_pose[:self.num_agent_robots]
        robots_adversary = self.robots_pose[self.num_agent_robots:]

        # Simulator expects lists, not dictionaries
        self.simulator.reset_simulator(robots_agent, self.ball_pos, robots_adversary)
        self.reward_system.reset()

    def _step_simulation(self) -> None:
        """Advance physics simulation by one timestep."""
        self.simulator.world.Step(
            timeStep=1/60,  # 60 FPS
            velocityIterations=6,
            positionIterations=2,
        )
        self.simulator.apply_force()
        self.reward_system.step()

    def get_reward(self) -> Tuple[float, bool, bool]:
        """Get reward and termination info. Override this method for custom rewards.

        Returns:
            Tuple of (reward, terminated, truncated)
        """
        return self.reward_system.calculate_reward()



    def _render_frame_common(self, renderer, robots_agent, robots_adversary, window_size, mode: Optional[str] = None) -> Optional[np.ndarray]:
        """Common rendering method for all environments.

        Args:
            renderer: Renderer instance (RenderVSSS)
            robots_agent: List of agent robot bodies
            robots_adversary: List of adversary robot bodies
            window_size: Window size as numpy array
            mode: Render mode

        Returns:
            RGB array if mode="rgb_array", None otherwise
        """
        import pygame

        if mode is None:
            mode = self.render_mode

        if mode == "human" and self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(window_size.astype(int))
        if mode == "human" and self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface(window_size.astype(int))

        # Draw field
        renderer.field(canvas)

        # Draw ball
        renderer.ball(
            canvas,
            self.simulator.ball_body.position.x,
            self.simulator.ball_body.position.y,
        )

        # Draw agent robots
        for idx in range(len(robots_agent)):
            renderer.robot(
                canvas,
                robots_agent[idx].position.x,
                robots_agent[idx].position.y,
                robots_agent[idx].angle,
                self.agent_color,
                idx,
            )

        # Draw adversary robots
        for idx in range(len(robots_adversary)):
            renderer.robot(
                canvas,
                robots_adversary[idx].position.x,
                robots_adversary[idx].position.y,
                robots_adversary[idx].angle,
                self.adversary_color,
                idx,
            )

        if mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(60)  # 60 FPS
        else:  # rgb_array
            return np.transpose(pygame.surfarray.array3d(canvas), axes=(1, 0, 2))
