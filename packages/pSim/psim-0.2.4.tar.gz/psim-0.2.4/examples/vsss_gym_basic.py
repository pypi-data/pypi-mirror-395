#!/usr/bin/env python3
"""
VSSS Gym Environment Basic Example

This example demonstrates basic usage of the VSSSGymEnv (Gymnasium) for testing
DRL algorithms. It runs a few steps with random actions to validate functionality.
"""

import numpy as np
from gymnasium.wrappers import FlattenObservation
from pSim.vsss_gym_env import VSSSGymEnv

def main():
    """Run basic VSSSGymEnv test with random actions."""

    # Create environment with flattened observations for easier handling
    # The environment automatically determines controllable robots from config
    # In "formation" scenario: ["action", "ou", "ou"] = 1 controllable robot
    env = FlattenObservation(VSSSGymEnv(
        render_mode="human",  # Set to None for headless testing
        scenario="formation",
        num_agent_robots=3,
        num_adversary_robots=3,
        color_team="blue",
        truncated_time=600,
    ))

    print("=== VSSS Gym Basic Test ===")
    print(f"Action space: {env.action_space}")
    print(f"Observation space: {env.observation_space}")

    # Debug: Check actual environment config (access unwrapped env)
    unwrapped_env = env.unwrapped if hasattr(env, 'unwrapped') else env
    if hasattr(unwrapped_env, 'action_robots'):
        print(f"Number of controllable robots: {unwrapped_env.action_robots}")
    if hasattr(unwrapped_env, 'movement_configs'):
        print(f"Movement configs: {unwrapped_env.movement_configs}")

    # Reset environment
    obs, info = env.reset()
    print(f"Initial observation shape: {obs.shape}")

    # Run a few steps with random actions
    for step in range(1000):
        # Generate random action
        action = env.action_space.sample()
        print(f"Step {step+1}: Action shape {action.shape}")
        print(action)
        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"  Reward: {reward:.3f}, Terminated: {terminated}, Truncated: {truncated}")

        if terminated or truncated:
            print("Episode ended, resetting...")
            obs, info = env.reset()

    print("VSSS Gym basic test completed successfully!")
    env.close()

if __name__ == "__main__":
    main()