import sys
import itertools
from typing import Any


def reflection(arr: list[Any]) -> int:
    # Finds perfect reflection point or 0 if it doesn't exist
    for pivot in range(1, len(arr)):
        to_start = reversed(range(pivot))
        to_end = range(pivot, len(arr))
        if all(arr[i] == arr[j] for i, j in zip(to_start, to_end)):
            return pivot
    return 0


def main():
    lines = [line.strip() for line in sys.stdin]
    patterns = [list(group) for key, group in itertools.groupby(lines, bool) if key]

    answer = 0
    for pattern in patterns:
        horizontal = [hash(line) for line in pattern]
        vertical = [hash(column) for column in zip(*pattern)]
        answer += reflection(vertical) + 100 * reflection(horizontal)
    print(f"Part 1: {answer}")


if __name__ == "__main__":
    main()
