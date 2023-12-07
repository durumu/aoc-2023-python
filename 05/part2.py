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

    @property
    def length(self) -> int:
        return self.end - self.start


def compress(add_ranges: list[Range], remove_ranges: list[Range]) -> list[Range]:
    """
    Takes a list of possibly-overlapping ranges to add and remove,
    and returns a list of non-overlapping ranges that cover these points.
    """
    # Adds should come before removals, so that two ranges that touch at one point
    # are condensed into one range.
    ADD, REMOVE = 0, 1
    events: list[tuple[int, int]] = []
    events.extend(e for r in add_ranges for e in [(r.start, ADD), (r.end, REMOVE)])
    events.extend(e for r in remove_ranges for e in [(r.start, REMOVE), (r.end, ADD)])
    events.sort()
    out = []
    left = 0
    n = 0
    for pos, what in events:
        if what == ADD:
            if n == 0:
                left = pos
            n += 1
        elif what == REMOVE:
            n -= 1
            assert n >= 0
            if n == 0:
                out.append(Range(left, pos))
    return out


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

    def _query_range(self, range_: Range) -> tuple[list[Range], list[Range]]:
        add_list = [range_]
        remove_list = []

        start_idx = max(0, bisect.bisect(self._sorted_keys, range_.start) - 1)
        end_idx = max(0, bisect.bisect(self._sorted_keys, range_.end) - 1)

        ...

        return add_list, remove_list

    def query(self, ranges: list[Range]) -> list[Range]:
        results = [self._query_range(r) for r in ranges]
        return compress(
            [r for add_list, _ in results for r in add_list],
            [r for _, remove_list in results for r in remove_list],
        )


def main():
    seeds_line, *map_line_lists = [
        list(group)
        for key, group in itertools.groupby(sys.stdin, lambda x: bool(x.strip()))
        if key
    ]

    seed_nums = [int(x) for x in seeds_line[0].split()[1:]]
    seeds = [
        Range(start, start + length)
        for start, length in zip(seed_nums[::2], seed_nums[1::2])
    ]

    maps = []
    for lines in map_line_lists:
        range_dict = {}
        for line in lines[1:]:
            dest_start, src_start, length = map(int, line.split())
            range_dict[Range(src_start, src_start + length)] = dest_start
        maps.append(RangeMap(range_dict))

    for m in maps:
        seeds = m.query(seeds)
    print(min(seed.start for seed in seeds))


if __name__ == "__main__":
    main()
