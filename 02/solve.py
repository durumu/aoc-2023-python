from __future__ import annotations
import attrs
import sys


@attrs.frozen
class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0

    @classmethod
    def parse(cls, cube_set_str: str) -> CubeSet:
        res = cls()
        for cube_str in cube_set_str.strip().split(", "):
            num, color = cube_str.split(" ")
            res = attrs.evolve(res, **{color: int(num)})
        return res


@attrs.frozen
class Game:
    game_id: int
    cube_sets: list[CubeSet]

    def is_possible(self) -> bool:
        red_required = max(s.red for s in self.cube_sets)
        green_required = max(s.green for s in self.cube_sets)
        blue_required = max(s.blue for s in self.cube_sets)
        return red_required <= 12 and green_required <= 13 and blue_required <= 14

    def min_power(self) -> int:
        red_required = max(s.red for s in self.cube_sets)
        blue_required = max(s.blue for s in self.cube_sets)
        green_required = max(s.green for s in self.cube_sets)
        return red_required * blue_required * green_required

    @classmethod
    def parse(cls, game_str: str) -> Game:
        game_id_str, cube_set_str = game_str.strip().split(": ")
        game_id = int(game_id_str.split(" ")[-1])
        cube_sets = [CubeSet.parse(s) for s in cube_set_str.split("; ")]
        return cls(game_id, cube_sets)


def main():
    games = [Game.parse(line) for line in sys.stdin]

    print(f"Part 1: {sum(game.game_id for game in games if game.is_possible())}")
    print(f"Part 2: {sum(game.min_power() for game in games)}")


if __name__ == "__main__":
    main()
