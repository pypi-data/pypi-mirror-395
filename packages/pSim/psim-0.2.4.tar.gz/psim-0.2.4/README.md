# pSim

[![PyPI version](https://badge.fury.io/py/pSim.svg)](https://badge.fury.io/py/pSim)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python versions](https://img.shields.io/pypi/pyversions/pSim.svg)](https://pypi.org/project/pSim)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://juliodltv.github.io/pSim/)

<div align="center">
    <img
        src="docs/assets/logov2.png"
        alt="pSim Logo"
        width="500"
        onerror="this.onerror=null; this.src='assets/logov2.png';"
    />
    <br>
    <h1>pSim: Very Small Size Soccer Simulation Environment</h1>
    <p><em>Comprehensive simulation platform for autonomous robotic soccer development</em></p>
</div>

---

## Welcome to pSim

**pSim** is a comprehensive, pythonic simulation environment specifically designed for the Very Small Size Soccer (VSSS) competition. It provides researchers, students, and developers with powerful tools to develop, test, and validate autonomous robotic soccer strategies and algorithms.

Whether you're working on traditional control algorithms, reinforcement learning, or multi-agent coordination, pSim offers the flexibility and performance you need.

---

## Quick Start

### Installation

pSim uses [uv](https://docs.astral.sh/uv/) for fast, reliable package management. See the [installation guide](https://juliodltv.github.io/pSim/installation/) for complete setup instructions including uv installation.

```bash
# Quick install with uv
uv venv --python 3.12
uv pip install pSim[all] --upgrade
```
```bash
# Or, after venv only install a specific dependency
uv pip install pSim[gym]   # For Gymnasium support
uv pip install pSim[zoo]   # For PettingZoo support
uv pip install pSim[all]   # For both Gymnasium and PettingZoo
```

### First Simulation

```python
from pSim import SimpleVSSSEnv
import numpy as np

# Create your first simulation with custom robot counts
env = SimpleVSSSEnv(
    render_mode="human",
    scenario="formation",
    num_agent_robots=2,      # Number of controllable robots
    num_adversary_robots=3   # Number of opponent robots
)
obs, info = env.reset()

# Run simulation steps with random actions
for step in range(1000):
    # Generate random actions for all agent robots [v, w] (velocity, angular velocity)
    action = np.random.uniform(-1, 1, (env.num_agent_robots, 2))
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

---

## Environment Types

pSim provides three main environment types, each designed for different use cases:

- **SimpleVSSSEnv**: For traditional control and testing.
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="flex: 1; text-align: center; padding: 5px;">
        <img
            src="docs/assets/single.png"
            alt="Single robot simulation"
            width="400"
            onerror="this.onerror=null; this.src='assets/single.png';"
        />
        <p><em>Single robot simulation environment</em></p>
    </div>
    <div style="flex: 1; text-align: center; padding: 5px;">
        <img
            src="docs/assets/match.png"
            alt="Full team match simulation"
            width="400"
            onerror="this.onerror=null; this.src='assets/match.png';"
        />
        <p><em>Full team match with complete team</em></p>
    </div>
</div>

- **VSSSGymEnv**: For reinforcement learning with Gymnasium compatibility.
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="flex: 1; text-align: center; padding: 10px;">
        <img
            src="docs/assets/gifs/video7.gif"
            alt="Single robot simulation"
            width="400"
            onerror="this.onerror=null; this.src='assets/gifs/video7.gif';"
        />
        <p><em>Single robot reinforcement learning</em></p>
    </div>
    <div style="flex: 1; text-align: center; padding: 10px;">
        <img
            src="docs/assets/gifs/single_agent_cl.gif"
            alt="Full team match simulation"
            width="400"
            onerror="this.onerror=null; this.src='assets/gifs/single_agent_cl.gif';"
        />
        <p><em>Single robot in competition</em></p>
    </div>
</div>

- **VSSSPettingZooEnv**: For multi-agent reinforcement learning with PettingZoo compatibility.

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: center;">
    <div style="text-align: center;">
        <img src="docs/assets/gifs/vf_8700.gif" alt="Feature 1" width="400" onerror="this.onerror=null; this.src='assets/gifs/vf_8700.gif';" />
        <p><em>Cooperative Two Agents</em></p>
    </div>
    <div style="text-align: center;">
        <img src="docs/assets/gifs/ma3_1350.gif" alt="Feature 2" width="400" onerror="this.onerror=null; this.src='assets/gifs/ma3_1350.gif';" />
        <p><em>Competitive Three Agents</em></p>
    </div>
    <div style="text-align: center;">
        <img src="docs/assets/gifs/3vs3_roles_3800.gif" alt="Feature 3" width="400" onerror="this.onerror=null; this.src='assets/gifs/3vs3_roles_3800.gif';" />
        <p><em>Three vs Three Roles</em></p>
    </div>
    <div style="text-align: center;">
        <img src="docs/assets/gifs/vs2_3380.gif" alt="Feature 4" width="400" onerror="this.onerror=null; this.src='assets/gifs/vs2_3380.gif';" />
        <p><em>Competitive Two Agents</em></p>
    </div>
</div>

## Features

### Traditional Control
- PID controllers, MPC, and other traditional methods
- Path planning and trajectory optimization
- Formation control and cooperative behaviors

### Reinforcement Learning
- Compatible with Stable Baselines 3, Ray RLlib, and other RL libraries
- Customizable reward functions and observation spaces
- Curriculum learning through scenario configuration

### Research & Education
- Multi-agent coordination studies
- Emergent behavior analysis
- Algorithm benchmarking and comparison

### Competition Preparation
- Strategy development and testing
- Opponent modeling and adaptation
- Performance analysis and optimization

### Realistic Physics
Box2D-powered physics simulation with customizable parameters for accurate robot and ball dynamics.

### Human-Machine Interface
- **Keyboard Controls**: Full keyboard input with intuitive mappings
- **Joystick Support**: Universal controller compatibility
- **Robot Switching**: Dynamic selection between controllable robots
- **Team Management**: Control different teams independently
- **Ball Control Mode**: Direct ball manipulation

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/juliodltv/pSim/issues)
- **Discussions**: [GitHub Discussions](https://github.com/juliodltv/pSim/discussions)
- **Documentation**: [Full Documentation](https://juliodltv.github.io/pSim/)

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/juliodltv/pSim/blob/main/CONTRIBUTING.md) for details.