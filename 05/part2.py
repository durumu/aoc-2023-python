from __future__ import annotations
import sys
import itertools
import bisect
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

    def _query_range(self, range_: Range) -> tuple[list[Range], list[Range]]:
        ranges = []

        for r, diff in self.ranges.items():
            if not (intersection := range_.intersect(r)).empty:
                ranges.append(Range(intersection.start + diff, intersection.end + diff))

        return ranges

    def query(self, ranges: list[Range]) -> list[Range]:
        return [res for r in ranges for res in self._query_range(r)]


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
            diff = dest_start - src_start
            range_dict[Range(src_start, src_start + length)] = diff

        # Fill gaps
        sorted_ranges = sorted(range_dict.keys(), key=lambda x: x.start)
        for r1, r2 in itertools.pairwise(sorted_ranges):
            range_dict[Range(r1.end, r2.start)] = r1.end
        range_dict[Range(0, sorted_ranges[0].start)] = 0
        range_dict[Range(sorted_ranges[-1].end, 10**12)] = 0

        maps.append(RangeMap(range_dict))

    for m in maps:
        seeds = m.query(seeds)
    print(min(seed.start for seed in seeds))


if __name__ == "__main__":
    main()
