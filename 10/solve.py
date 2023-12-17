from __future__ import annotations
from collections import deque
import sys
from typing import Iterable
import attrs
from enum import Enum


class Direction(Enum):
    North = "North"
    South = "South"
    East = "East"
    West = "West"

    def apply(self, pos: tuple[int, int]) -> tuple[int, int]:
        r, c = pos
        dr = 1 if self is self.South else -1 if self is self.North else 0
        dc = 1 if self is self.East else -1 if self is self.West else 0
        return (r + dr, c + dc)

    def connects(self, elem: str) -> bool:
        mapping = {
            self.North: "LJ|",
            self.South: "7F|",
            self.West: "J7-",
            self.East: "LF-",
        }
        return elem == "S" or elem in mapping[self]

    @property
    def opposite(self) -> Direction:
        return {
            self.South: self.North,
            self.North: self.South,
            self.West: self.East,
            self.East: self.West,
        }[self]


@attrs.frozen
class Grid:
    grid: list[str]

    @property
    def start_location(self) -> tuple[int, int]:
        for r, row in enumerate(self.grid):
            for c, elem in enumerate(row):
                if elem == "S":
                    return (r, c)
        raise AssertionError

    def neighbors(self, pos: tuple[int, int]) -> Iterable[tuple[int, int]]:
        r, c = pos
        for direction in Direction:
            if not direction.connects(self.grid[r][c]):
                continue
            r2, c2 = direction.apply(pos)
            if not (0 <= r2 < len(self.grid) and 0 <= c2 < len(self.grid[r])):
                continue
            if direction.opposite.connects(self.grid[r2][c2]):
                yield (r2, c2)

    def get_distances(self) -> list[list[int]]:
        dist = [[-1] * len(row) for row in self.grid]
        start = self.start_location
        start_r, start_c = start
        dist[start_r][start_c] = 0

        queue = deque([start])
        while queue:
            r, c = queue.popleft()
            for nr, nc in self.neighbors((r, c)):
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

        return dist


def main():
    grid = Grid([line.strip() for line in sys.stdin])
    distances = grid.get_distances()
    print(f"Part 1: {max(max(row) for row in distances)}")

    just_loop = []
    for i, dists in enumerate(distances):
        just_loop.append(["." if d == -1 else c for c, d in zip(grid.grid[i], dists)])

    for row in just_loop:
        intersections = 0
        for i, c in enumerate(row):
            if c == "." and intersections % 2 == 1:
                row[i] = "I"
            elif c in "J|L":
                intersections += 1

    print(f"Part 2: {sum(row.count('I') for row in just_loop)}")


if __name__ == "__main__":
    main()
