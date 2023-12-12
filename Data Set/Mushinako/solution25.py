# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from colorama import Fore, init

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Optional

    _Coord = tuple[int, int]
    _Data = list[list[str]]

init(autoreset=True)
_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]


class Solution(SolutionAbstract):
    day = 25
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 25 data.
        """
        return [list(row) for row in raw_data]

    def part_1(self) -> int:
        """
        Day 25 part 1 solution.
        """
        count = 0
        data = [row.copy() for row in self.data]
        height = len(data)
        width = len(data[0])
        while True:
            move_east: dict[_Coord, _Coord] = {}
            south_movers: list[_Coord] = []
            for y, row in enumerate(data):
                for x, cell in enumerate(row):
                    if cell == "v":
                        south_movers.append((y, x))
                        continue
                    if cell == ">":
                        new_x = (x + 1) % width
                        if data[y][new_x] == ".":
                            move_east[(y, x)] = (y, new_x)
            for (y, x) in move_east:
                data[y][x] = "."
            for (y, x) in move_east.values():
                data[y][x] = ">"
            move_south: dict[_Coord, _Coord] = {}
            for y, x in south_movers:
                new_y = (y + 1) % height
                if data[new_y][x] == ".":
                    move_south[(y, x)] = (new_y, x)
            for (y, x) in move_south:
                data[y][x] = "."
            for (y, x) in move_south.values():
                data[y][x] = "v"
            count += 1
            if not move_east and not move_south:
                return count

    def part_2(self) -> None:
        """
        Day 25 part 2 solution.
        """
        self._print_rainbow("Merry Chirstmas!")

    @staticmethod
    def _print_rainbow(
        text: str,
        *,
        sep: Optional[str] = None,
        end: Optional[str] = None,
        flush: bool = False,
    ) -> None:
        """"""
        length = len(text)
        colors_length = len(_COLORS)
        positions = [i * length // colors_length for i in range(colors_length)]
        for color, position in reversed(list(zip(_COLORS, positions))):
            text = text[:position] + color + text[position:]
        print(text, sep=sep, end=end, flush=flush)