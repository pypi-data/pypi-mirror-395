from collections.abc import Iterable, Mapping
from itertools import combinations
from typing import TypeVar, overload

import networkx as nx
from networkx.utils import UnionFind, groups

__all__ = ['group_equivalent_nodes_or_nodesets']


@overload
def group_equivalent_nodes_or_nodesets(
        nodes_or_nodesets: Iterable[str],
        isomorphisms: Iterable[Mapping[str, str]]
        ) -> set[frozenset[str]]: ...
@overload
def group_equivalent_nodes_or_nodesets(
        nodes_or_nodesets: Iterable[tuple[str, str]],
        isomorphisms: Iterable[Mapping[str, str]]
        ) -> set[frozenset[tuple[str, str]]]: ...
@overload
def group_equivalent_nodes_or_nodesets(
        nodes_or_nodesets: Iterable[tuple[str, str, str]],
        isomorphisms: Iterable[Mapping[str, str]]
        ) -> set[frozenset[tuple[str, str, str]]]: ...
@overload
def group_equivalent_nodes_or_nodesets(
        nodes_or_nodesets: Iterable[tuple[str, ...]],
        isomorphisms: Iterable[Mapping[str, str]]
        ) -> set[frozenset[tuple[str, ...]]]: ...
def group_equivalent_nodes_or_nodesets(
        nodes_or_nodesets, isomorphisms):
    """Compute node equivalence and return it as a dictionary."""
    uf = UnionFind(nodes_or_nodesets)

    for isomorphism in isomorphisms:
        while _update_equivalence(uf, isomorphism):
            pass

    return set([frozenset(group) for group in uf.to_sets()])


def _update_equivalence(
        uf: UnionFind, isomorphism: Mapping[str, str]
        ) -> bool:
    """Update the equivalence classes of node pairs in an assembly
    based on a new isomorphism."""
    roots = set(uf[element] for element in uf)
    for root1, root2 in combinations(roots, 2):
        rev_dict = groups(uf.parents)
        group1 = rev_dict[root1]
        group2 = rev_dict[root2]
        if any(
                apply_isomorphism(element1, isomorphism)
                in group2 for element1 in group1):
            uf.union(root1, root2)
            return True
        if any(
                apply_isomorphism(element2, isomorphism)
                in group1 for element2 in group2):
            uf.union(root1, root2)
            return True
    return False


@overload
def apply_isomorphism(
        node_or_nodeset: str, isomorphism: Mapping[str, str]
        ) -> str: ...
@overload
def apply_isomorphism(
        node_or_nodeset: tuple[str, str], isomorphism: Mapping[str, str]
        ) -> tuple[str, str]: ...
@overload
def apply_isomorphism(
        node_or_nodeset: tuple[str, str, str], isomorphism: Mapping[str, str]
        ) -> tuple[str, str, str]: ...
@overload
def apply_isomorphism(
        node_or_nodeset: tuple[str, ...], isomorphism: Mapping[str, str]
        ) -> tuple[str, ...]: ...
def apply_isomorphism(
        node_or_nodeset, isomorphism):
    if isinstance(node_or_nodeset, str):
        return isomorphism[node_or_nodeset]
    return tuple(isomorphism[node] for node in node_or_nodeset)
