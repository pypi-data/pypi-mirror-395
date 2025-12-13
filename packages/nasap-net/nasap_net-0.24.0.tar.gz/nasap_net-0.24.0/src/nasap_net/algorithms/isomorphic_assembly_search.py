from collections.abc import Iterable, Mapping

from nasap_net import Assembly, Component
from nasap_net.algorithms.hashing import calc_graph_hash_of_assembly
from nasap_net.algorithms.isomorphism import is_isomorphic


def find_isomorphic_assembly(
        target_assembly: Assembly,
        id_to_assembly: Mapping[int, Assembly],
        hash_to_ids: Mapping[str, Iterable[int]],
        component_structures: Mapping[str, Component]
        ) -> int | None:
    # TODO: Reduce the number of calls to calc_wl_hash_of_assembly.
    # Maybe we can use the numbers of each component kind in the assembly.
    hash_ = calc_graph_hash_of_assembly(target_assembly, component_structures)
    if hash_ not in hash_to_ids:
        return None
    for candidate_id in hash_to_ids[hash_]:
        candidate = id_to_assembly[candidate_id]
        if is_isomorphic(
                target_assembly, candidate, component_structures):
            return candidate_id
    return None
