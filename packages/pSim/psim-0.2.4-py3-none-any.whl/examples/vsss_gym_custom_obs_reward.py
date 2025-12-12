import gymnasium as gym
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from pSim.vsss_gym_env import VSSSGymEnv
from pSim.modules.env_description import ObservationSystem, RewardSystem

class CustomObservationSystem(ObservationSystem):
    """
    Custom Observation System example.
    Only returns agent position and ball position.
    """
    def agent_observation(self, idx: int) -> np.ndarray:
        """
        Calculate a simplified observation vector.
        """
        # Get agent and ball objects
        agent = self.simulator.robots_agent[idx]
        ball = self.simulator.ball_body

        observation = np.array(
            [
                agent.position.x,
                agent.position.y,
                agent.angle,
                ball.position.x,
                ball.position.y,
            ],
            dtype=np.float32,
        )
        return observation

class CustomRewardSystem(RewardSystem):
    """
    Custom Reward System example.
    Rewards only for moving towards the ball.
    """
    def calculate_reward(self) -> Tuple[float, bool, bool]:
        """
        Calculate custom reward.
        """
        # Simple reward: negative distance to ball for the first agent
        # Note: This is a very basic example and assumes single agent or shared reward
        agent = self.simulator.robots_agent[0]
        ball = self.simulator.ball_body
        
        distance = np.linalg.norm(agent.position - ball.position)
        reward = -distance

        # Check termination (e.g., if ball is touched)
        terminated = False
        if distance < 0.1:
            reward += 10
            terminated = True

        # Check truncation
        truncated = self.time_step >= self.truncated_time

        return reward, terminated, truncated

class CustomVSSSGymEnv(VSSSGymEnv):
    """
    VSSSGymEnv with custom observation and reward systems.
    """
    def __init__(
        self,
        render_mode: Optional[str] = None,
        scenario: str = "formation",
        num_agent_robots: int = 1,
        num_adversary_robots: int = 0,
        color_team: str = "blue",
        truncated_time: int = 600,
    ):
        # Initialize parent class
        super().__init__(
            render_mode=render_mode,
            scenario=scenario,
            num_agent_robots=num_agent_robots,
            num_adversary_robots=num_adversary_robots,
            color_team=color_team,
            truncated_time=truncated_time,
        )

        # Override systems with custom ones
        self.observation_system = CustomObservationSystem(self.simulator)
        self.reward_system = CustomRewardSystem(self.simulator, truncated_time=truncated_time)

        # Re-calculate observation space since we changed the observation system
        # We need to re-run the dynamic feature calculation logic from VSSSGymEnv.__init__
        
        # Calculate num_features dynamically by running a sample observation
        sample_obs = self.observation_system.agent_observation(0)
        num_features = len(sample_obs)
            
        self.observation_space = gym.spaces.Tuple(
            tuple(
                gym.spaces.Box(low=-np.inf, high=np.inf, shape=(num_features,), dtype=np.float32)
                for _ in range(self.action_robots)
            )
        )

def main():
    """Run the custom environment example."""
    print("=== Custom VSSS Gym Env Example ===")
    
    # Create custom environment
    env = CustomVSSSGymEnv(
        render_mode="human",
        scenario="formation",
        num_agent_robots=3,
        num_adversary_robots=3,
        color_team="blue"
    )

    print(f"Observation Space: {env.observation_space}")
    print(f"Action Space: {env.action_space}")

    # Reset environment
    obs, info = env.reset()
    print("Initial observation:", obs)

    # Run a few steps
    for i in range(100):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        if i % 10 == 0:
            print(f"Step {i}: Reward={reward:.4f}")

        if terminated or truncated:
            print("Episode finished")
            env.reset()

    env.close()
    print("Example finished successfully")

if __name__ == "__main__":
    main()
