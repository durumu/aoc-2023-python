from __future__ import annotations

import re
import sys
from collections import defaultdict

NON_SYMBOLS = set("1234567890.")


def is_symbol(r: int, c: int, schematic: list[str]) -> bool:
    if 0 <= r < len(schematic) and 0 <= c < len(schematic[r]):
        return schematic[r][c] not in NON_SYMBOLS
    return False


def get_part_numbers_and_gears(
    schematic: list[str],
) -> list[tuple[int, tuple[int, int]]]:
    regex = re.compile(r"\d+")
    numbers_and_gears = []
    for row_num, row in enumerate(schematic):
        for match in regex.finditer(row):
            start, end = match.span()

            symbols = [
                (r, c)
                for r in range(row_num - 1, row_num + 2)
                for c in range(start - 1, end + 1)
                if is_symbol(r, c, schematic)
            ]
            if symbols:
                numbers_and_gears.append(
                    (
                        int(match.group()),
                        [(r, c) for r, c in symbols if schematic[r][c] == "*"],
                    )
                )
    return numbers_and_gears


def get_gear_ratios(
    part_numbers_and_gears: list[tuple[int, tuple[int, int]]],
) -> list[int]:
    gear_vals = defaultdict(list)
    for part_number, gears in part_numbers_and_gears:
        for gear in gears:
            gear_vals[gear].append(part_number)

    gear_ratios = []
    for gear_val in gear_vals.values():
        if len(gear_val) == 2:
            x, y = gear_val
            gear_ratios.append(x * y)
    return gear_ratios


def main():
    schematic = [line.strip() for line in sys.stdin.readlines()]

    part_numbers_and_gears = get_part_numbers_and_gears(schematic)

    print(f"Part 1: {sum(x for x, _ in part_numbers_and_gears)}")
    print(f"Part 2: {sum(get_gear_ratios(part_numbers_and_gears))}")


if __name__ == "__main__":
    main()
