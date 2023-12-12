# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Numbers = list[int]
    _NumberBoard = list[list[int]]
    _SelectedBoard = list[list[bool]]
    _Data = tuple[_Numbers, list[_NumberBoard]]


class Solution(SolutionAbstract):
    day = 4
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 04 data.
        """
        numbers = [int(n) for n in raw_data[0].split(",")]
        lines = raw_data[1:]
        boards: list[_NumberBoard] = [
            [[int(n) for n in lines[6 * board_count + i].split()] for i in range(5)]
            for board_count in range(len(lines) // 6)
        ]
        return numbers, boards

    def part_1(self) -> int:
        """
        Day 04 part 1 solution.
        """
        numbers, num_boards = self.data
        sel_boards = [[[False] * 5 for _ in range(5)] for _ in num_boards]
        for n in numbers:
            for b, num_board in enumerate(num_boards):
                for i, num_row in enumerate(num_board):
                    for j, num_cell in enumerate(num_row):
                        if num_cell == n:
                            sel_boards[b][i][j] = True
            for b, sel_board in enumerate(sel_boards):
                if self._check_bingo(sel_board):
                    return n * sum(
                        num_cell
                        for num_row, sel_row in zip(num_boards[b], sel_board)
                        for num_cell, sel_cell in zip(num_row, sel_row)
                        if not sel_cell
                    )
        # Make linter happy
        return 0

    def part_2(self) -> int:
        """
        Day 04 part 2 solution.
        """
        numbers, num_boards = self.data
        sel_boards = [[[False] * 5 for _ in range(5)] for _ in num_boards]
        # Make linter happy
        result = 0
        for n in numbers:
            for b, num_board in enumerate(num_boards):
                for i, num_row in enumerate(num_board):
                    for j, num_cell in enumerate(num_row):
                        if num_cell == n:
                            sel_boards[b][i][j] = True
            new_board_nums: list[list[list[int]]] = []
            new_boards: list[list[list[bool]]] = []
            for b, sel_board in enumerate(sel_boards):
                board_num = num_boards[b]
                if self._check_bingo(sel_board):
                    result = n * sum(
                        num_cell
                        for num_row, sel_row in zip(board_num, sel_board)
                        for num_cell, sel_cell in zip(num_row, sel_row)
                        if not sel_cell
                    )
                else:
                    new_board_nums.append(board_num)
                    new_boards.append(sel_board)
            num_boards = new_board_nums
            sel_boards = new_boards
        return result

    @staticmethod
    def _check_bingo(board: _SelectedBoard) -> bool:
        return any(all(row) for row in board) or any(all(col) for col in zip(*board))