# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[int]


class Solution(SolutionAbstract):
    day = 6
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 06 data.
        """
        return [int(x) for x in raw_data[0].split(",")]

    def part_1(self) -> int:
        """
        Day 06 part 1 solution.
        """
        return self._solution(80)

    def part_2(self) -> int:
        """
        Day 06 part 2 solution.
        """
        return self._solution(256)

    def _solution(self, round_count: int) -> int:
        """
        General solution for day 06.
        """
        counts = [0] * 9
        for d in self.data:
            counts[d] += 1
        for _ in range(round_count):
            mature_count = counts.pop(0)
            counts.append(mature_count)
            counts[6] += mature_count
        return sum(counts)