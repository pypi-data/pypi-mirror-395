from collections.abc import Mapping

from cachetools import cached
from cachetools.keys import hashkey

from nasap_net import Assembly, Component

_cache = {}  # type: ignore

def clear_cache_for_enum_valid_ml_pairs():
    """Clear the cache used by `enum_valid_ml_pairs`."""
    _cache.clear()


def _cache_key(
        assembly_id: str | int,
        assembly: Assembly,
        metal_kind: str, leaving_kind: str,
        component_structures: Mapping[str, Component]
        ) -> tuple:
    return hashkey(assembly_id, metal_kind, leaving_kind)


@cached(cache=_cache, key=_cache_key)
def enum_valid_ml_pairs(
        assembly_id: str | int,  # only used for caching
        assembly: Assembly,
        metal_kind: str, leaving_kind: str,
        component_structures: Mapping[str, Component]
        ) -> list[tuple[str, str]]:
    """Enumerate valid metal-leaving pairs in an assembly.

    "Valid" means that the bindsites are connected to each other, and the
    component kinds of the metal and leaving bindsites are metal_kind and
    leaving_kind, respectively.

    Parameters
    ----------
    assembly_id : str
        The ID of the assembly. Used for caching.
    assembly : Assembly
        The assembly containing the bindsites.
    metal_kind : str
        The kind of the metal bindsite.
    leaving_kind : str
        The kind of the leaving bindsite.
    component_structures : Mapping[str, ComponentStructure]
        A mapping of component names to their structures.

    Returns
    -------
    list of tuple of str
        A list of tuples, each containing a metal bindsite and a leaving bindsite.

    Note
    -----
    The result is cached to avoid redundant computation.
    The key for caching is based on the assembly_id, metal_kind, and leaving_kind,
    i.e., assembly and component_structures are not used.
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
    return valid_ml_pairs
