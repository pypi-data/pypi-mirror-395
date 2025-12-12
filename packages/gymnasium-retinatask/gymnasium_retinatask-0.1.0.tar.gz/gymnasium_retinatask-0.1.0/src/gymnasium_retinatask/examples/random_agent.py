"""Random agent example for the Retina Task.

This example demonstrates how to use the Retina Task environment with a
random agent that outputs random classifications.
"""

import gymnasium as gym
import numpy as np

import gymnasium_retinatask  # noqa: F401


def main():
    """Run a random agent on the Retina Task."""
    # Create environment in batch mode
    env = gym.make("RetinaTask-v0", mode="batch", batch_size=100)

    print("=" * 60)
    print("Random Agent - Retina Task")
    print("=" * 60)

    # Run multiple episodes
    num_episodes = 5
    total_rewards = []

    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0.0
        steps = 0

        print(f"\nEpisode {episode + 1}")
        print(f"  Total patterns to classify: {info['total_patterns']}")

        while True:
            # Random action (classification outputs)
            action = env.action_space.sample()

            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += float(reward)
            steps += 1

            if terminated or truncated:
                break

        total_rewards.append(episode_reward)
        print(f"  Steps: {steps}")
        print(f"  Total error: {info['total_error']:.2f}")
        print(f"  Episode reward: {episode_reward:.2f}")

    env.close()

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Average reward: {np.mean(total_rewards):.2f} ± {np.std(total_rewards):.2f}")
    print(f"Max reward: {np.max(total_rewards):.2f}")
    print(f"Min reward: {np.min(total_rewards):.2f}")


if __name__ == "__main__":
    main()
