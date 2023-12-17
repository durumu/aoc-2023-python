from __future__ import annotations
import sys
import attrs
import itertools
from functools import cached_property
from typing import ClassVar


def _slide_row(row: str, reverse: bool) -> str:
    groups = itertools.groupby(row, lambda c: c == "#")
    return "".join("".join(sorted(group, reverse=reverse)) for _, group in groups)


@attrs.frozen
class Grid:
    grid: list[str]

    def transpose(self) -> Grid:
        return Grid(["".join(tup) for tup in zip(*self.grid)])

    def slide_left(self) -> Grid:
        return Grid([_slide_row(row, reverse=True) for row in self.grid])

    def slide_right(self) -> Grid:
        return Grid([_slide_row(row, reverse=False) for row in self.grid])

    def slide_up(self) -> Grid:
        return self.transpose().slide_left().transpose()

    def slide_down(self) -> Grid:
        return self.transpose().slide_right().transpose()

    def spin_cycle(self) -> Grid:
        return self.slide_up().slide_left().slide_down().slide_right()

    @property
    def load(self) -> int:
        return sum(
            (i + 1) * row.count("O") for i, row in enumerate(reversed(self.grid))
        )

    def cycle_length(self) -> tuple[int, int]:
        """Return tuple of (cycle length, cycle start)"""
        spin = self
        first_seen = {}
        for iteration in itertools.count():
            if str(spin) in first_seen:
                cycle_length = iteration - first_seen[str(spin)]
                return (cycle_length, first_seen[str(spin)])
            first_seen[str(spin)] = iteration
            spin = spin.spin_cycle()
        raise AssertionError

    def __str__(self) -> str:
        return "\n".join(self.grid)


def main():
    grid = Grid([line.strip() for line in sys.stdin])

    print(f"Part 1: {grid.slide_up().load}")

    n_iterations = 1000000000
    cycle_length, cycle_start = grid.cycle_length()
    spin = grid
    for _ in range(cycle_start):
        spin = spin.spin_cycle()
    for _ in range((n_iterations - cycle_start) % cycle_length):
        spin = spin.spin_cycle()
    print(f"Part 2: {spin.load}")


if __name__ == "__main__":
    main()
