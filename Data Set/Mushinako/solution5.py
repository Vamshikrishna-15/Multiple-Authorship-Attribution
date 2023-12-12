# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Coord = tuple[int, int]
    _CoordPair = tuple[_Coord, _Coord]
    _Data = list[_CoordPair]


class Solution(SolutionAbstract):
    day = 5
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 05 data.
        """
        data: _Data = []
        for line in raw_data:
            c1_str, c2_str = line.split("->")
            c1_nums = [int(n.strip()) for n in c1_str.strip().split(",")]
            c1: _Coord = c1_nums[0], c1_nums[1]
            c2_nums = [int(n.strip()) for n in c2_str.strip().split(",")]
            c2: _Coord = c2_nums[0], c2_nums[1]
            data.append((c1, c2))
        return data

    def part_1(self) -> int:
        """
        Day 05 part 1 solution.
        """
        coord_count: defaultdict[_Coord, int] = defaultdict(lambda: 0)
        for (x1, y1), (x2, y2) in self.data:
            # Vertical
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    coord_count[(x1, y)] += 1
                continue
            # Horizontal
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    coord_count[(x, y1)] += 1
                continue
        count_gt_1 = [n for n in coord_count.values() if n > 1]
        return len(count_gt_1)

    def part_2(self) -> int:
        """
        Day 05 part 2 solution.
        """
        coord_count: defaultdict[_Coord, int] = defaultdict(lambda: 0)
        for (x1, y1), (x2, y2) in self.data:
            # Vertical
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    coord_count[(x1, y)] += 1
                continue
            # Horizontal
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    coord_count[(x, y1)] += 1
                continue
            # Get coordinate's relative positions for diagonals
            if x1 < x2:
                big_x = x2
                small_x = x1
                start_y = y1
            else:
                big_x = x1
                small_x = x2
                start_y = y2
            # Bottom-left to top-right
            if x1 - y1 == x2 - y2:
                for s in range(big_x - small_x + 1):
                    coord_count[(small_x + s, start_y + s)] += 1
                continue
            # Top-left to bottom-right
            if x1 + y1 == x2 + y2:
                for s in range(big_x - small_x + 1):
                    coord_count[(small_x + s, start_y - s)] += 1
                continue
        count_gt_1 = [n for n in coord_count.values() if n > 1]
        return len(count_gt_1)