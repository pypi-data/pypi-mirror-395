import json, shutil, os
import numpy as np
from typing import Tuple, List, Dict, Any
from pathlib import Path
from scipy.spatial.distance import cdist

class GameSetup:
    """Handles game configuration and initial positioning."""
    def __init__(self):
        """Initialize with game configuration."""
        self.package_config_path = Path(__file__).parent.parent / 'config' / 'game_config.json'
        self.user_config_path = Path(os.getcwd()) / 'game_config.json'
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from determined path."""
        if not self.user_config_path.exists():
            print(f"Copying default config to project root: {self.user_config_path}")
            shutil.copy2(self.package_config_path, self.user_config_path)
        with open(self.user_config_path, 'r') as f:
            return json.load(f)

    def _generate_position(self, x_min: float, x_max: float,
        y_min: float, y_max: float
    ) -> Tuple[float, float]:
        """Generate a single random position within bounds."""
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        return x, y

    def _generate_poses(self, 
        n: int,
        x_min: float, x_max: float,
        y_min: float, y_max: float,
        t_min: float, t_max: float,
        reserved_poses: np.ndarray
    ) -> np.ndarray:
        """Generate n poses avoiding conflicts with reserved poses.

        Args:
            n: Number of poses to generate
            x_min, x_max: X coordinate bounds
            y_min, y_max: Y coordinate bounds
            t_min, t_max: Angle bounds
            reserved_poses: Already occupied positions to avoid

        Returns:
            Array of generated poses [x, y, theta]
        """
        xs = np.random.uniform(x_min, x_max, n)
        ys = np.random.uniform(y_min, y_max, n)
        ts = np.random.uniform(t_min, t_max, n)

        full_poses = np.array([xs, ys, ts]).T
        full_poses = np.vstack([full_poses, reserved_poses])

        # Calculate distance matrix (only considering x,y positions)
        positions = full_poses[:, :2]  # Only x,y coordinates for distance
        dist_matrix = cdist(positions, positions)
        dist_matrix[np.tril_indices(n + len(reserved_poses))] = np.inf

        if dist_matrix.min() < 0.15:  # Fixed minimum distance
            # Recursively try again if poses are too close
            return self._generate_poses(
                n, x_min, x_max, y_min, y_max, t_min, t_max, reserved_poses
            )
        return full_poses[:-len(reserved_poses)]

    def _get_robot_positions(self, 
        robot_config: Dict[str, Any], 
        num_robots: int, 
        ball_pos: Tuple[float, float], 
        reserved_poses: np.ndarray = None
    ) -> np.ndarray:
        """Get robot positions for agent or adversary robots.

        Args:
            robot_config: Configuration for this type of robots
            num_robots: Number of robots to generate
            ball_pos: Ball position to avoid
            reserved_poses: Already occupied positions to avoid

        Returns:
            Array of robot positions [x, y, theta]
        """
        if num_robots == 0:
            return np.array([]).reshape(0, 3)

        if reserved_poses is None:
            reserved_poses = np.array([[ball_pos[0], ball_pos[1], 0]])

        if robot_config['position_type'] == 'fixed':
            # Take only the first num_robots positions
            positions = np.array(robot_config['positions'][:num_robots], dtype=np.float64)
            return positions
        elif robot_config['position_type'] == 'range':
            # Generate random positions within range
            robot_range = robot_config['position_range']
            positions = self._generate_poses(
                num_robots,
                robot_range['x'][0], robot_range['x'][1],
                robot_range['y'][0], robot_range['y'][1],
                robot_range['angle'][0], robot_range['angle'][1],
                reserved_poses
            )
            return positions
        else:
            raise ValueError(f"Invalid position_type: {robot_config['position_type']}")

    def get_initial_state(self, 
        scenario: str,
        num_agent_robots: int,
        num_adversary_robots: int
    ) -> Tuple[Tuple[float, float], Tuple[float, float], np.ndarray]:
        """Get initial game state for a given scenario.

        Args:
            scenario: Scenario name from config
            num_agent_robots: Number of agent robots
            num_adversary_robots: Number of adversary robots

        Returns:
            Tuple of (ball_position, ball_velocity, robot_poses, movement_configs)
        """
        if scenario not in self.config['scenarios']:
            raise ValueError(f"Scenario {scenario} not found in config")

        scenario_config = self.config['scenarios'][scenario]
        
        ball_velocity = tuple(scenario_config['ball_velocity'])
        if scenario_config['ball_position_type'] == 'fixed':
            ball_pos = tuple(scenario_config['ball_position'])
        elif scenario_config['ball_position_type'] == 'range':
            ball_range = scenario_config['ball_position_range']
            ball_pos = self._generate_position(
                ball_range['x'][0], ball_range['x'][1],
                ball_range['y'][0], ball_range['y'][1]
            )
        else:
            raise ValueError(f"Position type {scenario_config['ball_position_type']} not valid")

        # Get agent robot positions
        agent_config = scenario_config['agent_robots']
        agent_positions = self._get_robot_positions(
            agent_config,
            num_agent_robots,
            ball_pos
        )
        # Get adversary robot positions
        adversary_config = scenario_config['adversary_robots']
        # Reserve agent positions to avoid collisions
        reserved_poses = np.array([[ball_pos[0], ball_pos[1], 0]] + agent_positions.tolist())
        adversary_positions = self._get_robot_positions(
            adversary_config,
            num_adversary_robots,
            ball_pos,
            reserved_poses
        )

        robot_positions = np.vstack([agent_positions, adversary_positions])

        # Get movement configurations
        agent_movement_types = agent_config.get(
            'movement_types', 
            ['action'] * num_agent_robots
        )[:num_agent_robots]
        
        adversary_movement_types = adversary_config.get(
            'movement_types', 
            ['ou'] * num_adversary_robots
        )[:num_adversary_robots]
        print(adversary_movement_types)

        movement_configs = {
            'agent_movement_types': agent_movement_types,
            'adversary_movement_types': adversary_movement_types,
            'action_robots': agent_movement_types.count('action')
        }

        return ball_pos, ball_velocity, robot_positions, movement_configs

if __name__=="__main__":
    game_setup = GameSetup()