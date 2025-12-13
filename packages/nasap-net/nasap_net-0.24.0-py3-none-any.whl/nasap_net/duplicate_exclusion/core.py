from collections import defaultdict
from collections.abc import Iterator, Mapping, Sequence

from nasap_net import Assembly, Component, calc_graph_hash_of_assembly

from .lib.is_new_check import is_new

__all__ = ['find_unique_assemblies']


def find_unique_assemblies(
        assemblies: Sequence[Assembly],
        component_structures: Mapping[str, Component]
        ) -> Iterator[Assembly]:
    """Get unique assemblies.

    "Unique" here means that the assemblies are not isomorphic to each
    other. See `stepwise_is_isomorphic` for the definition of isomorphism.
    
    Although `exclude_remaining_duplicates` provides a more detailed 
    information like which unique assembly corresponds to which duplicates, 
    this function is more efficient in terms of memory usage if you only 
    need the unique assemblies.

    Parameters
    ----------
    assemblies : Sequence[Assembly]
        A sequence of assemblies.
    component_structures : Mapping[str, Component]
        A mapping from component kinds to component structures.

    Yields
    ------
    tuple[str, Assembly]
        Unique assemblies with their IDs, i.e., (ID, assembly).

    Note
    ----
    From each group of isomorphic assemblies, the first assembly in the
    provided iterable is yielded as a unique assembly.
    """
    hash_to_uniques: dict[str, list[Assembly]] = defaultdict(list)
    for assembly in assemblies:
        hash_ = calc_graph_hash_of_assembly(assembly, component_structures)
        if is_new(
                hash_, assembly, hash_to_uniques, component_structures):
            hash_to_uniques[hash_].append(assembly)
            yield assembly
