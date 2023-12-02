import sys
import re

DIGIT_MAP: dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def make_digit_regex() -> re.Pattern:
    digits = "|".join([r"\d", *DIGIT_MAP.keys()])
    return re.compile(f"(?=({digits}))")


def main():
    ans = 0
    regex = make_digit_regex()
    for line in sys.stdin:
        digits = [DIGIT_MAP.get(d, d) for d in regex.findall(line)]
        ans += int(digits[0] + digits[-1])
    print(ans)


if __name__ == "__main__":
    main()
