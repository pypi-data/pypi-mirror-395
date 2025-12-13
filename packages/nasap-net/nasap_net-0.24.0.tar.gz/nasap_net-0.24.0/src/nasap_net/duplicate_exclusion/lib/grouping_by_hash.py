from collections import defaultdict
from collections.abc import Hashable, Mapping
from typing import TypeVar

from nasap_net import Assembly, Component, calc_graph_hash_of_assembly

__all__ = ['group_assemblies_by_hash']


_T = TypeVar('_T', bound=Hashable)

def group_assemblies_by_hash(
        id_to_assembly: Mapping[_T, Assembly],
        component_structures: Mapping[str, Component]
        ) -> dict[str, set[_T]]:
    # Group by hash
    hash_to_ids = defaultdict(set)
    for id_, assembly in id_to_assembly.items():
        hash_ = calc_graph_hash_of_assembly(assembly, component_structures)
        hash_to_ids[hash_].add(id_)
    return hash_to_ids
