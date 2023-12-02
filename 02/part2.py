import attrs
import sys


@attrs.frozen
class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0


@attrs.frozen
class Game:
    game_id: int
    cube_sets: list[CubeSet]

    def min_power(self) -> int:
        red_required = max(s.red for s in self.cube_sets)
        blue_required = max(s.blue for s in self.cube_sets)
        green_required = max(s.green for s in self.cube_sets)
        return red_required * blue_required * green_required


def parse_cube_set(cube_set_str: str) -> CubeSet:
    res = CubeSet()
    for cube_str in cube_set_str.strip().split(", "):
        num, color = cube_str.split(" ")
        res = attrs.evolve(res, **{color: int(num)})
    return res


def parse(game_str: str) -> Game:
    game_id_str, cube_set_str = game_str.strip().split(": ")
    game_id = int(game_id_str.split(" ")[-1])
    cube_sets = [parse_cube_set(s) for s in cube_set_str.split("; ")]
    return Game(game_id, cube_sets)


def main():
    ans = 0
    for line in sys.stdin:
        game = parse(line)
        ans += game.min_power()
    print(ans)


if __name__ == "__main__":
    main()
