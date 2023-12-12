# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from itertools import count
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Coord = tuple[int, int]
    _Data = list[list[int]]


class Solution(SolutionAbstract):
    day = 11
    data: _Data

    def __init__(self) -> None:
        super().__init__()
        self.height = len(self.data)
        self.width = len(self.data[0])

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 11 data.
        """
        return [[int(n) for n in line] for line in raw_data]

    def part_1(self) -> int:
        """
        Day 11 part 1 solution.
        """
        return sum(self._run_step()[0] for _ in range(100))

    def part_2(self) -> int:
        """
        Day 11 part 2 solution.
        """
        size = self.width * self.height
        # Make linter happy
        n = 0
        for n in count(1):
            flashed = self._run_step()[1]
            if len(flashed) == size:
                break
        return n

    def _get_affected_cells(self, i: int, j: int) -> set[_Coord]:
        """"""
        affected_rows: set[int] = {i}
        if i > 0:
            affected_rows.add(i - 1)
        if i < self.height - 1:
            affected_rows.add(i + 1)
        affected_cols: set[int] = {j}
        if j > 0:
            affected_cols.add(j - 1)
        if j < self.width - 1:
            affected_cols.add(j + 1)
        affected_cells: set[_Coord] = {
            (ai, aj) for ai in affected_rows for aj in affected_cols
        }
        affected_cells.remove((i, j))
        return affected_cells

    def _initial_flash(self) -> tuple[int, set[_Coord], set[_Coord]]:
        """"""
        counter = 0
        flashed: set[_Coord] = set()
        all_affected_cells: set[_Coord] = set()
        for i in range(self.height):
            for j in range(self.width):
                if self.data[i][j] <= 9:
                    continue
                flashed.add((i, j))
                counter += 1
                affected_cells = self._get_affected_cells(i, j)
                for ai, aj in affected_cells:
                    self.data[ai][aj] += 1
                all_affected_cells |= affected_cells
        return counter, flashed, all_affected_cells

    def _chain_flash(
        self, flashed: set[_Coord], all_affected_cells: set[_Coord]
    ) -> tuple[int, set[_Coord]]:
        """"""
        counter = 0
        new_affected_cells: set[_Coord] = set()
        for i, j in all_affected_cells:
            if (i, j) in flashed:
                continue
            if self.data[i][j] <= 9:
                continue
            flashed.add((i, j))
            counter += 1
            affected_cells = self._get_affected_cells(i, j)
            for ai, aj in affected_cells:
                self.data[ai][aj] += 1
            new_affected_cells |= affected_cells
        return counter, new_affected_cells

    def _run_step(self) -> tuple[int, set[_Coord]]:
        """"""
        for i in range(self.height):
            for j in range(self.width):
                self.data[i][j] += 1
        counter, flashed, affected_cells = self._initial_flash()
        while affected_cells:
            event_counter, affected_cells = self._chain_flash(flashed, affected_cells)
            counter += event_counter
        for i, j in flashed:
            self.data[i][j] = 0
        return counter, flashed