from collections.abc import Mapping

from cachetools import cached

from nasap_net import Assembly, Component
from nasap_net.algorithms import isomorphisms_iter

_cache = {}  # type: ignore

def clear_cache_for_iter_self_isomorphisms():
    """Clear the cache used by `iter_self_isomorphisms_with_cache`."""
    _cache.clear()


def _cache_key(
        assembly_id: str,
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        ) -> str:
    return assembly_id


@cached(cache=_cache, key=_cache_key)
def iter_self_isomorphisms_with_cache(
        assembly_id: str, assembly: Assembly,
        component_structures: Mapping[str, Component]
        ) -> list[dict[str, str]]:
    """Iterate over self-isomorphisms of an assembly.

    Parameters
    ----------
    assembly_id : str
        The ID of the assembly. Used for caching.
    assembly : Assembly
        The assembly.
    component_structures : Mapping[str, ComponentStructure]
        A mapping from component kind to its structure.

    Returns
    -------
    list[dict[str, str]]
        A list of isomorphisms.
        Each isomorphism is a mapping from node 
        (core or bindsite, e.g., 'M1.core', 'M1.a')

    Note
    -----
    The result is cached to avoid redundant computation.
    The key for caching is based on the assembly_id, 
    i.e., assembly and component_structures are not used.
    Make sure to provide the same assembly_id for the same assembly, 
    and not to change the component_structures between calls.
    """
    return list(isomorphisms_iter(
        assembly, assembly, component_structures))
