# Gymnasium Retina Task

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Gymnasium-compatible implementation of the **Left & Right Retina Problem**, a benchmark task for testing the evolution of modular neural networks.

<p align="center">
  <img src="https://raw.githubusercontent.com/Teaspoon-AI/gymnasium-retinatask/main/retinatask-text.png" alt="Gymnasium Retina Task Preview" width="500"/>
</p>

## Overview

The Retina Task is based on the work by Risi & Stanley (Artificial Life 2012) on evolving modular neural networks using ES-HyperNEAT. The task tests an agent's ability to independently classify patterns on the left and right sides of a 4x2 artificial retina.

This implementation is:
- **ML-agnostic**: Clean separation from evolutionary algorithms
- **Gymnasium-compatible**: Follows Farama Foundation standards
- **Well-tested**: Comprehensive test suite included
- **Easy to use**: Simple API with multiple evaluation modes

## Installation

Using `uv` (recommended):

```bash
uv pip install -e .
```

Using pip:

```bash
pip install -e .
```

## Quick Start

```python
import gymnasium as gym
import gymnasium_retinatask

# Create environment
env = gym.make("RetinaTask-v0")

# Reset environment
obs, info = env.reset()

# Take a step
action = env.action_space.sample()  # Random classification
obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

## The Task

The artificial retina consists of 8 pixels arranged in a 4x2 grid:

```
Left side (4 pixels) | Right side (4 pixels)
```

### Objective

The agent must independently classify whether patterns on each side are "valid":
- **Left output**: 1.0 if left pattern is valid, 0.0 if invalid
- **Right output**: 1.0 if right pattern is valid, 0.0 if invalid

### Pattern Distribution

Out of 256 possible patterns (2^8):
- 64 patterns have both sides valid (25%)
- 64 patterns have only left valid (25%)
- 64 patterns have only right valid (25%)
- 64 patterns have neither side valid (25%)

### Why This Task?

This task is designed to test **modularity** in neural networks. The left and right classification problems should ideally be solved by separate, independent modules in the network. This makes it an excellent benchmark for:
- Modular neural network evolution
- Structure learning algorithms
- Neuroevolution techniques (NEAT, HyperNEAT, ES-HyperNEAT)

## Environment Details

### Observation Space

`Box(0, 1, (8,), float32)` - 8 retina pixels, each either 0 (off) or 1 (on)

### Action Space

`Box(0, 1, (2,), float32)` - Classification outputs:
- `action[0]`: Left side classification
- `action[1]`: Right side classification

### Rewards

By default, uses the fitness function from the original paper:

```python
reward = 1000.0 / (1.0 + error�)
```

where `error` is the sum of absolute differences between outputs and correct labels.

### Episode Modes

The environment supports three modes:

1. **Single Pattern** (default): One random pattern per episode
   ```python
   env = gym.make("RetinaTask-v0", mode="single_pattern")
   ```

2. **Batch**: Fixed number of random patterns per episode
   ```python
   env = gym.make("RetinaTask-v0", mode="batch", batch_size=100)
   ```

3. **Full Evaluation**: All 256 patterns in sequence
   ```python
   env = gym.make("RetinaTask-v0", mode="full_evaluation")
   ```

### Reward Types

- **paper** (default): Uses `1000.0 / (1.0 + error)` fitness function
- **simple**: Returns negative error directly

```python
env = gym.make("RetinaTask-v0", reward_type="simple")
```

## Examples

### Random Agent

```python
import gymnasium as gym
import gymnasium_retinatask

env = gym.make("RetinaTask-v0", mode="batch", batch_size=100)
obs, info = env.reset()

episode_reward = 0
while True:
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    episode_reward += reward
    if terminated:
        break

print(f"Total reward: {episode_reward:.2f}")
env.close()
```

### Perfect Agent (Baseline)

```python
import gymnasium as gym
import numpy as np
from gymnasium_retinatask import RetinaPatterns

env = gym.make("RetinaTask-v0", mode="full_evaluation")
obs, info = env.reset()

episode_reward = 0
while True:
    # Get perfect classification
    pattern = info["pattern"]
    left, right = RetinaPatterns.get_labels(pattern)
    action = np.array([left, right], dtype=np.float32)

    obs, reward, terminated, truncated, info = env.step(action)
    episode_reward += reward
    if terminated:
        break

print(f"Accuracy: 100%")
print(f"Reward: {episode_reward:.2f}")  # Should be 1000.0
env.close()
```

## Running Examples

The package includes several example scripts:

```bash
# Analyze pattern distribution
uv run python src/gymnasium_retinatask/examples/pattern_analysis.py

# Test with perfect agent (baseline)
uv run python src/gymnasium_retinatask/examples/perfect_agent.py

# Test with random agent
uv run python src/gymnasium_retinatask/examples/random_agent.py
```

## Advanced Examples

The `examples/` directory contains complete, working implementations using different ML frameworks:

### NEAT Evolution

Evolve neural networks using NEAT (NeuroEvolution of Augmenting Topologies):

```bash
# Install NEAT dependencies
uv sync --group examples-neat

# Run NEAT evolution (50 generations)
uv run python examples/neat_evolution.py
```

This example demonstrates:
- Configuring NEAT for the Retina Task
- Evaluating genomes on all 256 patterns
- Tracking evolution statistics across generations
- Testing the best evolved network

Expected results: ~75-90% accuracy after 50 generations.

### HyperNEAT Evolution

Evolve networks using HyperNEAT, which exploits the geometric structure of the retina:

```bash
# Install NEAT dependencies (same as above)
uv sync --group examples-neat

# Run HyperNEAT evolution (30 generations)
uv run python examples/hyperneat_evolution.py
```

HyperNEAT features:
- CPPN (Compositional Pattern Producing Network) generates substrate weights
- Substrate network matches the 2D retina geometry
- Encourages modular solutions for left/right independence
- Analyzes evolved network structure

The geometric substrate layout helps HyperNEAT discover modular solutions more efficiently than standard NEAT.

## Development

### Running Tests

```bash
uv run pytest src/gymnasium_retinatask/tests/ -v
```

### Code Formatting

```bash
uv run black src/
uv run isort src/
```

## Reference

This implementation is based on:

> Risi, S., & Stanley, K. O. (2012). An enhanced hypercube-based encoding for evolving the placement, density, and connectivity of neurons. *Artificial Life*, 18(4), 331-363. doi: 10.1162/ARTL_a_00071

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
