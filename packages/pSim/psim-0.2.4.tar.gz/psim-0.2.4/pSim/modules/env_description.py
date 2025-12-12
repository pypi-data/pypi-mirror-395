import numpy as np
from typing import Any, Tuple, Dict

class ObservationSystem:
    """
    System for calculating observations in VSSS environments.
    """
    def __init__(self, simulator):
        """
        Initialize the ObservationSystem.

        Args:
            simulator: The simulator instance (pSim.modules.simulator.Simulator)
        """
        self.simulator = simulator

    def get_distance(self, idx: int, object: Any) -> float:
        """Calculate distance between agent robot and an object.
        
        Args:
            idx: Index of the agent robot
            object: Box2D body object (ball or another robot)
            
        Returns:
            Euclidean distance
        """
        return np.linalg.norm(self.simulator.robots_agent[idx].position - object.position)

    def get_diff_angle(self, idx: int, object: Any) -> Tuple[float, float]:
        """Calculate angle difference between agent robot and an object.
        
        Args:
            idx: Index of the agent robot
            object: Box2D body object (ball or another robot)
            
        Returns:
            Tuple of (cos(diff_angle), sin(diff_angle))
        """
        idx_object_angle = np.arctan2(
            object.position.y - self.simulator.robots_agent[idx].position.y,
            object.position.x - self.simulator.robots_agent[idx].position.x,
        )
        diff_angle = idx_object_angle - self.simulator.robots_agent[idx].angle
        return np.cos(diff_angle), np.sin(diff_angle)

    def agent_observation(self, idx: int) -> np.ndarray:
        """
        Calculate the observation vector for a specific agent robot.

        Args:
            idx: Index of the agent robot.

        Returns:
            Numpy array containing the observation features.
        """
        distance_ball = self.get_distance(idx, self.simulator.ball_body)
        distances_agent = [
            self.get_distance(idx, robot)
            for robot in self.simulator.robots_agent
            if robot != self.simulator.robots_agent[idx]
        ]
        distances_adversary = [self.get_distance(idx, robot) for robot in self.simulator.robots_adversary]

        angle_ball = self.get_diff_angle(idx, self.simulator.ball_body)
        angle_agent = [
            self.get_diff_angle(idx, robot)
            for robot in self.simulator.robots_agent
            if robot != self.simulator.robots_agent[idx]
        ]
        angle_adversary = [self.get_diff_angle(idx, robot) for robot in self.simulator.robots_adversary]

        cos_angle_agent = [angle[0] for angle in angle_agent]
        sin_angle_agent = [angle[1] for angle in angle_agent]
        cos_angle_adversary = [angle[0] for angle in angle_adversary]
        sin_angle_adversary = [angle[1] for angle in angle_adversary]

        observation = np.array(
            [
                # self observation
                self.simulator.robots_agent[idx].position.x,
                self.simulator.robots_agent[idx].position.y,
                np.cos(self.simulator.robots_agent[idx].angle),
                np.sin(self.simulator.robots_agent[idx].angle),
                self.simulator.robots_agent[idx].linearVelocity.x,
                self.simulator.robots_agent[idx].linearVelocity.y,
                self.simulator.robots_agent[idx].angularVelocity,
                # ball observation
                self.simulator.ball_body.position.x,
                self.simulator.ball_body.position.y,
                self.simulator.ball_body.linearVelocity.x,
                self.simulator.ball_body.linearVelocity.y,
                # distances
                distance_ball,
                *distances_agent,
                *distances_adversary,
                # # angles
                *angle_ball,
                *cos_angle_agent,
                *sin_angle_agent,
                *cos_angle_adversary,
                *sin_angle_adversary,
            ],
            dtype=np.float32,
        )

        return observation


class RewardSystem:
    """
    System for calculating rewards in VSSS environments.
    """
    def __init__(self, simulator, truncated_time: int = 3600):
        """
        Initialize RewardSystem.

        Args:
            simulator: The simulator instance (pSim.modules.simulator.Simulator)
            truncated_time: Maximum number of steps before truncation
        """
        self.simulator = simulator
        self.truncated_time = truncated_time
        self.time_step = 0

    def reset(self):
        """Reset the reward system for a new episode."""
        self.time_step = 0

    def step(self):
        """Increment the time step."""
        self.time_step += 1

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def calculate_reward(self) -> Tuple[float, bool, bool]:
        """Calculate reward, termination, and truncation status.
        
        Uses self.simulator to access game state.

        Returns:
            Tuple of (reward, terminated, truncated)
        """
        # Goal reward
        ball_x = self.simulator.ball_body.position.x
        if ball_x < -0.765:
            r_goal = 0  # Goal for agent (left goal)
        elif ball_x > 0.765:
            r_goal = 1  # Goal for adversary (right goal)
        else:
            r_goal = 0

        terminated = r_goal != 0

        # Time penalty
        r_time = -1

        # Check truncation
        truncated = self.time_step >= self.truncated_time

        # Ball movement reward
        ball_velocity = self.simulator.ball_body.linearVelocity
        if np.linalg.norm(ball_velocity) > 0.05:
            # Reward ball movement toward adversary goal, penalize toward agent goal
            agent_goal = np.array([-0.8, 0])
            adversary_goal = np.array([0.8, 0])

            similarity_to_agent_goal = self._cosine_similarity(
                ball_velocity,
                agent_goal - self.simulator.ball_body.position
            )
            similarity_to_adversary_goal = self._cosine_similarity(
                ball_velocity,
                adversary_goal - self.simulator.ball_body.position
            )

            r_ball_movement = (
                np.tanh(similarity_to_adversary_goal) -
                np.tanh(similarity_to_agent_goal) -
                3 * np.tanh(1)
            )
        else:
            # Penalize stationary ball
            r_ball_movement = -5 * np.tanh(1)

        # Contact rewards
        r_contact_robot_ball = (
            0.5 if self.simulator.contact_listener.collision_robot_ball else 0
        )
        r_contact_robot_wall = (
            -1.0 if self.simulator.contact_listener.collision_robot_wall else 0
        )

        # Reset collision flags
        self.simulator.contact_listener.collision_robot_ball = False
        self.simulator.contact_listener.collision_robot_wall = False

        # Combine all reward components
        reward_components = {
            'time': r_time,
            'goal': r_goal * 10,
            'robot_ball_contact': r_contact_robot_ball,
            'robot_wall_contact': r_contact_robot_wall,
            'ball_movement': r_ball_movement,
        }

        total_reward = sum(reward_components.values())

        return total_reward, terminated, truncated
