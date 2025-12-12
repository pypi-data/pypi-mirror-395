"""Gymnasium Retina Task - Left & Right Retina Problem.

A benchmark environment for testing modular neural network evolution.
Based on the task described in Risi & Stanley (Artificial Life 2012).
"""

from gymnasium.envs.registration import register

from gymnasium_retinatask.retina_env import RetinaEnv, RetinaEnvV0, RetinaPatterns

# Register the environment
register(
    id="RetinaTask-v0",
    entry_point="gymnasium_retinatask.retina_env:RetinaEnvV0",
    max_episode_steps=None,  # No limit - environment handles its own termination
)

__version__ = "0.1.0"
__all__ = ["RetinaEnv", "RetinaEnvV0", "RetinaPatterns"]
