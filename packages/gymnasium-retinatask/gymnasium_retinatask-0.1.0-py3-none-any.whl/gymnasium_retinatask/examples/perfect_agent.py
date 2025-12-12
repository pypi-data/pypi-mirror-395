"""Perfect agent example for the Retina Task.

This example demonstrates a perfect agent that uses the pattern validation
logic to achieve 100% accuracy. This serves as a baseline for ML algorithms.
"""

import gymnasium as gym
import numpy as np

import gymnasium_retinatask  # noqa: F401
from gymnasium_retinatask import RetinaPatterns


def main():
    """Run a perfect agent on the Retina Task."""
    # Create environment in full evaluation mode to test all patterns
    env = gym.make("RetinaTask-v0", mode="full_evaluation")

    print("=" * 60)
    print("Perfect Agent - Retina Task")
    print("=" * 60)
    print("\nThis agent uses the ground truth pattern validation")
    print("to achieve perfect classification on all 256 patterns.\n")

    obs, info = env.reset()
    episode_reward = 0.0
    correct_classifications = 0

    print(f"Evaluating all {info['total_patterns']} patterns...")

    while True:
        # Get the current pattern from the observation
        # Note: In a real ML scenario, the agent would not have access to
        # the pattern index, only the observation
        pattern = info["pattern"]

        # Get perfect classification using the pattern validation
        left_label, right_label = RetinaPatterns.get_labels(pattern)
        action = np.array([left_label, right_label], dtype=np.float32)

        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += float(reward)

        # Check if classification was correct
        if info["pattern_error"] == 0.0:
            correct_classifications += 1

        if terminated or truncated:
            break

    env.close()

    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Total patterns evaluated: {info['patterns_evaluated']}")
    print(f"Correct classifications: {correct_classifications}")
    print(
        f"Accuracy: {correct_classifications / info['patterns_evaluated'] * 100:.1f}%"
    )
    print(f"Total error: {info['total_error']:.2f}")
    print(f"Final reward: {episode_reward:.2f}")
    print("Expected reward (perfect): 1000.0")


if __name__ == "__main__":
    main()
