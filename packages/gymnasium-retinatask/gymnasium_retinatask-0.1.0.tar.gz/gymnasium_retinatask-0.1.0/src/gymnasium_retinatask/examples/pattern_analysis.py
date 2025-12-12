"""Analyze the distribution of patterns in the Retina Task.

This script analyzes all 256 possible patterns and their classifications.
"""

from gymnasium_retinatask import RetinaPatterns


def visualize_pattern(pattern: int) -> str:
    """Create a text visualization of a pattern.

    Args:
        pattern: 8-bit pattern to visualize.

    Returns:
        str: Text visualization of the pattern.
    """
    obs = RetinaPatterns.pattern_to_observation(pattern)
    # obs is ordered from bit 7 to bit 0
    # Reshape to 2x4 (2 rows, 4 columns)
    grid = obs.reshape(2, 4)

    lines = []
    lines.append("  Left  | Right")
    lines.append("--------+-------")
    for row in grid:
        left = "".join("█" if val > 0.5 else "·" for val in row[:2])
        right = "".join("█" if val > 0.5 else "·" for val in row[2:])
        lines.append(f"  {left}  |  {right}")

    return "\n".join(lines)


def main():
    """Analyze all 256 patterns."""
    print("=" * 60)
    print("Retina Task Pattern Analysis")
    print("=" * 60)

    # Count pattern types
    both_valid = 0
    only_left = 0
    only_right = 0
    neither_valid = 0

    for pattern in range(256):
        left_valid = RetinaPatterns.is_left_valid(pattern)
        right_valid = RetinaPatterns.is_right_valid(pattern)

        if left_valid and right_valid:
            both_valid += 1
        elif left_valid:
            only_left += 1
        elif right_valid:
            only_right += 1
        else:
            neither_valid += 1

    print("\nPattern Distribution:")
    print(
        f"  Both sides valid:     {both_valid:3d} / 256 ({both_valid / 256 * 100:.1f}%)"
    )
    print(
        f"  Only left valid:      {only_left:3d} / 256 ({only_left / 256 * 100:.1f}%)"
    )
    print(
        f"  Only right valid:     {only_right:3d} / 256 ({only_right / 256 * 100:.1f}%)"
    )
    print(
        f"  Neither side valid:   {neither_valid:3d} / 256 ({neither_valid / 256 * 100:.1f}%)"
    )
    print(
        f"  Total:                {both_valid + only_left + only_right + neither_valid:3d}"
    )

    # Show some example patterns
    print("\n" + "=" * 60)
    print("Example Patterns")
    print("=" * 60)

    examples = [
        (
            "Both valid",
            lambda p: RetinaPatterns.is_left_valid(p)
            and RetinaPatterns.is_right_valid(p),
        ),
        (
            "Only left",
            lambda p: RetinaPatterns.is_left_valid(p)
            and not RetinaPatterns.is_right_valid(p),
        ),
        (
            "Only right",
            lambda p: not RetinaPatterns.is_left_valid(p)
            and RetinaPatterns.is_right_valid(p),
        ),
        (
            "Neither",
            lambda p: not RetinaPatterns.is_left_valid(p)
            and not RetinaPatterns.is_right_valid(p),
        ),
    ]

    for category, condition in examples:
        print(f"\n{category}:")
        # Find first pattern matching condition
        for pattern in range(256):
            if condition(pattern):
                print(f"\nPattern {pattern} (0b{pattern:08b}):")
                print(visualize_pattern(pattern))
                left, right = RetinaPatterns.get_labels(pattern)
                print(f"Labels: Left={left:.0f}, Right={right:.0f}")
                break


if __name__ == "__main__":
    main()
