#!/usr/bin/env python3
"""
Simple Environment Basic Example

This example demonstrates basic usage of the SimpleEnv for testing traditional
control algorithms. It runs a few steps with random actions to validate functionality.
"""

import numpy as np
from pSim.vsss_simple_env import SimpleVSSSEnv

def main():
    """Run basic SimpleEnv test with random actions."""

    # Create environment
    env = SimpleVSSSEnv(
        render_mode="human",  # Set to None for headless testing
        scenario="formation",
        num_agent_robots=3,
        num_adversary_robots=3,
        color_team="blue"
    )

    print("=== SimpleEnv Basic Test ===")
    print(f"Agent robots: {env.num_agent_robots}")
    print(f"Adversary robots: {env.num_adversary_robots}")
    print(f"Movement configs: {env.movement_configs}")

    # Reset environment
    obs, info = env.reset()
    print(f"Initial observation keys: {list(obs.keys())}")

    # Run a few steps with random actions
    for step in range(1000):
        # Generate random action for ALL agent robots (not just controllable ones)
        action = np.random.uniform(-1, 1, (env.num_agent_robots, 2))

        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, info = env.reset()

    env.close()

if __name__ == "__main__":
    main()