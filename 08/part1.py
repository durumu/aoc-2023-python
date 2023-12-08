import sys
import itertools
import re


def main():
    direction_lines, lookup_lines = [
        list(group)
        for key, group in itertools.groupby(sys.stdin, lambda x: bool(x.strip()))
        if key
    ]
    directions = direction_lines[0].strip()

    lookup = {}
    for line in lookup_lines:
        start, left, right = re.findall(r"\b\w+\b", line)
        lookup[(start, "L")] = left
        lookup[(start, "R")] = right

    cur_node = "AAA"
    for step, direction in enumerate(itertools.cycle(directions)):
        if cur_node == "ZZZ":
            print(step)
            break
        cur_node = lookup[(cur_node, direction)]


if __name__ == "__main__":
    main()
