from __future__ import annotations
import sys
from typing import Iterable
import itertools
import bisect
import attrs


@attrs.frozen
class Range:
    start: int
    end: int


class RangeMap:
    def __init__(self, ranges: dict[Range, int]) -> None:
        self._dict = {0: 0}
        for r, dest in ranges.items():
            self._dict[r.start] = dest
            self._dict.setdefault(r.end, r.end)
        self._sorted_keys = sorted(self._dict.keys())

    def _query_point(self, key: int) -> int:
        nearest_key_idx = max(0, bisect.bisect(self._sorted_keys, key) - 1)
        nearest_key = self._sorted_keys[nearest_key_idx]
        return self._dict[nearest_key] + key - nearest_key

    def query(self, keys: list[int]) -> list[int]:
        return [self._query_point(key) for key in keys]


def main():
    seeds_line, *map_line_lists = [
        list(group)
        for key, group in itertools.groupby(sys.stdin, lambda x: bool(x.strip()))
        if key
    ]

    seeds = [int(x) for x in seeds_line[0].split()[1:]]
    maps = []
    for lines in map_line_lists:
        range_dict = {}
        for line in lines[1:]:
            dest_start, source_start, length = map(int, line.split())
            range_dict[Range(source_start, source_start + length)] = dest_start
        maps.append(RangeMap(range_dict))

    for m in maps:
        seeds = m.query(seeds)
    print(min(seeds))


if __name__ == "__main__":
    main()
