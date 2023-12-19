from __future__ import annotations

import heapq
import sys
from collections.abc import Callable
from enum import Enum
from typing import TypeVar

import attrs

T = TypeVar("T")


def dijkstra(
    start: T,
    neighbor_fn: Callable[[T], list[tuple[float, T]]],
    is_end_fn: Callable[[T], bool],
) -> float | None:
    dists: dict[T, float] = {}
    heap: list[tuple[float, T]] = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dists:
            continue
        if is_end_fn(u):
            return d
        dists[u] = d
        for cost, v in neighbor_fn(u):
            if v not in dists:
                heapq.heappush(heap, (d + cost, v))
    return None


class Direction(Enum):
    Left = (0, -1)
    Right = (0, 1)
    Up = (-1, 0)
    Down = (1, 0)

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    @property
    def opposite(self) -> Direction:
        return {
            self.Left: self.Right,
            self.Right: self.Left,
            self.Up: self.Down,
            self.Down: self.Up,
        }[self]


@attrs.frozen(order=True)
class Node:
    r: int
    c: int
    direction: Direction
    consecutive: int

    def get_directions(self) -> list[Direction]:
        directions = [d for d in Direction if d != self.direction.opposite]
        if self.consecutive == 3:
            directions.remove(self.direction)
        return directions

    def get_directions_ultra(self) -> list[Direction]:
        if 0 < self.consecutive < 4:
            return [self.direction]

        directions = [d for d in Direction if d != self.direction.opposite]
        if self.consecutive == 10:
            directions.remove(self.direction)
        return directions


def get_neighbors(
    node: Node, blocks: list[list[int]], directions: list[Direction]
) -> list[tuple[float, Node]]:
    nodes = []
    for direction in directions:
        dr, dc = direction.value
        r, c = node.r + dr, node.c + dc
        consecutive = 1 if direction != node.direction else (node.consecutive + 1)
        if 0 <= r < len(blocks) and 0 <= c < len(blocks[r]):
            nodes.append((blocks[r][c], Node(r, c, direction, consecutive)))
    return nodes


def main():
    blocks = [[int(c) for c in line.strip()] for line in sys.stdin]
    start = Node(0, 0, Direction.Right, 0)

    def is_end(node: Node) -> bool:
        return node.r == len(blocks) - 1 and node.c == len(blocks[0]) - 1

    def neighbor_fn(node: Node) -> list[tuple[float, Node]]:
        return get_neighbors(node, blocks, node.get_directions())

    def neighbor_fn_ultra(node: Node) -> list[tuple[float, Node]]:
        return get_neighbors(node, blocks, node.get_directions_ultra())

    print(f"Part 1: {dijkstra(start, neighbor_fn, is_end)}")
    print(f"Part 2: {dijkstra(start, neighbor_fn_ultra, is_end)}")


if __name__ == "__main__":
    main()
