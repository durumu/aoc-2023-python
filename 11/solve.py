import attrs
import sys
from itertools import combinations
from functools import cached_property
from bisect import bisect


@attrs.define(slots=False)
class Grid:
    grid: list[str]

    @cached_property
    def galaxies(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(len(self.grid))
            for c in range(len(self.grid[r]))
            if self.grid[r][c] == "#"
        ]

    @cached_property
    def expanded_rows(self) -> list[int]:
        galaxy_rows = {r for r, _ in self.galaxies}
        all_rows = set(range(len(self.grid)))
        return sorted(all_rows - galaxy_rows)

    @cached_property
    def expanded_cols(self) -> list[int]:
        galaxy_cols = {c for _, c in self.galaxies}
        all_cols = set(range(len(self.grid[0])))
        return sorted(all_cols - galaxy_cols)

    def distances(self, expansion_mult: int = 1) -> list[int]:
        def _distance_along_dim(x1: int, x2: int, xs: list[int]):
            if x1 > x2:
                x1, x2 = x2, x1
            n_expanded = len([x for x in xs if x1 < x < x2])
            return x2 - x1 + n_expanded * (expansion_mult - 1)

        dists = []
        for (r1, c1), (r2, c2) in combinations(self.galaxies, 2):
            row_dist = _distance_along_dim(r1, r2, self.expanded_rows)
            col_dist = _distance_along_dim(c1, c2, self.expanded_cols)
            dists.append(row_dist + col_dist)

        return dists


def main():
    grid = Grid([line.strip() for line in sys.stdin])
    print(f"Part 1: {sum(grid.distances(2))}")
    print(f"Part 2: {sum(grid.distances(1000000))}")


if __name__ == "__main__":
    main()
