"""Retina Task Environment for Gymnasium.

This module implements the Left & Right Retina Problem, a benchmark task for
evolving modular neural networks, as described in:

Risi, S., & Stanley, K. O. (2012). "An enhanced hypercube-based encoding for
evolving the placement, density, and connectivity of neurons."
Artificial Life, 18(4), 331-363. doi: 10.1162/ARTL_a_00071

The task tests the ability to independently classify patterns on the left and
right sides of a 4x2 artificial retina.
"""

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class RetinaPatterns:
    """Manages pattern validation for the Retina Task.

    The retina consists of 8 pixels arranged in a 4x2 grid:
        Left side (4 pixels) | Right side (4 pixels)

    Each side has 8 valid 2x2 patterns out of 16 possible patterns.
    """

    # Valid patterns for the RIGHT side (bottom 4 bits of 8-bit pattern)
    # Pattern representation: bit 0-3 represent the 4 right pixels
    RIGHT_PATTERNS = [0b1011, 0b0111, 0b1110, 0b1101, 0b0010, 0b0001, 0b0011, 0b1111]

    # Valid patterns for the LEFT side (top 4 bits of 8-bit pattern)
    # Pattern representation: bit 4-7 represent the 4 left pixels
    LEFT_PATTERNS = [0b1000, 0b0100, 0b1100, 0b1111, 0b1011, 0b0111, 0b1110, 0b1101]

    @staticmethod
    def is_right_valid(pattern: int) -> bool:
        """Check if the right side of the pattern is valid.

        Args:
            pattern: 8-bit integer representing the full retina state.

        Returns:
            bool: True if the right 4 bits match a valid right pattern.
        """
        right_bits = pattern & 0b1111
        return right_bits in RetinaPatterns.RIGHT_PATTERNS

    @staticmethod
    def is_left_valid(pattern: int) -> bool:
        """Check if the left side of the pattern is valid.

        Args:
            pattern: 8-bit integer representing the full retina state.

        Returns:
            bool: True if the left 4 bits match a valid left pattern.
        """
        left_bits = (pattern & 0b11110000) >> 4
        return left_bits in RetinaPatterns.LEFT_PATTERNS

    @staticmethod
    def get_labels(pattern: int) -> tuple[float, float]:
        """Get the correct classification labels for a pattern.

        Args:
            pattern: 8-bit integer representing the full retina state.

        Returns:
            Tuple[float, float]: (left_label, right_label) where each is 1.0 for
            valid and 0.0 for invalid.
        """
        left_label = 1.0 if RetinaPatterns.is_left_valid(pattern) else 0.0
        right_label = 1.0 if RetinaPatterns.is_right_valid(pattern) else 0.0
        return left_label, right_label

    @staticmethod
    def pattern_to_observation(pattern: int) -> np.ndarray:
        """Convert an 8-bit pattern to an observation array.

        Args:
            pattern: 8-bit integer representing the retina state.

        Returns:
            np.ndarray: Array of shape (8,) with values in {0.0, 1.0}.
            Index 0 corresponds to bit 7 (leftmost pixel),
            Index 7 corresponds to bit 0 (rightmost pixel).
        """
        obs = np.zeros(8, dtype=np.float32)
        for i in range(8):
            if pattern & (1 << i):
                obs[7 - i] = 1.0
        return obs


class RetinaEnvV0(gym.Env):
    """Retina pattern classification environment.

    ## Description

    The Left & Right Retina Problem is a benchmark task for testing the evolution
    of modular neural networks. The agent must independently classify whether
    patterns on the left and right sides of a 4×2 artificial retina are valid.

    This is a good test of modularity because the left and right classification
    problems are ideally separated into different functional structures in the
    network.

    ## Observation Space

    The observation space is `Box(0, 1, (8,), float32)`, representing the 8 pixels
    of the retina. Each pixel is either 0 (off) or 1 (on).

    ## Action Space

    The action space is `Box(0, 1, (2,), float32)`, representing the classification
    outputs:
    - action[0]: Left side classification (close to 1.0 = valid, close to 0.0 = invalid)
    - action[1]: Right side classification (close to 1.0 = valid, close to 0.0 = invalid)

    ## Rewards

    The reward is based on classification accuracy using the fitness function from
    the original paper:

        reward = 1000.0 / (1.0 + error²)

    where error is the sum of absolute differences between the agent's outputs and
    the correct labels across all patterns in the episode.

    For single-step episodes, this gives immediate feedback on classification accuracy.

    ## Episode Termination

    Episodes can be configured in different modes:
    - `single_pattern`: One random pattern per episode (default)
    - `full_evaluation`: All 256 patterns in sequence (for comprehensive evaluation)
    - `batch`: A fixed number of random patterns per episode

    ## Arguments

    ```python
    import gymnasium as gym
    import gymnasium_retinatask

    env = gym.make("RetinaTask-v0")
    ```

    - `mode`: Episode mode - 'single_pattern', 'full_evaluation', or 'batch'
    - `batch_size`: Number of patterns per episode (only for 'batch' mode)
    - `reward_type`: 'paper' (uses fitness function) or 'simple' (negative error)
    """

    metadata = {
        "render_modes": [],
    }

    def __init__(
        self,
        mode: str = "single_pattern",
        batch_size: int = 100,
        reward_type: str = "paper",
    ):
        """Initialize the Retina Task environment.

        Args:
            mode: Episode mode - 'single_pattern', 'full_evaluation', or 'batch'.
            batch_size: Number of patterns per episode (only used in 'batch' mode).
            reward_type: 'paper' for fitness function, 'simple' for negative error.
        """
        super().__init__()

        self.mode = mode
        self.batch_size = batch_size
        self.reward_type = reward_type

        # Define action and observation spaces
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(8,), dtype=np.float32
        )
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32)

        # Episode state
        self.current_pattern: int | None = None
        self.pattern_index = 0
        self.all_patterns = list(range(256))
        self.total_error = 0.0
        self.patterns_evaluated = 0

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """Reset the environment and return initial observation.

        Args:
            seed: Random seed for reproducibility.
            options: Additional options (not used).

        Returns:
            Tuple[np.ndarray, Dict[str, Any]]: Initial observation and info dict.
        """
        super().reset(seed=seed)

        # Reset episode state
        self.pattern_index = 0
        self.total_error = 0.0
        self.patterns_evaluated = 0

        # Set up pattern sequence based on mode
        if self.mode == "full_evaluation":
            # Evaluate all 256 patterns in order
            self.all_patterns = list(range(256))
        elif self.mode == "single_pattern":
            # Single random pattern
            self.all_patterns = [self.np_random.integers(0, 256)]
        elif self.mode == "batch":
            # Random batch of patterns
            self.all_patterns = self.np_random.integers(
                0, 256, size=self.batch_size
            ).tolist()
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        # Get first pattern
        self.current_pattern = int(self.all_patterns[self.pattern_index])
        observation = RetinaPatterns.pattern_to_observation(self.current_pattern)

        info = {
            "pattern": self.current_pattern,
            "total_patterns": len(self.all_patterns),
        }

        return observation, info

    def step(
        self, action: np.ndarray
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """Execute one step in the environment.

        Args:
            action: Classification outputs [left_output, right_output].

        Returns:
            Tuple containing:
            - observation: Next pattern (or zeros if done)
            - reward: Reward for this step
            - terminated: Whether episode is complete
            - truncated: Always False
            - info: Additional information
        """
        if self.current_pattern is None:
            raise RuntimeError("Cannot call step() before reset()")

        # Clip action to valid range
        action = np.clip(action, 0.0, 1.0)

        # Get correct labels
        left_label, right_label = RetinaPatterns.get_labels(self.current_pattern)

        # Calculate error for this pattern
        pattern_error = abs(action[0] - left_label) + abs(action[1] - right_label)
        self.total_error += pattern_error
        self.patterns_evaluated += 1

        # Move to next pattern
        self.pattern_index += 1
        terminated = self.pattern_index >= len(self.all_patterns)

        # Get next observation
        if not terminated:
            self.current_pattern = int(self.all_patterns[self.pattern_index])
            observation = RetinaPatterns.pattern_to_observation(self.current_pattern)
        else:
            observation = np.zeros(8, dtype=np.float32)

        # Calculate reward
        if self.reward_type == "paper":
            # Use fitness function from paper: F = 1000.0 / (1.0 + E²)
            # For episodic: E is total error across all patterns
            # For single step: E is error for this pattern
            if self.mode == "single_pattern":
                reward = 1000.0 / (1.0 + pattern_error**2)
            else:
                # In batch/full eval, give final reward at end
                reward = 1000.0 / (1.0 + self.total_error**2) if terminated else 0.0
        else:
            # Simple: negative error
            reward = -pattern_error

        info = {
            "pattern": self.current_pattern if not terminated else None,
            "correct_left": left_label,
            "correct_right": right_label,
            "pattern_error": pattern_error,
            "total_error": self.total_error,
            "patterns_evaluated": self.patterns_evaluated,
        }

        return observation, reward, terminated, False, info


# Alias for convenience
RetinaEnv = RetinaEnvV0
