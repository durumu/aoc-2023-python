from __future__ import annotations
import sys
from multiprocessing import Pool
from attr import evolve, field
import attrs
import enum
import os


class Direction(enum.IntEnum):
    Right = 0
    Up = 1
    Left = 2
    Down = 3


@attrs.frozen
class Beam:
    row: int
    col: int
    direction: Direction

    def advance(self) -> Beam:
        dr = {Direction.Up: -1, Direction.Down: 1}.get(self.direction, 0)
        dc = {Direction.Left: -1, Direction.Right: 1}.get(self.direction, 0)
        return Beam(self.row + dr, self.col + dc, self.direction)

    def process(self, tile: str) -> list[Beam]:
        if tile == "/":
            return [
                attrs.evolve(
                    self,
                    direction={
                        Direction.Left: Direction.Down,
                        Direction.Right: Direction.Up,
                        Direction.Down: Direction.Left,
                        Direction.Up: Direction.Right,
                    }[self.direction],
                )
            ]
        elif tile == "\\":
            return [
                attrs.evolve(
                    self,
                    direction={
                        Direction.Left: Direction.Up,
                        Direction.Right: Direction.Down,
                        Direction.Up: Direction.Left,
                        Direction.Down: Direction.Right,
                    }[self.direction],
                )
            ]
        elif tile == "|" and self.direction in {Direction.Left, Direction.Right}:
            return [
                attrs.evolve(self, direction=Direction.Up),
                attrs.evolve(self, direction=Direction.Down),
            ]
        elif tile == "-" and self.direction in {Direction.Up, Direction.Down}:
            return [
                attrs.evolve(self, direction=Direction.Left),
                attrs.evolve(self, direction=Direction.Right),
            ]
        return [self]


@attrs.frozen
class BeamGrid:
    layout: list[str]
    active_beams: set[Beam]
    processed_beams: set[Beam] = field(factory=set)

    def is_in_bounds(self, beam: Beam) -> bool:
        return 0 <= beam.row < len(self.layout) and 0 <= beam.col < len(
            self.layout[beam.row]
        )

    def step(self) -> BeamGrid:
        new_beams = set()
        processed_beams = self.active_beams | self.processed_beams
        for beam in self.active_beams:
            tile = self.layout[beam.row][beam.col]
            for rotated in beam.process(tile):
                new_beam = rotated.advance()
                if self.is_in_bounds(new_beam):
                    new_beams.add(new_beam)
        new_beams -= processed_beams
        return evolve(self, active_beams=new_beams, processed_beams=processed_beams)

    def num_energized(self) -> int:
        grid = self
        while grid.active_beams:
            grid = grid.step()
        return len({(beam.row, beam.col) for beam in grid.processed_beams})


def main():
    layout = [line.strip() for line in sys.stdin]
    grids = []
    grids.extend(
        BeamGrid(layout=layout, active_beams={Beam(r, 0, Direction.Right)})
        for r in range(len(layout))
    )
    grids.extend(
        BeamGrid(
            layout=layout, active_beams={Beam(r, len(layout[0]) - 1, Direction.Left)}
        )
        for r in range(len(layout))
    )
    grids.extend(
        BeamGrid(layout=layout, active_beams={Beam(0, c, Direction.Down)})
        for c in range(len(layout[0]))
    )
    grids.extend(
        BeamGrid(layout=layout, active_beams={Beam(len(layout) - 1, c, Direction.Up)})
        for c in range(len(layout[0]))
    )

    print(f"Part 1: {grids[0].num_energized()}")

    with Pool((os.cpu_count() or 2) - 1) as p:
        energized_nums = p.map(BeamGrid.num_energized, grids)
    print(f"Part 2: {max(energized_nums)}")


if __name__ == "__main__":
    main()
