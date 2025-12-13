from collections import defaultdict
from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar

_T = TypeVar('_T', bound=Hashable)


class UnionFind(Generic[_T]):
    """Union-Find"""
    def __init__(self, nodes: Iterable[_T]):
        self.parent: dict[_T, _T] = {node: node for node in nodes}

    def find(self, x: _T) -> _T:
        """Find the root of the set containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: _T, y: _T) -> None:
        """Union the sets containing x and y."""
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root != y_root:
            self.parent[y_root] = x_root

    @property
    def root_to_elements(self) -> dict[_T, set[_T]]:
        """Map each root to the set of its elements."""
        root_to_elements = defaultdict(set)
        for element in self.parent:
            root = self.find(element)
            root_to_elements[root].add(element)
        return root_to_elements
