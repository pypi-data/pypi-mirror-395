from .vsss_base_env import BaseVSSSEnv
from .vsss_gym_env import VSSSGymEnv
from .vsss_simple_env import SimpleVSSSEnv
from .vsss_pettingzoo_env import VSSSPettingZooEnv
from .modules.hmi import HMI
from gymnasium.envs.registration import register

# Register Gymnasium environment
register(
    id="VSSS/Env-v0",
    entry_point="pSim.vsss_gym_env:VSSSGymEnv",
    max_episode_steps=3600,
)

# Main exports
__all__ = ['BaseVSSSEnv', 'SimpleVSSSEnv', 'VSSSGymEnv', 'VSSSPettingZooEnv', 'HMI']

