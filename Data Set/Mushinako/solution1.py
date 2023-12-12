# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[int]


class Solution(SolutionAbstract):
    day = 1
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 01 data.
        """
        return [int(line) for line in raw_data]

    def part_1(self) -> int:
        """
        Day 01 part 1 solution.
        """
        return sum(self.data[i + 1] > self.data[i] for i in range(len(self.data) - 1))

    def part_2(self) -> int:
        """
        Day 01 part 2 solution.
        """
        return sum(self.data[i + 3] > self.data[i] for i in range(len(self.data) - 3))