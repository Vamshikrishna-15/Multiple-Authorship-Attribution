# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _DigitSegments = frozenset[str]
    _TestSet = tuple[list[_DigitSegments], list[_DigitSegments]]
    _Data = list[_TestSet]


class Solution(SolutionAbstract):
    day = 8
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 08 data.
        """
        data: _Data = []
        for line in raw_data:
            digits, value = line.split("|")
            data.append(
                (
                    [frozenset(d) for d in digits.strip().split()],
                    [frozenset(v) for v in value.strip().split()],
                )
            )
        return data

    def part_1(self) -> int:
        """
        Day 08 part 1 solution.
        """
        return sum(len(v) in {2, 3, 4, 7} for _, values in self.data for v in values)

    def part_2(self) -> int:
        """
        Day 08 part 2 solution.
        """
        sum_ = 0
        for digits, values in self.data:
            digit_list: list[_DigitSegments] = [frozenset() for _ in range(10)]
            digit_map: dict[_DigitSegments, int] = {}
            seg_length_map: dict[int, set[_DigitSegments]] = {
                5: set(),  # 2, 3, 5
                6: set(),  # 0, 6, 9
            }
            # Identify the easy digits
            for d in digits:
                len_ = len(d)
                if len_ == 2:
                    digit_list[1] = d
                    digit_map[d] = 1
                elif len_ == 3:
                    digit_list[7] = d
                    digit_map[d] = 7
                elif len_ == 4:
                    digit_list[4] = d
                    digit_map[d] = 4
                elif len_ == 7:
                    digit_list[8] = d
                    digit_map[d] = 8
                else:
                    seg_length_map[len_].add(d)
            # Identify 0, 6, and 9
            for s6 in seg_length_map[6]:
                if len(s6 & digit_list[1]) == 1:
                    digit_list[6] = s6
                    digit_map[s6] = 6
                elif len(s6 & digit_list[4]) == 4:
                    digit_list[9] = s6
                    digit_map[s6] = 9
                else:
                    digit_list[0] = s6
                    digit_map[s6] = 0
            # Identify 2, 3, and 5
            for s5 in seg_length_map[5]:
                if len(s5 & digit_list[6]) == 5:
                    digit_list[5] = s5
                    digit_map[s5] = 5
                elif len(s5 & digit_list[1]) == 2:
                    digit_list[3] = s5
                    digit_map[s5] = 3
                else:
                    digit_list[2] = s5
                    digit_map[s5] = 2
            sub_sum = 0
            # Calculate sum
            for v in values:
                sub_sum *= 10
                sub_sum += digit_map[v]
            sum_ += sub_sum
        return sum_