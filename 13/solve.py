from __future__ import annotations

import itertools
import sys
from functools import cached_property

import attrs


@attrs.define(slots=False)
class Pattern:
    grid: list[str]

    @cached_property
    def transpose(self) -> Pattern:
        return Pattern(["".join(tup) for tup in zip(*self.grid)])

    @cached_property
    def reflections(self) -> list[int]:
        """Finds perfect reflection points"""
        pivots = []
        for pivot in range(1, len(self.grid)):
            to_start = reversed(range(pivot))
            to_end = range(pivot, len(self.grid))
            if all(self.grid[i] == self.grid[j] for i, j in zip(to_start, to_end)):
                pivots.append(pivot)
        return pivots

    @cached_property
    def smudges(self) -> list[Pattern]:
        """All smudges that could potentially change the reflection"""
        row_set = set(self.grid)
        smudges = []
        for r, row in enumerate(self.grid):
            for c in range(len(row)):
                smudged = row[:c] + ("." if row[c] == "#" else "#") + row[c + 1 :]
                if smudged in row_set:
                    smudges.append(
                        Pattern(self.grid[:r] + [smudged] + self.grid[r + 1 :])
                    )
        return smudges

    @cached_property
    def reflection_id(self) -> int:
        return sum(self.reflections) * 100 + sum(self.transpose.reflections)

    def __str__(self) -> str:
        return "\n".join(self.grid)


def main():
    lines = [line.strip() for line in sys.stdin]
    patterns = [
        Pattern(list(group)) for key, group in itertools.groupby(lines, bool) if key
    ]

    p1_ans = 0
    p2_ans = 0
    for pattern in patterns:
        p1_ans += pattern.reflection_id
        smudges = [*pattern.smudges, *(s.transpose for s in pattern.transpose.smudges)]
        for smudge in smudges:
            if smudge.reflection_id and smudge.reflection_id != pattern.reflection_id:
                p2_ans += smudge.reflection_id
                if len(smudge.reflections) + len(smudge.transpose.reflections) > 1:
                    p2_ans -= pattern.reflection_id
                break
        else:
            raise AssertionError

    print(f"Part 1: {p1_ans}")
    print(f"Part 2: {p2_ans}")


if __name__ == "__main__":
    main()
