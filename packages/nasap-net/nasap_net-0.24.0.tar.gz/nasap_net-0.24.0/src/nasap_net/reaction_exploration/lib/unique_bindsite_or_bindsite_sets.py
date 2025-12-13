from collections.abc import Iterable, Mapping
from typing import overload

from cachetools import cached
from cachetools.keys import hashkey

from nasap_net import Assembly, Component
from nasap_net.utils import group_equivalent_nodes_or_nodesets

from .cached_self_isomorphism_iteration import \
    iter_self_isomorphisms_with_cache

_cache = {}  # type: ignore

def clear_cache_for_compute_unique_bindsites_or_bindsite_sets():
    """Clear the cache used by `compute_unique_bindsites_or_bindsite_sets`."""
    _cache.clear()


def _cache_key(
        assembly_id: str | int,
        assembly: Assembly,
        bindsites_or_bindsite_sets: Iterable[str] | Iterable[tuple[str, ...]],
        component_structures: Mapping[str, Component],
        ) -> tuple:
    return hashkey(assembly_id, frozenset(bindsites_or_bindsite_sets))


@overload
def compute_unique_bindsites_or_bindsite_sets(
        assembly_id: str | int, assembly: Assembly,
        bindsites_or_bindsite_sets: Iterable[str],
        component_structures: Mapping[str, Component],
        ) -> list[tuple[str, int]]: ...
@overload
def compute_unique_bindsites_or_bindsite_sets(
        assembly_id: str | int, assembly: Assembly,
        bindsites_or_bindsite_sets: Iterable[tuple[str, str]],
        component_structures: Mapping[str, Component],
        ) -> list[tuple[tuple[str, str], int]]: ...
@overload
def compute_unique_bindsites_or_bindsite_sets(
        assembly_id: str | int, assembly: Assembly,
        bindsites_or_bindsite_sets: Iterable[tuple[str, str, str]],
        component_structures: Mapping[str, Component],
        ) -> list[tuple[tuple[str, str, str], int]]: ...
@overload
def compute_unique_bindsites_or_bindsite_sets(
        assembly_id: str | int, assembly: Assembly,
        bindsites_or_bindsite_sets: Iterable[tuple[str, ...]],
        component_structures: Mapping[str, Component],
        ) -> list[tuple[tuple[str, ...], int]]: ...
@cached(cache=_cache, key=_cache_key)
def compute_unique_bindsites_or_bindsite_sets(
        assembly_id,  # only used for caching
        assembly, bindsites_or_bindsite_sets, 
        component_structures):
    """Compute unique bindsites or bindsite sets.

    Parameters
    ----------
    assembly_id : str
        The ID of the assembly. Used for caching.
    assembly : Assembly
        The assembly containing the bindsites.
    bindsites_or_bindsite_sets : Iterable[str] | Iterable[tuple[str, ...]]
        The bindsites or bindsite sets to be considered.
    component_structures : Mapping[str, ComponentStructure]
        A mapping of component names to their structures.

    Returns
    -------
    list of tuple[str, int] | tuple[tuple[str, ...], int]
        A list of unique bindsites or bindsite sets and their counts.

    Note
    -----
    The result is cached to avoid redundant computation.
    The key for caching is based on the assembly_id and the set of bindsites or
    bindsite sets, i.e., assembly and component_structures are not used.
    Make sure to provide the same assembly_id for the same assembly, and not to
    change the component_structures between calls.
    """
    isomorphisms = iter_self_isomorphisms_with_cache(
        assembly_id, assembly, component_structures)

    grouped_nodesets = group_equivalent_nodes_or_nodesets(
        bindsites_or_bindsite_sets, isomorphisms)
    
    return [
        (min(group), len(group)) for group  # type: ignore
        in grouped_nodesets]
