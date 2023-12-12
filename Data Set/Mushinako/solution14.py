# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from collections import Counter
from operator import itemgetter
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = tuple[str, dict[str, str]]


class Solution(SolutionAbstract):
    day = 14
    data: _Data

    def __init__(self) -> None:
        super().__init__()
        self.template, self.rules = self.data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 14 data.
        """
        template = raw_data[0]
        rules: dict[str, str] = {}
        for rule in raw_data[1:]:
            position, value = rule.split("->")
            rules[position.strip()] = value.strip()
        return template, rules

    def part_1(self) -> int:
        """
        Day 14 part 1 solution.
        """
        return self._solve(10)

    def part_2(self) -> int:
        """
        Day 14 part 2 solution.
        """
        return self._solve(40)

    def _solve(self, step_count: int) -> int:
        """
        General solution.
        """
        # Record initial condition. Map each rule to the number of occurrences in the
        #   template
        counts = {position: 0 for position in self.rules}
        for i in range(len(self.template) - 1):
            counts[self.template[i : i + 2]] += 1
        # Run required number of steps
        for _ in range(step_count):
            counts = self._run_step(counts)
        # Get count for each character
        char_counts = self._get_char_counts(counts)
        # Sort to get the largest and smallest. Reversed only to mimic the behavior of
        #   `collections.Counter.most_common`
        counts_list = sorted(char_counts.items(), key=itemgetter(1), reverse=True)
        return counts_list[0][1] - counts_list[-1][1]

    def _run_step(self, counts: dict[str, int]) -> dict[str, int]:
        """
        Run one step.
        """
        # `AB -> C` means `AB` becomes `AC` and `CB`. If we had *n* groups of `AB`
        #   before, we should expect *n* groups of `AC` and *n* groups of `CB`
        new_counts = {position: 0 for position in counts}
        for position, count in counts.items():
            value = self.rules.get(position)
            if not value:
                continue
            new_counts[position[0] + value] += count
            new_counts[value + position[1]] += count
        return new_counts

    def _get_char_counts(self, pair_counts: dict[str, int]) -> dict[str, int]:
        """
        Get character count from pair count.
        """
        char_counts = {
            char: 0 for char in (set(self.template) | set(self.rules.values()))
        }
        for position, count in pair_counts.items():
            char_counts[position[0]] += count
            char_counts[position[1]] += count
        # Add the first and last character because they're not double counted
        char_counts[self.template[0]] += 1
        char_counts[self.template[-1]] += 1
        # Sanity check
        for char, count in char_counts.items():
            if count % 2:
                raise ValueError(f"{char!r} does not have an even count: {count}.")
        char_counts = {char: count // 2 for char, count in char_counts.items()}
        return char_counts