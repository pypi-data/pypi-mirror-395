"""
HMI Control Example for Agent Team Robots

This example demonstrates using the Human-Machine Interface (HMI) for manual
control of individual agent team robots. You can switch between robots in your
team and control each one independently. Supports keyboard and joystick input.
"""

from pSim.vsss_simple_env import SimpleVSSSEnv
from pSim.modules.hmi import HMI
import numpy as np, pygame

def main():
    """Run HMI control example for agent team robots."""

    # Create environment for agent team control
    env = SimpleVSSSEnv(
        render_mode="human",
        scenario="full_random",
        num_agent_robots=3,
        num_adversary_robots=3,
        color_team="blue"
    )

    # Initialize HMI (use simple_mode=False for advanced features)
    hmi = HMI(dead_zone=0.1)

    # Reset environment
    obs, info = env.reset()
    print(f"Agent team: {env.num_agent_robots} robots")
    print(f"Adversary team: {env.num_adversary_robots} robots")

    # Update HMI with controllable robots
    hmi.update_robot_list(
        agent_team_color=env.agent_color,
        agent_movement_types=env.movement_configs['agent_movement_types'],
        adversary_movement_types=env.movement_configs['adversary_movement_types']
    )

    # Main control loop
    while hmi.active:
        hmi_state = hmi()
        
        if not hmi_state["active"]:
            break
            
        if hmi_state["reset_commanded"]:
            obs, info = env.reset()
            print("Environment reset!")
            continue

        # Get control inputs
        actions = hmi_state["actions"]
        current_team = hmi_state["current_team"]
        current_robot_id = hmi_state["current_robot_id"]
        ball_control = hmi_state["ball_control_mode"]

        # Initialize action arrays
        agent_actions = np.zeros((env.num_agent_robots, 2))
        adversary_actions = np.zeros((env.num_adversary_robots, 2))

        if ball_control:
            # Control ball directly
            # Scale velocity for better control
            ball_vel = actions
            env.set_ball_velocity(ball_vel[0], ball_vel[1])
        else:
            # Route actions to the correct robot
            if current_team == "blue":
                if current_robot_id < env.num_agent_robots:
                    agent_actions[current_robot_id] = actions
            else:  # yellow
                if current_robot_id < env.num_adversary_robots:
                    adversary_actions[current_robot_id] = actions

        # Step environment with both agent and adversary actions
        obs, reward, terminated, truncated, info = env.step(agent_actions, adversary_actions=adversary_actions)
        
        # Handle episode termination
        if terminated or truncated:
            print("Episode ended - resetting...")
            obs, info = env.reset()

    hmi.quit()
    env.close()

if __name__ == "__main__":
    main()