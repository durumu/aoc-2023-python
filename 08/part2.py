import sys
import itertools
import re
import math


def path_length(node: str, directions: str, lookup: dict[tuple[str, str], str]) -> int:
    for step, direction in enumerate(itertools.cycle(directions)):
        if node.endswith("Z"):
            return step
        node = lookup[(node, direction)]


def main():
    direction_lines, lookup_lines = [
        list(group)
        for key, group in itertools.groupby(sys.stdin, lambda x: bool(x.strip()))
        if key
    ]
    directions = direction_lines[0].strip()

    lookup = {}
    starts = []
    for line in lookup_lines:
        start, left, right = re.findall(r"\b\w+\b", line)
        if start.endswith("A"):
            starts.append(start)
        lookup[(start, "L")] = left
        lookup[(start, "R")] = right

    print(math.lcm(*[path_length(start, directions, lookup) for start in starts]))


if __name__ == "__main__":
    main()
