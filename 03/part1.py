import sys
import re


NON_SYMBOLS = set("1234567890.")


def is_symbol(r: int, c: int, schematic: list[str]) -> bool:
    if 0 <= r < len(schematic) and 0 <= c < len(schematic[r]):
        return schematic[r][c] not in NON_SYMBOLS
    return False


def get_part_numbers(schematic: list[str]) -> list[int]:
    regex = re.compile(r"\d+")
    numbers = []
    for row_num, row in enumerate(schematic):
        for match in regex.finditer(row):
            start, end = match.span()

            if any(
                is_symbol(r, c, schematic)
                for r in range(row_num - 1, row_num + 2)
                for c in range(start - 1, end + 1)
            ):
                numbers.append(int(match.group()))
    return numbers


def main():
    schematic = [line.strip() for line in sys.stdin.readlines()]

    print(sum(get_part_numbers(schematic)))


if __name__ == "__main__":
    main()
