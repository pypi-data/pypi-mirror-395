from collections.abc import Hashable, Iterable, Mapping
from itertools import combinations
from typing import TypeVar, cast

from networkx.utils import UnionFind

from nasap_net import Assembly, Component, is_isomorphic

from .grouping_by_hash import group_assemblies_by_hash

__all__ = ['group_assemblies_by_isomorphism']

_T = TypeVar('_T', bound=Hashable)

def group_assemblies_by_isomorphism(
        id_to_assembly: Mapping[_T, Assembly],
        component_structures: Mapping[str, Component],
        *,
        non_isomorphic_groups: Iterable[set[_T]] | None = None
        ) -> dict[_T, set[_T]]:
    """Group duplicates by assembly isomorphism.

    Parameters
    ----------
    id_to_assembly : Mapping[_T, Assembly]
        A mapping from IDs to assemblies.
    component_structures : Mapping[str, Component]
        A mapping from component kinds to component structures.
    non_isomorphic_groups : Iterable[set[_T]], optional
        Predefined groups of assemblies that are guaranteed to be unique
        and non-isomorphic. Assemblies in the same group will not be 
        checked for isomorphism. If None, all assemblies are checked for 
        isomorphism.

    Returns
    -------
    dict[_T, set[_T]]
        A mapping from unique IDs to sets of duplicate IDs.
        Unique IDs are the minimum IDs in each group.
        Duplicate IDs include the unique IDs themselves.

    Notes
    -----
    The parameter `non_isomorphic_groups` is useful when there are
    assemblies that are known to be unique and non-isomorphic. This
    can be used to reduce the number of isomorphism checks, which can
    be computationally expensive.
    """
    hash_to_ids = group_assemblies_by_hash(id_to_assembly, component_structures)
    
    if non_isomorphic_groups is not None:
        id_to_non_isomorphic_group = {
            id_: group for group in non_isomorphic_groups for id_ in group}

    uf = UnionFind(id_to_assembly.keys())

    for hash_, same_hash_ids in hash_to_ids.items():
        if len(same_hash_ids) == 1:
            continue

        for id1, id2 in combinations(same_hash_ids, 2):
            if uf[id1] == uf[id2]:  # Already checked to be isomorphic
                continue
            if non_isomorphic_groups is not None:
                non_isom_group1 = id_to_non_isomorphic_group.get(id1)
                non_isom_group2 = id_to_non_isomorphic_group.get(id2)
                if non_isom_group1 is not None and non_isom_group1 == non_isom_group2:
                    # Already guaranteed to be non-isomorphic
                    continue
            if is_isomorphic(  # Need isomorphism check
                    id_to_assembly[id1], id_to_assembly[id2],
                    component_structures):
                uf.union(id1, id2)

    grouped_ids = cast(Iterable[set[_T]], uf.to_sets())
    unique_id_to_ids = {min(ids): ids for ids in grouped_ids}
    return unique_id_to_ids
