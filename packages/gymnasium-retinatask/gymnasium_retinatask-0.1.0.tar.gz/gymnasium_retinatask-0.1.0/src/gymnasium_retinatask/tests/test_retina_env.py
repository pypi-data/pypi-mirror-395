"""Tests for the Retina Task environment."""

from typing import cast

import gymnasium as gym
import numpy as np
import pytest

from gymnasium_retinatask import RetinaEnvV0


class TestRetinaPatterns:
    """Test pattern validation logic."""

    def test_all_valid_left_patterns(self):
        """Verify all 8 valid left patterns are correctly identified."""
        from gymnasium_retinatask import RetinaPatterns

        valid_left = [0b1000, 0b0100, 0b1100, 0b1111, 0b1011, 0b0111, 0b1110, 0b1101]

        for pattern in valid_left:
            # Shift to left side (bits 4-7) and test
            full_pattern = pattern << 4
            assert RetinaPatterns.is_left_valid(
                full_pattern
            ), f"Pattern {pattern:04b} should be valid on left"

    def test_all_valid_right_patterns(self):
        """Verify all 8 valid right patterns are correctly identified."""
        from gymnasium_retinatask import RetinaPatterns

        valid_right = [0b1011, 0b0111, 0b1110, 0b1101, 0b0010, 0b0001, 0b0011, 0b1111]

        for pattern in valid_right:
            assert RetinaPatterns.is_right_valid(
                pattern
            ), f"Pattern {pattern:04b} should be valid on right"

    def test_invalid_patterns_rejected(self):
        """Verify that invalid patterns are correctly rejected."""
        from gymnasium_retinatask import RetinaPatterns

        # All possible 4-bit patterns
        all_patterns = set(range(16))

        # Valid patterns
        valid_left = {0b1000, 0b0100, 0b1100, 0b1111, 0b1011, 0b0111, 0b1110, 0b1101}
        valid_right = {0b1011, 0b0111, 0b1110, 0b1101, 0b0010, 0b0001, 0b0011, 0b1111}

        # Invalid patterns are the complement
        invalid_left = all_patterns - valid_left
        invalid_right = all_patterns - valid_right

        # Test invalid left patterns
        for pattern in invalid_left:
            full_pattern = pattern << 4
            assert not RetinaPatterns.is_left_valid(
                full_pattern
            ), f"Pattern {pattern:04b} should be invalid on left"

        # Test invalid right patterns
        for pattern in invalid_right:
            assert not RetinaPatterns.is_right_valid(
                pattern
            ), f"Pattern {pattern:04b} should be invalid on right"

    def test_pattern_independence(self):
        """Verify left and right pattern validation are independent."""
        from gymnasium_retinatask import RetinaPatterns

        # Valid left (0b1000 = 8), invalid right (0b0000 = 0)
        pattern = (0b1000 << 4) | 0b0000
        assert RetinaPatterns.is_left_valid(pattern)
        assert not RetinaPatterns.is_right_valid(pattern)

        # Invalid left (0b0000 = 0), valid right (0b1011 = 11)
        pattern = (0b0000 << 4) | 0b1011
        assert not RetinaPatterns.is_left_valid(pattern)
        assert RetinaPatterns.is_right_valid(pattern)

        # Both valid
        pattern = (0b1000 << 4) | 0b1011
        assert RetinaPatterns.is_left_valid(pattern)
        assert RetinaPatterns.is_right_valid(pattern)

        # Both invalid
        pattern = (0b0000 << 4) | 0b0000
        assert not RetinaPatterns.is_left_valid(pattern)
        assert not RetinaPatterns.is_right_valid(pattern)

    def test_exactly_64_fully_valid_patterns(self):
        """Verify there are exactly 64 patterns with both sides valid (8 * 8)."""
        from gymnasium_retinatask import RetinaPatterns

        fully_valid_count = 0
        for pattern in range(256):
            if RetinaPatterns.is_left_valid(pattern) and RetinaPatterns.is_right_valid(
                pattern
            ):
                fully_valid_count += 1

        assert (
            fully_valid_count == 64
        ), f"Expected 64 fully valid patterns, got {fully_valid_count}"

    def test_pattern_to_observation_bit_order(self):
        """Verify bit ordering in observation matches pattern bits correctly."""
        from gymnasium_retinatask import RetinaPatterns

        # Test specific bit patterns
        test_cases = [
            (0b00000001, [0, 0, 0, 0, 0, 0, 0, 1]),  # Rightmost bit
            (0b10000000, [1, 0, 0, 0, 0, 0, 0, 0]),  # Leftmost bit
            (0b11110000, [1, 1, 1, 1, 0, 0, 0, 0]),  # Left side on
            (0b00001111, [0, 0, 0, 0, 1, 1, 1, 1]),  # Right side on
            (0b10101010, [1, 0, 1, 0, 1, 0, 1, 0]),  # Alternating
            (0b01010101, [0, 1, 0, 1, 0, 1, 0, 1]),  # Alternating inverse
        ]

        for pattern, expected in test_cases:
            obs = RetinaPatterns.pattern_to_observation(pattern)
            expected_array = np.array(expected, dtype=np.float32)
            assert np.array_equal(
                obs, expected_array
            ), f"Pattern {pattern:08b} -> {obs} != {expected_array}"

    def test_get_labels_correctness(self):
        """Verify get_labels returns correct classification for all patterns."""
        from gymnasium_retinatask import RetinaPatterns

        for pattern in range(256):
            left_label, right_label = RetinaPatterns.get_labels(pattern)

            # Labels should match individual validity checks
            expected_left = 1.0 if RetinaPatterns.is_left_valid(pattern) else 0.0
            expected_right = 1.0 if RetinaPatterns.is_right_valid(pattern) else 0.0

            assert (
                left_label == expected_left
            ), f"Pattern {pattern:08b}: left label mismatch"
            assert (
                right_label == expected_right
            ), f"Pattern {pattern:08b}: right label mismatch"


class TestRetinaEnv:
    """Test the Retina environment."""

    def test_observation_space_bounds(self):
        """Verify observation space is properly bounded [0, 1]."""
        from gymnasium import spaces

        env = gym.make("RetinaTask-v0")
        obs_space = cast(spaces.Box, env.observation_space)
        assert obs_space.low.min() == 0.0
        assert obs_space.high.max() == 1.0
        assert obs_space.shape == (8,)
        assert obs_space.dtype == np.float32
        env.close()

    def test_action_space_bounds(self):
        """Verify action space is properly bounded [0, 1]."""
        from gymnasium import spaces

        env = gym.make("RetinaTask-v0")
        action_space = cast(spaces.Box, env.action_space)
        assert action_space.low.min() == 0.0
        assert action_space.high.max() == 1.0
        assert action_space.shape == (2,)
        assert action_space.dtype == np.float32
        env.close()

    def test_seed_reproducibility_single_pattern(self):
        """Verify seeding produces reproducible pattern sequences."""
        env1 = gym.make("RetinaTask-v0", mode="single_pattern")
        env2 = gym.make("RetinaTask-v0", mode="single_pattern")

        # Reset with same seed
        obs1, info1 = env1.reset(seed=42)
        obs2, info2 = env2.reset(seed=42)

        assert info1["pattern"] == info2["pattern"]
        assert np.array_equal(obs1, obs2)

        # Different seed should give different pattern (with high probability)
        obs3, info3 = env1.reset(seed=123)
        # Not guaranteed but extremely likely to be different
        assert not np.array_equal(obs1, obs3) or info1["pattern"] != info3["pattern"]

        env1.close()
        env2.close()

    def test_seed_reproducibility_batch_mode(self):
        """Verify seeding produces reproducible batch sequences."""
        env1 = gym.make("RetinaTask-v0", mode="batch", batch_size=20)
        env2 = gym.make("RetinaTask-v0", mode="batch", batch_size=20)

        # Collect all patterns from both envs with same seed
        patterns1 = []
        patterns2 = []

        obs1, info1 = env1.reset(seed=42)
        obs2, info2 = env2.reset(seed=42)
        patterns1.append(info1["pattern"])
        patterns2.append(info2["pattern"])

        for _ in range(19):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs1, _, _, _, info1 = env1.step(action)
            obs2, _, _, _, info2 = env2.step(action)
            if info1["pattern"] is not None:
                patterns1.append(info1["pattern"])
            if info2["pattern"] is not None:
                patterns2.append(info2["pattern"])

        assert patterns1 == patterns2

        env1.close()
        env2.close()

    def test_full_evaluation_covers_all_patterns(self):
        """Verify full_evaluation mode presents all 256 patterns exactly once."""
        env = gym.make("RetinaTask-v0", mode="full_evaluation")
        obs, info = env.reset()

        patterns_seen = {info["pattern"]}

        for _ in range(255):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)
            if info["pattern"] is not None:
                patterns_seen.add(info["pattern"])

        # Should have seen all 256 patterns
        assert len(patterns_seen) == 256
        assert patterns_seen == set(range(256))

        env.close()

    def test_action_clipping(self):
        """Verify actions outside [0, 1] are clipped correctly."""
        env = gym.make("RetinaTask-v0", mode="single_pattern")
        obs, info = env.reset(seed=42)

        # Get the correct labels for comparison
        from gymnasium_retinatask import RetinaPatterns

        left_label, right_label = RetinaPatterns.get_labels(info["pattern"])

        # Test clipping high values
        action_high = np.array([1.5, 2.0], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action_high)

        # Error should be calculated as if action was [1.0, 1.0]
        expected_error = abs(1.0 - left_label) + abs(1.0 - right_label)
        assert info["pattern_error"] == pytest.approx(expected_error)

        # Reset and test clipping low values
        obs, info = env.reset(seed=42)
        action_low = np.array([-0.5, -1.0], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action_low)

        # Error should be calculated as if action was [0.0, 0.0]
        expected_error = abs(0.0 - left_label) + abs(0.0 - right_label)
        assert info["pattern_error"] == pytest.approx(expected_error)

        env.close()

    def test_reward_paper_formula(self):
        """Verify the paper's fitness function is correctly implemented."""
        env = gym.make("RetinaTask-v0", mode="single_pattern", reward_type="paper")

        # Test with known error values
        test_cases = [
            (0.0, 1000.0),  # Perfect: 1000 / (1 + 0²) = 1000
            (1.0, 500.0),  # Error 1: 1000 / (1 + 1²) = 500
            (2.0, 200.0),  # Error 2: 1000 / (1 + 2²) = 200
        ]

        for target_error, expected_reward in test_cases:
            obs, info = env.reset(seed=42)
            from gymnasium_retinatask import RetinaPatterns

            left_label, right_label = RetinaPatterns.get_labels(info["pattern"])

            # Create action that produces the target error
            # If target_error = 0, action should match labels
            # If target_error = 2, we could use action = [1-left_label, 1-right_label]
            if target_error == 0.0:
                action = np.array([left_label, right_label], dtype=np.float32)
            elif target_error == 2.0:
                # Opposite of correct labels gives error of 2
                action = np.array(
                    [1.0 - left_label, 1.0 - right_label], dtype=np.float32
                )
            elif target_error == 1.0:
                # One correct, one wrong
                action = np.array([left_label, 1.0 - right_label], dtype=np.float32)

            obs, reward, terminated, truncated, info = env.step(action)

            # Verify reward matches formula
            calculated_reward = 1000.0 / (1.0 + info["pattern_error"] ** 2)
            assert reward == pytest.approx(
                calculated_reward
            ), f"Expected reward {expected_reward}, got {reward}"

        env.close()

    def test_reward_simple_formula(self):
        """Verify simple reward is negative error."""
        env = gym.make("RetinaTask-v0", mode="single_pattern", reward_type="simple")
        obs, info = env.reset(seed=42)

        from gymnasium_retinatask import RetinaPatterns

        left_label, right_label = RetinaPatterns.get_labels(info["pattern"])

        # Test with specific action
        action = np.array([0.3, 0.7], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        # Simple reward should be -error
        expected_reward = -info["pattern_error"]
        assert reward == pytest.approx(expected_reward)

        env.close()

    def test_error_accumulation_batch_mode(self):
        """Verify error accumulates correctly across batch."""
        env = gym.make(
            "RetinaTask-v0", mode="batch", batch_size=10, reward_type="paper"
        )
        obs, info = env.reset(seed=42)

        total_error_manual = 0.0

        for i in range(10):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)

            # Track error manually
            # Get previous pattern (current one in info is the next pattern)
            # Actually, we need to calculate based on the info returned
            total_error_manual += info["pattern_error"]

            # Verify total_error in info matches our calculation
            assert info["total_error"] == pytest.approx(total_error_manual)

            # Only last step should have non-zero reward
            if i < 9:
                assert reward == 0.0
            else:
                expected_final_reward = 1000.0 / (1.0 + total_error_manual**2)
                assert reward == pytest.approx(expected_final_reward)

        env.close()

    def test_perfect_score_all_patterns(self):
        """Verify perfect classification on all patterns gives maximum reward."""
        env = gym.make("RetinaTask-v0", mode="full_evaluation", reward_type="paper")
        obs, info = env.reset()

        from gymnasium_retinatask import RetinaPatterns

        for _ in range(256):
            # Get correct labels for current pattern
            pattern = info["pattern"]
            left_label, right_label = RetinaPatterns.get_labels(pattern)

            # Give perfect action
            action = np.array([left_label, right_label], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)

        # With perfect classification, total error should be 0
        assert info["total_error"] == pytest.approx(0.0)
        # Final reward should be 1000.0 / (1.0 + 0.0) = 1000.0
        assert reward == pytest.approx(1000.0)

        env.close()

    def test_worst_score_calculation(self):
        """Verify worst possible classification gives expected low reward."""
        env = gym.make("RetinaTask-v0", mode="full_evaluation", reward_type="paper")
        obs, info = env.reset()

        from gymnasium_retinatask import RetinaPatterns

        for _ in range(256):
            # Get correct labels
            pattern = info["pattern"]
            left_label, right_label = RetinaPatterns.get_labels(pattern)

            # Give opposite action (worst possible)
            action = np.array([1.0 - left_label, 1.0 - right_label], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)

        # Each pattern contributes error of 2.0 (both sides wrong by 1.0)
        # Total error = 256 * 2.0 = 512.0
        assert info["total_error"] == pytest.approx(512.0)
        # Reward = 1000.0 / (1.0 + 512.0²) = 1000.0 / (1.0 + 262144.0)
        expected_reward = 1000.0 / (1.0 + 512.0**2)
        assert reward == pytest.approx(expected_reward)

        env.close()

    def test_step_before_reset_raises(self):
        """Verify calling step() before reset() raises an error."""
        from gymnasium.error import ResetNeeded

        env = gym.make("RetinaTask-v0")

        with pytest.raises(ResetNeeded):
            action = np.array([0.5, 0.5], dtype=np.float32)
            env.step(action)

        env.close()

    def test_invalid_mode_raises(self):
        """Verify invalid mode raises an error on reset."""
        from gymnasium_retinatask import RetinaEnvV0

        # Create unwrapped env to test invalid mode handling
        env = RetinaEnvV0(mode="valid_mode")
        env.mode = "invalid_mode"  # Directly set invalid mode

        with pytest.raises(ValueError, match="Unknown mode"):
            env.reset()

    def test_episode_termination_single_pattern(self):
        """Verify single_pattern mode terminates after one step."""
        env = gym.make("RetinaTask-v0", mode="single_pattern")
        obs, info = env.reset()

        action = np.array([0.5, 0.5], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        assert terminated
        assert not truncated
        assert info["patterns_evaluated"] == 1

        env.close()

    def test_episode_termination_batch(self):
        """Verify batch mode terminates after batch_size steps."""
        batch_size = 15
        env = gym.make("RetinaTask-v0", mode="batch", batch_size=batch_size)
        obs, info = env.reset()

        for i in range(batch_size):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)

            if i < batch_size - 1:
                assert not terminated
            else:
                assert terminated

        assert info["patterns_evaluated"] == batch_size

        env.close()

    def test_info_dict_completeness(self):
        """Verify info dict contains all expected keys."""
        env = gym.make("RetinaTask-v0", mode="single_pattern")
        obs, info = env.reset()

        # Reset info should have these keys
        assert "pattern" in info
        assert "total_patterns" in info

        action = np.array([0.5, 0.5], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        # Step info should have these keys
        expected_keys = {
            "pattern",
            "correct_left",
            "correct_right",
            "pattern_error",
            "total_error",
            "patterns_evaluated",
        }
        assert set(info.keys()) == expected_keys

        env.close()

    def test_observation_values_are_binary(self):
        """Verify observations only contain 0.0 and 1.0."""
        env = gym.make("RetinaTask-v0", mode="batch", batch_size=50)
        obs, info = env.reset()

        # Check reset observation
        assert np.all((obs == 0.0) | (obs == 1.0))

        # Check step observations
        for _ in range(50):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)
            if not terminated:
                assert np.all((obs == 0.0) | (obs == 1.0))

        env.close()

    def test_correct_labels_in_info(self):
        """Verify info dict contains correct labels that match the pattern."""
        env = gym.make("RetinaTask-v0", mode="single_pattern")
        obs, info = env.reset(seed=42)

        from gymnasium_retinatask import RetinaPatterns

        action = np.array([0.5, 0.5], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        # The pattern from reset should be used
        pattern = info[
            "pattern"
        ]  # This is None after termination, but we get it from previous
        # Actually, we need to save it from reset
        obs, info_reset = env.reset(seed=42)
        pattern = info_reset["pattern"]

        action = np.array([0.5, 0.5], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        # Verify correct labels match pattern validation
        expected_left, expected_right = RetinaPatterns.get_labels(pattern)
        assert info["correct_left"] == expected_left
        assert info["correct_right"] == expected_right

        env.close()

    def test_pattern_distribution_batch_mode(self):
        """Verify batch mode samples from full pattern space."""
        env = gym.make("RetinaTask-v0", mode="batch", batch_size=256)

        # Run multiple episodes and collect patterns
        all_patterns = []
        for episode in range(10):
            obs, info = env.reset()
            patterns_this_episode = [info["pattern"]]

            for _ in range(255):
                action = np.array([0.5, 0.5], dtype=np.float32)
                obs, reward, terminated, truncated, info = env.step(action)
                if info["pattern"] is not None:
                    patterns_this_episode.append(info["pattern"])

            all_patterns.extend(patterns_this_episode)

        # With 10 episodes of 256 patterns each, we should see good coverage
        unique_patterns = set(all_patterns)
        # We expect to see most patterns at least once (not all due to randomness)
        assert (
            len(unique_patterns) > 200
        ), f"Only saw {len(unique_patterns)}/256 patterns"

        env.close()

    def test_zero_observation_after_termination(self):
        """Verify observation is zeros after episode terminates."""
        env = gym.make("RetinaTask-v0", mode="single_pattern")
        obs, info = env.reset()

        action = np.array([0.5, 0.5], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(action)

        assert terminated
        assert np.all(obs == 0.0)

        env.close()

    def test_pattern_index_increments(self):
        """Verify pattern_index increments correctly through episode."""
        env = gym.make("RetinaTask-v0", mode="batch", batch_size=5)
        obs, info = env.reset()

        # Access unwrapped environment to check internal state
        unwrapped = cast(RetinaEnvV0, env.unwrapped)

        # pattern_index should start at 0 after reset
        assert unwrapped.pattern_index == 0

        for i in range(5):
            action = np.array([0.5, 0.5], dtype=np.float32)
            obs, reward, terminated, truncated, info = env.step(action)

            # After step i, pattern_index should be i+1
            assert unwrapped.pattern_index == i + 1

        env.close()

    def test_multiple_episodes_reset_state(self):
        """Verify environment properly resets state between episodes."""
        env = gym.make("RetinaTask-v0", mode="batch", batch_size=10)
        unwrapped = cast(RetinaEnvV0, env.unwrapped)

        # First episode
        obs1, info1 = env.reset(seed=42)
        for _ in range(10):
            action = np.array([0.5, 0.5], dtype=np.float32)
            env.step(action)

        # Second episode with same seed
        obs2, info2 = env.reset(seed=42)

        # Verify internal state was reset
        assert unwrapped.pattern_index == 0
        assert unwrapped.total_error == 0.0
        assert unwrapped.patterns_evaluated == 0
        assert np.array_equal(obs1, obs2)
        assert info1["pattern"] == info2["pattern"]

        env.close()
