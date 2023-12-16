from __future__ import annotations
import attrs
import sys
from functools import cache


@attrs.frozen
class Arrangement:
    conditions: str
    clue: list[int]

    @classmethod
    def parse(cls, line: str) -> Arrangement:
        conditions, clue_str = line.strip().split()
        clue = [int(x) for x in clue_str.split(",")]
        return cls(conditions=conditions, clue=clue)

    def maybe_damaged(self, i: int) -> bool:
        return self.conditions[i] in "?#"

    def maybe_undamaged(self, i: int) -> bool:
        return self.conditions[i] in "?."

    def count_ways(self) -> int:
        @cache
        def ways(i: int, j: int, cons: int) -> int:
            if i == len(self.conditions):
                if j == len(self.clue):
                    return 1
                if j == len(self.clue) - 1 and cons == self.clue[j]:
                    return 1
                return 0
            res = 0
            if self.maybe_damaged(i) and j < len(self.clue) and cons < self.clue[j]:
                # Extend current clue.
                res += ways(i + 1, j, cons + 1)
            if self.maybe_undamaged(i):
                if cons == 0:
                    # Delay applying current clue.
                    res += ways(i + 1, j, 0)
                elif j < len(self.clue) and cons == self.clue[j]:
                    # Move on to next clue.
                    res += ways(i + 1, j + 1, 0)
            return res

        return ways(0, 0, 0)


def main():
    arrangements = [Arrangement.parse(line) for line in sys.stdin]
    print(f"Part 1: {sum(a.count_ways() for a in arrangements)}")

    unfolded_arrangements = [
        Arrangement("?".join([a.conditions] * 5), a.clue * 5) for a in arrangements
    ]
    print(f"Part 2: {sum(a.count_ways() for a in unfolded_arrangements)}")


if __name__ == "__main__":
    main()
