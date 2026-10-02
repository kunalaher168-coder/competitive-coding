"""Find a longest contiguous range containing at most K distinct values."""

from __future__ import annotations

import json
import sys


def longest_window(values: list[int], limit: int) -> dict[str, int]:
    """Return half-open bounds [start, end) and length; earliest tie wins."""
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    counts: dict[int, int] = {}
    left = 0
    best_left = 0
    best_length = 0

    for right, value in enumerate(values):
        counts[value] = counts.get(value, 0) + 1
        while len(counts) > limit:
            old = values[left]
            counts[old] -= 1
            if counts[old] == 0:
                del counts[old]
            left += 1
        length = right + 1 - left
        if length > best_length:
            best_left = left
            best_length = length
    return {"start": best_left, "end": best_left + best_length, "length": best_length}


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(longest_window(**data)))
