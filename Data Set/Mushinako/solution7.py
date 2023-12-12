# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from math import inf
from statistics import median
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[int]


class Solution(SolutionAbstract):
    day = 7
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 07 data.
        """
        return [int(x) for x in raw_data[0].split(",")]

    def part_1(self) -> int:
        """
        Day 07 part 1 solution.
        """
        median_ = round(median(self.data))
        return sum(abs(n - median_) for n in self.data)

    def part_2(self) -> int:
        """
        Day 07 part 2 solution.
        """
        min_ = min(self.data)
        max_ = max(self.data)
        min_fuel = inf
        for t in range(min_, max_):
            fuel = sum(abs(n - t) * (abs(n - t) + 1) // 2 for n in self.data)
            if fuel < min_fuel:
                min_fuel = fuel
        return int(min_fuel)