# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Optional

    _Data = tuple["_Node", "_Node"]


class Solution(SolutionAbstract):
    day = 12
    data: _Data

    def __init__(self) -> None:
        super().__init__()
        self.start_node, self.end_node = self.data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 12 data.
        """
        node_map: dict[str, _Node] = {}
        for line in raw_data:
            node1_name, node2_name = line.split("-")
            if (node1 := node_map.get(node1_name)) is None:
                node1 = _Node(node1_name)
                node_map[node1_name] = node1
            if (node2 := node_map.get(node2_name)) is None:
                node2 = _Node(node2_name)
                node_map[node2_name] = node2
            node1.connections.append(node2)
            node2.connections.append(node1)
        return node_map["start"], node_map["end"]

    def part_1(self) -> int:
        """
        Day 12 part 1 solution.
        """
        return self._part_1_path_count(self.start_node, set())

    def part_2(self) -> int:
        """
        Day 12 part 2 solution.
        """
        return self._part_2_path_count(self.start_node, set(), False)

    def _part_1_path_count(self, node: _Node, visited_nodes: set[_Node]) -> int:
        """
        Recursion depth-first path-finder for part 1.
        """
        # Found a path!
        if node == self.end_node:
            return 1
        # Don't allow small node to be visited twice
        if node in visited_nodes and not node.is_large:
            return 0
        # Sum all path counts from connected nodes
        return sum(
            self._part_1_path_count(next_node, {node, *visited_nodes})
            for next_node in node.connections
        )

    def _part_2_path_count(
        self, node: _Node, visited_nodes: set[_Node], small_visited_twice: bool
    ) -> int:
        """
        Recursion depth-first path-finder for part 2.
        """
        # Found a path!
        if node == self.end_node:
            return 1
        # Conditionally don't allow small node to be visited twice
        if node in visited_nodes and not node.is_large:
            # Stop if start node or another node is visited twice
            if node == self.start_node or small_visited_twice:
                return 0
            # Mark this node as visited twice
            small_visited_twice = True
        # Sum all path counts from connected nodes
        return sum(
            self._part_2_path_count(
                next_node, {node, *visited_nodes}, small_visited_twice
            )
            for next_node in node.connections
        )


class _Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connections: list[_Node] = []

    def __eq__(self, o: object) -> bool:
        if isinstance(o, _Node):
            return self.name == o.name
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)

    @cached_property
    def is_large(self) -> bool:
        return self.name.isupper()