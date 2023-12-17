from __future__ import annotations
from enum import IntEnum
from functools import partial
import sys
from typing import TypeVar, Callable
import attrs
import heapq

T = TypeVar("T")


def dijkstra(
    start: T,
    neighbor_fn: Callable[[T], list[tuple[float, T]]],
    is_end_fn: Callable[[T], bool],
) -> float | None:
    dists = {}
    heap: list[tuple[float, T]] = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if is_end_fn(u):
            return d
        if u in dists:
            continue
        dists[u] = d
        for w, v in neighbor_fn(u):
            if v not in dists:
                heapq.heappush(heap, (d + w, v))
    return None


class Direction(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

    def apply(self, pos: tuple[int, int]) -> tuple[int, int]:
        r, c = pos
        dr = 1 if self is self.Down else -1 if self is self.Up else 0
        dc = 1 if self is self.Right else -1 if self is self.Left else 0
        return (r + dr, c + dc)

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


def get_neighbors(blocks: list[list[int]], node: Node) -> list[tuple[float, Node]]:
    directions = [d for d in Direction if d != node.direction.opposite]
    if node.consecutive == 3:
        directions.remove(node.direction)

    nodes = []
    for direction in directions:
        r, c = direction.apply((node.r, node.c))
        consecutive = 1 if direction != node.direction else (node.consecutive + 1)
        if 0 <= r < len(blocks) and 0 <= c < len(blocks[r]):
            nodes.append((blocks[r][c], Node(r, c, direction, consecutive)))
    return nodes


def get_neighbors_ultra(
    blocks: list[list[int]], node: Node
) -> list[tuple[float, Node]]:
    if node.consecutive == 0:
        directions = list(Direction)
    elif node.consecutive < 4:
        directions = [node.direction]
    else:
        directions = [d for d in Direction if d != node.direction.opposite]

    if node.consecutive == 10:
        directions.remove(node.direction)

    nodes = []
    for direction in directions:
        r, c = direction.apply((node.r, node.c))
        consecutive = 1 if direction != node.direction else (node.consecutive + 1)
        if 0 <= r < len(blocks) and 0 <= c < len(blocks[r]):
            nodes.append((blocks[r][c], Node(r, c, direction, consecutive)))
    return nodes


def main():
    blocks = [[int(c) for c in line.strip()] for line in sys.stdin]
    start = Node(0, 0, Direction.Right, 0)

    def is_end(node: Node) -> bool:
        return node.r == len(blocks) - 1 and node.c == len(blocks[0]) - 1

    least_heat = dijkstra(start, partial(get_neighbors, blocks), is_end)
    print(f"Part 1: {least_heat}")

    least_heat_ultra = dijkstra(start, partial(get_neighbors_ultra, blocks), is_end)
    print(f"Part 2: {least_heat_ultra}")


if __name__ == "__main__":
    main()
