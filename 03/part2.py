import sys
import re
from collections import defaultdict


def is_gear(r: int, c: int, schematic: list[str]) -> bool:
    if 0 <= r < len(schematic) and 0 <= c < len(schematic[r]):
        return schematic[r][c] == "*"
    return False


def get_gear_ratios(schematic: list[str]) -> list[int]:
    regex = re.compile(r"\d+")
    gear_vals = defaultdict(list)
    for row_num, row in enumerate(schematic):
        for match in regex.finditer(row):
            start, end = match.span()
            for r in range(row_num - 1, row_num + 2):
                for c in range(start - 1, end + 1):
                    if is_gear(r, c, schematic):
                        gear_vals[(r, c)].append(int(match.group()))

    gear_ratios = []
    for gear_val in gear_vals.values():
        if len(gear_val) == 2:
            x, y = gear_val
            gear_ratios.append(x * y)
    return gear_ratios


def main():
    schematic = [line.strip() for line in sys.stdin.readlines()]

    print(sum(get_gear_ratios(schematic)))


if __name__ == "__main__":
    main()
