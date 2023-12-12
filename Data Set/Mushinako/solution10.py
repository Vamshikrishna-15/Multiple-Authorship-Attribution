# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from statistics import median
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[str]


class Solution(SolutionAbstract):
    day = 10
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 10 data.
        """
        return raw_data

    def part_1(self) -> int:
        """
        Day 10 part 1 solution.
        """
        pair_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
        score_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
        sum_ = 0
        for line in self.data:
            stack: list[str] = []
            for char in line:
                if char in pair_map:
                    stack.append(char)
                else:
                    last_open = stack.pop()
                    correct_char = pair_map[last_open]
                    if char != correct_char:
                        sum_ += score_map[char]
                        break
        return sum_

    def part_2(self) -> int:
        """
        Day 10 part 2 solution.
        """
        pair_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
        score_map = {"(": 1, "[": 2, "{": 3, "<": 4}
        scores: list[int] = []
        for line in self.data:
            stack: list[str] = []
            for char in line:
                if char in pair_map:
                    stack.append(char)
                else:
                    last_open = stack.pop()
                    correct_char = pair_map[last_open]
                    # Broken line
                    if char != correct_char:
                        break
            else:
                # All checked, no broken
                sub_total = 0
                for char in reversed(stack):
                    sub_total *= 5
                    sub_total += score_map[char]
                scores.append(sub_total)
        return int(median(scores))