import sys


def main():
    ans = 0
    for line in sys.stdin:
        digits = [c for c in line if c.isdigit()]
        ans += int(digits[0] + digits[-1])
    print(ans)


if __name__ == "__main__":
    main()
