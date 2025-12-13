from collections.abc import Mapping
from itertools import product

from cachetools import cached
from cachetools.keys import hashkey

from nasap_net import Assembly, Component

_cache = {}  # type: ignore

def clear_cache_for_enum_valid_mles_for_intra():
    """Clear the cache used by `enum_valid_mles_for_intra`."""
    _cache.clear()


def _cache_key(
        assembly_id: str | int,
        assembly: Assembly,
        metal_kind: str, leaving_kind: str, entering_kind: str,
        component_structures: Mapping[str, Component],
        ) -> tuple:
    return hashkey(assembly_id, metal_kind, leaving_kind, entering_kind)


@cached(cache=_cache, key=_cache_key)
def enum_valid_mles_for_intra(
        assembly_id: str | int,  # only used for caching
        assembly: Assembly,
        metal_kind: str, leaving_kind: str, entering_kind: str,
        component_structures: Mapping[str, Component],
        ) -> list[tuple[str, str, str]]:
    """
    Get all possible metal-leaving-entering (MLE) site trios in an assembly.

    This function identifies all valid combinations of metal bindsites, 
    leaving bindsites, and entering bindsites based on the specified 
    component kinds and their connectivity.

    Returned trios meet the following conditions:
    - The metal bindsite and leaving bindsite are connected to each other.
    - The component kind of the metal bindsite is metal_kind.
    - The component kind of the leaving bindsite is leaving_kind.
    - The entering bindsite is free and has the component kind entering_kind.

    Parameters
    ----------
    assembly : Assembly
        The assembly containing the bindsites.
    component_structures : Mapping[str, ComponentStructure]
        A mapping of component names to their structures.
    metal_kind : str
        The kind of the metal bindsite.
    leaving_kind : str
        The kind of the leaving bindsite.
    entering_kind : str
        The kind of the entering bindsite.

    Returns
    -------
    list of tuple of str
        A list of tuples, each containing a metal bindsite, a leaving bindsite, 
        and an entering bindsite.

    Note
    -----
    The result is cached to avoid redundant computation.
    The key for caching is based on the assembly_id, metal_kind, leaving_kind,
    and entering_kind, i.e., assembly and component_structures are not used.
    Make sure to provide the same assembly_id for the same assembly, and not to
    change the component_structures between calls.
    """
    # Pairs of metal bindsites and leaving bindsites
    # that meet the following conditions:
    # - The bindsites are connected to each other
    # - The component kind of the metal bindsite is metal_kind
    # - The component kind of the leaving bindsite is leaving_kind
    valid_ml_pairs = []
    for metal_bs in assembly.get_all_bindsites_of_kind(
            metal_kind, component_structures):
        connected_bs = assembly.get_connected_bindsite(metal_bs)
        if connected_bs is None:  # metal bindsite is free
            continue
        if assembly.get_component_kind_of_bindsite(
                connected_bs) == leaving_kind:
            valid_ml_pairs.append((metal_bs, connected_bs))

    # Entering bindsites that meet the following conditions:
    # - The bindsite is free
    # - The component kind of the entering bindsite is entering_kind
    entering_bindsites = [
        bs for bs in assembly.get_all_bindsites_of_kind(
        entering_kind, component_structures)
        if assembly.is_free_bindsite(bs)]

    # Trios of metal bindsites, leaving bindsites, and entering bindsites.
    return [
        (metal_bs, leaving_bs, entering_bs)
        for (metal_bs, leaving_bs), entering_bs
        in product(valid_ml_pairs, entering_bindsites)]
