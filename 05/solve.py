from __future__ import annotations

import itertools
import sys

import attrs


@attrs.frozen
class Range:
    start: int
    end: int

    def intersect(self, other: Range) -> Range:
        return Range(max(self.start, other.start), min(self.end, other.end))

    @property
    def empty(self):
        return self.start >= self.end


@attrs.define
class RangeMap:
    ranges: dict[Range, int]

    def query_ranges(self, ranges: list[Range]) -> list[Range]:
        ret = []

        for range_ in ranges:
            for r, diff in self.ranges.items():
                intersection = range_.intersect(r)
                if not intersection.empty:
                    ret.append(
                        Range(intersection.start + diff, intersection.end + diff)
                    )

        return ret

    def query_points(self, points: list[int]) -> list[int]:
        return [r.start for r in self.query_ranges([Range(p, p + 1) for p in points])]


def main():
    seeds_line, *map_line_lists = (
        list(group)
        for key, group in itertools.groupby(sys.stdin, lambda x: bool(x.strip()))
        if key
    )

    maps = []
    for lines in map_line_lists:
        range_dict = {}
        for line in lines[1:]:
            dest_start, src_start, length = map(int, line.split())
            diff = dest_start - src_start
            range_dict[Range(src_start, src_start + length)] = diff

        # Fill gaps
        sorted_ranges = sorted(range_dict.keys(), key=lambda x: x.start)
        for r1, r2 in itertools.pairwise(sorted_ranges):
            range_dict[Range(r1.end, r2.start)] = r1.end
        range_dict[Range(0, sorted_ranges[0].start)] = 0
        range_dict[Range(sorted_ranges[-1].end, 10**12)] = 0

        maps.append(RangeMap(range_dict))

    seeds = [int(x) for x in seeds_line[0].split()[1:]]
    seed_ranges = [
        Range(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])
    ]

    for m in maps:
        seeds = m.query_points(seeds)
    print(f"Part 1: {min(seeds)}")

    for m in maps:
        seed_ranges = m.query_ranges(seed_ranges)
    print(f"Part 2: {min(r.start for r in seed_ranges)}")


if __name__ == "__main__":
    main()
