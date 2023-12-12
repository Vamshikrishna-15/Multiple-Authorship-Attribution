# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[str]


class Solution(SolutionAbstract):
    day = 3
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 03 data.
        """
        return raw_data

    def part_1(self) -> int:
        """
        Day 03 part 1 solution.
        """
        gamma_str = ""
        epsilon_str = ""
        for digits in zip(*self.data):
            counter = Counter(digits)
            common_order = counter.most_common()
            gamma_str += common_order[0][0]
            epsilon_str += common_order[-1][0]
        return int(gamma_str, 2) * int(epsilon_str, 2)

    def part_2(self) -> int:
        """
        Day 03 part 2 solution.
        """
        # Data is sorted in decending order to make sure that 1's are always at the
        #   front and therefore will always be returned as the most common one in the
        #   case of a tie
        self.data.sort(reverse=True)
        length = len(self.data[0])
        # Careful not to modify the original data
        o2_values = self.data
        for i in range(length):
            if len(o2_values) == 1:
                break
            o2_counter = Counter(d[i] for d in o2_values)
            most_common = o2_counter.most_common(1)[0][0]
            o2_values = [d for d in o2_values if d[i] == most_common]
        # Careful not to modify the original data
        co2_values = self.data
        for i in range(length):
            if len(co2_values) == 1:
                break
            co2_counter = Counter(d[i] for d in co2_values)
            least_common = co2_counter.most_common()[-1][0]
            co2_values = [d for d in co2_values if d[i] == least_common]
        return int(o2_values[0], 2) * int(co2_values[0], 2)