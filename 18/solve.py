from __future__ import annotations

import itertools
import sys

import attrs


@attrs.define
class Vector2:
    x: int
    y: int

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: int) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def cross(self, other: Vector2) -> int:
        return self.x * other.y - other.x * self.y


def num_contained_points(side_vectors: list[Vector2]) -> int:
    points = [Vector2(0, 0)]
    for vector in side_vectors:
        points.append(points[-1] + vector)

    area = abs(sum(u.cross(v) for u, v in itertools.pairwise(points))) / 2
    boundary_points = sum(abs(vector) for vector in side_vectors)
    interior_points = area - boundary_points / 2 + 1  # by Pick's theorem
    return int(interior_points + boundary_points)


def main():
    vectors_p1 = []
    vectors_p2 = []

    units = [Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1)]
    direction_to_unit = dict(zip("RDLU", units))

    for line in sys.stdin:
        direction, length, color = line.strip().split()
        vectors_p1.append(direction_to_unit[direction] * int(length))

        length_p2 = int(color[2:7], 16)
        unit_p2 = units[int(color[7])]
        vectors_p2.append(unit_p2 * length_p2)

    print(f"Part 1: {num_contained_points(vectors_p1)}")
    print(f"Part 2: {num_contained_points(vectors_p2)}")


if __name__ == "__main__":
    main()
