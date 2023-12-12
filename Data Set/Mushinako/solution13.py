# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Coord = tuple[int, int]
    _Fold = tuple[str, int]
    _Data = tuple[set[_Coord], list[_Fold]]


class Solution(SolutionAbstract):
    day = 13
    data: _Data

    def __init__(self) -> None:
        super().__init__()
        self.dots, self.folds = self.data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 13 data.
        """
        dots: set[_Coord] = set()
        # Make linter happy
        i = 0
        for i, line in enumerate(raw_data):
            if not line:
                break
            try:
                x_str, y_str = line.split(",")
            except ValueError:
                break
            dots.add((int(x_str), int(y_str)))
        folds: list[_Fold] = []
        for line in raw_data[i:]:
            axis_str, index_str = line.split("=")
            folds.append((axis_str[-1], int(index_str)))
        return dots, folds

    def part_1(self) -> int:
        """
        Day 13 part 1 solution.
        """
        axis, index = self.folds[0]
        dots = self._fold_paper(self.dots, axis, index)
        return len(dots)

    def part_2(self) -> None:
        """
        Day 13 part 2 solution.
        """
        dots = self.dots
        for axis, index in self.folds:
            dots = self._fold_paper(dots, axis, index)
        # Make visual
        max_x, max_y = map(max, zip(*dots))
        board: list[list[str]] = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
        for x, y in dots:
            board[y][x] = "█"
        print("\n".join("".join(row) for row in board))

    @staticmethod
    def _fold_paper(dots: set[_Coord], axis: str, index: int) -> set[_Coord]:
        """
        Fold the paper once.
        """
        new_dots: set[_Coord] = set()
        for x, y in dots:
            if axis == "x":
                new_dots.add((x if x < index else 2 * index - x, y))
            else:
                new_dots.add((x, y if y < index else 2 * index - y))
        return new_dots