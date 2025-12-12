#!/usr/bin/env python3
"""
VSSS PettingZoo Environment Basic Example

This example demonstrates basic usage of the VSSSPettingZooEnv for testing
multi-agent algorithms. It runs a few steps with random actions to validate functionality.
"""

import numpy as np
from pSim.vsss_pettingzoo_env import VSSSPettingZooEnv

def main():
    """Run basic VSSSPettingZooEnv test with random actions."""

    # Create environment
    env = VSSSPettingZooEnv(
        render_mode="human",  # Set to None for headless testing
        scenario="formation",
        num_agent_robots=3,
        num_adversary_robots=3,
        color_team="blue",
        truncated_time=600,
    )

    print("=== VSSS PettingZoo Basic Test ===")
    print(f"Agents: {env.possible_agents}")
    print(f"Action space: {env.action_space('agent_0')}")
    print(f"Observation space: {env.observation_space('agent_0')}")

    # Reset environment
    obs, info = env.reset()
    print(f"Initial observations for {len(obs)} agents")

    # Run a few steps with random actions
    for step in range(1000):
        # Generate random actions for all agents
        actions = {agent: env.action_space(agent).sample() for agent in env.agents}
        print(f"Step {step+1}: Controlling {len(actions)} agents")
        print(actions)
        # Step environment
        obs, rewards, terminations, truncations, infos = env.step(actions)

        # Show summary
        total_reward = sum(rewards.values())
        terminated_count = sum(terminations.values())
        truncated_count = sum(truncations.values())
        print(f"  Total reward: {total_reward:.3f}, Terminated: {terminated_count}, Truncated: {truncated_count}")

        if any(terminations.values()) or any(truncations.values()):
            print("Episode ended, resetting...")
            obs, info = env.reset()

    print("VSSS PettingZoo basic test completed successfully!")
    env.close()

if __name__ == "__main__":
    main()