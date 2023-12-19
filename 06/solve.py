from __future__ import annotations

import functools
import math
import operator


def solve(time: int, distance: int) -> int:
    # if we hold for H, the distance we'll go is (time - H) * H
    # we want to find H s.t. (time - H) * H = distance
    # rewriting this, we get -H^2 + H*time - distance = 0
    # solutions are given by quadratic formula.
    a = -1
    b = time
    c = -distance
    discriminant = (b**2 - 4 * a * c) ** 0.5
    h_low, h_high = sorted(
        [(-b + discriminant) / (2 * a), (-b - discriminant) / (2 * a)]
    )
    h_low = max(0, math.floor(h_low) + 1)
    h_high = min(time, math.ceil(h_high) - 1)
    return h_high - h_low + 1


def main():
    times = [int(x) for x in input().split()[1:]]
    distances = [int(x) for x in input().split()[1:]]

    solutions = [solve(time, distance) for time, distance in zip(times, distances)]
    print(f"Part 1: {functools.reduce(operator.mul, solutions)}")

    big_time = int("".join(str(t) for t in times))
    big_distance = int("".join(str(d) for d in distances))
    print(f"Part 2: {solve(big_time, big_distance)}")


if __name__ == "__main__":
    main()
