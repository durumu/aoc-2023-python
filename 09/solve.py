import sys
import itertools


def main():
    histories = [[int(x) for x in line.split()] for line in sys.stdin]
    forward_extrapolations = []
    backward_extrapolations = []
    for history in histories:
        sequences = [history]
        while not all(x == 0 for x in sequences[-1]):
            sequences.append([b - a for a, b in itertools.pairwise(sequences[-1])])
        forward_extrapolations.append(sum(sequence[-1] for sequence in sequences))

        backward = 0
        for sequence in reversed(sequences[:-1]):
            backward = sequence[0] - backward
        backward_extrapolations.append(backward)

    print(f"Part 1: {sum(forward_extrapolations)}")
    print(f"Part 2: {sum(backward_extrapolations)}")


if __name__ == "__main__":
    main()
