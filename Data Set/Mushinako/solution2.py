# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Instruction = tuple[str, int]
    _Data = list[_Instruction]


class Solution(SolutionAbstract):
    day = 2
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 02 data.
        """
        data: _Data = []
        for line in raw_data:
            a, b = line.split()
            data.append((a.lower(), int(b)))
        return data

    def part_1(self) -> int:
        """
        Day 02 part 1 solution.
        """
        hori = depth = 0
        for direction, distance in self.data:
            if direction == "forward":
                hori += distance
                continue
            if direction == "down":
                depth += distance
                continue
            if direction == "up":
                depth -= distance
                continue
        return hori * depth

    def part_2(self) -> int:
        """
        Day 02 part 2 solution.
        """
        hori = depth = aim = 0
        for direction, distance in self.data:
            if direction == "forward":
                hori += distance
                depth += aim * distance
                continue
            if direction == "down":
                aim += distance
                continue
            if direction == "up":
                aim -= distance
                continue
        return hori * depth