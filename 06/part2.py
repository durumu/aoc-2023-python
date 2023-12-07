import math
import functools
import operator


def main():
    time = int("".join(x for x in input() if x.isdigit()))
    distance = int("".join(x for x in input() if x.isdigit()))
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
    print(h_high - h_low + 1)


if __name__ == "__main__":
    main()
