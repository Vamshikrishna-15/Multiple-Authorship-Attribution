# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from collections import defaultdict
from itertools import count
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Range = tuple[int, int]
    _Data = tuple[_Range, _Range]


class Solution(SolutionAbstract):
    day = 17
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 17 data.
        """
        (raw_str,) = raw_data
        data = raw_str.removeprefix("target area:").strip()
        x_str, y_str = data.split(",")
        x_coords = x_str.strip().removeprefix("x=").strip().split(".")
        y_coords = y_str.strip().removeprefix("y=").strip().split(".")
        return (
            (int(x_coords[0]), int(x_coords[-1])),
            # Absolute values are taken here to make it easier to calculate
            (abs(int(y_coords[-1])), abs(int(y_coords[0]))),
        )

    def part_1(self) -> int:
        """
        Day 17 part 1 solution.
        """
        y_depth = self.data[1][1]
        return y_depth * (y_depth - 1) // 2

    def part_2(self) -> int:
        """
        Day 17 part 2 solution.
        """
        (x_min, x_max), (y_min, y_max) = self.data

        # [Will overshoot?][Min step count]
        x_counts: dict[bool, defaultdict[int, set[int]]] = {
            True: defaultdict(set),
            False: defaultdict(set),
        }
        for x_end in count(1):
            if x_end > x_max:
                break
            x_acc = 0
            for x in count(x_end):
                x_acc += x
                if x_acc > x_max:
                    break
                if x_acc >= x_min:
                    x_counts[x_end > 1][x - x_end + 1].add(x)

        # [Min step count]
        y_counts: defaultdict[int, set[int]] = defaultdict(set)
        for y_start in count(1):
            if y_start > y_max:
                break
            y_acc = 0
            for y in count(y_start):
                y_acc += y
                if y_acc > y_max:
                    break
                if y_acc >= y_min:
                    base_y_step = y - y_start + 1
                    y_counts[base_y_step].add(-y_start)
                    y_counts[base_y_step + y_start * 2 - 1].add(y_start)

        all_starts: set[tuple[int, int]] = set()
        # For ones that won't overshoot, as long as the y step count is no smaller than
        #   x step count then it's OK
        for x_min_step, x_vecs in x_counts[False].items():
            for y_min_step, y_vecs in y_counts.items():
                if y_min_step < x_min_step:
                    continue
                all_starts |= {(x, y) for x in x_vecs for y in y_vecs}
        # For ones that will overshoot, we need to get exact step count
        for x_min_step, x_vecs in x_counts[True].items():
            y_vecs = y_counts.get(x_min_step)
            if not y_vecs:
                continue
            all_starts |= {(x, y) for x in x_vecs for y in y_vecs}

        return len(all_starts)