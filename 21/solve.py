from __future__ import annotations

import itertools
import math
import numpy as np
import sys

import attrs
from scipy.sparse import csr_matrix


@attrs.frozen
class Grid:
    grid: list[str]

    @property
    def n_rows(self) -> int:
        return len(self.grid)

    @property
    def n_cols(self) -> int:
        return len(self.grid[0])

    def flatten(self, r: int, c: int) -> int:
        return r * self.n_cols + c

    def unflatten(self, idx: int) -> tuple[int, int]:
        return divmod(idx, self.n_cols)

    def matrix(self, *, wrap_around: bool) -> csr_matrix:
        i_arr = []
        j_arr = []

        for r, c in itertools.product(range(self.n_rows), range(self.n_cols)):
            if self.grid[r][c] == "#":
                continue
            if (r >= 1 or wrap_around) and self.grid[(r + 1) % self.n_rows][c] != "#":
                u, v = self.flatten(r, c), self.flatten((r + 1) % self.n_rows, c)
                i_arr.extend([u, v])
                j_arr.extend([v, u])
            if (c >= 1 or wrap_around) and self.grid[r][(c + 1) % self.n_cols] != "#":
                u, v = self.flatten(r, c), self.flatten(r, (c + 1) % self.n_cols)
                i_arr.extend([u, v])
                j_arr.extend([v, u])

        n = len(self.grid) * len(self.grid[0])
        return csr_matrix(([1] * len(i_arr), (i_arr, j_arr)), shape=(n, n))

    @property
    def start(self) -> int:
        for r, row in enumerate(self.grid):
            for c in range(len(row)):
                if self.grid[r][c] == "S":
                    return self.flatten(r, c)
        return -1

    def count(self, steps: int, *, wrap_around: bool) -> int:
        matrix = self.matrix(wrap_around=wrap_around) ** steps
        return matrix[:, [self.start]].count_nonzero()


def main():
    grid = Grid([line.strip() for line in sys.stdin])
    print(f"Part 1: {grid.count(64, wrap_around=False)}")
    print(f"Part 2: {grid.count(26501365, wrap_around=False)}")


if __name__ == "__main__":
    main()
